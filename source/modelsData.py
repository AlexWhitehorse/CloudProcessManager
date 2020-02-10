from multiprocessing import Value
import json
from constants import STATUS_FILE

class UserProc():

    def __init__(self, user = 'default', nameProcess = "none"):
        self.process = False
        self.parrent_pid = 0
        self.child_pid = Value('i')
        self.nameProcess = nameProcess
        self.user = user
        self.stasus = STATUSES[2]
        self.statusFile = STATUS_FILE
        self.comand = 'HERE'

    def getChildPid(self):
        return self.child_pid.value

    def IsTrue(self, user, nameProcess):
        if user == self.user and nameProcess == self.nameProcess:
            return True
        return False

    def changeStatus(self, newStatus):
        d = self.readFile(self.statusFile)

        data = json.loads(d)

        user = data[self.user]
        process = user[self.nameProcess]

        self.stasus = newStatus
        process["status"] = newStatus

        user[self.nameProcess] = process
        data[self.user] = user

        toFile = json.dumps(data)

        self.writeFile(self.statusFile, toFile)

    def addUserProcess(self):
        d = self.readFile(self.statusFile)

        try:
            data = json.loads(d)
        except json.decoder.JSONDecodeError:
            data = {}

        try:
            user = data[self.user]
        except KeyError:
            user = {}

        process = {}

        process["comand"] = self.comand
        self.stasus = STATUSES[1]
        process["status"] = self.stasus

        user[self.nameProcess] = process
        data[self.user] = user

        toFile = json.dumps(data)

        self.writeFile(self.statusFile, toFile)

    def deleteUserProcess(self):
        d = self.readFile(self.statusFile)

        data = json.loads(d)

        # Если это последний процесс у пользоваткля
        if len(data[self.user]) <= 1:
            data.pop(self.user)

            toFile = json.dumps(data)

            self.writeFile(self.statusFile, toFile)

        else:

            user = data[self.user]
            user.pop(self.nameProcess)
            data[self.user] = user

            toFile = json.dumps(data)

            self.writeFile(self.statusFile, toFile)

    def readFile(self, file):
        f = open(file, "r")
        d = f.read()
        f.close()
        return d

    def writeFile(self, file, data):
        f = open(file, "w")
        f.write(data)
        f.close()


STATUSES = [
    "STOPING",
    "WORKING",
    "NONE"
]
