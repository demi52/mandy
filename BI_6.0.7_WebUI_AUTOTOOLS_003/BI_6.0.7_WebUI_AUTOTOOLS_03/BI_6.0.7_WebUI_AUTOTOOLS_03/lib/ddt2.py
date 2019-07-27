__autor__ = "鲁旭"
import copy
datas={}

def data(user=(1, 2,3,4,5)):

    def b(func):
        if not "data" in globals():
            global datas
            datas = {}
        if not func.__name__ in datas:
           datas[func.__name__] = user

        def c(self, x, *args, **kwargs):
            func(self, x, *args, **kwargs)
        return c
    return b

def ddt(cls):
    for name, parm in datas.items():
        for p in parm:
            source=getattr(cls, name)
            sources=copy.deepcopy(source)
            print(id(sources))
            setattr(cls, "test_%s" % p, sources)
            func = getattr(cls, "test_%s" % p)
            sources.__defaults__ = (p, p)
            # exec("""cls.test_%s.__defaults__ = (%s, %s)"""%(p,p,p))
            print(source.__defaults__,sources.__name__)

    return cls

@ddt
class M():

    @data()
    def putme(self, x):
        print("puttme", x)


if __name__ == "__main__":
    print(dir(M))
    m=M()
    m.test_1()
    m.test_2()
    m.test_3()
    m.test_4()
