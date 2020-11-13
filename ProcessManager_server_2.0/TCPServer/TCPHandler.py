import json
import time
# import threading
# import asyncio

from source.codec       import Codec, ACTIONS
from TCPServer.server   import Server
from source.constants   import STATUS
from controllerProceses.controller import Process


class Alice(Server):

    proceses = []

    def handle(self, message):
        # data = json.dumps(message.decode('ascii'))

        # tests
        data = message

        self.codec = Codec()
        self.codec.decodeMsg(data)

        self.printDebugMsg()

    # DEBUG ConnectionRefusedError: [Errno 111] Connection refused
        if self.codec.action == 'run':
            self.sendStart()
            return

        if self.codec.action == 'stop':
            self.sendStop()
            return

        if self.codec.action == 'restart':
            self.sendRestart()
            return

        if self.codec.action == 'status':
            self.sendStatus()
            return

    def sendStart(self):
        status = self.codec.sendMsg('localhost', 33333)

        # print("Answer sratus: ", status)

        if status:
            procData = self.codec.resArr
            user = procData['user']
            process = procData['process']
            comand = procData['comand']
            status = STATUS[1]
            process = Process(user, process, comand, status)
            process.addProcessToFile()
            
            self.proceses.append(process)
            # controller.user = self.codec.resArr['user']
            # controller.processName = self.codec.resArr['process']
            # controller.comand = self.codec.resArr['comand']
            # controller.status = STATUS[1]         

    def sendStop(self):
        status = self.codec.sendMsg('localhost', 33333)

        if status:
            procData = self.codec.resArr
            user = procData['user']
            process = procData['process']

            self.deleteInfoProc(user, process)
            
    def deleteInfoProc(self, user, process):
        # Find user and his process
            for elem in self.proceses:

                if elem.user == user:

                    if elem.processName == process:

                        # Delete process frmo Proceses file
                        elem.deleteProcess()

                        i = self.proceses.index(elem)
                        # Delete process from array
                        self.proceses.pop(i)
                        print("Num of elemdnts: ", len(self.proceses))

                        return True
            
            # If process doesn't exists in array
            process = Process(user, process)
            process.deleteProcess()

            return False

    def sendStatus(self):
        # print("HERE")
        # procData = self.codec.resArr
        # user = procData['user']
        # process = procData['process']

        # for proc in self.proceses:
        #     if proc.IsTrue(user, process):

        print("Message sended")
        self.wfile.write("Test Mesage")
        # print("Message sended")


    def sendRestart(self):
        self.codec.sendMsg('localhost', 33333)

    def sendRequestStatus(self):
        pass

    def asyncRequest(self, execute):
        pass

    def printDebugMsg(self):
        s = ''
        
        for elem in self.codec.resArr:
            s += self.codec.resArr[elem]
            s += '\t'
        print('Message debug:', s)

if __name__ == "__main__":
    alice = Alice('localhost', 25000)
    alice.handle('{"action": "run", "user": "vasia", "process": "p1", "comand": "ping"}')
