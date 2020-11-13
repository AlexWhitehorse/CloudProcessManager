import json
import socket

ACTIONS = {
    'run' : 'run',
    'stop' : 'stop',
    'restart' : 'restart',
    'status' : 'status'
    }

class Codec():
    def __init__(self, resArr = None):
        self.resArr = dict()
        self.action = ''


    def sendMsg(self, host, port):
        message = json.dumps(self.toCodecStr(self.resArr))
        
        # AF_INET - ipv4, int - port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # try:
        sock.connect((host, port))
        sock.sendall(bytes(message, 'ascii'))
        answ = sock.recv(1024)

        data = self.isAnsOk(answ)
        print("Server answer: ", answ, "\nIs means: ", data)
        # except:
        #     data = False
        # finally:
        sock.close()

        return data

    def toCodecStr(self, arrMsg):

        if 'comand' in arrMsg:
            comand = arrMsg['comand']
        else:
            comand = ''
        
        user = arrMsg['user']
        process = arrMsg['process']
        action = arrMsg['action']


        comand = comand.replace("\"","").split()

        # {"vasia": 
        # {"NameProcess" : 
        # {"comand": "ping", comand: "run/stop/restart"}}}
        rs = {user : {process: {"comand": comand, "state": action}}}
        print(rs)
        return rs


    def decodeMsg(self, message):
        try:
            data = json.loads(message)
        except:
            print("Can not read json:")
            print(message)
            return

        self.action = ACTIONS[data['action']]
        self.resArr['action'] = ACTIONS[data['action']]
        self.resArr['user'] = data['user']
        self.resArr['process'] = data['process']

        # if data['comand']:
        if 'comand' in data:
            self.resArr['comand'] = data['comand']
        

    # Инициализация значений
    def setData(self, action, user, process, comand = None):
        self.action = ACTIONS[action]
        self.resArr['action'] = ACTIONS[action]
        self.resArr['user'] = user
        self.resArr['process'] = process

        if comand is not None:
            self.resArr['comand'] = comand


    def isAnsOk(self, data):
        data = data.decode('utf-8')
        data = json.loads(data)
        el = data[0]
        # print('Is oK ', data, '\nEl: ', el['ok'])

        if el["ok"]:
            return True
        return False


    def debugData(self):
        return json.dumps(self.resArr)
        pass

#test
# if __name__ == "__main__":
#     codec = Codec()
#     codec.setData('run', 'vasia', 'p1', 'ping')
#     print(codec.resArr)
#     print(codec.debugData())
#     codec.decodeMsg(codec.debugData())
#     print(codec.resArr)