
from lib.funcslib import parserxlsx
path=r"D:\自动化用例统计.xls"
a=parserxlsx(path)
# print(a,)

count_all=len(a)
new_case=[]
for i in range(0,count_all):
    sep=a[i]
    if "实时数据" in sep[1]:
        sep[2]="".replace(sep[1],"")
        sep_str="-".join(sep)
        sep_str.replace("_","-")
        new_case.append(sep_str)

[print(i) for i in new_case]