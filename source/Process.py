from subprocess import Popen, PIPE
from subprocess import STDOUT

from constants import DIR_LOGS 

import os
import shlex
# import signal
import psutil

# 
# from threading import Thread
from multiprocessing import Process, Lock

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
        print(args)

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

