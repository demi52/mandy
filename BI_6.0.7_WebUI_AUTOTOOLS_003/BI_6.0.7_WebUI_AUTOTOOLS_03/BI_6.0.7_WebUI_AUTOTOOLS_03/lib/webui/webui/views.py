from django.shortcuts import render
from django.http import HttpResponse
import os
import re
import sys
import signal
from multiprocessing import Process
from . import usercache

# Create your views here.
def hello(request):
    return HttpResponse("connect sucess")

def runat(request):
    # workspace=re.compile(r".+?(?=webui)").match(__file__).group()
    # sys.path.append(workspace)

    import main
    P = Process(target=main.run)
    usercache.Ioput.input("p", P)
    rp = usercache.Ioput.output("p")
    if isinstance(rp, Process) and not rp.is_alive():
        rp.start()
        return HttpResponse("run  main.py sucess" )
    else:
        return HttpResponse("main.py is  executing")

def killat(request):
    processobject= usercache.Ioput.output("p")
    if isinstance(processobject, Process) and  processobject.is_alive():
        id=processobject.ident
        os.kill(id,signal.SIGTERM)
        usercache.Ioput.output("p", clean=True)
        return HttpResponse("kill pid %s sucess" % id)
    else:
        return HttpResponse("task stop")


if __name__ == "__main__":
    print(runat(1))