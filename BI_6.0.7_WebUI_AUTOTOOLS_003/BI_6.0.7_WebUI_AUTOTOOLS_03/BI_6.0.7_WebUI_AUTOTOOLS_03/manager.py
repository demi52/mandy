import os
import sys
from WEB import main
from multiprocessing import Process

if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(path)
    sys.path.append(r"%s\lib\webui" %path)
    Process(target=main,).start()
    import managerun
    managerun.start()
