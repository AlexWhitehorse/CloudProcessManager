package main

import (
  "strconv"
  "encoding/json"
  "time"
  "os"
  "net"
  "fmt"
)

//use weberr/(isDebug,config,errors)
//provide TcpLogServer

type TcpLogRequestMessage struct {
  ProcId string `json:"procId"`
  TsFrom string `json:"tsFrom"`
}

func handleTcpLogRequest(conn net.Conn) {
  if isDebug {fmt.Printf("handle tcp log request: get connection from %v\n", conn.RemoteAddr())}
  defer conn.Close()
  buf := make([]byte, config.TcpLogBufferSize)
  reqLen, err := conn.Read(buf)
  if err != nil {
    fmt.Println("handle tcp log request: error reading message:" + err.Error())
    return
  }
  //if isDebug {fmt.Printf("handle tcp log request: receive message(%d): %s\n", reqLen, string(buf[:reqLen]))}

  msg := TcpLogRequestMessage{}
  err = json.Unmarshal(buf[:reqLen], &msg)
  if err != nil {
    fmt.Println("handle tcp log request: json parse error: " + err.Error())
    conn.Write([]byte("Parse log request message error."))
    return
  }
  if isDebug {fmt.Printf("handle tcp log request: get message: %+v\n", msg)}

  procId := msg.ProcId
  tsFrom := time.Now().UnixNano()
  if msg.TsFrom != "" {
    i64, err := strconv.ParseInt(msg.TsFrom, 10, 64)
    if err == nil {
      tsFrom = i64
    }else{
      fmt.Println("handle tcp log request: error parse timestamp: " + err.Error())
    }
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
    fmt.Printf("handle tcp log request: get errors of %s: json encoding error: %s\n", procId, err.Error())
    return
  }
  conn.Write([]byte(errorsJson))
}

func TcpLogServer(addr string) {
	l, err := net.Listen("tcp", addr)
	if err != nil {
	  fmt.Println("tcp log server: error listening: " + err.Error())
	  os.Exit(1)
	}
	defer l.Close()
	fmt.Println("tcp log server listening on " + addr)
	for {
	  conn, err := l.Accept()
	  if err != nil {
		fmt.Println("tcp log server: error accepting: ", err.Error())
		os.Exit(1)
	  }
	  go handleTcpLogRequest(conn)
	}
}