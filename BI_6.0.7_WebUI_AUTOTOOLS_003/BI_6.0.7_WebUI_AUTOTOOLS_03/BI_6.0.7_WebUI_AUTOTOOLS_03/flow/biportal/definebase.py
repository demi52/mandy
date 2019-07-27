"""自定义报告"""
import time
from flow.biportal.base import Base, ReqData
from lib.funcslib import getparamnow


class DefineReportBase(Base):


    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="自定义报告"]/parent::*')
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
        self.checktext(2, element=getattr(self, "text", ""))
        self.getsysereorlog("start")
        self.change_user()
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


class Define指标定义(ReqData,DefineReportBase):

    data_list = {
            "home":
                   """
                    qdi: queryCustomAllDESCRIBE
                    city: beijing
                    token: ac4bc5b527a47a2f6c640d99065daee1
                    sysid: u
                    userid: test1
                    """
            }

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="指标定义"]/parent::*')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "realTable")
        self.apiqdi = kwargs.get("apiqdi", "queryordersinglepoint")
        self.data_str = self.data_list["home"]
        self.dlfile = "指标定义.xlsx"
        self.text = ""


if __name__ == "__main__":
    obj=Define指标定义()
    obj._begin()
    obj.f_search()
    obj.check_web_api()
    # obj.f_outxlsx()