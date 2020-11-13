package main

import (
  "strings"
  "encoding/json"
  "os"
  "net"
  "fmt"
)

//use weberr/(isDebug,config)
//use dispatcher/(start,stop)
//provide TcpCtrlServer

type TcpCtrlMessageProcess struct {
  Command []string `json:"comand"`
  State string `json:"state"`
}
type TcpCtrlMessageUser map[string]TcpCtrlMessageProcess
type TcpCtrlMessage map[string]TcpCtrlMessageUser

func handleTcpCtrlRequest(conn net.Conn) {
  if isDebug {fmt.Printf("handle tcp control request: get connection from %v\n", conn.RemoteAddr())}
  defer conn.Close()
  buf := make([]byte, config.TcpCtrlBufferSize)
  reqLen, err := conn.Read(buf)
  if err != nil {
    fmt.Println("handle tcp control request: error reading message:" + err.Error())
    return
  }
  if isDebug {fmt.Printf("handle tcp control request: receive message(%d): %s\n", reqLen, string(buf[:reqLen]))}


  msg := TcpCtrlMessage{}
  err = json.Unmarshal(buf[:reqLen], &msg)
  if err != nil {
    fmt.Println("handle tcp control request: json parse error: " + err.Error())
    conn.Write([]byte("Parse control message error."))
    return
  }
  if isDebug {fmt.Printf("handle tcp control request: get message: %+v\n", msg)}

  arrResults := []string{}
  for userId, userObj := range msg {
    for procId, procObj := range userObj {
      if isDebug {fmt.Printf("user: %s, proc: %s, cmd: %s, state: %s\n", userId, procId, procObj.Command, procObj.State)}
      if procObj.State == "run" {
        result := start(userId, procId, procObj.Command)
        arrResults = append(arrResults, result)
      } else if procObj.State == "stop" {
        result := stop(userId, procId)
        arrResults = append(arrResults, result)
      }
    }
  }
  strResults := "[" + strings.Join(arrResults, ",") + "]"
  conn.Write([]byte(strResults))
}

func TcpCtrlServer(addr string) {
  l, err := net.Listen("tcp", addr)
  if err != nil {
    fmt.Println("tcp control server: error listening: ", err.Error())
    os.Exit(1)
  }
  defer l.Close()
  fmt.Println("tcp control server listening on " + addr)
  for {
    conn, err := l.Accept()
	//logger.Println("tcp ctrl connection...")
    if err != nil {
      fmt.Println("tcp control server: Error accepting: ", err.Error())
      os.Exit(1)
    }
	//fmt.Printf("conn %T", conn)
    go handleTcpCtrlRequest(conn)
  }
}