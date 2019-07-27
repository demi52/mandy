def a():
    while True:
        pass
import os,time
import signal
from multiprocessing import Process
if __name__ == '__main__':

    p=Process(target=a,)
    p.name="luxu"
    p.start()

    time.sleep(5)
    os.kill(p.ident, signal.SIGTERM)