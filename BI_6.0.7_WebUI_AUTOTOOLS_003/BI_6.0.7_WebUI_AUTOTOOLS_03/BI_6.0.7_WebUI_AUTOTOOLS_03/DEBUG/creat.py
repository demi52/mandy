__autor__ = "鲁旭"

from lib.funcslib import writexlsx as wx
import re
p = r"C:\Users\BenQ\Desktop\无数据.txt"

fp = open(p, mode="r", encoding="utf-8")
s = fp.read()
res = re.compile(r"test_(.+?)\s*\(test_case\.bi\.(.+?)\.case(.+?)\.Test(.+?)\)").findall(s)
print(len(res))

newres=[]
for i in res:
    i = list(i)
    head = i.pop(0)
    i.append(head)
    i.append("无数据")
    print(len(i))
    newres.append(i)
print(newres)

newres.insert(0, ["页面一级菜单", "页面二级菜单", "测试项", "测试项", "有无数据"])


if __name__ == "__main__":
   wx("无数据统计.xlsx",newres)