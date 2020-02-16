import socket
import time

from source.codex_queue import Queue


class Server:

    def __init__(self, ip, port):
        self.queue = Queue(ip, port)

    def start_server(self):
        self.queue.start_server()

    def stop_server(self):
        self.queue.stop_server()

    def loop(self):
        while True:
            if self.queue.exists():
                # print(self.queue.get())
                self.handle(self.queue.get())
            time.sleep(0.4)

    def handle(self, message):
        """
        Prototype
        """
        pass

    def send(self, ip, port, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        try:
            sock.sendall(bytes(message, 'ascii'))
        finally:
            sock.close()