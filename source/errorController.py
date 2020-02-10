# from ..source.constants import *
import os
import socket
DIR_LOGS = "/tmp/ProcessController/"
import json

import time

NUM_OF_CHECKING_LOG_STR = 20
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
        print(r)
def send(ip, port, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        try:
            sock.sendall(bytes(message, 'ascii'))
        finally:
            sock.close()

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
    