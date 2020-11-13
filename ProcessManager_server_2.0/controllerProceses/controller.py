import json

from source.constants import STATUS, fileProc

class Process():
    def __init__(self, user, process, comand = None, status = None):
        # self.processPid = 0
        self.user = user
        self.processName = process
        self.status = status
        self.comand = comand
        self.processesFile = fileProc

    def IsTrue(self, user, nameProcess):
        if user == self.user and nameProcess == self.nameProcess:
            return True
        return False

    # def changeStatus(self, newStatus):
    #     pass
    def addProcessToFile(self):
        df = self.readFile(self.processesFile)

        # if file does not exists
        try:
            data = json.loads(df)
        except json.decoder.JSONDecodeError as e:
            print(e)
            data = {}

        # if not user in file
        try:
            user = data[self.user]
        except KeyError as k:
            print(k)
            user = {}

        process = {}
        process['comand'] = self.comand
        # self.status = STATUS[1] ???
        user[self.processName] = process
        data[self.user] = user
        tofile = json.dumps(data)

        self.writeFile(self.processesFile, tofile)
    

    def deleteProcess(self):
        df = self.readFile(self.processesFile)

        data = json.loads(df)

        try:
            # Если это последний процесс у пользоваткля
            if len(data[self.user]) <= 1:

                data.pop(self.user)

                toFile = json.dumps(data)

                self.writeFile(self.processesFile, toFile)

            else:
                user = data[self.user]
                user.pop(self.processName)
                data[self.user] = user

                toFile = json.dumps(data)

                self.writeFile(self.processesFile, toFile)

        except KeyError as e:
            pass

    def readFile(self, file):
        f = open(file, "r")
        d = f.read()
        f.close()
        return d

    def writeFile(self, file, data):
        f = open(file, "w")
        f.write(data)
        f.close()

class Controller(Process):
    def __init__(self):
        Process.__init__(self)

    def addProcessToFile(self):
        df = self.readFile(self.processesFile)

        # if file does not exists
        try:
            data = json.loads(df)
        except json.decoder.JSONDecodeError as e:
            print(e)
            data = {}

        # if not user in file
        try:
            user = data[self.user]
        except KeyError as k:
            print(k)
            user = {}

        process = {}
        process['comand'] = self.comand
        # self.status = STATUS[1] ???
        user[self.nameProcess] = self.process
        data[self.user] = user
        tofile = json.dumps(data)

        self.writeFile(self.File, tofile)