import time
from multiprocessing import Process


class Ioput():

    __data = {"p":None}

    @classmethod
    def input(cls, key="p", value=None):
        """
        线程通信input  str
        :param key:
        :param valueold:
        :return:
        """
        valueold=cls.__data.get(key, 0)
        if key == "p" and isinstance(valueold, Process) and valueold.is_alive():
            pass
        else:
            cls.__data[key] = value

    @classmethod
    def output(cls,key,clean=False):
        """
        """
        if key =="p":
            result = cls.__data.get("p", 0)
            if clean:
                cls.__data.pop(key,None)
            return result


def run():
    while True:
        pass
if __name__ == '__main__':
    p=Process(target=run)
    p2 = Process(target=run)
    Ioput.input("p",p)
    a=Ioput.output("p")
    a.start()
    time.sleep(4)
    Ioput.input("p",p2)
    a2=Ioput.output("p")
    print("bb",a2)