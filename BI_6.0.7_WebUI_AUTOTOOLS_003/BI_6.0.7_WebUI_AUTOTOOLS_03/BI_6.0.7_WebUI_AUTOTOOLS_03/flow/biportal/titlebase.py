"""专题分析"""
import re
import time

from flow.biportal.base import Base
from lib.funcslib import getparamnow, log


class TitleBase(Base):
    """专题分析步骤基本方法"""
    alltime = 15
    def _first(self, **kwargs):
        """专题分析前置环境"""
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="专题分析"]/..')
        time.sleep(2)

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
        self.change_user(pull_spanid="select2-userGroupSelect-container",
                         pull_ulid="select2-userGroupSelect-results")
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

    def request_data_home(self):
        start_time = self.start_time
        end_time = self.end_time
        f = re.compile(r"(\w+):(.+)").findall(self.data_str)
        data = {x.strip(): y.strip() for x, y in f}

        # data = self.dict_update(data, "qdi", self.apiqdi)
        data = self.dict_update(data, "token", self.token)
        data = self.dict_update(data, "starttime", start_time)
        data = self.dict_update(data, "endtime", end_time)
        data = self.dict_update(data, "datetype", self.apidatatype)
        data = self.dict_update(data, "sysid", getattr(self, "secsiono", "u"))
        data = self.dict_update(data, "userid", "test1")
        data = self.dict_update(data, "positioncode", getattr(self, "request_code", None))
        self.data=data
        log().debug("requests 'url, data' \t {1},{0}".format(self.data, self.url_api))

    def get_home_code(self):
        pass



class Title专题实时数据(TitleBase):

    data_list={
                    "home":
                        """
                            qdi: queryonlinespecial
                            token: ac4bc5b527a47a2f6c640d99065daee1
                            sysid: u
                            userid: test1
                        """
               }

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="专题实时数据"]/parent::*')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "realTopicTable")
        self.apiqdi = kwargs.get("apiqdi", "queryvodchannelgroupcount")
        self.dlfile = "专题实时数据.xlsx"
        self.data_str=self.data_list["home"]
        self.text = ""

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
        self.change_user(pull_spanid="select2-userGroupSelect-container",
                         pull_ulid="select2-userGroupSelect-results")
        self.get_tablefirstdata()

class Title专题分析(TitleBase):

    data_list = {
        "home":
            """
                qdi: querypastspecial
                starttime: 20190215
                endtime: 20190429
                datetype: D
                token: ac4bc5b527a47a2f6c640d99065daee1
                sysid: u
                userid: test1
            """
    }

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="专题分析"]/../../ul//span[text()="专题分析"]/..')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "topicAnalyzeTable")
        self.apiqdi = kwargs.get("apiqdi", "queryvodchannelgroupcount")
        self.data_str = self.data_list["home"]
        self.dlfile = "专题分析数据.xlsx"
        self.text = "查询"

class Title专区实时数据(TitleBase):

    data_list = {
        "home":
            """
                qdi: queryspecialarealist
                token: ac4bc5b527a47a2f6c640d99065daee1
                sysid: u
                userid: test1
            """
    }

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="专题分析"]/../../ul//span[text()="专区实时数据"]/..')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "realAreaTable")
        self.apiqdi = kwargs.get("apiqdi", "queryvodchannelgroupcount")
        self.data_str = self.data_list["home"]
        self.dlfile = "专区分析数据.xlsx"
        self.text = "查询"

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
        self.change_user(pull_spanid="select2-userGroupSelect-container",
                         pull_ulid="select2-userGroupSelect-results")
        self.click_serach()
        self.move_detaildata()
        self.get_tablefirstdata()


class  Title专区分析(TitleBase):

    data_list = {
        "home":
            """
                qdi: queryspecialareaall
                starttime: 20190426
                endtime: 20190429
                datetype: D
                token: ac4bc5b527a47a2f6c640d99065daee1
                sysid: u
                userid: test1
            """
    }

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="专题分析"]/../../ul//span[text()="专区分析"]/..')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "areaAnalyzeTable")
        self.apiqdi = kwargs.get("apiqdi", "queryvodchannelgroupcount")
        self.dlfile = "专区实时数据.xlsx"
        self.data_str = self.data_list["home"]
        self.text = "查询"

if __name__ == "__main__":
    objectuser=Title专区实时数据()
    objectuser._begin()
    objectuser.f_search()