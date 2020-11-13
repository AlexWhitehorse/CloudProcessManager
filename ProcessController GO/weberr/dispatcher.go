package main

import (
  "strconv"
  "strings"
  //"bytes"
  "time"
  "sync"
  "net"
  "io"
  "bufio"
  "fmt"
  "os/exec"
  "runtime"
)

//use weberr/(isDebug,mustNotify)
//use weberr/(config,tcpNotifyAddr,nErrorTemplates,errorsCheckPeriod)
//use weberr/(procs,errors)

type ErrorChecker struct {
  countingStartTime int64
  errCount int
}
func (ec *ErrorChecker) append(line string) bool {
  if time.Now().UnixNano() > ec.countingStartTime + errorsCheckPeriod {
    ec.errCount = 0
  }
  for i:=0; i<nErrorTemplates; i++ {
    errTemplate := config.ErrorTemplates[i]
    if strings.Contains(line, errTemplate) {
      ec.errCount++
      if isDebug {fmt.Printf("errCount: %d\n", ec.errCount)}
      if ec.errCount >= config.ErrorsCheckCount {
        return true
      }
    }
  }
  return false
}

func tcpNotify(txt string) {
  conn, err := net.Dial("tcp", config.TcpNotifyAddress)
  if err != nil {
    fmt.Println("tcp notify: error connecting server: " + err.Error())
    return
  }
  _, err = fmt.Fprintf(conn, txt + "\n")
  if err != nil {
    fmt.Println("tcp notify: error sending message: " + err.Error())
    return
  }
  // Прослушиваем ответ
  // buf := make([]byte, 1024)
  // respLen, err := conn.Read(buf)
  // if err != nil {
  //   log.Println("tcpNotify: Error reading message:", err.Error())
  //   return
  // }
  // log.Printf("tcpNotify: receive message: %s", string(buf[:respLen]))

  //message, _ := bufio.NewReader(conn).ReadString('\n')
  //fmt.Print("Message from server: "+message)
}

func startProcess(procId string, arrCmd []string) (*exec.Cmd, io.ReadCloser, string){
  cmdStr := arrCmd[:1][0]
  if runtime.GOOS == "windows" {
    cmdStr += ".exe"
  }
  args := arrCmd[1:]
  cmd := exec.Command(cmdStr, args...)
  stderr, err := cmd.StderrPipe()
  if err != nil {
    return nil, nil, "create stderr pipe error: " + err.Error()
  }
  if isDebug {fmt.Printf("starting process %s...\n", procId)}
  err = cmd.Start();
  if err != nil {
    return nil, nil, "cmd start error: " + err.Error()
  }
  if mustNotify {tcpNotify(fmt.Sprintf(`{"procId": "%s", "state": "runned"}`, procId))}
  return cmd, stderr, ""
}

func stopProcess(procId string, cmd *exec.Cmd, wg *sync.WaitGroup){
  if isDebug {fmt.Printf("stopping process %s...\n", procId)}
  err := cmd.Process.Kill()
  if err != nil {
    fmt.Println("failed to kill process: " + err.Error())
    return
  }
  wg.Wait()
  if mustNotify {tcpNotify(fmt.Sprintf(`{"procId": "%s", "state": "stopped"}`, procId))}
}


func ScanLinesWithCR(data []byte, atEOF bool) (advance int, token []byte, err error) {
  if atEOF && len(data) == 0 {
      return 0, nil, nil
  }

  for i := 0; i < len(data); i++ {
    if i+1 < len(data) {
      if data[i] == '\r' && data[i+1] == '\n' {
        continue
      }
    }
    if data[i] == '\r' || data[i] == '\n' {
      return i + 1, data[:i], nil
    }
  }

  // if i := bytes.IndexByte(data, '\r'); i >= 0 {
  //     // We have a full newline-terminated line.
  //     return i + 1, data[0:i], nil
  // }
  // If we're at EOF, we have a final, non-terminated line. Return it.
  if atEOF {
      return len(data), data, nil
  }
  // Request more data.
  return 0, nil, nil
}

func startProcessWithRestarts(procId string, arrCmd []string, stopSignal <-chan struct{}){
  RestartLoop:
  for{
    cmd, stderr, strError := startProcess(procId, arrCmd)
    if strError != "" {
      fmt.Printf("start process %s error: %s\n", procId, strError)
      return
    }

    ch := make(chan string)
    wg := sync.WaitGroup{}
    wg.Add(1)
    go func(ch chan<- string) {
      scanner := bufio.NewScanner(stderr)
      scanner.Split(ScanLinesWithCR)
      for scanner.Scan() {
        line := scanner.Text()
        ch <- line
      }
      if err := scanner.Err(); err != nil {
        if isDebug {fmt.Println("log scanner error: " + err.Error())}
      }
      close(ch)
      //wg.Done()
    }(ch)
    go func() {
      err := cmd.Wait()
      if err != nil {
        if isDebug {fmt.Println("cmd wait error: " + err.Error())}
      }
      wg.Done()
    }()

    errorChecker := ErrorChecker{
      countingStartTime: time.Now().UnixNano(),
      errCount: 0,
    }

    ReadLineLoop:
    for {
      select {
      case <-stopSignal:
        if isDebug {fmt.Println("Stop signal...")}
        if isDebug {fmt.Printf("killing process %s...\n", procId)}
        stopProcess(procId, cmd, &wg)
        break RestartLoop
      case <-time.After(time.Duration(config.EmptyCheckPeriod) * time.Millisecond):
        if isDebug {fmt.Println("Timeout...")}
        if isDebug {fmt.Printf("killing process %s for restart...\n", procId)}
        stopProcess(procId, cmd, &wg)
        break ReadLineLoop
      case line, ok := <-ch:
        if !ok {
          if isDebug {fmt.Println("Process finished...")}
          break ReadLineLoop
        }
        if isDebug {fmt.Println("error line received: " + line)}
        errData := ErrorData {
          Ts: strconv.FormatInt(time.Now().UnixNano(), 10),
          Txt: line,
        }
		errors.Lock()
        errors.mp[procId] = append(errors.mp[procId], errData)
		if len(errors.mp[procId]) > config.NProcLogsSize {
          errors.mp[procId] = errors.mp[procId][len(errors.mp[procId])-config.NProcLogsSize:]
        }
		errors.Unlock()
		//fmt.Println("err data: ", errData)
		//logger.Printf("err data: %v", errData)
		
        tooMuchErrors := errorChecker.append(line)
        if tooMuchErrors {
          if isDebug {fmt.Println("Too much errors...")}
          if isDebug {fmt.Printf("killing process %s for restart...\n", procId)}
          stopProcess(procId, cmd, &wg)
          break ReadLineLoop
        }
      }
    }
  }
}

func start(user string, process string, arrCmd []string) string{
  procs.Lock()
  defer procs.Unlock()

  procId := user + "/" + process
  //maybe need timeout before stop
  _, exists := procs.mp[procId]
  if exists {
    return fmt.Sprintf(`{"ok": %t, "status": "%s already exist"}`, false, procId)
  }else{
    stopSignal := make(chan struct{})
    procs.mp[procId] = ProcessInfo {
      StopSignal: stopSignal,
    }
    go startProcessWithRestarts(procId, arrCmd, stopSignal)
    return fmt.Sprintf(`{"ok": %t, "status": "%s starting success"}`, true, procId)
  }
}

func stop(user string, process string) string{
  procs.Lock()
  defer procs.Unlock()

  procId := user + "/" + process
  _, exists := procs.mp[procId]
  if exists {
    close(procs.mp[procId].StopSignal)
    delete(procs.mp, procId)
    return fmt.Sprintf(`{"ok": %t, "status": "%s stopping success"}`, true, procId)
  }else{
    return fmt.Sprintf(`{"ok": %t, "status": "%s not found"}`, false, procId)
  }
}