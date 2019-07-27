import configparser
import random


def add_testdata(sec=None,opt=None,value=None):
    cfg=configparser.ConfigParser()
    cfg.read(r"D:\Script\UD_BI\data\data.txt",encoding="utf-8")
    # s=cfg.get("idpc","test25")
    # print(type(eval(s)),eval(s))
    cfg.set(sec,opt,value)
    with   open(r"D:\Script\UD_BI\data\data.txt",mode="w") as fp:
        cfg.write(fp)


def creatv():
    number=0

    v={"list_code":['02000022000000102015092199000056','02000000000000010000000002445933'],"rule":(("YEAR", "2"),("TITLE","3"))}
    v.pop("list_code")
    print(v)
    key=['YEAR', 'DIRECTORS', 'CASTS', 'TITLE', 'RATING', 'GENRES', 'WRITERS', 'LANGUAGES']

    for i in key:
        for k in range(1,4):
            v["rule"]=[("%s"%i,"%s"%k)]
            number +=1
            add_testdata("idpc","test%s"%(number),str(v))

    for i in range(0,20):
        ke=set(key)
        rule=[(t,str(random.choice(range(1,4)))) for t in ke]
        v["rule"]=rule
        number += 1
        add_testdata("idpc", "test%s" % (number), str(v))



# add_testdata()
creatv()

# from lib.dboracle import db_oracle
# print(db_oracle("SELECT count(*) from WS_PROCESS where   PROCESSRESULT='3' and  CODE in ('02000022000000102015092199000056','02000000000000010000000002445933')"))