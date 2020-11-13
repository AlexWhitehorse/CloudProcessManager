package main

import (
	"strconv"
	"encoding/json"
	"time"
	"net"
	"bufio"
	"fmt"
)

type ErrorData struct {
	Ts string `json:"ts"`
	Txt string `json:"txt"`
  }

const (
	tcpLogServerAddr = "127.0.0.1:33334"
	procId = "iptv/ffmpeg_rtmp"
	logRequestPeriod = 1000
)

func main(){
	ts := strconv.FormatInt(time.Now().UnixNano(), 10)
	for {
		conn, err := net.Dial("tcp", tcpLogServerAddr)
		if err != nil {
			fmt.Println("Fail to connect tcp log server")
			return
		}
		//fmt.Printf("log tcp client connected to %s\n", tcpLogServerAddr)
		
		fmt.Fprintf(conn, `{"procId":"%s", "tsFrom": "%s"}`, procId, ts)
		scanner := bufio.NewScanner(conn)
		for scanner.Scan() {
		  line := scanner.Text()
		  //fmt.Printf("receive log response message line: %s\n", line)
		  msg := []ErrorData{}
		  err = json.Unmarshal([]byte(line), &msg)
		  if err != nil {
			fmt.Println("json parse log response data error: " + err.Error())
			return
		  }
		  fmt.Printf("Receive log response: %v\n", msg)
		  if len(msg) > 0 {
			lastLogObj := msg[len(msg)-1:][0]
			ts = lastLogObj.Ts
		  }
		}
		if err := scanner.Err(); err != nil {
		  fmt.Println("Log scannel error: " + err.Error())
		}

		conn.Close()
		time.Sleep(time.Duration(logRequestPeriod) * time.Millisecond)
	}
}
