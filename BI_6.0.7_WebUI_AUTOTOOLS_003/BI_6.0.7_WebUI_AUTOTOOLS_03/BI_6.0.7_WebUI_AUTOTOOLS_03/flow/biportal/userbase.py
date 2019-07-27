r"""
用户分析

"""

import os
import re
import time
import random

import requests

from lib.funcslib import log, getparamnow, get_token, Ioput
from lib.listen import ListenServerLog

__author__ = "luxu"

# from selenium.webdriver.support.select import Select

from flow.biportal.base import Base, Base实时数据

class UserBase( Base ):

    def _first(self,**kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="用户分析"]/..')
        # self.exement('//*[@id="menu"]//a/span[text()="实时数据"]/..')
        time.sleep(1)

    def get_home_code(self):
        """ 获取code 供请求详情页使用"""

        code=re.compile(r"\d{4}-\d{1,2}-\d{1,2}").findall(str(self.datatext))[0]

        self.request_code = code.replace("-", "")



    def f_search(self,**kwargs):
        """
        查询流程
        :param kwargs:
        :return
        """
        self.pararms(**kwargs)
        self.get_data_home()
        self._before()
        self.pararms(**kwargs)
        self.get_data_home()
        self.checktext(2, element=getattr(self, "text", ""))
        self.getsysereorlog("start")
        self.change_user(pull_spanid="select2-userGroupSelect-container", pull_ulid="select2-userGroupSelect-results")
        self.search_time_type()
        self.click_serach()
        self.move_detaildata()
        self.get_tablefirstdata()



    def f_outxlsx(self,**kwargs):
        """校验下载的XLSX数据"""
        self.f_search(**kwargs)
        self.outxlsx()
        self.getxlsxcontent()
        self.get_tablehead()

    def f2_search(self, **kwargs):
        """查看的流程"""
        self.pararms2(**kwargs)
        self.get_data_datil()
        self._before(**kwargs)
        self.pararms2(**kwargs)
        self.checktext(2, element=getattr(self, "text", ""))
        self.getsysereorlog("start")
        self.change_time(pull_spanid="select2-changetime-container", pull_ulid="select2-changetime-results")
        self.click_type()
        self.move_detaildata()
        self.get_tablefirstdata()

    def f2_outxlsx(self, **kwargs):
        """查看的导出数据流程"""
        self.f2_search(**kwargs)
        self.outxlsx()
        self.getxlsxcontent()
        self.get_tablehead()


class User机顶盒收视( UserBase ):

    def _first(self,**kwargs):
        super()._first(**kwargs)
        self.apiqdi = kwargs.get( "apiqdi", "querystbtype" )
        self.getsysereorlog("start")
        self.exement('//*[@id="menu"]//span[text()="机顶盒收视"]/..')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get( "table_id", "boxViewTable")
        self.dlfile = kwargs.get( "dlfile", "机顶盒收视数据.xlsx")
        self.apiqdi = kwargs.get( "apiqdi", "querystbtype")
        self.text=""

    def f_search(self, **kwargs):
        """
        查询流程
        :param kwargs:
        :return
        """
        self.pararms(**kwargs)
        self.move_detaildata()
        self.checktext(2, element=getattr(self, "text", ""))
        self.get_tablefirstdata()


class User用户发展(UserBase):

    def _first(self, **kwargs):
        """进入用户发展页面"""
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//span[text()="用户发展"]/..')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get( "table_id", "userDevelopTable")
        self.dlfile = kwargs.get( "dlfile", "用户发展数据.xlsx")
        self.apiqdi = kwargs.get( "apiqdi", "queryOffLineUserDevelop")
        self.text = "查询"


class User用户发展详情(User用户发展):
    Pararm =\
        {
            "区域分布": {"table_id":"areaDistributionTable","dlfile":"用户发展区域分布.xlsx","apiqdi":"queryOffLineUserDevelopDtlA"},
            "用户类型": {"table_id":"typeTable","dlfile":"用户发展类型分布.xlsx","apiqdi":"queryOffLineUserDevelopDtlT"}
        }

    def _first(self,**kwargs):
        """进入用户发展页面"""
        super()._first(**kwargs)
        self.f_search()
        self.look()

    @getparamnow
    def pararms2(self, **kwargs):
        """查看用户发展详情参数设置"""
        self.pararms(**kwargs)
        self.buttontext = kwargs.get("buttontext", "区域分布")
        self.table_id = kwargs.get("table_id", self.Pararm[self.buttontext]["table_id"])
        self.dlfile = kwargs.get("dlfile",self.Pararm[self.buttontext]["dlfile"])
        self.apiqdi = kwargs.get( "apiqdi", self.Pararm[self.buttontext]["apiqdi"])
        self.text = self.buttontext
        self.time_index = kwargs.get("time_index", "1")



class User用户发展C3(User用户发展):
    pass
    def _first(self):
        """进入用户发展页面"""
        UserBase._first(self)
        self.exement('//*[@id="menu"]//span[text()="用户发展C3"]/..')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "userDevelopTable")
        self.dlfile = kwargs.get("dlfile", "用户发展数据.xlsx")
        self.apiqdi = kwargs.get("apiqdi", "queryc3OffLineUserDevelop")
        self.text = "查询"


class User用户发展详情C3(User用户发展C3, User用户发展详情):
    Pararm = \
        {
            "区域分布": {"table_id": "areaDistributionTable", "dlfile": "用户发展区域分布.xlsx",
                     "apiqdi": "queryc3OffLineUserDevelopDtlA"},
            "用户类型": {"table_id": "typeTable", "dlfile": "用户发展类型分布.xlsx", "apiqdi": "queryc3OffLineUserDevelopDtlT"}
        }

    def _first(self):
        """进入用户发展页面"""
        super()._first()
        self.f_search()
        self.look()


class User收视概况(UserBase, Base实时数据):

    time_type = "week"
    Buttontext = "详情数据表"
    Pararm = \
        {
            "收视时长分布": {"table_id": "secondsinfo", "tabletype": "order_count"},
            "收视次数分布": {"table_id": "countInfo", "tabletype": "order_count"},
            "详情数据表": {"table_id": "surveyTable", "dlfile": "订购总览.xlsx", "apiqdi": "queryviewstatisticsdetail",
                     "tabletype": "get_tablefirstdata"},
        }

    def _first(self, **kwargs):
        """进入用户发展页面"""
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//span[text()="收视概况"]/..')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.buttontext = kwargs.get("buttontext", self.Buttontext)
        self.table_id = self.Pararm[self.buttontext]["table_id"]
        self.tabletype = self.Pararm[self.buttontext]["tabletype"]
        self.dlfile = kwargs.get("dlfile", "收视概况.xlsx")
        self.apiqdi = kwargs.get( "apiqdi", "queryOffLineUserDevelop")
        self.text = "查询"
        self.down_text = {"by": "id", "value": self.table_id}

    def f_search(self,**kwargs):
        self.pararms(**kwargs)
        self.get_data_home()
        self._before()
        self.pararms(**kwargs)
        self.checktext(2, element=getattr(self, "text", ""))
        self.getsysereorlog("start")
        self.search_time_type()
        self.click_serach()
        self.move_detaildata()
        self.get_data()


class User收视概况C3(User收视概况):

    alltime = 20
    Pararm = \
        {
            "收视时长分布": {"table_id": "secondsinfo", "tabletype": "order_count"},
            "收视次数分布": {"table_id": "countInfo", "tabletype": "order_count"},
            "详情数据表": {"table_id": "surveyTable", "dlfile": "订购总览.xlsx", "apiqdi": "queryc3viewstatisticsdetail",
                      "tabletype": "get_tablefirstdata"},
        }

    def _first(self, **kwargs):
        """进入用户发展页面"""
        UserBase._first(self,**kwargs)
        self.exement('//*[@id="menu"]//span[text()="收视概况C3"]/..')
        self.frame_change()


class  User版本统计(UserBase):
    alltime = 15
    def _first(self, **kwargs):
        """进入用户发展页面"""
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//span[text()="版本统计"]/..')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        super().pararms(**kwargs)
        self.table_id ="apkInfoTable"
        self.dlfile = kwargs.get("dlfile", "APK版本统计.xlsx")
        self.apiqdi = kwargs.get("apiqdi", "queryternimaltypeall")
        self.text = "查询"
        self.down_text = {"by": "id", "value": self.table_id}

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
                "monthday": getattr(self, "request_code", None),
                "sysid": getattr(self,"secsiono","u"),
                "userid": "test1",
                "terminaltype":getattr(self, "request_code2", None),
            }
        log().debug("requests 'url, data' \t {1},{0}".format(self.data, self.url_api))


    def get_home_code(self):
        """ 获取code 供请求详情页使用"""
        code = [x["MONTHDAY"] for x in self.datatext][0]
        self.request_code = code.replace("-","")
        self.request_code2 = [x["TERMINALTYPE"] for x in self.datatext][0]


class User版本统计详情(User版本统计):
    Pararm =\
        {
            "详情页": {"table_id":"apkInfoTable","dlfile":"APK版本统计-详情.xlsx","apiqdi":"queryternimaltypedetail"},
        }

    def _first(self,**kwargs):
        """进入用户发展页面"""
        super()._first(**kwargs)
        self.f_search()
        self.look()

    @getparamnow
    def pararms2(self, **kwargs):
        """查看用户发展详情参数设置"""
        self.pararms(**kwargs)
        self.buttontext = kwargs.get("buttontext", "详情页")
        self.table_id = kwargs.get("table_id", self.Pararm[self.buttontext]["table_id"])
        self.dlfile = kwargs.get("dlfile",self.Pararm[self.buttontext]["dlfile"])
        self.apiqdi = kwargs.get( "apiqdi", self.Pararm[self.buttontext]["apiqdi"])
        self.text = ""
        self.down_text = {"by": "id", "value": self.table_id}

    def f2_search(self, **kwargs):
        """查看的流程"""
        self.pararms2(**kwargs)
        self.get_data_datil()
        self._before(**kwargs)
        self.pararms2(**kwargs)
        self.checktext(2, element=getattr(self, "text", ""))
        self.getsysereorlog("start")
        self.screenhost_to_report(alt="版本统计详情" + "header", name="版本统计详情" + "header")
        self.get_tablefirstdata()



class User用户统计(UserBase):

    Usertype = "全网用户数据"

    Pararm = \
        {
            "全网用户数据": {"table_id": "allUserTable", "dlfile": "用户统计统计.xlsx","apiqdi": "queryAllUserStatistics"},
            "UIOS用户数据": {"table_id": "UIOSUserTable", "dlfile": "UIOS用户统计统计.xlsx", "apiqdi": "queryUiosUserStatistics"},
            "C3用户数据": {"table_id": "BSUserTable", "dlfile": "C3用户统计统计.xlsx", "apiqdi": "queryBsUserStatistics"}
        }

    def _first(self, **kwargs):
        """进入用户统计页面"""
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//span[text()="用户统计"]/..')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """查看用户统计参数设置"""
        super().pararms(**kwargs)
        self.buttontext = kwargs.get("buttontext", self.Usertype)
        self.table_id = self.Pararm[self.buttontext]["table_id"]
        self.dlfile = self.Pararm[self.buttontext]["dlfile"]
        self.apiqdi = self.Pararm[self.buttontext]["apiqdi"]
        self.text = "查询"
        self.time_index = kwargs.get("time_index", "1")
        self.down_text = {"by": "id", "value": self.table_id}

    def request_data_home(self):
        """构造首页请求数据"""
        start_time = self.start_time
        end_time = self.end_time
        self.data = \
            {
                "qdi": self.apiqdi,
                'begindate': start_time,
                "enddate": end_time,
                "datetype": self.apidatatype,
                "token": self.token,
                "sysid": getattr(self, "secsiono", "u"),
                "userid": "test1",
            }


        log().debug("requests 'url, data' \t {1},{0}".format(self.data, self.url_api))

class User用户统计详情(User用户统计):


    Pararm2 = \
        {
            "区域分布": {"table_id": "areaDistributionTable", "dlfile": "用户发展区域分布.xlsx","apiqdi": "DtlA"},
            "用户类型": {"table_id": "typeTable", "dlfile": "用户发展类型分布.xlsx", "apiqdi": "DtlT"}
        }

    Pararm3={

    }

    def _first(self):
        """进入用户统计详情页面"""
        super()._first()
        self.f_search()
        self.look()

    @getparamnow
    def pararms2(self, **kwargs):
        """ 查看用户统计详情参数设置 """
        self.pararms(**kwargs)
        self.buttontext = kwargs.get("buttontextdetail", "区域分布")
        self.table_id = self.Pararm2[self.buttontext]["table_id"]
        self.dlfile =  self.Pararm2[self.buttontext]["dlfile"]
        self.apiqdi ="{0}{1}".format(self.Pararm[self.Usertype]["apiqdi"],self.Pararm2[self.buttontext]["apiqdi"])
        self.text = self.buttontext
        self.time_index = kwargs.get("time_index", "1")
        self.down_text = {"by": "xpath", "value": '//span[text()="导出数据"]'}
        if "详情" in self.__class__.__name__:
            self.data["enddate"] =getattr(self, "request_code", None)
            self.data["begindate"] = getattr(self, "request_code", None)
            log().debug("requests 'url, data' \t {1},{0}".format(self.data, self.url_api))

class User收视(UserBase):


    def _first(self):

        """进入用户收视页面"""
        super()._first()
        self.exement('//*[@id="menu"]//span[text()="用户收视"]/..')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "userViewTable")
        self.dlfile = kwargs.get("dlfile", "用户收视数据.xlsx")
        self.apiqdi = kwargs.get("apiqdi", "queryOffLineUserView")
        self.text = "查询"



class User收视详情(User收视):

    Pararm = \
        {
            "时段数据": {"table_id": "timeTable", "dlfile": "用户收视时段分布.xlsx", "apiqdi": "queryOffLineUserViewDtlD"},
            "区域分布": {"table_id": "areaDistributionTable", "dlfile": "用户收视区域分布.xlsx", "apiqdi": "queryOffLineUserViewDtlA"},
            "用户类型": {"table_id": "typeTable", "dlfile": "用户收视类型分布.xlsx","apiqdi": "queryOffLineUserViewDtlT"}
        }

    def _first(self):
        """进入用户收视详情"""
        super()._first()
        self.f_search()
        self.look()

    @getparamnow
    def pararms2(self, **kwargs):
        """用户发展详情页参数设置"""
        self.pararms(**kwargs)
        self.buttontext = kwargs.get("buttontext", "时段数据")
        self.table_id = kwargs.get("table_id", self.Pararm[self.buttontext]["table_id"])
        self.dlfile = kwargs.get("dlfile",self.Pararm[self.buttontext]["dlfile"])
        self.apiqdi = kwargs.get("apiqdi", self.Pararm[self.buttontext]["apiqdi"])
        self.text = self.buttontext
        self.time_index = kwargs.get("time_index", "1")


class User收视C3(User收视):

    def _first(self):
        """进入用户发展页面"""
        UserBase._first(self)
        self.exement('//*[@id="menu"]//span[text()="用户收视C3"]/..')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "userViewTable")
        self.dlfile = kwargs.get("dlfile", "用户收视数据.xlsx")
        self.apiqdi = kwargs.get("apiqdi", "queryc3OffLineUserView")
        self.text = "查询"


class User收视详情C3(User收视C3,User收视详情):

    Pararm = \
        {
            "时段数据": {"table_id": "timeTable", "dlfile": "用户收视时段分布.xlsx", "apiqdi": "queryc3OffLineUserViewDtlD"},
            "区域分布": {"table_id": "areaDistributionTable", "dlfile": "用户收视区域分布.xlsx",
                     "apiqdi": "queryc3OffLineUserViewDtlA"},
            "用户类型": {"table_id": "typeTable", "dlfile": "用户收视类型分布.xlsx", "apiqdi": "queryc3OffLineUserViewDtlT"}
        }

    def _first(self):
        """进入用户发展页面"""
        super()._first()
        self.f_search()
        self.look()


class  User特殊统计C3(UserBase):

    Usertype = "频道厂商详情列表"

    Pararm = \
        {
            "频道厂商详情列表": {"table_id": "channelTable", "dlfile": "频道厂商详情列表.xlsx","apiqdi": "queryc3specialchannel"},
            "订购详情列表": {"table_id": "orderTable", "dlfile": "订购详情列表.xlsx", "apiqdi": "queryc3specialordersum"},
            "支付详情列表": {"table_id": "payTable", "dlfile": "支付详情列表.xlsx", "apiqdi": "queryc3specialpaydetail"},
            "活跃用户详情列表": {"table_id": "boothalfyearTable", "dlfile": "活跃用户列表.xlsx", "apiqdi": "queryc3specialboothalfyear"},
            "用户统计列表": {"table_id": "userStatisticsTable", "dlfile": "用户统计列表.xlsx",
                         "apiqdi": "queryc3specialbootweek"},

        }

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
                "userid": "test1",
                "sysid": getattr(self, "secsiono", "u"),
            }
        log().debug("requests 'url, data' \t {1},{0}".format(self.data, self.url_api))

    def _first(self, **kwargs):
        """进入特殊统计C3页面"""
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//span[text()="特殊统计C3"]/..')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """查看用户统计参数设置"""
        super().pararms(**kwargs)
        self.buttontext = kwargs.get("buttontext", self.Usertype)
        self.table_id = self.Pararm[self.buttontext]["table_id"]
        self.dlfile = self.Pararm[self.buttontext]["dlfile"]
        self.apiqdi = self.Pararm[self.buttontext]["apiqdi"]
        self.text = "查询"
        self.time_index = kwargs.get("time_index", "1")
        self.down_text = {"by": "id", "value": self.table_id}


class User用户活跃(UserBase):


    def _first(self):
        """进入用户发展页面"""
        super()._first()
        self.exement('//*[@id="menu"]//span[text()="用户活跃"]/..')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "userActiveTable")
        self.dlfile = kwargs.get("dlfile", "用户活跃数据.xlsx")
        self.apiqdi = kwargs.get("apiqdi", "queryOffLineUserActivity")
        self.text = "查询"

    def request_data_home(self):
        """构造首页请求数据"""
        start_time = self.start_time
        end_time = self.end_time
        self.data = \
            {
                "qdi": self.apiqdi,
                'begindate': start_time,
                "enddate": end_time,
                "datetype": self.apidatatype,
                "token": self.token,
                "selectdate": getattr(self, "request_code", None),
                "sysid": getattr(self,"secsiono","u"),
                "userid": "test1",
            }
        if getattr(self, "buttontext", None) == "区域分布" and  ("C3" not in self.__class__.__name__ ):
            self.data.pop("selectdate")

        log().debug("requests 'url, data' \t {1},{0}".format(self.data, self.url_api))


class User用户活跃详情(User用户活跃):
    Pararm = \
        {"时段数据":{"table_id":"timeTable","dlfile":"用户活跃时段分布.xlsx","apiqdi":"queryOffLineUserActivityDtlD"},
         "区域分布": {"table_id":"areaDistributionTable","dlfile":"用户活跃区域分布.xlsx","apiqdi":"queryOffLineUserActivityDtlA"},
         "用户类型":{"table_id":"typeTable","dlfile":"用户活跃类型分布.xlsx","apiqdi":"queryOffLineUserActivityDtlT"}
         }

    def _first(self):
        """进入用户发展页面"""
        super()._first()
        self.f_search()
        self.look()

    @getparamnow
    def pararms2(self, **kwargs):
        """查看用户发展详情参数设置"""
        self.pararms(**kwargs)
        self.buttontext = kwargs.get("buttontext", "时段数据")
        self.table_id = kwargs.get("table_id", self.Pararm[self.buttontext]["table_id"])
        self.dlfile = kwargs.get("dlfile",self.Pararm[self.buttontext]["dlfile"])
        self.apiqdi = kwargs.get("apiqdi", self.Pararm[self.buttontext]["apiqdi"])
        self.text = self.buttontext
        self.time_index = kwargs.get("time_index", "1")


class User用户活跃C3(User用户活跃):

    def _first(self, **kwargs):
        """进入用户活跃页面"""
        UserBase._first(self,**kwargs)
        self.exement('//*[@id="menu"]//span[text()="用户活跃C3"]')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "userActiveTable")
        self.dlfile = kwargs.get("dlfile", "用户活跃数据.xlsx")
        self.apiqdi = kwargs.get("apiqdi", "queryc3OffLineUserActivity")
        self.text = "查询"


class User用户活跃详情C3(User用户活跃C3, User用户活跃详情):
    """"""
    Pararm = \
        {"时段数据": {"table_id": "timeTable", "dlfile": "用户活跃时段分布.xlsx", "apiqdi": "queryc3OffLineUserActivityDtlD"},
         "区域分布": {"table_id": "areaDistributionTable", "dlfile": "用户活跃区域分布.xlsx",
                  "apiqdi": "queryc3OffLineUserActivityDtlA"},
         "用户类型": {"table_id": "typeTable", "dlfile": "用户活跃类型分布.xlsx", "apiqdi": "queryc3OffLineUserActivityDtlT"}
         }

    def _first(self):
        """进入用户活跃页面"""
        super()._first()
        self.f_search()
        self.look()


class User实时数据(UserBase,Base实时数据):

    Pararm=\
        {
            "全网用户": {"table_id": "allUserCount", "tabletype": "count_user"},
            "当前在线用户": {"table_id": "onLineUserCount", "tabletype": "count_user",},
            "开机率": {"table_id": "peruserCount", "tabletype": "count_user"},
            "24小时内最高在线用户数": {"table_id": "todayHighestCount", "tabletype": "count_user"},
            "在线用户使用功能": {"table_id": "userOnLineUseInfo", "tabletype": "order_count","apiqdi":"queryRealTimeUserActionType"},
            "在线用户类型分布": {"table_id": "userOnLineTypeInfo", "tabletype": "order_count","apiqdi":"queryuserstatus"},
        }

    def _first(self, **kwargs):
        super()._first()
        self.exement('//*[@id="menu"]//a/span[text()="实时数据"]/..')
        self.frame_change()
        time.sleep(3)

    @getparamnow
    def pararms(self, **kwargs):
        super().pararms(**kwargs)
        self.buttontext = kwargs.get("buttontext", "全网用户")
        self.table_id = kwargs.get("table_id", self.Pararm[self.buttontext]["table_id"])
        self.tabletype = self.Pararm[self.buttontext]["tabletype"]
        self.apiqdi = "queryRealTimeUserActionType"
        self.text = ""
        self.down_text = {"by": "id", "value": self.table_id}


    def f_search(self, **kwargs):
        """
        查询流程
        :param :
        :return
        """
        self.pararms( **kwargs )
        self._before()
        self.pararms(**kwargs)
        self.checktext(2, element=getattr(self, "text", ""))
        self.getsysereorlog("start")
        self.move_detaildata()
        self.get_data()

if __name__ == "__main__":
    p = User用户统计详情()
    p.Usertype="全网用户数据"
    p._begin()
    p.f2_search(**{"buttontextdetail": "区域分布", "casename": "区域分布"})
    p.check_web_api()

