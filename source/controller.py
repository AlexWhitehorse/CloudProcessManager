from source.Process import MyProcess

from source.modelsData import UserProc

from multiprocessing import Process, Value

# Функции поведения для handle
def spawnProcess(nameUser):

    userProc = UserProc("vasia")

    proc = Process(target=rn, args = (userProc.child_pid, "ping -c 100 1.1.1.1" ))
    proc.start()

    userProc.process = proc
    userProc.parrent_pid = proc.pid

    return userProc

def rn(val, comand):
    while 1:
        proc = MyProcess(comand)
        proc.mstart()
        print(proc.mprocess.pid)
        val.value = proc.mprocess.pid
        proc.mprocess.wait()
                

        