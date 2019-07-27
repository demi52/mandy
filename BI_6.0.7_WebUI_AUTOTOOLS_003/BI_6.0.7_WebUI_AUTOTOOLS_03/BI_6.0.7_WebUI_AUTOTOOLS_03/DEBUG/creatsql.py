# sql="UPDATE CATEGORYMAP SET EPGGROUP='' where name='上新了故宫';"
# import random
# gropu=["企业","家庭","军队","政府"]
#
# import requests
#
# url=r"http://10.50.108.20:8092/idp/search?q=a&userid=123456&sdonly=0&group=政府"
# url=r"http://10.50.108.20:8092/idp/search?q=a&userid=123456&sdonly=0&group=家庭"
# url=r"http://10.50.108.20:8092/idp/search?q=a&userid=123456&sdonly=0&group=企业"
# url=r"http://10.50.108.20:8092/idp/search?q=a&userid=123456&sdonly=0&group=酒店"
# result=requests.get(url)
# print(result.text)

from lib.funcslib import db_oracle
url=r"credb/oss@10.50.108.17:1521/ORCL"
sql="SELECT code from CATEGORYMAP"
code=db_oracle(sql,url)
print(code)
import os
import random

sqlactive="update  ws_mergedmedia set syncflagt = '2' where substr(status,1,1)='0'"

def k():
    for x in code:
        x=x[0]
        gropu=["企业","家庭","政府"]
        y=[random.choice(gropu) for i in range(0,random.randrange(1,4,1))]
        g=(",".join(y))
        sql2="UPDATE CATEGORYMAP SET EPGGROUP='%s'  where code='%s'" % (g,x)
        print(sql2)
        db_oracle(sql2,url)
k()
# db_oracle(sqlactive,url)