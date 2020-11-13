package main

import (
  "encoding/json"
  "sync"
  "os"
  "net"
  "io/ioutil"
  "fmt"
  "log"
)

type Config struct {
  WebServerAddress string `json:"webServerAddress"`
  TcpCtrlAddress string `json:"tcpCtrlAddress"`
  TcpLogAddress string `json:"tcpLogAddress"`
  TcpNotifyAddress string `json:"tcpNotifyAddress"`
  ErrorsCheckPeriod int `json:"errorsCheckPeriod"`
  ErrorsCheckCount int `json:"errorsCheckCount"`
  EmptyCheckPeriod int `json:"emptyCheckPeriod"`
  NProcLogsSize int `json:"nProcLogsSize"`
  NAllProcLogsSize int `json:"nAllProcLogsSize"`
  ErrorTemplates []string `json:"errorTemplates"`
}

type ProcessInfo struct {
  StopSignal chan struct{}
}
type Procs struct {
  sync.Mutex
  mp map[string]ProcessInfo
}

type ErrorData struct {
  Ts string `json:"ts"`
  Txt string `json:"txt"`
}
type Errors struct {
  sync.Mutex
  mp map[string][]ErrorData
}

const requiredMacAddress = "00:50:56:80:bf:8a"
var (
  isDebug bool
  mustRunWebserver bool
  mustNotify bool

  config Config
  errorsCheckPeriod int64
  nErrorTemplates int
  tcpNotifyAddr string

  procs Procs
  errors Errors
  logger *log.Logger
)

func init() {
  args := os.Args[1:]
  if len(args) == 1 && args[0] == "help" {
    fmt.Println("usage: ./weberr [debug] [webserver] [notify]")
    os.Exit(0)
  }

  isDebug = false
  mustRunWebserver = false
  mustNotify = false
  for _, arg := range args {
    switch arg {
      case "debug":
        isDebug = true
      case "webserver":
        mustRunWebserver = true
      case "notify":
        mustNotify = true
    }
  }
  if isDebug {
    fmt.Printf("isDebug: %t, mustRunWebserver: %t, mustNotify: %t\n", isDebug, mustRunWebserver, mustNotify)
  }
}

func init() {
  if isDebug {fmt.Println("checking mac address...")}
  ifas, err := net.Interfaces()
  if err != nil {
    fmt.Println("check mac address error: " + err.Error())
    os.Exit(1)
  }
  isFound := false
  for _, ifa := range ifas {
    a := ifa.HardwareAddr.String()
	 fmt.Println(a)
    if a == requiredMacAddress {
      isFound = true
    }
  }
  if !isFound {
    fmt.Println("Invalid mac adress")
    os.Exit(1)
  }
}

func init() {
  if isDebug {fmt.Println("loading config...")}
  configJson, err := ioutil.ReadFile("./config.json")
  if err != nil {
    fmt.Println("Read config error: " + err.Error())
    os.Exit(1)
  }
  err = json.Unmarshal(configJson, &config)
  if err != nil {
    fmt.Println("config json parse error: " + err.Error())
    os.Exit(1)
  }
  if isDebug {fmt.Printf("Config: %+v", config)}

  errorsCheckPeriod = int64(config.ErrorsCheckPeriod) * 1e6
  nErrorTemplates = len(config.ErrorTemplates)
}

func init() {
  if isDebug {fmt.Println("initiating proc and err data...")}
  procs.mp = make(map[string]ProcessInfo)
  errors.mp = make(map[string][]ErrorData)
}


func init(){
	f, err := os.OpenFile("text.log", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		fmt.Println("err open log file: ",err)
	}
	//defer f.Close()

	logger = log.New(f, "prefix", log.LstdFlags)
	logger.Println("start logging...")
	//w := bufio.NewWriter(f)
	//fmt.Fprintln(w, "test")
	//w.Flush()
}

func main() {
  go TcpCtrlServer(config.TcpCtrlAddress)
  go TcpLogServer(config.TcpLogAddress)
  if mustRunWebserver {
    go WebServer(config.WebServerAddress)
  }
  select{}
}
