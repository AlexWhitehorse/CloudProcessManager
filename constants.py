import os
from config import *
 
import json

# PATH_TO_PROC_S = os.path.abspath("processes.json")
DIR_LOGS = "/tmp/ProcessController/"
STATUS_FILE = os.path.abspath("processes.json")

IP = server_ip

PORT = server_port

NUM_OF_CHECKING_LOG_STR = 20

# CODEC
def sendStart(user, process, comand):
    strn = '{\"action\":%s,\"user\":%s,\"process\":%s,\"comand\":%s}' % ('"%s"' % "run", '"%s"' % user, '"%s"' % process, '"%s"' % comand)
    print(strn)
    return json.loads(strn)

# returns a dictionarry with data to process start
def receiveDecode(data):
    message = data.decode('ascii')
    data = json.loads(message)
    return data

