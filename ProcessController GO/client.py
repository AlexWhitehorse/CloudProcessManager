import json
import socket


# Данные сервера на который будет отправлен запрос с этого клиента
HOST = 'localhost'
PORT = 33333    # Может быть любым


# restart   - перезапуск процесса
# status    - Ожидаеться ответ: runing/stopped & PID процесса, если запущен, в формате json
# out       - Запрос на вывод логов. 1 запрос = 1 строка логов
ACTIONS = {
    'run': 'run',
    'stop' : 'stop',
    'restart' : 'restart',
    'status' : 'status',
    'out' : 'out'
    }

class Message():
    def __init__(self):
        self.user = ''
        self.comand = ''
        self.action = ''
        self.processName = ''

    # Отправка байт в формате ascii
    def send(self):
        message = json.dumps(self.toCodecStr())
        # AF_INET - ipv4, int - port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            sock.connect((HOST, PORT))
            sock.sendall(bytes(message, 'ascii'))
            data = sock.recv(1024)
        except ConnectionRefusedError:
            data = 'Connection error! '
        finally:
            sock.close()

        return data

    # Формирование строки для передачи 
    def toCodecStr(self):

        if 'comand' is not '':
            comand = self.comand
        else:
            comand = ''
        
        user = self.user
        process = self.processName
        action = self.action


        # Итоговое формирование массива для json и дальнейшей передачи на серв 
        # Поле "comand" заполнено только в сообщениия для старта. Во всех остальных случаях оно пустое или игнорируется 
        # {"vasia": 
        # {"NameProcess" : 
        # {"comand": "ping", comand: "run/stop/restart"}}}
        rs = {user : {process: {"comand": comand, "state": action}}}
        print('Try to send msg: ')
        print(rs)
        
        return rs

def toServ(user, proc, comand, action):
    msg = Message()

    msg.user = user
    msg.processName = proc
    msg.comand = comand
    msg.action = action

    ans = msg.send()

    print('Answ: ' + str(ans))



#=============Processes data==========================

# Данные для старта процесса
def sendStart():
    toServ(
        'Vasia', 
        'first_process', 
        #'ffmpeg -i \"rtmp://cdn10.live-tv.od.ua/7tvod/7tvod\" -c copy -f mpegts -flush_packets 0 \"udp://127.0.0.1:1111?fifo_size=50000&pkt_size=1316\"',
        ["ffmpeg","-i","rtmp://cdn10.live-tv.od.ua/7tvod/7tvod","-c","copy","-f","mpegts","-flush_packets","0","udp://127.0.0.1:1111?fifo_size=50000&pkt_size=1316"],
        ACTIONS['run']
     )

def sendStop():
    toServ(
        'Vasia', 
        'first_process', 
        [], 
        ACTIONS['stop']
    )
    
def switch(argument):
    switcher = {
        1: sendStart,
        2: sendStop
    }

    func = switcher.get(argument, lambda: "Invalid value")
    func()

#====================================================

def main():
    print('\nChoise action:')
    print('1: start process')
    print('2: stop process')
    print('Ctrl + c to exit')

    act = input()
    switch(int(act))
    main()

if __name__ == "__main__":
    main()

