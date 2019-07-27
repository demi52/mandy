"""
频道分析
"""
import random
import re
import time

__author__ = "luxu"

from lib.funcslib import log, getparamnow
from flow.biportal.base import Base, Base实时数据



class ChannelBase(Base):

    group_codes = None

    def _first(self,**kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="频道分析"]/parent::*')
        # self.exement('//*[@id="menu"]//a/span[text()="频道分析"]/parent::*/parent::*/ul//span[text()="实时数据"]/parent::*')
        time.sleep(1)

    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.groupid="directchannelGroup"
        self.channel="高清"


    def get_home_code(self):
        """ 获取code 供请求详情页使用"""
        # code = [x["CHANNELCODE"] for x in self.datatext][0]
        code=re.compile(r"\d{32}").findall(str(self.datatext))[0]
        self.request_code = code

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
        self.click_channel()
        self.click_serach()
        self.move_detaildata()
        classname=self.__class__.__name__
        if classname.count("直播频道") or classname.count("回看频道") or classname.count("时移频道"):
            time.sleep(1)
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

class ChannelBase2(ChannelBase):

    def request_data_home(self):
        """构造首页请求数据"""
        start_time = self.start_time
        end_time = self.end_time
        self.data = \
            {
                "offset": "0",
                "limit":"20",
                "searchname":None,
                "SCHEDULENAME":None,
                "qdi": self.apiqdi,
                "starttime": start_time,
                "endtime": end_time,
                "datetype": self.apidatatype,
                "token": self.token,
                "channelcode": None,
                "code":getattr(self, "request_code", None),
                "type":None,
                "sysid": getattr(self, "secsiono", "u"),
                "userid": "test1",
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
        self.search_time_type()
        self.click_serach()
        self.move_detaildata()
        self.get_tablefirstdata()

class Channel回看频道(ChannelBase):
    movetype = "高清频道"
    group_codes = None

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="回看频道"]/parent::*')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "lookBackChannelTable")
        self.groupid ="lookBackChannelGroup"
        self.apiqdi = kwargs.get("apiqdi", "queryvodchannelgroupcount")
        self.channel = kwargs.get("list_page", self.movetype)
        self.groupcode = kwargs.get("groupcode", self.group_codes)
        self.dlfile = "回看频道.xlsx"
        self.text = "查询"



class Channel回看频道详情(Channel回看频道):


    Pararm = \
        {
            "时段收视": {"table_id": "timeTable", "dlfile": "回看频道-时段收视-日期.xlsx", "apiqdi": "queryvodchanneltimedetail"},
            "节目收视": {"table_id": "rateTable", "dlfile": "回看频道-节目收视.xlsx", "apiqdi": "queryvodchannelprogramdetail"},
            "区域分布": {"table_id": "areaTable", "dlfile": "回看频道-区域分布.xlsx", "apiqdi": "queryvodchannelareadetail"},
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




class Channel回看频道C3(Channel回看频道):

    def _first(self, **kwargs):
        ChannelBase._first(self,**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="回看频道C3"]/parent::*')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "lookBackChannelTable")
        self.groupid = "lookBackChannelGroup"
        self.apiqdi = kwargs.get("apiqdi", "queryc3vodchannelgroupcount")
        self.channel = kwargs.get("list_page", self.movetype)
        self.dlfile = "回看频道-全网频道.xlsx"
        self.text = "查询"



class Channel回看频道详情C3(Channel回看频道C3, Channel回看频道详情):
    Pararm = \
        {
            "时段收视": {"table_id": "timeTable", "dlfile": "回看频道-时段收视-日期.xlsx", "apiqdi": "queryc3vodchanneltimedetail"},
            "节目收视": {"table_id": "rateTable", "dlfile": "回看频道-节目收视.xlsx", "apiqdi": "queryc3vodchannelprogramdetail"},
            "区域分布": {"table_id": "areaTable", "dlfile": "回看频道-区域分布.xlsx", "apiqdi": "queryc3vodchannelareadetail"},
        }

    def _first(self):
        """进入用户发展页面"""
        super()._first()
        self.f_search()
        self.look()


class Channel直播频道(ChannelBase):

    movetype = "高清频道"

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="直播频道"]/parent::*')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "directChannelTable")
        self.groupid = "directchannelGroup"
        self.apiqdi = kwargs.get("apiqdi", "querylivechannelgroupcount")
        self.groupcode = kwargs.get("groupcode", self.group_codes)
        self.channel = kwargs.get( "list_page", self.movetype)
        self.dlfile = "直播频道-{0}.xlsx".format(self.channel)
        self.text = "查询"


class Channel直播频道详情(Channel直播频道):

    Pararm = \
        {
            "时段对比": {"table_id": "timeTable", "dlfile": "直播频道-时段对比-24小时.xlsx", "apiqdi": "queryChannelHoursContrast"},
            "时段收视": {"table_id": "timeTable", "dlfile": "直播频道-时段收视-日期.xlsx", "apiqdi": "querylivechanneltimedetail"},
            "节目收视": {"table_id": "rateTable", "dlfile": "直播频道-节目收视.xlsx", "apiqdi": "querylivechannelprogramdetail"},
            "区域分布": {"table_id": "areaTable", "dlfile": "直播频道-区域分布.xlsx", "apiqdi": "querylivechannelareadetail"},
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




class Channel直播频道C3(Channel直播频道):

    def _first(self, **kwargs):
        ChannelBase._first(self, **kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="直播频道C3"]/parent::*')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "directChannelTable")
        self.groupid = "directchannelGroup"
        self.apiqdi = kwargs.get("apiqdi", "queryc3livechannelgroupcount")
        self.channel = kwargs.get("list_page", self.movetype)
        self.dlfile = "直播频道-全网频道.xlsx"
        self.text = "查询"



class Channel直播频道详情C3(Channel直播频道C3, Channel直播频道详情):

    Pararm = \
        {
            "时段对比": {"table_id": "timeTable", "dlfile": "直播频道-时段对比-24小时.xlsx", "apiqdi": "queryC3ChannelHoursContrast"},
            "时段收视": {"table_id": "timeTable", "dlfile": "直播频道-时段收视-日期.xlsx", "apiqdi": "queryc3livechanneltimedetail"},
            "节目收视": {"table_id": "rateTable", "dlfile": "直播频道-节目收视.xlsx", "apiqdi": "queryc3livechannelprogramdetail"},
            "区域分布": {"table_id": "areaTable", "dlfile": "直播频道-区域分布.xlsx", "apiqdi": "queryc3livechannelareadetail"},
        }

    def _first(self):
        super()._first()
        self.f_search()
        self.look()




class Channel直播节目(ChannelBase2):

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="直播节目"]/parent::*')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "directProgramTable")
        self.apiqdi = kwargs.get("apiqdi", "queryliveschedulecount")
        self.dlfile = "频道分析-直播节目.xlsx"
        self.text = "查询"




class Channel直播节目C3(Channel直播节目):

    def _first(self,**kwargs):
        ChannelBase._first(self,**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="直播节目C3"]/parent::*')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "directProgramTable")
        self.apiqdi = kwargs.get("apiqdi", "queryc3liveschedulecount")
        self.dlfile = "频道分析-直播节目C3.xlsx"
        self.text = "查询"


class Channel回看节目(ChannelBase2):

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="回看节目"]/parent::*')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "lookBackProgramTable")
        self.apiqdi = kwargs.get("apiqdi", "queryvodschedulecountpx_base")
        self.dlfile = "频道分析-回看节目.xlsx"
        self.text = "查询"




class Channel回看节目C3(Channel回看节目):

    def _first(self,**kwargs):
        ChannelBase._first(self,**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="回看节目C3"]/parent::*')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "lookBackProgramTable")
        self.apiqdi = kwargs.get("apiqdi", "queryc3vodschedulecount")
        self.dlfile = "频道分析-回看节目C3.xlsx"
        self.text = "查询"


class Channel实时数据频道总览(ChannelBase, Base实时数据):

    Pararm = \
        {
            "频道在线用户": {"table_id": "channelOnlineUser", "tabletype": "count_user"},
            "直播在线用户": {"table_id": "scheduleOnlineUser", "tabletype": "count_user"},
            "回看在线用户": {"table_id": "vodOnlineUser", "tabletype": "count_user"},
            "时移在线用户": {"table_id": "shiftOnlineUser", "tabletype": "count_user"},
            "频道实时在线人数曲线图": {"table_id": "people", "tabletype": "count_user"},
            "回看实时在线人数曲线图": {"table_id": "people2", "tabletype": "count_user"},
            "频道分组在线用户": {"table_id": "channelInfo", "tabletype": "order_count"},
            "频道收视类型分布": {"table_id": "channelViewInfo", "tabletype": "order_count"},
        }

    def _first(self, **kwargs):
        super()._first()
        self.exement('//*[@id="menu"]//a/span[text()="频道分析"]/parent::*/parent::*/ul//span[text()="实时数据"]/parent::*')
        self.frame_change()
        time.sleep(5)

    @getparamnow
    def pararms(self, **kwargs):
        super().pararms(**kwargs)
        self.buttontext = kwargs.get("buttontext", "频道在线用户")
        self.table_id = kwargs.get("table_id", self.Pararm[self.buttontext]["table_id"])
        self.tabletype = self.Pararm[self.buttontext]["tabletype"]
        self.apiqdi = "queryuserarea"
        self.text = ""
        self.p = "groupToggle"
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

    def request_data_home(self):
        """构造首页请求数据"""
        self.data = \
            {
                "qdi": self.apiqdi,
                "groupcode": getattr(self, "groupcode", None),
                "token": self.token,
                "channelcode":getattr(self, "request_code", None),
                "sysid": getattr(self,"secsiono","u"),
                "userid": "test1",
            }
        if  getattr(self, "movetype","") == "全网频道":
            self.data["groupcode"] = None
        log().debug("requests 'url, data' \t {1},{0}".format(self.data, self.url_api))

class Channel实时数据频道(ChannelBase, Base实时数据):

    Channel = "高清频道"


    def _first(self, **kwargs):
        super()._first()
        self.exement('//*[@id="menu"]//a/span[text()="频道分析"]/parent::*/parent::*/ul//span[text()="实时数据"]/parent::*')
        self.frame_change()
        time.sleep(5)

    @getparamnow
    def pararms(self, **kwargs):
        super().pararms(**kwargs)
        self.channel = kwargs.get("buttontext", self.Channel)
        self.table_id = "realChannelTable"
        self.dlfile="%s.xlsx" % self.channel
        self.groupid = "realGroup"
        self.apiqdi = "querychannelgrouptopn"
        self.groupcode = kwargs.get("groupcode", self.group_codes)
        self.text = ""
        self.p = "groupToggle"
        self.down_text = {"by": "id", "value": self.table_id}

    def get_home_code(self):
        """ 获取code 供请求详情页使用"""
        code = [x["CHANNELCODE"] for x in self.datatext][0]
        # code=re.compile(r"\d{32}").findall(str(self.datatext))[0]
        self.request_code = code

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


class Channel实时数据频道详情(Channel实时数据频道):

    Pararm2 = \
        {
            "时段收视": {"table_id": "timeTable","apiqdi":"querychanneldetail"}
        }

    def _first(self, **kwargs):
        super()._first()
        self.f_search()
        self.look()

    @getparamnow
    def pararms2(self, **kwargs):
        super().pararms(**kwargs)
        self.buttontext = kwargs.get("buttontext", "时段收视")
        self.table_id = self.Pararm2[self.buttontext]["table_id"]
        self.apiqdi = self.Pararm2[self.buttontext]["apiqdi"]
        self.text = ""
        self.p = ""
        self.down_text = {"by": "id", "value": self.table_id}


class Channel分钟收视(ChannelBase2):

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="分钟收视"]/parent::*')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "minuteTable")
        self.apiqdi = kwargs.get("apiqdi", "queryminutechannel")
        self.dlfile = "分钟收视.xlsx"
        self.text = "查询"

    def f_search(self, **kwargs):
        """
        查询流程
        :param kwargs:
        :return
        """
        self.pararms( **kwargs )
        self.get_data_home()
        self._before()
        self.checktext(2, element=getattr(self, "text", ""))
        self.getsysereorlog("start")
        self.change_user()
        self.search_time_type()
        self.click_serach()
        self.move_detaildata()
        self.get_tablefirstdata()


class Channel分钟收视详情(Channel分钟收视):


    Pararm = \
        {
            "时段收视": {"table_id": "timeTable", "dlfile": "分钟收视.xlsx", "apiqdi": "queryminutechannelall"},
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


class Channel分钟收视C3(Channel分钟收视):

    def _first(self,**kwargs):
        ChannelBase._first(self,**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="分钟收视C3"]/parent::*')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "minuteTable")
        self.apiqdi = kwargs.get("apiqdi", "queryc3minutechannel")
        self.dlfile = "分钟收视.xlsx"
        self.text = "查询"

class Channel分钟收视详情C3(Channel分钟收视C3, Channel分钟收视详情):

    Pararm = \
        {
            "时段收视": {"table_id": "timeTable", "dlfile": "分钟收视.xlsx", "apiqdi": "queryc3minutechannelall"},
        }

    def _first(self):
        """进入用户发展页面"""
        super()._first()
        self.f_search()
        self.look()


class Channel时移频道(ChannelBase):

    movetype = "全网频道"

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="时移频道"]/parent::*')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "timeshiftChannelTable")
        self.groupid = "timeshiftChannelGroup"
        self.apiqdi = kwargs.get("apiqdi", "queryschannelinfo")
        self.groupcode = kwargs.get("groupcode", self.group_codes)
        self.channel = kwargs.get("list_page", self.movetype)
        self.dlfile = "直播频道-{0}.xlsx".format(self.channel)
        self.text = "查询"



if __name__ == "__main__":
    p = Channel实时数据频道详情()
    # p.group_codes=None
    # p.movetype="全网频道"
    p._begin()
    # p.f_search()
    p.f2_search()
    # p.f2_search(**{"buttontext":"区域分布","casename":"区域分布"})
    # p.f2_search(**{"buttontext":"节目收视","casename":"节目收视"})
    # p.check_web_api()