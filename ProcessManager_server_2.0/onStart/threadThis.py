from onStart.onStart import onStart
from source.constants import TIME_TO_AUTOSTART
import threading
import time

class MyThreads:
    def __init__(self):
        pass

    def ThreadOnStart(self):
        print('Автостарт процессов через %sс.' % (TIME_TO_AUTOSTART))
        time.sleep(TIME_TO_AUTOSTART)
        test = onStart()
        test.go()

    def threadsStart(self):
        threadOnStart = threading.Thread(target=self.ThreadOnStart)
        threadOnStart.start()