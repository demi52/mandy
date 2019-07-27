__author__ = "luxu"
import sys, os
from lib.listen import ListenServerLog
path = os.getcwd()

if path not in sys.path:
    sys.path.insert(0, path)
print(sys.path)

if __name__ == "__main__":
    ListenServerLog().socketserver()

