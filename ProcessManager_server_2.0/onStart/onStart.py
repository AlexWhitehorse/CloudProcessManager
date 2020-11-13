from controllerProceses.controller import Process
from source.constants import STATUS, fileProc, PORT, IP, DEBUG
from source.codec import Codec
import socket
import json
import time

# Запуск ранее активных процессов при старте программы
class onStart(Process):

    def __init__(self):
        super().__init__(None, None)
        #path to saved processes
        self.savedProc = fileProc
        self.processes = []


    def getRuningProc(self):
        f = self.readFile(self.savedProc)
        data = json.loads(f)

        # Именя пользователей
        for user in data:
            #Процесы пользователя
            userData = data[user]

            for pName in userData:
                # Даныые процеса
                procData = userData[pName]
                uName = user
                processName = pName
                comand = procData['comand']

                self.setValuesProcess(uName, processName, comand)
        
        # Очистка файла с процессами после выполнения скрипта
        self.delFileData(self.savedProc)


    #Удаление данных из файла с процессами
    #  ! процессы не запустяться если в файле они уже будут        
    def delFileData(self, file):
        toFile = '{' + '}' # = пустой json
        self.writeFile(file, toFile)


    #Получает данные о процессе и добавляет его в масиив
    def setValuesProcess(self, user, process, comand):
        self.processes.append(Process(user, process, comand))


    # Debug method
    def showProcesses(self): 
        for proc in self.processes:
            print(proc.processName)


    # returns json like {action: run, user: ..., process: ..., comand: ...}
    def _makeMsg(self, user, process, comand):
        msgPattern = {}
        msgPattern['action'] = 'run'
        msgPattern['user'] = user
        msgPattern['process'] = process
        msgPattern["comand"] = comand
        
        return json.dumps(msgPattern)


    # Отправка запросов запуска процессов на сервер
    # Если нет соединения - ошибка и ожидание подключения
    def sendAllData(self):
        user = ''
        comand = ''
        process = ''
        i = 0
        
        while i < len(self.processes):
            process = self.processes[i]
            user = process.user
            procName = process.processName
            comand = process.comand 
            message = self._makeMsg(user, procName, comand)

            try:
                self._sendStartComand(message)
                #del self.processes[i]
                time.sleep(1)
                print("["+user+":"+procName+"] Запущен.")
                i = i +1
            except ConnectionRefusedError:
                print("Нет подключения к серверу %s:%s" % (IP, PORT))
                time.sleep(1)


    #Отправляет запрос на сокет IP PORT
    def _sendStartComand(self, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((IP, PORT))
        sock.sendall(bytes(message, 'ascii'))
        answ = sock.recv(1024)
        sock.close()


    def go(self):
        self.getRuningProc()
        self.showProcesses()
        self.sendAllData()