# from ..source.constants import *
import os
import socket
DIR_LOGS = "/tmp/ProcessController/"
import json
from constants import STATUS_FILE, ERRORS_PATTERN, DIR_LOGS, NUM_MONO_CHECS, IP, PORT, MAX_NUM_ERRORS, NUM_OF_CHECKING_LOG_STR
from constants import MAX_TIMER_SEC
import time
from datetime import datetime

# NUM_OF_CHECKING_LOG_STR = 20
# from subprocess import Popen

class ErrorController():

    def __init__(self):
        # pass
        self.directory = DIR_LOGS
        self.files = os.listdir(self.directory)

    def getFilesInDir(self):
        pass

    def inspectFile(self, fileName):
        numOfSrt = NUM_OF_CHECKING_LOG_STR

        r = os.system("tail -n " + str(NUM_OF_CHECKING_LOG_STR) + " " + self.directory + fileName)
        
        return r

def send(ip, port, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        try:
            sock.sendall(bytes(message, 'ascii'))
        finally:
            sock.close()

class ErrorChecker():

    def __init__(self):
        self.errorPatern = ERRORS_PATTERN
        self.statusFile = STATUS_FILE
        self.errors = self.getErrors()
        self.logDir = DIR_LOGS
        self.numMonoChecs = NUM_MONO_CHECS
        self.maxNumErrors = MAX_NUM_ERRORS
        self.maxTimer = MAX_TIMER_SEC

    def getProcesses(self):
        processes = []
        jsonData = self.readFile(self.statusFile)
        data = json.loads(jsonData)

        for user in data.keys():

            for process in data[user].items():

                proc = Proc()

                proc.user = user
                proc.process        = process[0]
                proc.comand         = process[1].get("comand")
                proc.errors         = process[1].get("numErrors")
                proc.timerLastError = float(process[1].get("timeFirstError"))

                processes.append(proc)

        return processes

    def checkProc(self):
        # test
        begin = time.time()

        processes = self.getProcesses()

        for proc in processes:

            # data может быть str[n] или ''
            data = self.getOutputProcess(proc.user, proc.process)
            
            proc.data = data
            self.checkError(proc)
            
        # test
        end = time.time()
        # print("Проверка заняла: ", end - begin)

        return [begin, end]
        



    def checkError(self, process):

        # Разбитие входных данных на строки
        for string in process.data.split("\n"):

            # try:
            #     self.errors.index(string)

            #     print("Find error: ", process.errors)

            #     self.whatToDo(process)

            # except ValueError:
            #     pass

            if string in self.errors:
                print("Find error: " , string, "\n - Total mistakes: ", process.errors)
                self.whatToDo(process)


        # TODO

    def whatToDo(self, process):

        difference = process.getDifferenceTime()
        # Сбросить счетчик
        # Если прошло много времени с момента последней ошибки
        if difference  > self.maxTimer:

            process.errors = 1
            process.timerLastError = time.time()

            self.changeLogProcess(process)
            pass

        # Перезапуск 
        # Если за отведеннfor
            self.restart(process.user, process.process, process.comand)

        # Ошибка инкрементируеться и записываеться в файл
        else:
            # Пооверка таймера
            # Если таймер не запущен
            if process.timerLastError == 0:

                process.errors = 1 + process.errors

                # Запуск таймера
                process.timerLastError = time.time()

                # Запись его в файл
                self.changeLogProcess(process)
            else:

                process.errors = 1 + process.errors
                self.changeLogProcess(process)


# Проверка монотонности процесса (старый вывод != новому)
    """ 
    def checkMono(self, process, newdata):
        print("process.data: ", type(getDifferenceTimeprocess.data), "newdata: ", type(newdata))
        if process.data == newdata:
            print("Mono check: " + str(process.monoCheck))

            process.monoCheck = 1 + process.monoCheck
        else:
            process.monoCheck = 0

        if process.monoCheck >= self.numMonoChecs:
            print("RESTART MONO:", process.user, process.process)

            self.restart(process.user, process.process)
    """


    def getOutputProcess(self, user, process):
        f = "%s%s_%s.txt" % (self.logDir, user, process)

        data = self.getData_tail(f)

        if data:
            return data
        else:
            return ''
    

    def getErrors(self):

        jsonData = self.readFile(self.errorPatern)
        return json.loads(jsonData)


    def changeLogProcess(self, process):

        f = self.statusFile
        dataJson = self.readFile(f)
        data = json.loads(dataJson)

        user = data[process.user]
        proc = user[process.process]

        proc['numErrors'] = process.errors
        proc["timeFirstError"] = process.timerLastError
        user[process.process] = proc
        data[process.user] = user

        data = json.dumps(data)
        self.writeFile(f, data)


    def addProcessError(self, process, time):
        # TODO
        # Инкремент ошибки
        countErrors = process.errors + 1

        # Запись в файл процесса с ошибкой
        f = self.statusFile
        dataJson = self.readFile(f)
        data = json.loads(dataJson)

        user = data[process.user]
        proc = user[process.process]

        proc['numErrors'] = countErrors
        proc["timeFirstError"] = float(time)
        user[process.process] = proc
        data[process.user] = user

        # Конвертация обратно в json
        data = json.dumps(data)

        self.writeFile(f, data)


    def readFile(self, file):
        f = open(file, "r")
        d = f.read()
        f.close()
        return d


    def writeFile(self, file, data):
        f = open(file, "w")
        f.write(data)
        f.close()


    def restart(self, user, process, comand):
        restart = {"action":"restart", "user":user, "process":process, "comand": comand}
        restart = json.dumps(restart)
        print("Restart: ", restart)

        self.sendMsg(restart)


    def getData_tail(self, fileName):

        numOfSrt = NUM_OF_CHECKING_LOG_STR
        # r = os.system("tail -n " + str(NUM_OF_CHECKING_LOG_STR) + " " + fileName)
        r = os.popen("tail -n " + str(NUM_OF_CHECKING_LOG_STR) + " " + fileName).read()
        
        return r


    def sendMsg(self, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((IP, PORT))
        try:
            sock.sendall(bytes(message, 'ascii'))
        finally:
            sock.close()




class Proc():
    def __init__(self):
        self.user = ''
        self.process = ''
        self.comand = ''
        self.errors = 0
        self.monoCheck = 0
        self.timerLastError = 0
        # Полученый лог процесса
        self.data = ''

    def set_user(self, user):
        self.user = user
    
    def set_process(self, process):
        self.process = process

    def set_comand(self, comand):
        self.comand = comand

    # Возвращает разницу во времени 
    # между отщетом от первой ошибки и текушем временем
    def getDifferenceTime(self):
        now = time.time()
        difference = now - self.timerLastError
        return difference




class RiseProc(ErrorChecker):
    
    def __init__(self):
        self.statusFile = STATUS_FILE
        pass


    def rise(self):
        processes = self.getProcesses()

        for proc in processes:
            self.sendStart(proc.user, proc.process, proc.comand)
    

    def sendStart(self, user, process, comand):
        message = {"action":"run", "user":user, "process":process, "comand":comand}
        message = json.dumps(message)
        print("Rise: ", message)
        self.sendMsg(message)




'''
# Переместить!!!
def sendStart(user, process, comand):
    # strn = '{\"action\":%s,\"user\":%s,\"process\":%s,\"comand\":%s}' % ('"%s"' % "run", '"%s"' % user, '"%s"' % process, '"%s"' % comand)
    # print(strn)
    ron = {"action":"run", "user":user, "process":process, "comand":comand}
    return json.dumps(ron)

def sendStop(user, process):
    ron = {"action":"stop", "user":user, "process":process}
    return json.dumps(ron)

if __name__ == "__main__":
    message =  sendStart("test_1", "first", "ping -c 100 1.1.1.1")
    message_stop = sendStop("test_1", "first")
    message2 =  sendStart("test_2", "second", "ping -c 100 1.1.1.1")
    # print (message)
    # tosend = 

    # controller = ErrorController()
    # controller.inspectFile("vasia_first.txt")
    send('localhost', 5003, str(message))
    send('localhost', 5003, str(message2))
    time.sleep(2)
    send('localhost', 5003, str(message_stop))
'''

    