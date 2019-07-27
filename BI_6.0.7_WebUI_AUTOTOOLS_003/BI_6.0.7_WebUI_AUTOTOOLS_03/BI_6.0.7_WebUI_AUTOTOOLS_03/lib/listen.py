#encoding='utf-8'
__author__ = "luxu"

import re
import socket
from lib.funcslib import log
from config.conf import Listen, Idpcs


class ListenServerLog():

    Numbers = 0
    IdpcsNumbers = 0
    Data = {"active": "getlog", "status": "start", "qdi": "queryOffLineUserDevelop"}
    Idmp_data = {"active":"get_idmp_log","status":"start"}

    def parrecvdata(self):
        """status == start  记录初始匹配日志条数
            status == end   获取所有匹配的日志条数
        """

        if "active" in self.data and "status" in self.data:
            if self.data.get("active", "") == "getlog" and "qdi" in self.data:
                self.__bi_protoal_log()

            elif self.data.get("active", "") == "get_idmp_log":
                self.__ipcs()
            else:
                self.result = {"status": "other", "result": [], "error": "param error"}
        else:
            self.result = {"status": "other", "result": [], "error": "param error"}

    def __bi_protoal_log(self):

        self.qdi = self.data["qdi"]
        self.status = self.data["status"]
        self.__readlogfile()

        if self.status == "start":
            ListenServerLog.Numbers = len( self.alllist )
            self.result = {"status": "start", "result": [], "error": ""}
            log().info( "return client %s ,userlog stop lins:%d" % (self.result, ListenServerLog.Numbers) )

        elif self.status == "end":
            self.__searchsql()
            ListenServerLog.Numbers = len( self.alllist )
            if len(self.list ) == 0:
                self.result = {"status": "end", "result": self.list, "error": "not found new userlog"}
                log().error( "return client %s " % self.result )

            elif len(self.list ) >= 1:
                self.result = {"status": "end", "result": self.list, "error": ""}
                log().info( "return client %s " % self.result )

    def __ipcs(self):

        self.status = self.data["status"]
        self.__readlogfile(file=Idpcs.idpcs_path)

        if self.status == "start":
            ListenServerLog.IdpcsNumbers = len( self.alllist )
            self.result = {"status": "start", "result": [], "error": ""}
            log().info("return client %s ,userlog stop lins:%d" % (self.result, ListenServerLog.Numbers) )

        elif self.status == "end":
            self.__search_id()
            ListenServerLog.IdpcsNumbers = len( self.alllist )
            if len( self.list ) == 0:
                self.result = {"status": "end", "result": self.list, "error": "not found new userlog"}
                log().error( "return client %s " % self.result )

            elif len( self.list ) >= 1:
                self.result = {"status": "end", "result": self.list, "error": ""}
                log().info("return client %s " % self.result )

    def __readlogfile(self, file=Listen.serverlogpath):
        with open(file) as fp:
            self.alllist = fp.readlines()


    def __search_id(self):
        """获取中间表ID"""
        lastlist = self.alllist[ListenServerLog.IdpcsNumbers:]
        strs = "".join(lastlist)
        patt = r"(?<=there outside id is: )\w+"
        self.list = re.compile(patt).findall(strs)


    def __searchsql(self):
        """根据qdi匹配日志中的sql"""
        lastlist = self.alllist[ListenServerLog.Numbers:]
        strs = "".join(lastlist)

        p1 = r"\d.+?%s:.+?(\[oracle.+?\])\n+" % self.qdi
        p2 = r"\d.+?%s:.+?Preparing: (select.+?)\n+" % self.qdi
        p3 = r"\d.+?%s:.+?Parameters: ((?:.+\(.+?\), ){0,}(?:.+\(.+?\)))\n" % self.qdi
        pattern = p1+p2+p3
        self.list = re.compile(pattern=pattern).findall(strs)
        log().info("%s search  count %s = %s" % (self.status, self.qdi, len(self.list)))


    def socketserver(self):
        self.list = []
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((Listen.hostaddres, Listen.port))
            s.listen(2)
            while True:
                conn, addr = s.accept()
                try:
                    self.data = eval(conn.recv(102400))
                    log().info("{1}->{0}".format(self.data, addr))
                    self.parrecvdata()
                except Exception as e:
                    value = bytes(str({"status": "functionerror", "result": [], "error": "server no execute"}),
                              encoding='utf-8')
                    log().error(" return client %s , recv data is %s " % (e, value))
                else:
                    value = bytes(str(self.result), encoding='utf-8')
                conn.sendall(value)

    def _socketclient(self, senddata=None):
        """
        :param senddata: dict   sample {"active": "getlog", "status": "start", "qdi": "queryOffLineUserDevelop"}
        :return: dict
        """
        if senddata == None :
            senddata = ListenServerLog.Data
        if type(senddata) is not dict:
            raise Exception("params type  error is not a dict ")
        if senddata["status"] not in ["start", "end"]:
            raise Exception("params status error not in  start or  end ")

        b_send = bytes(str(senddata), encoding='utf-8')

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((Listen.hostaddres, Listen.port))
            s.sendall(b_send)
            log().info("send data  %s  is success  " % senddata)
            data = s.recv(102400)
        receive = eval(str(data,encoding="utf-8"))
        log().debug(("get result dict sucess ", receive))
        return receive

    def searchqdi(self, status="start", qdi="queryOffLineUserDevelop"):
        return self._socketclient( senddata={"active": "getlog", "status": status, "qdi": qdi})

    def userdevelopsearch(self, status="start"):
        """用户发展获取日志接口"""
        return self._socketclient(senddata={"active": "getlog", "status": status, "qdi": "queryOffLineUserDevelop"})

    def user_develop_searchC3(self, status="start"):
        """用户发展C3获取日志接口"""
        return self._socketclient(senddata={"active": "getlog", "status": status, "qdi": "queryc3OffLineUserDevelop"})

    def user_active_search(self, status="start"):
        """用户活跃获取日志接口"""
        return self._socketclient(senddata={"active": "getlog", "status": status, "qdi": "queryOffLineUserActivity"})
    def idpcs_get_id(self,status="start"):
        """idpcs获取中间表id"""
        return self._socketclient(senddata={"active": "get_idmp_log", "status": status})


if __name__ == "__main__":
    import threading
    import os
    p=ListenServerLog()
    # t1=threading.Thread(target=p.socketserver)
    # t1.start()
    # print(__file__)
    # print(os.getcwd())
    # p._socketclient()
    # w=p.idpcs_get_id("start")
    w = p.idpcs_get_id( "end" )
    print(w)
