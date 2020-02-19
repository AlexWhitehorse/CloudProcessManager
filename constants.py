# import os
from config import *
 
import json


NAME_FOLDER_LOGS = "ProcessManager_tmp/"
DIR_LOGS = path_to_tmp_file + NAME_FOLDER_LOGS


STATUS_FILE = os.path.abspath("processes.json")
ERRORS_PATTERN = os.path.abspath("errors.json")

IP = server_ip

PORT = server_port

NUM_OF_CHECKING_LOG_STR = 1

NUM_MONO_CHECS = 3

MAX_NUM_ERRORS = 3

MAX_TIMER_SEC = 300

PERIOD_CHECK_LOG_SEC = 3

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

