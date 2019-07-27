"""运营分析"""

import time
from flow.biportal.base import Base, ReqData
from lib.funcslib import getparamnow


class BusinessBase(ReqData,Base):


    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="运营分析"]/parent::*')
        time.sleep(1)


    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)

    def get_home_code(self):
        """skip"""

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

class Business节目订购(BusinessBase):

    data_list = {"home":
                    """
                        qdi: queryordercarouselschedule
                        starttime: 20190215
                        endtime: 20190429
                        datetype: D
                        channelcode: 
                        token: ac4bc5b527a47a2f6c640d99065daee1
                        sysid: u
                        userid: test1
                    """
                 }

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="节目订购"]/parent::*')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "pandectTable")
        self.apiqdi = kwargs.get("apiqdi", "queryordersinglepoint")
        self.data_str=self.data_list["home"]
        self.dlfile = "栏目分析.xlsx"
        self.text = "查询"

class Business订购时段分析C3(BusinessBase):

    data_list={"home":
                   """
                        qdi: queryc3ordercarouselhours
                        starttime: 20190215
                        endtime: 20190429
                        datetype: D
                        iptvproductcode: 
                        price: 
                        channelcode: 
                        token: ac4bc5b527a47a2f6c640d99065daee1
                        sysid: u
                        userid: test1
                   """
               }

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="订购时段分析C3"]/parent::*')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "pandectTable")
        self.apiqdi = kwargs.get("apiqdi", "queryordersinglepoint")
        self.data_str = self.data_list["home"]
        self.dlfile = "栏目分析.xlsx"
        self.text = "查询"

    def get_home_code(self):
        """ 获取code 供请求详情页使用"""
        code = [x["HOUR"] for x in self.datatext][0]
        self.request_code = code.replace("-", "")

class Business订购时段分析详情C3(Business订购时段分析C3):

    data_list = {"home":
                """
                    qdi: queryc3ordercarouselhours
                    starttime: 20190215
                    endtime: 20190429
                    iptvproductcode: 
                    price: 
                    channelcode: 
                    hour: 00:00-00:59
                    datetype: D
                    token: ac4bc5b527a47a2f6c640d99065daee1
                    sysid: u
                    userid: test1
                """
                 }

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.f_search()
        self.look()

    @getparamnow
    def pararms2(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "rateTable")
        self.apiqdi = kwargs.get("apiqdi", "queryordersinglepoint")
        self.dlfile = "直播频道-节目收视.xlsx"
        self.data_str = self.data_list["home"]
        self.text = ""
        self.up_text = {"by":"id", "value": "userType"}

    def f2_search(self, **kwargs):
        """查看的流程"""
        self.pararms2(**kwargs)
        self.get_data_datil()
        self._before(**kwargs)
        self.pararms2(**kwargs)
        self.checktext(2, element=getattr(self, "text", ""))
        self.getsysereorlog("start")
        self.change_time(pull_spanid="select2-changetime-container", pull_ulid="select2-changetime-results")
        # self.click_type()
        self.move_detaildata()
        self.get_tablefirstdata()


class Business运营概况(BusinessBase):

    data_list={"home":
                   """
                        qdi: queryoperationthreepage
                        starttime: 20190201
                        endtime: 20190401
                        datetype: M
                        token: ac4bc5b527a47a2f6c640d99065daee1
                        sysid: u
                        userid: test1
                   """
               }

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="运营概况"]/parent::*')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "operateTable")
        self.apiqdi = kwargs.get("apiqdi", "queryordersinglepoint")
        self.dlfile = "运营概况.xlsx"
        self.data_str=self.data_list["home"]
        self.text = "查询"

if __name__ == "__main__":
    from config.conf import BI_protal as bi
    obj=Business运营概况()
    obj._begin()
    obj.f_outxlsx(**{"starttime": bi.weekstarttime, "endtime":bi.weekendtime , "timetype": "week", "casename": "周报"})