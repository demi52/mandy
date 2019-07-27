"""
结算信息流程

"""
import re
import time

from flow.biportal.base import Base
from lib.funcslib import getparamnow, log


class CountDataBase( Base ):
    alltime = 20

    def _first(self,**kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="结算数据"]/..')
        time.sleep(1)


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
        self.checktext(2, element=getattr(self, "text", ""))
        self.getsysereorlog("start")
        self.change_user(pull_spanid="select2-userGroupSelect-container", pull_ulid="select2-userGroupSelect-results")
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

class CountData结算明细(CountDataBase):
    Pararm = \
        {
            "全量明细": {"table_id": "allDetailTable", "dlfile": "结算明细-全量明细.xlsx", "apiqdi": "queryaccountdetailall"},
            "更新量明细": {"table_id": "updateDetailTable", "dlfile": "结算明细-更新量明细.xlsx", "apiqdi": "queryaccountdetailadd"},
            "热榜明细": {"table_id": "hotDetailTable", "dlfile": "结算明细-热榜明细.xlsx", "apiqdi": "queryaccountdetailtop"},
            "订购指标": {"table_id": "orderDetailTable", "dlfile": "结算明细-订购指标.xlsx", "apiqdi": "queryaccountorder"},
        }

    data_list="""
            qdi: queryaccountorder
            starttime: 20190201
            endtime: 20190401
            datetype: M
            target: numbers
            token: ac4bc5b527a47a2f6c640d99065daee1
            sysid: t
            userid: test1
        """


    def _first(self, **kwargs):
        """进入用户发展页面"""
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//span[text()="结算明细"]/..')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.buttontext = kwargs.get("buttontext", "全量明细")
        self.table_id = kwargs.get("table_id", self.Pararm[self.buttontext]["table_id"])
        self.dlfile = kwargs.get("dlfile", self.Pararm[self.buttontext]["dlfile"])
        self.apiqdi = self.Pararm[self.buttontext]["apiqdi"]
        self.data_str = self.data_list
        self.text = "查询"
        self.down_text = {"by": "id", "value": self.table_id}

    def request_data_home(self):
        start_time = self.start_time
        end_time = self.end_time
        f = re.compile(r"(\w+):(.+)").findall(self.data_str)
        data = {x.strip(): y.strip() for x, y in f}

        data = self.dict_update(data, "qdi", self.apiqdi)
        data = self.dict_update(data, "token", self.token)
        data=self.dict_update(data, "starttime", start_time)
        data = self.dict_update(data, "endtime", end_time)
        data = self.dict_update(data, "sysid", getattr(self, "secsiono", "u"))
        data = self.dict_update(data, "userid", "test1")
        data = self.dict_update(data, "positioncode", getattr(self, "request_code", None))
        self.data=data
        log().debug("requests 'url, data' \t {1},{0}".format(self.data, self.url_api))

    def get_home_code(self):
        pass

if __name__ == "__main__":
    p=CountData结算明细()
    p._begin()
    p.f_search()