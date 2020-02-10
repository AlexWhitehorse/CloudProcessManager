from source.Process import *
from constants import *
# from source.controller import *
from config import *
from source.modelsData import UserProc
# 
from source.states import spawnProcess, stopProces, changeStatus, addUser
# 
import os
import json
# from threading import Thread
import time
from source.server import Server
# from multiprocessing import Process, Lock, Value

class Alice(Server):
    proceses = []

    def handle(self, message):
        print(message)
        data = json.dumps(message.decode('ascii'))
        message = receiveDecode(message)
        # print(message["user"])

        if message["action"] == "run":
            userProc = spawnProcess(
                message["user"],
                message["process"],
                message["comand"] 
              )
            self.proceses.append(userProc)

            # changeStatus("petusa", "ping150", "NEW STATUS")
            # addUser("kolia", "test", "test coamnd", "statr")
        
        if message["action"] == 'stop':
            print("stoping")

            target_user = message['user']
            target_process = message['process']
            # UserProc
            # prc = self.proceses[0]
            counter = 0
            # UserProc <---
            for elem in self.proceses:

                if elem.IsTrue(target_user, target_process):

                    #  == is alive()
                    if stopProces(elem):
                        self.proceses.pop(counter)
                        pass

                counter += 1

            print(self.proceses)
            #  == is alive()
            # if stopProces(prc):
            #     print("Process sucscfully killed")
            #     self.proceses.pop(0)
            # else:
            #     print("Process is not killed")

        if message["action"] == "ts":
            print("sh")

            for proc in self.proceses:
                if proc.nameIsTrue("vasia"):
                    userProc = self.proceses[0]
                    print("data: ", userProc.process, userProc.parrent_pid)
                    print("child pid: ", userProc.getChildPid())
                    pass

def startAlice(ip, port):
    try:
        print("App started")
        return Alice(ip, port)

    except OSError:
        print("trying srart server again")
        time.sleep(1)
        return startAlice(ip, port)


if __name__ == "__main__":
    # print("Server starting")
    app = startAlice(IP, PORT)
    app.start_server()
    app.loop()
    app.stop_server()