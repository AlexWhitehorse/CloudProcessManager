package main

import (
  "encoding/json"
  "strconv"
  "strings"
  "bytes"
  "io/ioutil"
  "net/http"
  "fmt"
)

//use dispatcher/(start,stop)
//use weberr/(procs,errors)
//provide WebServer

type CtrlMsg struct {
  Action []string `json:"action"`
  User string `json:"user"`
  Process string `json:"process"`
  Pid string `json:"pid"`
}

func testHandler(w http.ResponseWriter, r *http.Request) {
  fmt.Fprintf(w, "Hello World!")
}

func indexHandler(w http.ResponseWriter, r *http.Request) {
  if isDebug {fmt.Println("get index request")}
  indexHtml, err := ioutil.ReadFile("./index.html")
  if err != nil {
    fmt.Println("index handler: read index html file error")
    http.Error(w, err.Error(), http.StatusBadRequest)
    return
  }
  
  w.Header().Set("Content-type", "text/html")
  b := bytes.NewBuffer(indexHtml)
  _, err = b.WriteTo(w)
  if err != nil {
    fmt.Fprintf(w, "Fail to read index.html: %s", err)
    http.Error(w, err.Error(), http.StatusBadRequest)
  }
}

func startHandler(w http.ResponseWriter, r *http.Request) {
  if isDebug {fmt.Println("get start request")}
  //err1 := json.NewDecoder(r.Body).Decode(&msg)
  //body := `{"action":"test","user":"usr","process":"p1","pid":"xxxx"}`
  body, err := ioutil.ReadAll(r.Body)
  defer r.Body.Close()
  if err != nil {
    fmt.Println("start handler: read request data error: " + err.Error())
    http.Error(w, err.Error(), http.StatusBadRequest)
    return
  }
  //fmt.Fprintf(w, "Control message body: %s", string(body))
  //fmt.Println("start handler: request body: " + string(body))
  
  msg := CtrlMsg{}
  err = json.Unmarshal(body, &msg)
  if err != nil {
    fmt.Println("start handler: json parse error: " + err.Error())
    http.Error(w, err.Error(), http.StatusBadRequest)
    return
  }
  if isDebug {fmt.Printf("start handler: control message received: %+v\n", msg)}

  result := start(msg.User, msg.Process, msg.Action)
  fmt.Fprintf(w, "%s", result)
  //io.WriteString(w, result)
}

func stopHandler(w http.ResponseWriter, r *http.Request) {
  if isDebug {fmt.Println("get stop request")}
  body, err := ioutil.ReadAll(r.Body)
  defer r.Body.Close()
  if err != nil {
    fmt.Println("stop handler: read request data error: " + err.Error())
    http.Error(w, err.Error(), http.StatusBadRequest)
    return
  }
  msg := CtrlMsg{}
  err = json.Unmarshal(body, &msg)
  if err != nil {
    fmt.Println("stop handler: json parse error: " + err.Error())
    http.Error(w, err.Error(), http.StatusBadRequest)
    return
  }
  if isDebug {fmt.Printf("start handler: control message received: %+v\n", msg)}

  result := stop(msg.User, msg.Process)
  fmt.Fprintf(w, "%s", result)
}

func listHandler(w http.ResponseWriter, r *http.Request){
  if isDebug {fmt.Println("get list request")}
  procs.Lock()
  defer procs.Unlock()

  ps := make([]string, 0, len(procs.mp))
  for procId := range procs.mp {
    ps = append(ps, procId)
  }

  procsJson, err := json.Marshal(ps)
  if err != nil {
    fmt.Println("list handler: json encoding error: " + err.Error())
    http.Error(w, err.Error(), http.StatusBadRequest)
  }
  fmt.Fprintf(w, "%s", procsJson)
}

func getProcessErrorsHandler(w http.ResponseWriter, r *http.Request) {
  if isDebug {fmt.Println("get process errors request")}
  strParams := strings.TrimPrefix(r.URL.Path, "/errors/")
  arrParam := strings.Split(strParams, "/")
  if len(arrParam) < 2 {
    fmt.Println("get process errors handler: bad url: " + r.URL.Path)
    http.Error(w, "Bad url", http.StatusBadRequest)
    return
  }
  procId := arrParam[0] + "/" + arrParam[1]
  tsFrom := int64(0)
  if len(arrParam) == 3 {
    i64, err := strconv.ParseInt(arrParam[2], 10, 64)
    if err != nil {
        fmt.Println("get process errors handler: error parse timestamp: " + err.Error())
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }
    tsFrom = i64
  }

  errors.Lock()
  procErrs := errors.mp[procId]
  errors.Unlock()
  procErrsAfter := []ErrorData{}
  for i := range procErrs {
    tsError, _ := strconv.ParseInt(procErrs[i].Ts, 10, 64)
    if tsFrom < tsError {
      procErrsAfter = append(procErrsAfter, procErrs[i])
    }
  }

  errorsJson, err := json.Marshal(procErrsAfter)
  if err != nil {
    fmt.Printf("get process errors handler: get errors of %s: json encoding error: %s\n", procId, err.Error())
    http.Error(w, err.Error(), http.StatusBadRequest)
    return
  }
  fmt.Fprintf(w, "%s", errorsJson)
}

func WebServer(addr string) {
  mux := http.NewServeMux()
  mux.Handle("/", http.HandlerFunc(indexHandler))
  mux.Handle("/test", http.HandlerFunc(testHandler))
  mux.Handle("/start", http.HandlerFunc(startHandler))
  mux.Handle("/stop", http.HandlerFunc(stopHandler))
  mux.Handle("/list", http.HandlerFunc(listHandler))
  mux.Handle("/errors/", http.HandlerFunc(getProcessErrorsHandler))
  s := http.Server{Addr: addr, Handler: mux}
  fmt.Println("web server listening on " + addr)
  err := s.ListenAndServe()
  if err != nil {
    fmt.Println("ListenAndServe: " + err.Error())
  }
}