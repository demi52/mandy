s="""
    qdi: queryepgmedia
    starttime: 20190215
    endtime: 20190315
    datetype: D
    positioncode: 
    groupcode: MangGuoZhuanQuReMenTuiJian.java
    epggroup: 1
    token: ac4bc5b527a47a2f6c640d99065daee1
    sysid: t
    userid: test1
    """
import re
f=re.compile(r"(\w+):(.+)").findall(s)
data={x:y.strip() for x,y in f}
print(data)
