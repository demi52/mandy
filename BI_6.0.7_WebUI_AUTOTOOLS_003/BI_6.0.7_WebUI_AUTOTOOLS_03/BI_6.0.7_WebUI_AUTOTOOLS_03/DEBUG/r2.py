__autor__ = "鲁旭"
datas={}

class Meta(type):

    def __new__(meta, *args, **kwargs):
        meta.args=args
        clsname, bases, namespace = args
        print(namespace,"--------------",type(namespace))
        print(clsname, '3 created', )
        # print("clsname==%s\tbase==%s \tnamespace==%s\tkwargs==%s" % (clsname, bases, namespace, kwargs))
        print("kwargs==%s" % (kwargs))

        return super().__new__(meta, *args)

    def __init__(cls, *args, **kwargs):
        print(51111111,kwargs)
        for name, parm in datas.items():
            for p in parm:
                setattr(cls, "test_%s" % p, getattr(cls, name))
                func = getattr(cls, "test_%s" % p)
                func.__defaults__ = (p, p)
        print(cls.__name__, '5  inited',"__init__args==")
        super().__init__(*args)


    @classmethod
    def __prepare__(meta, name, bases):
        print(name,bases, " 1 class namespace created")
        return {}


class Base(object,metaclass=Meta,):
    a = 1
    b = 2
    def __new__(cls, *args, **kwargs):
        print(cls.__name__, ' 6 class instance created')
        return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        print(type(self).__name__, ' 7 class instance inited')

    def hello(self):
        pass










if __name__ == "__main__":
    pass
