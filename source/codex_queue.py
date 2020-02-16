# codex_queue.py
import threading
import socketserver


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024)
        self.server.queue.add(data)

class Queue:

    def __init__(self, ip, port):
        self.messages = []
        self.server = ThreadedTCPServer((ip, port), ThreadedTCPRequestHandler)
        self.server.queue = self
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True

        

    def start_server(self):
        self.server_thread.start()
        # print("Server loop running in thread:", self.server_thread.name)

    def stop_server(self):
        self.server.shutdown()
        self.server.server_close()

    def add(self, message):
        self.messages.append(message)

    def view(self):
        return self.messages

    def get(self):
        try:
            return self.messages.pop()
        except:
            print("Exception: in Queue, get()")

    def exists(self):
        return len(self.messages)