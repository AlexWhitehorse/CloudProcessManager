from subprocess import Popen, PIPE
from subprocess import STDOUT

from constants import DIR_LOGS, PERIOD_CHECK_LOG_SEC


from source.errorController import ErrorChecker, RiseProc
import os
import shlex
# import signal
import psutil

# 
# from threading import Thread
from multiprocessing import Process, Lock
import time




class MyProcess():

    user = ""
    processName = ""
    mpid = 0
    mprocess = False
    strProcess = ""
    # dontStop = True
    logDir = DIR_LOGS


    def __init__(self, nameUser, nameProcess, comand):
        # self.user = userName
        self.strProcess = comand
        self.user = nameUser
        self.processName = nameProcess


    # Запускает процесс в фоне и продолжает работу программы
    def mstart(self):
        args = shlex.split(self.strProcess)

        # print(self.makeStrFOpen())
        try:
            f = open ( self.makeStrFOpen(), "w" )
        # Если нет такой папки
        except FileNotFoundError:
            os.mkdir ( self.logDir)
            f = open ( self.makeStrFOpen(), "w" )

        # Запуск процесса
        self.mprocess = Popen(
            args,
            shell=False,
            stdout=f, stderr=STDOUT,
            preexec_fn=os.setsid
        )
        self.setPid()


    def makeStrFOpen(self):
        return self.logDir + self.user + "_" + self.processName + ".txt"


    # Запуск процесса и ожидание выполнения
    def startAndWait(self):
        self.mstart()
        self.mprocess.wait()


    # Запуск самоподнимающегося процесса
    def continiousWork(self):
        while True:
            self.startAndWait()


    # ??
    def setPid(self):
        self.mpid = self.mprocess.pid


    def getPid(self):
        return self.mprocess.pid


    def test(self):
        print(self.user, self.strProcess)


    def isAlive(self):
        # return self.process.
        pass


    # TODO 
    # Обработать всевозможные варинты
    def stop(self):
        self.mprocess.kill()


    def getLine(self, byte):
        return self.mprocess.stdout.readline(byte)




class ErrorController():

    def __init__(self):
        pass


    def run(self):
        self.riseProcesses()

        monotonus = Process(target=self.monotonus)
        monotonus.start()


    def riseProcesses(self):
        rise = RiseProc()
        time.sleep(1)
        rise.rise()


    def monotonus(self):
        # count = 0
        # average = 0
        while 1:
            # count = count + 1
            e = ErrorChecker()
            res = e.checkProc()
            # average = average + (res[1] - res[0])
            # print("Average: ", str( average / count) )
            time.sleep(PERIOD_CHECK_LOG_SEC)





# class MProceses(Process, MyProcess):

#     def __init__(self, com):
#         Process.__init__(self)
#         MyProcess.__init__(self, com)
#         # self.proc = MyProcess(com)
#         self.spid = 0
#         self.lock = Lock()

#     def run(self):
#         """Запуск потока"""
#         while 1:
#             self.mstart()
#             self.lock.acquire()
#             self.spid = self.mprocess.pid
#             print("pid run: ", self.spid)
#             self.lock.release()
#             # self.lock()
#             self.mprocess.wait()
            

    # def appendToPool():

