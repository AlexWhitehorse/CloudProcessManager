
from TCPServer.TCPHandler import Alice
from source.constants import IP, PORT
from onStart.threadThis import MyThreads

class Main():
    
    def __init__(self):
        self.alice = Alice(IP, PORT)

    def startTCPserver(self):
        self.alice.start_server()

    def runForever(self):
        self.alice.loop()
        self.alice.stop_server()


if __name__ == "__main__":    
    threads = MyThreads()
    threads.threadsStart()

    main = Main()
    main.startTCPserver()
    print('Application started on ', IP, ':', PORT)
    main.runForever()