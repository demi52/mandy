import re
path=r"D:\\data.txt"
# path=r"D:\\web.txt"
with open(path,mode="r",encoding="utf-8") as fp:
    strs=fp.read()

n=re.compile(r"{.+?}",).findall(strs)

def parse(s=""):
    s=str(s).strip()
    if s.endswith("%") :
        """百分数转换"""
        res=re.compile(r".+(?=%)").findall(s)
        if res:
            result=str(int(float(res[0])/100))
        else:
            result = str()
    elif "." in s:
        try:
            result = str(int(float(s)))
        except:
            result =""
    elif "," in s:
        result =s.replace(",","")
    else:
        result=s
    return result

print(len(n))
for  i in n:
    i=eval(i)
    for y in i.values():
        print(parse(y))