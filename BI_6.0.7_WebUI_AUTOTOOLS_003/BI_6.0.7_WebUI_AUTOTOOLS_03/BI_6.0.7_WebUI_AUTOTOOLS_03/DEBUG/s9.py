from lib.funcslib import get_token, Ioput
import requests,time
dict_reult = {
	"ACTIVEPERSENT": 1.0041,
	"ACTIVEUSER": 139177,
	"ACTIVITYUSER": 139177,
	"ALLUSER": 138612,
	"BOOTPERSENT": 1.0041,
	"BOOTUSER": 139177,
	"CYCLETYPE": "D",
	"HIGHLIVEUSER": 48875,
	"LOGINCOUNT": 194662,
	"LOGINCOUNTAVG": 1.4044,
	"ONLINESECONDS": 1243599.1486,
	"ONLINESECONDSAVG": 8.9718,
    "ORDERPERSENT": 0.0013,
    "ORDERUSER": 176,
    "ORDINARYUSER": 33887,
    "SILENTPERSENT": -0.0041,
    "SILENTUSER": -565,
    "SUMDATE": "2019-02-15"}
cache = dict()

data = {
"qdi": "queryOffLineUserDevelop",
"begindate": "20180415",
"enddate": "20190418",
    "x":"1",
"datetype": "D",
"token": "2b4e8e5b6d706140f4019a8a2391856f",
"sysid": "u",
"userid": "test1"
    }
from threading import Thread,Timer

class M():

    @get_token
    def ret_result(self):
        url = r"http://10.48.115.25/statplatform5/query"
        data["token"] = self.token
        try:
            res = requests.post(url, data=data, timeout=5)
            text = eval(res.text)["subject"][0]
        except:
            text = None
        Ioput.input("text0", text)
        print(text)


    def execute(self):
        t=Thread(target=self.ret_result,)
        t.start()




# print(time.time())
#
# m=M()
# m.execute()



