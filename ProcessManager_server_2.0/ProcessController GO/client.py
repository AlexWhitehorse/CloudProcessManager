import json
import socket


# Данные сервера на который будет отправлен запрос с этого клиента
HOST = 'localhost'
PORT = 33334    # Может быть любым


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
        ["/home/transcod/new/ffmpeg/ffmpeg", 
        "-rtbufsize", 
        "10M", 
        "-hwaccel", 
        "nvdec", 
        "-hwaccel_output_format", 
        "cuda", "-c:v", 
        "h264_cuvid", 
        "-i" "udp://239.111.11.12:11012?localaddr=192.168.111.2", 
        "-filter_complex", "[0:v]yadif_cuda=0:-1:0, split=2[out1][link2]; [link2]scale_cuda=1280:720[out2]", 
        "-map", "[out1]", "-map", "0:a", "-c:v", 
        "h264_nvenc", "-profile:v", "main", "-preset:v", 
        "llhq", "-no-scenecut", "true", "-bf", "3", 
        "-b_adapt", "0", "-coder", "cabac", "-b:v", 
        "6000k", "-maxrate", "6000k", "-bufsize", "6000k", 
        "-g", 
        "50", 
        "-keyint_min",
        "25", "-c:a", "aac", 
        "-b:a", "128k", "-ar", "48000", "-f", "flv", "rtmp://192.168.111.5/iptv?rtmpauth=ip:tv/otse-1080",  
        "-map", "[out2]", "-map", "0:a", "-c:v", "h264_nvenc", "-profile:v high", "-preset:v", "fast", "-no-scenecut", "true", "-bf", "3", "-b_adapt", "0", "-coder", "cabac", "-b:v", "3000k", "-maxrate", "3000k", "-bufsize", "3000k", "-g", "50", "-keyint_min", "25", "-c:a aac", "-b:a 128k", "-ar", "48000", "-f", "flv", "rtmp://192.168.111.5/iptv?rtmpauth=ip:tv/otse-720"],
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

