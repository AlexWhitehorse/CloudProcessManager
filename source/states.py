from source.Process import MyProcess
from constants import DIR_LOGS, STATUS_FILE
from source.modelsData import UserProc, STATUSES

from multiprocessing import Process, Value

import subprocess 
# 
import json
import os

# Функции поведения для handle
def spawnProcess(nameUser, nameProcess, comand):

    userProc = UserProc(nameUser, nameProcess)

    proc = Process(target=rn, args = (userProc.child_pid, nameUser, nameProcess, comand ))
    proc.start()

    userProc.process = proc
    userProc.parrent_pid = proc.pid
    userProc.comand = comand

    userProc.addUserProcess()

    return userProc

def rn(val, nameUser, nameProcess, comand):

    while 1:
        proc = MyProcess(nameUser, nameProcess, comand)
        proc.mstart()

        print(proc.mprocess.pid)

        val.value = proc.mprocess.pid
        proc.mprocess.wait()

# geting obj UserProc as first argument
def stopProces(userProc):

    userProc = userProc
    pid      = userProc.child_pid.value
    process  = userProc.process

    process.terminate()
    process.join()

    # We heave a problem!
    if killProc(pid):
        
        print("Error: user: %s, nameProcess: %s, pid: %s. NOT killed!" % (userProc.user, userProc.nameProcess, pid))
        return False
    # Sucscess
    else:
        print("Process user: %s, nameProcess: %s, pid: %s. Sucscessfully killed" % (userProc.user, userProc.nameProcess, pid))
        
        pathToPidFile = DIR_LOGS + "%s_%s.txt" % (userProc.user, userProc.nameProcess)

        os.remove(pathToPidFile)

        userProc.deleteUserProcess()
        return True

def killProc(pid):
    return subprocess.call("kill %s" % str(pid), shell=True)

# change status
def changeStatus(nameUser, nameProcess, newStatus):
    statusFile = STATUS_FILE
    
    f = open(statusFile, "r")
    d = f.read()
    f.close()

    data = json.loads(d)
    
    user = data[nameUser]
    process = user[nameProcess]

    process["status"] = newStatus

    user[nameProcess] = process
    data[nameUser] = user

    toFile = json.dumps(data)

    f = open(statusFile, "w")
    f.write(toFile)
    f.close()

    with open(statusFile) as f:
        print(f.read())

def addStatus(nameUser, nameProcess, comand, status):
    statusFile = STATUS_FILE
    
    f = open(statusFile, "r")
    d = f.read()
    f.close()

    data = json.loads(d)
    
    user = data[nameUser]
    process = user[nameProcess]

    process["status"] = newStatus

    user[nameProcess] = process
    data[nameUser] = user

    toFile = json.dumps(data)

    f = open(statusFile, "w")
    f.write(toFile)
    f.close()

def addUser(nameUser, nameProcess, comand, status):
    statusFile = STATUS_FILE
    
    f = open(statusFile, "r")
    d = f.read()
    f.close()

    data = json.loads(d)

    process = {}
    user = {}
    process["comand"] = comand
    process["status"] = status

    user[nameProcess] = process
    data[nameUser] = user

    toFile = json.dumps(data)

    f = open(statusFile, "w")
    f.write(toFile)
    f.close()






