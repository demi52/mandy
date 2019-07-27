import requests,time



url = r"http://10.48.115.25/statplatform5/query"
data = {
        'token': '92f08c39250159d262508d3ad20789d5',
        'qdi': 'queryOffLineUserActivityDtlA',
        'userid': 'test1',
        'begindate':'20190215',
        'enddate': '20190315',
        'datetype': 'D',
        'sysid': 'u'
}

print(time.time())
result=requests.post(url=url, data=data)
print(result.text)
print(time.time())
