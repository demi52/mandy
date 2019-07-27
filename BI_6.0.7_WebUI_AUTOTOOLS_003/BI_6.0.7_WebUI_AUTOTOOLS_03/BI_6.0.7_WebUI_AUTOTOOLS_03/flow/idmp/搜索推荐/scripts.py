from lib.funcslib import log
__author__ = "luxu"
import requests
import re
import json

class Api_搜索推荐():

    addres = "http://10.50.108.16:8092"
    obj = None
    timeout = 10
    mc = "02000000000000010000000002894376"
    typeid = "002"
    userid="123456"

    def replacepar(self,url):
        self.url = re.compile( r"[htps]+?://[^/]+" ).sub( self.addres, url)
        self.url = re.sub(r"(?<={0}=)[^&]*".format("mc"), self.mc, self.url)
        self.url = re.sub(r"(?<={0}=)[^&]*".format("typeid"), self.typeid, self.url )
        self.url = re.sub(r"(?<={0}=)[^&]*".format("userid"), self.userid, self.url )
        print(self.url)

    def execute_test(self, url,data={}):
        self.replacepar(url=url)
        if data:
            self.result = requests.post(url=self.url, data=data,timeout=self.timeout)
        elif not data:
            self.result = requests.get(url=self.url, timeout=self.timeout)

        log().info("\n{1}{0}".format(self.result.text, "\t" * 2))
        log().info(self.result.url)
        self.get_text()
        self.out()

    def get_text(self):
        e = []
        try:
            try:
                self.text = eval(self.result.text)
            except Exception as e1:
                e.append(e1)
                self.text= json.loads(self.result.text)
        except Exception as e2:
            e.append(e2)
            log().error("不合发的数据")
            raise Exception(e)

    def replacetime(self):
        pass

    def out(self):

        print(self.text)
        s=self.result.url
        print(str(bytes(s,encoding="utf-8"),encoding="utf-8"))
        print("total == {0}".format(self.text.get("total")))

        if "count " in self.text.keys():
            print( "count   == %s" % self.text["count"])
        elif "columntype" in self.text.keys():
            print("columntype == ", len(self.text.get("columntype")), [i.get("columnname") for i in self.text.get("columntype",[])])



        try:
            coluname_subject = [i["columnname"] for i in self.text["subject"]]
            print("all  ",len(coluname_subject), "\n", coluname_subject)

            sublist=[]
            for i in coluname_subject:
                if sublist==[] or sublist[-1]!=i:
                    sublist.append(i)
            print("sublist == ", sublist)


        except:
         ""


class 搜索():

    addres = "http://10.50.108.16:8092"
    obj = None
    timeout = 10
    mc = "02000000000000010000000002894376"
    typeid = "002"
    userid="123456"
    hdflag="2"

    def replacepar(self,url):
        self.url = re.compile( r"[htps]+?://[^/]+" ).sub( self.addres, url)
        if self.par:
            self.url = re.sub(r"(?<={0}=)[^&]*".format("mc"), self.mc, self.url)
            self.url = re.sub( r"(?<={0}=)[^&]*".format("typeid"), self.typeid, self.url )
            self.url = re.sub( r"(?<={0}=)[^&]*".format("userid"), self.userid, self.url )
            self.url = re.sub( r"(?<={0}=)[^&]*".format( "hdflag" ), self.hdflag, self.url )

    def executeapi(self, url, data={}):
        self.replacepar(url=url)
        if data:
            self.result = requests.post( url=self.url, data=data, timeout=self.timeout )
        elif not data:
            self.result = requests.get( url=self.url, timeout=self.timeout )

        log().info( "\n{1}{0}".format( self.result.text, "\t" * 2 ) )
        log().info( self.result.url )

    def __get_text(self):
        e = []
        try:
            try:
                self.text = json.loads( self.result.text )
            except Exception as e1:
                e.append(e1)
                self.text = eval( self.result.text)
        except Exception as e2:
            e.append(e2)
            log().error("不合法的数据")
            raise Exception(e)

    def search_url(self,key):
        value=re.compile(r"(?<={0}=)[^&]*".format(key)).findall(self.url)
        if value:
            return value[0]

    def get_text_value(self,kone=None,ktwo=None,repeat=False):
        """获取响应内容"""
        if kone !=None :
            self.datalist1=self.text.get(kone, "")
            log().debug( "datalist1--{0}==   {1}".format( kone, self.datalist1 ) )
            if ktwo !=None and type(self.datalist1) == list and self.datalist1:
                self.datalist2=[x.get(ktwo,"") for x in self.datalist1]
                if repeat:
                    b = ""
                    sub = []
                    for y in self.datalist2:
                        if y != b:
                            sub.append(y)
                            b = y
                    self.datalist2=sub
            else:
                self.datalist2 = []
                log().debug( "datalist2--{0}==   {1}".format(ktwo,self.datalist2))
            return  self.datalist2

    def execute_test(self, url,data={},par=True):
        self.par=par
        self.executeapi( url=url, data=data )
        self.__get_text()

if __name__ == "__main__":
    pass
    url = "http://{{idpURL}}/idpvoice/searchchannel?name=小金&start=0&count=20"
    sample = Api_搜索推荐()
    sample.execute_test(url)




