__author__ = "luxu"

import requests as rs
import re
import json


class test_api():

    def SearchWiki(self, title="天龙八部22"):
        url = """http://epgapi.cnsta.cn/epgapi?jsonstr={
          "action": "SearchWiki", 
          "developer": {
            "apikey": "339H6LPM", 
            "secretkey": "135b91657f582790f015301bf5f6fba7"
          }, 
          "user": {
            "userid": "123"
          }, 
          "device": {
            "dnum": "123"
          }, 
          "param": {
            "keyword": "title:动物世界"
          }
        }
            """
        url = re.sub(r"(?<=\"keyword\": \"title:).+?(?=\")", title, url)
        self.url = url

    def GetProgramsByChannel(self):
        url = """http://epgapi.cnsta.cn/epgapi?jsonstr={
         "action": "GetProgramsByChannel", 
         "developer": {
         "apikey": "339H6LPM", 
         "secretkey": "135b91657f582790f015301bf5f6fba7"
          }, 
         "user": {
         "userid": "123"
         }, 
         "device": {
         "dnum": "123"
          }, 
         "param": {
          "channel_code": "guofangjunshi", 
          "start_time": "2018-10-29 00:00:00", 
          "end_time": "2017-10-29 23:59:59"
         }
     }
    """
        self.url = url

    def GetProgramByChannels(self):
        url = """http://epgapi.cnsta.cn/epgapi?jsonstr={
       "action": "GetProgramByChannels", 
       "developer": {
       "apikey": "339H6LPM", 
        "secretkey": "135b91657f582790f015301bf5f6fba7"
        }, 
          "user": {
      "userid": "123"
         }, 
         "device": {
        "dnum": "123"
      }, 
      "param": {
         "channel_codes": [
         "guofangjunshi"

     ]
     }
    }
        """
        self.url = url

    def GetChannelsBySP(self):
        url = """http://epgapi.cnsta.cn/epgapi?jsonstr={
        "action": "GetChannelsBySP", 
        "developer": {
        "apikey": "339H6LPM", 
        "secretkey": "135b91657f582790f015301bf5f6fba7"
        }, 
        "user": {
        "userid": "123"
        }, 
        "device": {
        "dnum": "123"
        }, 
        "param": { "guofangjunshi": "国防军事", 
        "type": "2",
        "typevalue": "请联系相关人员索要 [spcode唯一不变的]"
        }
    }
         """
        self.url = url

    def get(self):
        result = rs.get(self.url)
        return str(result.content, encoding="unicode-escape"),result.text


if __name__ == "__main__":
    ob = test_api()
    ob.SearchWiki()
    r,r2=ob.get()
    print(r)
    print(re.findall(r"(?<=\"num\"\:).+?(?=,)",r))











