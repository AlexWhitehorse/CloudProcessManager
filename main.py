from source.Process import *
from constants import *
# from source.controller import *
from config import *
from source.modelsData import UserProc
# 
from source.states import spawnProcess, stopProces, restart, runErrorController
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
        data = json.dumps(message.decode('ascii'))
        message = receiveDecode(message)

        if message["action"] == "run":
            self.process_run(message)
        
        if message["action"] == 'stop':
            self.process_stop(message)

        if message["action"] == 'restart':
            """ 
            print("stoping")

            target_user = message['user']
            target_process = message['process']

            for elem in self.proceses:
                if elem.IsTrue(target_user, target_process):
                    restart(elem)
            """
            self.process_restart(message)


    def process_run(self, message):

        userProc = spawnProcess(
                message["user"],
                message["process"],
                message["comand"] 
              )
        self.proceses.append(userProc)


    def process_stop(self, message):

        # print("stoping")

        target_user = message['user']
        target_process = message['process']

        counter = 0
        # UserProc <---
        for elem in self.proceses:

            if elem.IsTrue(target_user, target_process):

                #  == is alive()
                if stopProces(elem):
                    self.proceses.pop(counter)
                    pass

            counter += 1


    def process_restart(self, message):
        self.process_stop(message)
        self.process_run(message)


def startAlice(ip, port):
    try:
        print("App started")
        return Alice(ip, port)

    except OSError:
        print("trying srart server again")
        time.sleep(1)
        return startAlice(ip, port)



if __name__ == "__main__":
    
    app = startAlice(IP, PORT)
    app.start_server()

    runErrorController()

    app.loop()
    app.stop_server()