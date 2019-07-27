from config.dataoftest import *

print(BaseData.Time.test1)
if __name__ == "__main__":

    area="NanChuan"
    c=eval(area)
    name=[n for n in dir(c) if not n.startswith("__")]
    path=[]
    for x in name:
        classname=eval("""{0}.{1}""" .format(area,x))
        classlist = [n for n in dir(classname) if not n.startswith("__")]
        for y in classlist:
            path.append("%s.%s.%s" %(area,x,y))

    print(path)
    path="#".join(path)
    import re
    x=re.compile(r"[^#]+%s"%("Channellive")).findall(path)[0]
    print(x)
    cn=eval("%s.%s" %(x,"Time"))
    # print(cn.__dict__)
    name3 = [n for n in dir(cn) if not n.startswith("__")]
    print(name3)
    print([eval("%s.%s" %("cn",v)) for v in name3])