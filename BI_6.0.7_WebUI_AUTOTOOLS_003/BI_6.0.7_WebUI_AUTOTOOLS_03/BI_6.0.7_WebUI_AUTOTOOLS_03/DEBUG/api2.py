import requests
url = r"http://10.50.108.20/statplatform5/query"

# s="""
# qdi: queryordercarouselschedule
# starttime: 20190215
# endtime: 20190429
# datetype: D
# channelcode:
# token: ac4bc5b527a47a2f6c640d99065daee1
# sysid: u
# userid: test1
# """
# import re
# f=re.compile(r"(\w+):(.+)").findall(s)
# data={x.strip():y.strip() for x,y in f}
# print(data)

data = {'begindate': '20190331',
        'sysid': 'u',
        'qdi': 'queryc3OffLineUserActivity',
        'datetype': 'D',
        'userid': 'test1',
        'selectdate': None,
        'enddate': '20190331',
        'token': '2360df7a60de2b7e08c390594aecdc70'}




h={
"Accept": "application/json, text/javascript, */*; q=0.01",
"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}
m=requests.post(url,data=data,headers=h,timeout=30).text
print(m)


