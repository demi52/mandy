"""
EPG分析
"""
import re
import time

from flow.biportal.script登陆 import Land

__author__ = "luxu"
from lib.funcslib import log, getparamnow
from config.conf import BI_protal as bt, BI_protal

from flow.biportal.base import Base, Base实时数据


class EpgBase(Base):
    movetype = "点播"
    sec_text = "1"
    secsiono = {"1": "t", "2": "m", "3": "u"}[sec_text]

    def _first(self,**kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="EPG分析"]/parent::*')
        # self.exement('//*[@id="menu"]//a/span[text()="EPG分析"]/parent::*/parent::*/ul//span[text()="高清实时数据"]/parent::*')
        time.sleep(1)

    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)


    def f_search(self, **kwargs):
        """
        查询流程
        :param kwargs:
        :return
        """
        self.pararms( **kwargs )
        self._before()
        self.pararms(**kwargs)
        self.checktext(2, element=getattr(self, "text", ""))
        self.getsysereorlog("start")
        self.change_user()
        self.click_channel()
        self.search_time_type()
        self.click_serach()
        self.move_detaildata()
        time.sleep(3)
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
        self._before(**kwargs)
        self.pararms2(**kwargs)
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

    def request_data_home(self):
        start_time = self.start_time
        end_time = self.end_time
        f = re.compile(r"(\w+):(.+)").findall(self.data_str)
        data = {x.strip(): y.strip() for x, y in f}

        data = self.dict_update(data, "starttime", start_time)
        data = self.dict_update(data, "endtime", end_time)
        data = self.dict_update(data, "token", self.token)
        # data = self.dict_update(data, "qdi",self.apiqdi)
        data = self.dict_update(data, "datetype", self.apidatatype)
        data = self.dict_update(data, "sysid", getattr(self, "secsiono", "u"))
        data = self.dict_update(data, "userid","test1")
        data = self.dict_update(data, "positioncode", getattr(self, "request_code", None))
        self.data=data
        log().debug("requests 'url, data' \t {1},{0}".format(self.data, self.url_api))

    def get_home_code(self):
        """ 获取code 供请求详情页使用"""
        code = [x["REFPOSID"] for x in self.datatext][0]
        self.request_code = code.replace("-", "")

class Epg高清EPG(EpgBase):

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="高清EPG"]/parent::*')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "epgTable")
        self.apiqdi = kwargs.get("apiqdi", "queryvodchannelgroupcount")
        self.groupid = "realGroup"
        self.channel = kwargs.get("list_page", self.movetype)
        self.dlfile = "高清EPG数据.xlsx"
        self.text = "查询"

class Epg高清EPG详情(Epg高清EPG):

    Pararm = \
        {
            "时段收视": {"table_id": "timeTable", "dlfile": "高清EPG-时段收视-日期.xlsx", "apiqdi": "querylivechanneltimedetail"},
            "节目收视": {"table_id": "programTable", "dlfile": "高清EPG节目收视.xlsx", "apiqdi": "querylivechannelprogramdetail"},
            "区域分布": {"table_id": "areaTable", "dlfile": "高清EPG区域分布.xlsx", "apiqdi": "querylivechannelareadetail"},
            "类型分布": {"table_id": "typeTable", "dlfile": "高清EPG类型分布.xlsx", "apiqdi": "querylivechannelareadetail"},
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


class Epg智能EPG(EpgBase):

    data_dict={
            "点播":
                """
                    qdi: queryepgpath
                    groupcode: JingCaiTuiJian.java
                    groupname: 点播
                    epggroup: 2
                    starttime: 20190215
                    endtime: 20190315
                    datetype: D
                    token: ac4bc5b527a47a2f6c640d99065daee1
                    sysid: t
                    userid: test
                """,
            "精品":
                """
                    qdi: queryepgpath
                    groupcode: MangGuoZhuanQuReMenTuiJian.java
                    groupname: 精品
                    epggroup: 2
                    starttime: 20190215
                    endtime: 20190315
                    datetype: D
                    token: ac4bc5b527a47a2f6c640d99065daee1
                    sysid: t
                    userid: test1
                """,
            "专题":
                """
                    qdi: queryepgpath
                    groupcode: JingPinHuiCui.java
                    groupname: 专题
                    epggroup: 2
                    starttime: 20190215
                    endtime: 20190315
                    datetype: D
                    token: ac4bc5b527a47a2f6c640d99065daee1
                    sysid: t
                    userid: test1
                """,
            "首页":
                """
                    qdi: queryepgpath
                    groupcode: ShouYe.java
                    groupname: 首页
                    epggroup: 2
                    starttime: 20190215
                    endtime: 20190315
                    datetype: D
                    token: ac4bc5b527a47a2f6c640d99065daee1
                    sysid: t
                    userid: test
                """,
            "聚精彩":
                """
                    qdi: queryepgpath
                    groupcode: JuJingCai.java
                    groupname: 聚精彩
                    epggroup: 2
                    starttime: 20190215
                    endtime: 20190315
                    datetype: D
                    token: ac4bc5b527a47a2f6c640d99065daee1
                    sysid: t
                    userid: test1
            """,
            }

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="智能EPG"]/parent::*')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "epgTable")
        self.groupid = "realGroup"
        self.channel = kwargs.get("list_page", self.movetype)
        self.data_str=self.data_dict[self.channel]
        self.dlfile = "智能EPG数据.xlsx"
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
        self.pararms(**kwargs)
        self.checktext(2, element=getattr(self, "text", ""))
        self.getsysereorlog("start")
        self.change_user()
        self.click_channel()
        self.search_time_type()
        self.click_serach()
        self.move_detaildata()
        time.sleep(3)
        self.get_tablefirstdata()

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


class Epg智能EPG详情(Epg智能EPG):

    data_dict2 = {
        "点播":{
                "时段收视":
                    """
                        qdi: queryepghdday
                        starttime: 20190215
                        endtime: 20190315
                        datetype: D
                        positioncode: 13
                        groupcode: JingCaiTuiJian.java
                        token: ac4bc5b527a47a2f6c640d99065daee1
                        sysid: t
                        userid: test1
                    """,
                "节目收视":
                    """
                        qdi: queryepgmedia
                        starttime: 20190215
                        endtime: 20190315
                        datetype: D
                        positioncode: 13
                        groupcode: JingCaiTuiJian.java
                        epggroup: 1
                        token: ac4bc5b527a47a2f6c640d99065daee1
                        sysid: t
                        userid: test1
                    """,
                "区域分布":
                    """
                        qdi: queryepghdarea
                        starttime: 20190215
                        endtime: 20190315
                        datetype: D
                        positioncode: 13
                        groupcode: JingCaiTuiJian.java
                        token: ac4bc5b527a47a2f6c640d99065daee1
                        sysid: t
                        userid: test1
                    """,
                "类型分布":
                    """
                        qdi: queryepghdtype
                        starttime: 20190215
                        endtime: 20190315
                        datetype: D
                        positioncode: 13
                        groupcode: JingCaiTuiJian.java
                        token: ac4bc5b527a47a2f6c640d99065daee1
                        sysid: t
                        userid: test1
                    """,
                },
        "精品": {
            "时段收视":
                """
                    qdi: queryepghdday
                    starttime: 20190215
                    endtime: 20190315
                    datetype: D
                    positioncode: 7
                    groupcode: MangGuoZhuanQuReMenTuiJian.java
                    token: ac4bc5b527a47a2f6c640d99065daee1
                    sysid: t
                    userid: test1
                """,
            "节目收视":
                """
                    qdi: queryepgmedia
                    starttime: 20190215
                    endtime: 20190315
                    datetype: D
                    positioncode: 7
                    groupcode: MangGuoZhuanQuReMenTuiJian.java
                    epggroup: 1
                    token: ac4bc5b527a47a2f6c640d99065daee1
                    sysid: t
                    userid: test1
                """,
            "区域分布":
                """
                    qdi: queryepghdarea
                    starttime: 20190215
                    endtime: 20190315
                    datetype: D
                    positioncode: 7
                    groupcode: MangGuoZhuanQuReMenTuiJian.java
                    token: ac4bc5b527a47a2f6c640d99065daee1
                    sysid: t
                    userid: test1
                """,
            "类型分布":
                """
                    qdi: queryepghdtype
                    starttime: 20190215
                    endtime: 20190315
                    datetype: D
                    positioncode: 7
                    groupcode: MangGuoZhuanQuReMenTuiJian.java
                    token: ac4bc5b527a47a2f6c640d99065daee1
                    sysid: t
                    userid: test1
                """,
        },
         "专题": {
            "时段收视":
                """
                    qdi: queryepghdday
                    starttime: 20190215
                    endtime: 20190315
                    datetype: D
                    positioncode: 2
                    groupcode: JingPinHuiCui.java
                    token: ac4bc5b527a47a2f6c640d99065daee1
                    sysid: t
                    userid: test1
                """,
            "节目收视":
                """
                    qdi: queryepgmedia
                    starttime: 20190215
                    endtime: 20190315
                    datetype: D
                    positioncode: 2
                    groupcode: JingPinHuiCui.java
                    epggroup: 1
                    token: ac4bc5b527a47a2f6c640d99065daee1
                    sysid: t
                    userid: test1
                """,
            "区域分布":
                """
                    qdi: queryepghdarea
                    starttime: 20190215
                    endtime: 20190315
                    datetype: D
                    positioncode: 2
                    groupcode: JingPinHuiCui.java
                    token: ac4bc5b527a47a2f6c640d99065daee1
                    sysid: t
                    userid: test1
                """,
            "类型分布":
                """
                    qdi: queryepghdtype
                    starttime: 20190215
                    endtime: 20190315
                    datetype: D
                    positioncode: 2
                    groupcode: JingPinHuiCui.java
                    token: ac4bc5b527a47a2f6c640d99065daee1
                    sysid: t
                    userid: test1
                """,
        },
        "首页": {
            "时段收视":
                """
                    qdi: queryepghdday
                    starttime: 20190215
                    endtime: 20190315
                    datetype: D
                    positioncode: 0
                    groupcode: ShouYe.java
                    token: ac4bc5b527a47a2f6c640d99065daee1
                    sysid: t
                    userid: test1
                """,
            "节目收视":
                """
                    qdi: queryepgmedia
                    starttime: 20190215
                    endtime: 20190315
                    datetype: D
                    positioncode: 0
                    groupcode: ShouYe.java
                    epggroup: 1
                    token: ac4bc5b527a47a2f6c640d99065daee1
                    sysid: t
                    userid: test1
                """,
            "区域分布":
                """
                    qdi: queryepghdarea
                    starttime: 20190215
                    endtime: 20190315
                    datetype: D
                    positioncode: 0
                    groupcode: ShouYe.java
                    token: ac4bc5b527a47a2f6c640d99065daee1
                    sysid: t
                    userid: test1
                """,
            "类型分布":
                """
                    qdi: queryepghdtype
                    starttime: 20190215
                    endtime: 20190315
                    datetype: D
                    positioncode: 0
                    groupcode: ShouYe.java
                    token: ac4bc5b527a47a2f6c640d99065daee1
                    sysid: t
                    userid: test1
                """,
        },
        "聚精彩": {
            "时段收视":
                """
                    qdi: queryepghdday
                    starttime: 20190215
                    endtime: 20190315
                    datetype: D
                    positioncode: 4
                    groupcode: JuJingCai.java
                    token: ac4bc5b527a47a2f6c640d99065daee1
                    sysid: t
                    userid: test1
                """,
            "节目收视":
                """
                    qdi: queryepgmedia
                    starttime: 20190215
                    endtime: 20190315
                    datetype: D
                    positioncode: 4
                    groupcode: JuJingCai.java
                    epggroup: 1
                    token: ac4bc5b527a47a2f6c640d99065daee1
                    sysid: t
                    userid: test1
                """,
            "区域分布":
                """
                    qdi: queryepghdarea
                    starttime: 20190215
                    endtime: 20190315
                    datetype: D
                    positioncode: 4
                    groupcode: JuJingCai.java
                    token: ac4bc5b527a47a2f6c640d99065daee1
                    sysid: t
                    userid: test1
                """,
            "类型分布":
                """
                    qdi: queryepghdtype
                    starttime: 20190215
                    endtime: 20190315
                    datetype: D
                    positioncode: 4
                    groupcode: JuJingCai.java
                    token: ac4bc5b527a47a2f6c640d99065daee1
                    sysid: t
                    userid: test1
                """,
        },
                  }

    Pararm = \
        {
            "时段收视": {"table_id": "timeTable", "dlfile": "智能EPG-时段收视-日期.xlsx", "apiqdi": "querylivechanneltimedetail"},
            "节目收视": {"table_id": "programTable", "dlfile": "智能EPG节目收视.xlsx", "apiqdi": "querylivechannelprogramdetail"},
            "区域分布": {"table_id": "areaTable", "dlfile": "智能EPG区域分布.xlsx", "apiqdi": "querylivechannelareadetail"},
            "类型分布": {"table_id": "typeTable", "dlfile": "智能EPG类型分布.xlsx", "apiqdi": "querylivechannelareadetail"},
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
        self.data_str = self.data_dict2[self.channel][self.buttontext]
        self.text = self.buttontext


class Epg标清EPG(EpgBase):

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="标清EPG"]/parent::*')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "epgTable")
        self.apiqdi = kwargs.get("apiqdi", "queryvodchannelgroupcount")
        self.groupid = "realGroup"
        self.channel = kwargs.get("list_page", self.movetype)
        self.dlfile = "标清EPG数据.xlsx"
        self.text = "查询"

class Epg标清EPG详情(Epg标清EPG):

    Pararm = \
        {
            "时段收视": {"table_id": "timeTable", "dlfile": "智能EPG-时段收视-日期.xlsx", "apiqdi": "querylivechanneltimedetail"},
            "节目收视": {"table_id": "programTable", "dlfile": "智能EPG节目收视.xlsx", "apiqdi": "querylivechannelprogramdetail"},
            "区域分布": {"table_id": "areaTable", "dlfile": "智能EPG区域分布.xlsx", "apiqdi": "querylivechannelareadetail"},
            "类型分布": {"table_id": "typeTable", "dlfile": "高清EPG类型分布.xlsx", "apiqdi": "querylivechannelareadetail"},
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


class Epg高清实时数据(EpgBase):

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="高清实时数据"]/parent::*')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "realEpgTable")
        self.apiqdi = kwargs.get("apiqdi", "queryvodchannelgroupcount")
        self.groupid = "realGroup"
        self.channel = kwargs.get("list_page", self.movetype)
        self.dlfile = "高清实时数据.xlsx"
        self.text = ""
        self.up_text = {"by": "id", "value": 'realGroup'}

    def f_search(self, **kwargs):
        """
        查询流程
        :param kwargs:
        :return
        """
        self.pararms(**kwargs)
        self._before()
        self.pararms(**kwargs)
        self.checktext(2, element=getattr(self, "text", ""))
        self.getsysereorlog("start")
        self.change_user()
        self.click_channel()
        self.move_detaildata()
        time.sleep(5)
        self.get_tablefirstdata()


class Epg智能实时数据(EpgBase):

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="智能实时数据"]/parent::*')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "realEpgTable")
        self.apiqdi = kwargs.get("apiqdi", "queryvodchannelgroupcount")
        self.groupid = "realGroup"
        self.channel = kwargs.get("list_page", self.movetype)
        self.dlfile = "智能实时数据.xlsx"
        self.text = ""
        self.up_text = {"by": "id", "value": 'realGroup'}

    def f_search(self, **kwargs):
        """
        查询流程
        :param kwargs:
        :return
        """
        self.pararms(**kwargs)
        self._before()
        self.pararms(**kwargs)
        self.checktext(2, element=getattr(self, "text", ""))
        self.getsysereorlog("start")
        self.change_user()
        self.click_channel()
        self.move_detaildata()
        time.sleep(5)
        self.get_tablefirstdata()


class Epg标清实时数据(EpgBase):

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="标清实时数据"]/parent::*')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "realEpgTable")
        self.apiqdi = kwargs.get("apiqdi", "queryvodchannelgroupcount")
        self.groupid = "realGroup"
        self.channel = kwargs.get("list_page", self.movetype)
        self.dlfile = "标清实时数据.xlsx"
        self.text = ""
        self.up_text = {"by": "id", "value": 'realGroup'}

    def f_search(self, **kwargs):
        """
        查询流程
        param kwargs
        """
        self.pararms(**kwargs)
        self._before()
        self.pararms(**kwargs)
        self.checktext(2, element=getattr(self, "text", ""))
        self.getsysereorlog("start")
        self.change_user()
        self.click_channel()
        self.move_detaildata()
        time.sleep(5)
        self.get_tablefirstdata()

if __name__ == "__main__":
    p=Epg智能实时数据()
    p._begin()
    p.f_search()