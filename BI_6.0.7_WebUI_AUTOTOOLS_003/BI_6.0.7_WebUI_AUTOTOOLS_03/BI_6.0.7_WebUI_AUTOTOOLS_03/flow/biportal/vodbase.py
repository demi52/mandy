import re
import time

__author__ = "luxu"

from lib.funcslib import log, getparamnow
from config.conf import BI_protal as bt, BI_protal

from flow.biportal.base import Base, Base实时数据


class   VodlBase( Base):

    def _first(self,**kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="点播分析"]/parent::*')
        # self.exement('//*[@id="menu"]//a/span[text()="点播分析"]/parent::*/parent::*/ul//span[text()="实时数据"]/parent::*')
        time.sleep(3)

    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "userDevelopTable")
        self.dlfile = kwargs.get("dlfile", "直播频道-高清.xlsx")
        self.apiqdi = kwargs.get("apiqdi", "querycattopdetail")
        self.text = "查询"
        self.groupid ="realGroup"
        self.program=kwargs.get("program","提供商")

    def click_program(self):
        log().debug(self.program)
        self.checktext(element=self.program)
        self.exement('//*[@id="{0}"]//a[text()="{1}"]'.format(self.groupid, self.program))
        time.sleep(5)

    def f_search(self, **kwargs):
        """
        查询流程
        :param kwargs:
        :return
        """
        self.pararms( **kwargs )
        self.get_data_home()
        self._before()
        self.pararms(**kwargs)
        self.checktext(2, element=getattr(self, "text", ""))
        self.getsysereorlog("start")
        self.change_user()
        self.search_time_type()
        self.click_serach()
        self.move_detaildata()
        self.get_tablefirstdata()

    def f_outxlsx(self, **kwargs):
        """校验下载的XLSX数据"""
        self.f_search(**kwargs)
        self.outxlsx()
        self.getxlsxcontent()
        self.get_tablehead()

    def f2_search(self, **kwargs):
        """查看的流程"""
        self.pararms2(**kwargs)
        if getattr(self,"buttontext", None) != "子级栏目":
            self.get_data_datil()
        self._before(**kwargs)
        self.pararms2(**kwargs)
        if getattr(self, "buttontext", None) == "子级栏目":
            self.datatext = None
        self.checktext(2, element=getattr(self, "text", ""))
        self.getsysereorlog("start")
        self.change_time(pull_spanid="select2-changetime-container", pull_ulid="select2-changetime-results" )
        self.click_type()
        self.move_detaildata()
        self.get_tablefirstdata()

    def f2_outxlsx(self, **kwargs):
        """查看的导出数据流程"""
        self.f2_search(**kwargs)
        self.outxlsx()
        self.getxlsxcontent()
        self.get_tablehead()


class   Vod栏目分析(VodlBase):

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="栏目分析"]/parent::*')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)

        self.table_id = kwargs.get("table_id", "pandectTable")
        self.dlfile = kwargs.get("dlfile", "栏目分析.xlsx")
        self.apiqdi = kwargs.get("apiqdi", "querycattopdetail")
        self.text = "查询"

    def get_home_code(self):
        """ 获取code 供请求详情页使用"""
        code = [x["CATEGORYID"] for x in self.datatext][0]
        self.request_code = code

    def request_data_home(self):
        """构造首页请求数据"""
        start_time = self.start_time
        end_time = self.end_time
        self.data = \
            {
                "qdi": self.apiqdi,
                "starttime": start_time,
                "endtime": end_time,
                "categoryid":getattr(self, "request_code", None),
                "datetype": self.apidatatype,
                "rootcategoryid": None,
                "token": self.token,
                "sysid": getattr(self, "secsiono", "u"),
                "userid": "test1",
            }
        log().debug("requests 'url, data' \t {1},{0}".format(self.data, self.url_api))


class   Vod栏目分析详情(Vod栏目分析):

    Pararm = \
        {
            "时段数据": {"table_id": "timeTable", "dlfile": "点播栏目分析日期数据详情.xlsx", "apiqdi": "querycatdaydetail"},
            "子级栏目": {"table_id": "catDetailTable", "dlfile": "点播栏目分析子集栏目.xlsx", "apiqdi": "querycatchildall"},
            "节目收视": {"table_id": "programTable", "dlfile": "点播栏目分析节目收视.xlsx", "apiqdi": "querycatdaymedia"},
            "区域分布": {"table_id": "areaTable", "dlfile": "点播栏目分析区域分布.xlsx", "apiqdi": "querycatdayarea"},
        }


    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.f_search()
        self.look()

    @getparamnow
    def pararms2(self, **kwargs):
        """设置参数"""
        self.pararms(**kwargs)
        self.buttontext = kwargs.get("buttontext", "时段数据")
        self.table_id = kwargs.get("table_id", self.Pararm[self.buttontext]["table_id"])
        self.dlfile = kwargs.get("dlfile", self.Pararm[self.buttontext]["dlfile"])
        self.apiqdi = kwargs.get("apiqdi", self.Pararm[self.buttontext]["apiqdi"])
        self.text = self.buttontext

class   Vod栏目分析C3(Vod栏目分析):

    def _first(self, **kwargs):
        VodlBase._first(self,**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="栏目分析C3"]/parent::*')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)

        self.table_id = kwargs.get("table_id", "pandectTable")
        self.dlfile = kwargs.get("dlfile", "栏目分析.xlsx")
        self.apiqdi = kwargs.get("apiqdi", "queryc3cattopdetail")
        self.text = "查询"

class   Vod栏目分析详情C3(Vod栏目分析C3,Vod栏目分析详情):
    Pararm = \
        {
            "时段数据": {"table_id": "timeTable", "dlfile": "点播栏目分析日期数据详情.xlsx", "apiqdi": "queryc3catdaydetail"},
            "子级栏目": {"table_id": "catDetailTable", "dlfile": "点播栏目分析子集栏目.xlsx", "apiqdi": "queryc3catchildall"},
            "节目收视": {"table_id": "programTable", "dlfile": "点播栏目分析节目收视.xlsx", "apiqdi": "queryc3catdaymedia"},
            "区域分布": {"table_id": "areaTable", "dlfile": "点播栏目分析区域分布.xlsx", "apiqdi": "queryc3catdayarea"},
        }

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.f_search()
        self.look()



class   Vod节目信息(VodlBase):

    def get_home_code(self):
        """ 获取code 供请求详情页使用"""
        code = [x["CODE"] for x in self.datatext][0]
        self.request_code = code

    def request_data_home(self):
        """构造首页请求数据"""
        start_time = self.start_time
        end_time = self.end_time
        self.data = \
            {
                "offset": "0",
                "limit": "20",
                "name": None,
                "qdi": self.apiqdi,
                "starttime": start_time,
                "endtime": end_time,
                "code": getattr(self, "request_code", None),
                "datetype": self.apidatatype,
                "tagid": None,
                "token": self.token,
                "sysid": getattr(self, "secsiono", "u"),
                "userid": "test1",
            }
        log().debug("requests 'url, data' \t {1},{0}".format(self.data, self.url_api))

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//span[text()="节目信息"]')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "programTable")
        self.dlfile = kwargs.get("dlfile", "点播分析-节目信息.xlsx")
        self.apiqdi = kwargs.get("apiqdi", "querymediadetail_base")
        self.text = "查询"



class   Vod节目信息详情(Vod节目信息):
    Pararm = \
        {
            "时段收视": {"table_id": "timeTable", "dlfile": "节目收视详情日期数据.xlsx", "apiqdi": "querycatdaymonthdaydetail"},
            "子节目收视": {"table_id": "programTable", "dlfile": "专题分析-节目收视.xlsx", "apiqdi": "querycatdaymediadetail"},
            "路径分析": {"table_id": "pageTable", "dlfile": "节目收视-路径分析.xlsx", "apiqdi": "querymediapath"},
            "区域分布": {"table_id": "areaTable", "dlfile": "节目信息详情-区域分布.xlsx", "apiqdi": "querycatdayareadetail"},
        }

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.f_search()
        self.look()

    @getparamnow
    def pararms2(self, **kwargs):
        """设置参数"""
        self.pararms(**kwargs)
        self.buttontext = kwargs.get("buttontext", "时段收视")
        self.table_id = kwargs.get("table_id", self.Pararm[self.buttontext]["table_id"])
        self.dlfile = kwargs.get("dlfile", self.Pararm[self.buttontext]["dlfile"])
        self.apiqdi = kwargs.get("apiqdi", self.Pararm[self.buttontext]["apiqdi"])
        self.text = self.buttontext


class   Vod节目信息C3(Vod节目信息):
    alltime = 15
    def _first(self, **kwargs):
        VodlBase._first(self, **kwargs)
        self.exement('//*[@id="menu"]//span[text()="节目信息C3"]')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "programTable")
        self.dlfile = kwargs.get("dlfile", "点播分析-节目信息.xlsx")
        self.apiqdi = kwargs.get("apiqdi", "queryc3mediadetail_base")
        self.text = "查询"


class   Vod节目信息详情C3(Vod节目信息C3, Vod节目信息详情):

    Pararm = \
        {
            "时段收视": {"table_id": "timeTable", "dlfile": "节目收视详情日期数据.xlsx", "apiqdi": "queryc3catdaymonthdaydetail"},
            "子节目收视": {"table_id": "programTable", "dlfile": "专题分析-节目收视.xlsx", "apiqdi": "queryc3catdaymediadetail"},
            "路径分析": {"table_id": "pageTable", "dlfile": "节目收视-路径分析.xlsx", "apiqdi": "querymediapath"},
            "区域分布": {"table_id": "areaTable", "dlfile": "节目收视详情-区域分布.xlsx", "apiqdi": "queryc3catdayareadetail"},
        }

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.f_search()
        self.look()

class Vod媒资数据(VodlBase):

    movetype="底量"

    Pararm = \
        {
            "底量": {"table_id": "baseDataTable", "dlfile": "点播媒资数据-底量.xlsx", "apiqdi": "querycontentbaseall"},
            "增加量": {"table_id": "addDataTable", "dlfile": "点播媒资数据-新增.xlsx", "apiqdi": "querycontentaddall"},
            "删除量": {"table_id": "deleteDataTable", "dlfile": "点播媒资数据-删除量.xlsx", "apiqdi": "querycontentdelall"},
        }

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//span[text()="媒资数据"]')
        self.frame_change()


    def get_home_code(self):
        """ 获取code 供请求详情页使用"""
        code = re.compile(r"\d{4}-\d{0,2}-\d{0,2}").findall(str(self.datatext))[0]
        self.request_code = code.replace("-", "")

    def request_data_home(self):
        """构造首页请求数据"""
        start_time = self.start_time
        end_time = self.end_time
        self.data = \
            {
                "offset": "0",
                "limit": "20",
                "searchname": None,
                "qdi": self.apiqdi,
                "starttime": start_time,
                "endtime": end_time,
                "categoryid": getattr(self, "request_code", None),
                "datetype": self.apidatatype,
                "rootcategoryid": None,
                "monthday": getattr(self, "request_code", None),
                "token": self.token,
                "sysid": getattr(self, "secsiono", "u"),
                "userid": "test1",
            }
        log().debug("requests 'url, data' \t {1},{0}".format(self.data, self.url_api))

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.buttontext2 = kwargs.get("buttontext", self.movetype)
        self.table_id = self.Pararm[self.buttontext2]["table_id"]
        self.dlfile = self.Pararm[self.buttontext2]["dlfile"]
        self.apiqdi = self.Pararm[self.buttontext2]["apiqdi"]
        self.text = "查询"

    def click_butten2(self):
        element='//*[@id="navigation"]/li/a[text()="{0}"]'.format(self.buttontext2)
        self.exement(elements=element)

    def f_search(self, **kwargs):
        """
        查询流程
        :param kwargs:
        :return
        """
        self.pararms(**kwargs)
        self.get_data_home()
        self._before()
        self.pararms(**kwargs)
        self.checktext(2, element=getattr(self, "text", ""))
        self.getsysereorlog("start")
        self.change_user()
        self.click_butten2()
        self.search_time_type()
        self.click_serach()
        self.move_detaildata()
        self.get_tablefirstdata()

class Vod媒资数据详情(Vod媒资数据):

    Pararm2 = \
        {
            "单剧集": {"table_id": "singleTable", "dlfile": "点播媒资数据-底量-单剧集.xlsx", "apiqdi": "queryuseronlinefourmin"},
            "连续剧": {"table_id": "teleplayTable", "dlfile": "点播媒资数据-底量-连续剧.xlsx", "apiqdi": "querycatchildall"},
            "提供商": {"table_id": "providerTable", "dlfile": "点播媒资数据-底量-内容提供商.xlsx", "apiqdi": "querycatchildallmedia"},
        }
    Allqdi={
        "底量":{
            "单剧集":{"apiqdi":"querycontentbasesingle"},
            "连续剧": {"apiqdi": "querycontentbaseteleplay"},
            "提供商": {"apiqdi": "querycontentbasevsp"},
                },
        "增加量": {
            "单剧集": {"apiqdi": "querycontentaddsingle"},
            "连续剧": {"apiqdi": "querycontentaddteleplay"},
            "提供商": {"apiqdi": "querycontentaddvsp"},
                    },
        "删除量": {
            "单剧集": {"apiqdi": "querycontentdelsingle"},
            "连续剧": {"apiqdi": "querycontentdelteleplay"},
            "提供商": {"apiqdi": "querycontentdelvsp"},
                    },

    }

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.f_search()
        self.look()

    @getparamnow
    def pararms2(self, **kwargs):
        """设置参数"""
        self.pararms(**kwargs)
        self.buttontext = kwargs.get("buttontext2", "单剧集")
        self.table_id = self.Pararm2[self.buttontext]["table_id"]
        self.dlfile = self.Pararm2[self.buttontext]["dlfile"]
        self.apiqdi = self.Allqdi[self.movetype][self.buttontext]["apiqdi"]
        self.text = self.buttontext

    def get_data_datil(self):
        self.data = \
            {
                "qdi": self.apiqdi,
                "starttime": getattr(self, "request_code", None),
                "endtime":  getattr(self, "request_code", None),
                "datetype": self.apidatatype,
                "token": self.token,
                "sysid": getattr(self, "secsiono", "u"),
                "userid": "test1",
            }
        log().debug("requests 'url, data' \t {1},{0}".format(self.data, self.url_api))

        self.data["starttime"] = self.request_code
        self.data["endtime"] = self.request_code
        self.api_result()


class   Vod内容标签(VodlBase):

    programtype="提供商"
    Qdi_home = {
        "提供商": {"apiqdi":"queryvsptopdetail"},
        "导演": {"apiqdi": "querydirectorhis"},
        "演员": {"apiqdi": "queryactorhis"},
        "年份": {"apiqdi": "queryyearhis"},
              }

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="内容标签"]/parent::*')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.program = kwargs.get("program", self.programtype)
        self.table_id = kwargs.get("table_id", "columnTable")
        self.dlfile = kwargs.get("dlfile", "点播-{0}标签.xlsx".format(self.program))
        self.apiqdi = self.Qdi_home[self.program]["apiqdi"]
        self.text = "查询"
        self.groupid ="realGroup"

    def get_home_code(self):
        """ 获取code 供请求详情页使用"""
        if self.program == "年份":
            code = [x["YEAR"] for x in self.datatext][0]
        elif self.program == "提供商":
            code = "1"
        elif self.program == "导演":
            code = [x["DIRECTOR"] for x in self.datatext][0]
        elif self.program == "演员":
            code = [x["ACTOR"] for x in self.datatext][0]
        self.request_code = code

    def request_data_home(self):
        """构造首页请求数据"""
        start_time = self.start_time
        end_time = self.end_time
        self.data = \
            {
                "qdi": self.apiqdi,
                "starttime": start_time,
                "endtime": end_time,
                "datetype": self.apidatatype,
                "token": self.token,
                "tagid": None,
                "sysid": getattr(self,"secsiono","u"),
                "userid": "test1",
                "year": getattr(self, "request_code", None),
                "actor":getattr(self, "request_code", None),
                "director":getattr(self, "request_code", None),
                "vspid": getattr(self, "request_code", "1"),
            }
        log().debug("requests 'url, data' \t {1},{0}".format(self.data, self.url_api))

    def f_search(self, **kwargs):
        """
        查询流程
        :param kwargs:
        :return
        """
        self.pararms(**kwargs)
        self.get_data_home()
        self._before()
        self.pararms(**kwargs)
        self.checktext(2, element=getattr(self, "text", ""))
        self.getsysereorlog("start")
        self.change_user()
        self.click_program()
        self.search_time_type()
        self.click_serach()
        self.move_detaildata()
        self.get_tablefirstdata()


class Vod内容标签详情(Vod内容标签):

    Pararm = \
        {
            "时段数据": {"table_id": "timeTable", "dlfile": "点播内容标签-提供商-日期数据详情.xlsx", "apiqdi": "queryvspdaydetail"},
            "节目收视": {"table_id": "programTable", "dlfile": "点播内容标签-提供商-节目收视.xlsx", "apiqdi": "queryvspdaymedia"},
            "区域分布": {"table_id": "areaTable", "dlfile": "点播内容标签-提供商-区域分布.xlsx", "apiqdi": "queryvspdayarea"},
        }

    Qdi_tail ={
        "提供商": {
            "时段数据": {"apiqdi":"queryvspdaydetail"},
            "节目收视": {"apiqdi": "queryvspdaymedia"},
            "区域分布": {"apiqdi": "queryvspdayarea"},
            },
        "导演": {
            "时段数据": {"apiqdi": "querydirectordayhis"},
            "节目收视": {"apiqdi": "querydirectordaymedia"},
            "区域分布": {"apiqdi": "querydirectordayarea"},
                 },
        "演员": {
            "时段数据": {"apiqdi": "queryactordayhis"},
            "节目收视": {"apiqdi": "queryactordaymedia"},
            "区域分布": {"apiqdi": "queryactordayarea"},
        },
        "年份": {
            "时段数据": {"apiqdi": "queryyeardayhis"},
            "节目收视": {"apiqdi": "queryyeardaymedia"},
            "区域分布": {"apiqdi": "queryyeardayarea"},
        },

    }

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.f_search()
        self.look()

    @getparamnow
    def pararms2(self, **kwargs):
        """设置参数"""
        self.pararms(**kwargs)
        self.buttontext = kwargs.get("buttontext", "时段数据")
        self.table_id = kwargs.get("table_id", self.Pararm[self.buttontext]["table_id"])
        self.dlfile = kwargs.get("dlfile", self.Pararm[self.buttontext]["dlfile"])
        self.dlfile = self.dlfile.replace("提供商", self.programtype)
        if self.dlfile == "点播内容标签-演员-节目收视.xlsx":
            self.dlfile = "点播内容标签-导演-节目收视.xlsx"
        self.apiqdi = self.Qdi_tail[self.program][self.buttontext]["apiqdi"]
        self.text = self.buttontext

class Vod实时数据频道总览(VodlBase, Base实时数据):

    Pararm = \
        {
            "点播在线用户": {"table_id": "vodOnlineUser", "tabletype": "count_user"},
            "曲线":         {"table_id": "people", "tabletype": "count_user"},
            "栏目TOP5":     {"table_id": "columnTopFiveBar", "tabletype": "order_top5"},
            "提供商TOP5":   {"table_id": "vspTopFiveBar", "tabletype": "order_top5"},
            "导演TOP5":     {"table_id": "directorTopFiveBar", "tabletype": "order_top5"},
            "演员TOP5":     {"table_id": "actorTopFiveBar", "tabletype": "order_top5"},
            "年份TOP5":     {"table_id": "yearTopFiveBar", "tabletype": "order_top5"},
        }


    def _first(self, **kwargs):
        super()._first()
        self.exement('//*[@id="menu"]//a/span[text()="点播分析"]/parent::*/parent::*/ul//span[text()="实时数据"]/parent::*')
        self.frame_change()
        time.sleep(5)

    @getparamnow
    def pararms(self, **kwargs):
        super().pararms(**kwargs)
        self.buttontext = kwargs.get("buttontext", "点播在线用户")
        self.table_id = kwargs.get("table_id", self.Pararm[self.buttontext]["table_id"])
        self.tabletype = self.Pararm[self.buttontext]["tabletype"]
        self.apiqdi = "queryuserarea"
        self.text = ""
        self.p="groupToggle"
        self.down_text = {"by": "id", "value": self.table_id}

    def f_search(self, **kwargs):
        """
        查询流程
        :param :
        :return
        """
        self.pararms(**kwargs)
        self._before()
        self.pararms(**kwargs)
        self.checktext(2, element=getattr(self, "text", ""))
        self.getsysereorlog("start")
        self.move_detaildata()
        self.get_data()


class Vod实时数据频道(VodlBase, Base实时数据):

    Channel = "栏目"
    Pararm = \
        {
            "栏目": {"table_id": "realChannelTable", "dlfile": "点播-栏目.xlsx", "apiqdi": "querycolumntopdetil"},
            "提供商": {"table_id": "realChannelTable", "dlfile": "点播-提供商.xlsx", "apiqdi": "queryrealvsptopdetil"},
            "导演": {"table_id": "realChannelTable", "dlfile": "点播-导演.xlsx", "apiqdi": "queryrealdirectortopdetil"},
            "演员": {"table_id": "realChannelTable", "dlfile": "点播-演员.xlsx", "apiqdi": "queryrealactortopdetil"},
            "年份": {"table_id": "realChannelTable", "dlfile": "点播-年份.xlsx", "apiqdi": "queryrealyeartopdetil"},
        }

    def _first(self, **kwargs):
        super()._first()
        self.exement('//*[@id="menu"]//a/span[text()="点播分析"]/parent::*/parent::*/ul//span[text()="实时数据"]/parent::*')
        self.frame_change()
        time.sleep(5)

    @getparamnow
    def pararms(self, **kwargs):
        super().pararms(**kwargs)
        self.channel = kwargs.get("buttontext", self.Channel)
        self.table_id = "columnTable"
        self.dlfile=self.Pararm[self.channel]["dlfile"]
        self.groupid = "realGroup"
        self.apiqdi = self.Pararm[self.channel]["apiqdi"]
        self.text = ""
        self.p = "groupToggle"
        self.down_text = {"by": "id", "value": self.table_id}

    def get_home_code(self):
        """ 获取code 供请求详情页使用"""
        if self.channel == "年份":
            code = [x["NAME"] for x in self.datatext][0]
        elif self.channel == "提供商":
            code = "1"
        elif self.channel == "导演":
            code = [x["DIRECTOR"] for x in self.datatext][0]
        elif self.channel == "演员":
            code = [x["ACTOR"] for x in self.datatext][0]
        elif self.channel == "栏目":
            code = [x["CATEGORYID"] for x in self.datatext][0]

        self.request_code = code


    def request_data_home(self):
        """构造首页请求数据"""
        self.data = \
            {
                "userid": "test1",
                "qdi": self.apiqdi,
                "token": self.token,
                "sysid": getattr(self, "secsiono", "u"),

                "categoryid": getattr(self, "request_code", None),
                "year": getattr(self, "request_code", None),
                "actor": getattr(self, "request_code", None),
                "director": getattr(self, "request_code", None),
                "vspid": getattr(self, "request_code", "1"),
            }
        log().debug("requests 'url, data' \t {1},{0}".format(self.data, self.url_api))



    def f_search(self, **kwargs):
        """
        查询流程
        :param :
        :return
        """
        self.pararms(**kwargs)
        self.get_data_home()
        self._before()
        self.pararms(**kwargs)
        self.checktext(2, element=getattr(self, "text", ""))
        self.getsysereorlog("start")
        self.click_channel()
        time.sleep(15)
        self.move_detaildata()
        self.get_tablefirstdata()


class Vod实时数据频道详情(Vod实时数据频道):


    Pararm2 = \
        {
            "时段收视": {"table_id": "userOnlineTable", "dlfile": "栏目-子级栏目数据.xlsx"},
            "节目收视": {"table_id": "programTable", "dlfile": "栏目-节目收视数据.xlsx"},
            "区域收视": {"table_id": "areaTable", "dlfile": "栏目-区域收视数据.xlsx"},
            "二级栏目": {"table_id": "twoColumnTable", "dlfile": "栏目-子级栏目数据.xlsx"},
        }

    Qdi_tail = {
        "栏目": {
            "时段收视": {"apiqdi": "querycatonlineoneday"},
            "二级栏目": {"apiqdi": "querycatchildtop"},
            "节目收视": {"apiqdi": "querycatmediatop"},
            "区域收视": {"apiqdi": "querycatareatop"},
        },
        "提供商": {
             "时段收视": {"apiqdi": "queryrealvsponeday"},
            "节目收视": {"apiqdi": "queryrealvspmediatop"},
            "区域收视": {"apiqdi": "queryrealvspareatop"},
        },
        "导演": {
            "时段收视": {"apiqdi": "queryrealdirectoroneday"},
            "节目收视": {"apiqdi": "queryrealdirectormediatop"},
            "区域收视": {"apiqdi": "queryrealdirectorareatop"},
        },
        "演员": {
            "时段收视": {"apiqdi": "queryrealactoroneday"},
            "节目收视": {"apiqdi": "queryrealactormediatop"},
            "区域收视": {"apiqdi": "queryrealactorareatop"},
        },
        "年份": {
            "时段收视": {"apiqdi": "queryrealyearonehour"},
            "节目收视": {"apiqdi": "queryrealyearmeidatop"},
            "区域收视": {"apiqdi": "queryrealyearareatop"},
        },

    }

    def _first(self, **kwargs):
        super()._first()
        self.f_search()
        self.look()

    @getparamnow
    def pararms2(self, **kwargs):
        super().pararms(**kwargs)
        self.buttontext = kwargs.get("buttontext0", "时段收视")
        self.table_id = self.Pararm2[self.buttontext]["table_id"]
        self.dlfile = self.Pararm2[self.buttontext]["dlfile"].replace("栏目",self.Channel)
        self.apiqdi = self.Qdi_tail[self.Channel][self.buttontext]["apiqdi"]
        self.text = self.buttontext
        self.p = ""
        self.down_text = {"by": "id", "value": self.table_id}




if __name__ == "__main__":
    p = Vod媒资数据详情()
    p.time_type = "week"
    p._begin()
    # p.f2_search(**{"buttontext0": "区域收视"})

