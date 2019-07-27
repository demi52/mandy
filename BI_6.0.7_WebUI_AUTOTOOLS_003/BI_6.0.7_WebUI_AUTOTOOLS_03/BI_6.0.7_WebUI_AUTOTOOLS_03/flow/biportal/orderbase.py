"""
订购分析
"""
import os
import time

from lib.funcslib import log, exef, getparamnow
from config.conf import BI_protal as bt
__author__ = "luxu"
from flow.biportal.base import Base, Base实时数据


class OrderBase( Base ):

    def _first(self,**kwargs):
        super()._first(**kwargs)
        self.checktext(1, element="订购分析")
        self.exement('//*[@id="menu"]//a/span[text()="订购分析"]/..')
        # self.exement('//*[@id="menu"]//a/span[text()="订购总览"]/..')
        time.sleep(2)
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "userDevelopTable")
        self.dlfile = kwargs.get("dlfile", "用户发展数据.xlsx")
        self.apiqdi = kwargs.get("apiqdi", "queryOffLineUserDevelop")
        self.text = "实时数据"


    # def keyword_search(self):
    #     self.driver.find_element_by_xpath('//*[@class="table-search"]').send_keys("节目")

    @exef()
    def page_type(self):

        self.exement('//*[@id="_easyui_textbox_input1"]/parent::*/span/a') #点击下拉框
        self.exement('//*[@id="_easyui_tree_1"]/span[1]') #展开
        for n in range(0, 3):
            flag = self.driver.find_element_by_xpath( '//*[@id="_easyui_tree_1"]/span[3]' )
            if flag.get_attribute("class").endswith("1") or flag.get_attribute("class").endswith("2"):
                flag.click()                                  #去勾选
            elif n==3:
                break
            elif flag.get_attribute("class").endswith("0"):
                break

        for i in self.lists_page:
            for m in range(0,2):
                flag2 = self.driver.find_element_by_xpath('//span[text()="{0}"]/parent::*/span[4]'.format(i))
                if flag2.get_attribute( "class" ).endswith( "0" ):
                    flag2.click()
                elif m == 1:
                    break
                elif flag2.get_attribute( "class" ).endswith( "1" ):
                    break
        self.exement('//*[@id="_easyui_tree_1"]/span[1]')  #收起


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
                "qdi": self.apiqdi,
                "starttime": start_time,
                "endtime": end_time,
                "datetype": self.apidatatype,
                "type": "0','3','4','5','6",
                "token": self.token,
                "ordertype":"3",
                "code": getattr(self, "request_code", None),
                "sysid": getattr(self,"secsiono","u"),
                "userid": "test1",
            }
        log().debug("requests 'url, data' \t {1},{0}".format(self.data, self.url_api))

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
        self.getsysereorlog( "start" )
        self.change_user( pull_spanid="select2-userGroupSelect-container", pull_ulid="select2-userGroupSelect-results" )
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
        self.pararms2( **kwargs )
        self.get_data_datil()
        self._before(**kwargs)
        self.pararms2( **kwargs )
        self.checktext(2, element=getattr(self, "text", ""))
        self.getsysereorlog( "start" )
        self.change_time( pull_spanid="select2-changetime-container", pull_ulid="select2-changetime-results" )
        self.click_type()
        self.move_detaildata()
        self.get_tablefirstdata()

    def f2_outxlsx(self, **kwargs):
        """查看的导出数据流程"""
        self.f2_search(**kwargs)
        self.outxlsx()
        self.getxlsxcontent()
        self.get_tablehead()



class Order周期订购( OrderBase ):

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.checktext(2,element="周期订购")
        self.exement('//*[@id="menu"]//a/span[text()="周期订购"]/..')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "periodTable")
        self.dlfile = kwargs.get("dlfile", "周期订购.xlsx")
        self.apiqdi = kwargs.get("apiqdi", "queryordermonthpoint")
        self.text = "查询"
        self.lists_page = kwargs.get("list_page", ["包月", "包年", "包季度", "包半年"])



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
        self.page_type()
        self.click_serach()
        self.move_detaildata()
        self.get_tablefirstdata()


class Order周期订购详情(Order周期订购):

    Pararm=\
        {
        "时段订购": {"table_id": "timeTable", "dlfile": "周期订购日期数据详情.xlsx", "apiqdi": "queryordermonthpointday"},
        "区域分布": {"table_id": "areaDistributionTable", "dlfile": "周期订购区域分布数据.xlsx", "apiqdi": "queryordermonthpointarea"},
        "类型分布": {"table_id": "typeTable", "dlfile": "周期订购类型分布数据.xlsx", "apiqdi": "queryordermonthpointtype"},
        "支付方式": {"table_id": "paymentTable", "dlfile": "周期订购支付方式数据.xlsx", "apiqdi": "queryordermonthpaytype"},
        "价格分析": {"table_id": "priceAnalyzeTable", "dlfile": "周期订购价格分析数据.xlsx", "apiqdi": "queryordermonthprice"},
        }

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.f_search()
        self.look()

    @getparamnow
    def pararms2(self, **kwargs):
        """设置参数"""
        self.pararms(**kwargs)
        self.buttontext = kwargs.get("buttontext", "时段订购")
        self.table_id = kwargs.get("table_id", self.Pararm[self.buttontext]["table_id"])
        self.dlfile = kwargs.get("dlfile", self.Pararm[self.buttontext]["dlfile"])
        self.apiqdi = kwargs.get("apiqdi", self.Pararm[self.buttontext]["apiqdi"])
        self.text = self.buttontext


class Order周期订购C3(Order周期订购):

    def _first(self, **kwargs):
        OrderBase._first(self,**kwargs)
        self.checktext(1,element="周期订购C3")
        self.exement('//*[@id="menu"]//a/span[text()="订购分析"]/parent::*/parent::*/ul//span[text()="周期订购C3"]/parent::*')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "periodTable")
        self.dlfile = kwargs.get("dlfile", "周期订购.xlsx")
        self.apiqdi = kwargs.get("apiqdi", "queryc3ordermonthpoint")
        self.text = "查询"
        self.lists_page = kwargs.get("list_page", ["包月", "包年", "包季度", "包半年"])

class Order周期订购详情C3(Order周期订购C3, Order周期订购详情):
    Pararm = \
        {
            "时段订购": {"table_id": "timeTable", "dlfile": "周期订购日期数据详情.xlsx", "apiqdi": "queryc3ordermonthpointday"},
            "区域分布": {"table_id": "areaDistributionTable", "dlfile": "周期订购区域分布数据.xlsx",
                     "apiqdi": "queryc3ordermonthpointarea"},
            "类型分布": {"table_id": "typeTable", "dlfile": "周期订购类型分布数据.xlsx", "apiqdi": "queryc3ordermonthpointtype"},
            "支付方式": {"table_id": "paymentTable", "dlfile": "周期订购支付方式数据.xlsx", "apiqdi": "queryc3ordermonthpaytype"},
            "价格分析": {"table_id": "priceAnalyzeTable", "dlfile": "周期订购价格分析数据.xlsx", "apiqdi": "queryc3ordermonthprice"},
        }

    def _first(self):
        super()._first()
        self.f_search()
        self.look()

class Order按次订购( OrderBase ):

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="按次订购"]/..')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "dueTable")
        self.dlfile = kwargs.get("dlfile", "按次订购.xlsx")
        self.apiqdi = kwargs.get("apiqdi", "queryordersinglepoint")
        self.text = "查询"
        self.lists_page = kwargs.get("list_page", ["包月", "包年", "包季度", "包半年"] )


class Order按次订购详情(Order按次订购):

    Pararm=\
        {
        "时段订购": {"table_id": "timeTable", "dlfile": "按次订购日期数据详情.xlsx", "apiqdi": "queryordersinglepointday"},
        "区域分布": {"table_id": "areaDistributionTable", "dlfile": "按次订购区域分布数据.xlsx", "apiqdi": "queryordersinglepointarea"},
        "类型分布": {"table_id": "typeTable", "dlfile": "按次订购类型分布数据.xlsx", "apiqdi": "queryordersinglepointtype"},
        "单片订购": {"table_id": "monolithicTable", "dlfile": "按次订购单片订购数据.xlsx", "apiqdi": "queryordersinglepointdetail"},
        "支付方式": {"table_id": "paymentTable", "dlfile": "按次订购支付方式数据.xlsx", "apiqdi": "queryordersinglepaytype"},
        "价格分析": {"table_id": "priceAnalyzeTable", "dlfile": "按次订购价格分析数据.xlsx", "apiqdi": "queryordersingleprice"},
        }


    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.f_search()
        self.look()

    @getparamnow
    def pararms2(self, **kwargs):
        """设置参数"""
        self.pararms(**kwargs)
        self.buttontext = kwargs.get("buttontext", "时段订购")
        self.table_id = kwargs.get("table_id", self.Pararm[self.buttontext]["table_id"])
        self.dlfile = kwargs.get("dlfile", self.Pararm[self.buttontext]["dlfile"])
        self.apiqdi = kwargs.get("apiqdi", self.Pararm[self.buttontext]["apiqdi"])
        self.text = self.buttontext


class Order按次订购C3(Order按次订购):

    def _first(self, **kwargs):
        OrderBase._first(self,**kwargs)
        self.checktext(1,element="按次订购C3")
        self.exement('//*[@id="menu"]//a/span[text()="订购分析"]/parent::*/parent::*/ul//span[text()="按次订购C3"]/parent::*')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "dueTable")
        self.dlfile = kwargs.get("dlfile", "按次订购.xlsx")
        self.apiqdi = kwargs.get("apiqdi", "queryc3ordersinglepoint")
        self.text = "查询"
        self.lists_page = kwargs.get("list_page", ["包月", "包年", "包季度", "包半年"])

class Order按次订购详情C3(Order按次订购C3, Order按次订购详情):

    Pararm=\
        {
        "时段订购": {"table_id": "timeTable", "dlfile": "按次订购日期数据详情.xlsx", "apiqdi": "queryc3ordersinglepointday"},
        "区域分布": {"table_id": "areaDistributionTable", "dlfile": "按次订购区域分布数据.xlsx", "apiqdi": "queryc3ordersinglepointarea"},
        "类型分布": {"table_id": "typeTable", "dlfile": "按次订购类型分布数据.xlsx", "apiqdi": "queryc3ordersinglepointtype"},
        "单片订购": {"table_id": "monolithicTable", "dlfile": "按次订购单片订购数据.xlsx", "apiqdi": "queryc3ordersinglepointdetail"},
        "支付方式": {"table_id": "paymentTable", "dlfile": "按次订购支付方式数据.xlsx", "apiqdi": "queryc3ordersinglepaytype"},
        "价格分析": {"table_id": "priceAnalyzeTable", "dlfile": "按次订购价格分析数据.xlsx", "apiqdi": "queryc3ordersingleprice"},
        }

    def _first(self):
        super()._first()
        self.f_search()
        self.look()

class Order订购总览(Base实时数据,OrderBase):


    Pararm = \
        {
            "订购人数": {"table_id": "orderUserInfo", "tabletype": "order_count", "apiqdi":"queryordercards"},
            "订购次数": {"table_id": "orderCountInfo", "tabletype": "order_count", "apiqdi":"queryordercards"},
            "订购金额": {"table_id": "orderAmountInfo", "tabletype": "order_count", "apiqdi":"queryordercards"},
            "订购冠军": {"table_id": "orderChampionDiv", "tabletype": "order_mvp","apiqdi":"queryordertopn"},
            "详情数据": {"table_id": "orderSumTable", "dlfile": "订购总览.xlsx", "apiqdi": "queryordersum", "tabletype":"get_tablefirstdata"},
            "单片收入排行": {"table_id": "singleCard", "tabletype": "order_sort", "detail": "singleDetail","apiqdi":"queryordersingle"},
            "产品包收入排行": {"table_id": "productPackageCard", "tabletype": "order_sort", "detail": "productPackageDetail","apiqdi":"queryorderpackage"},
            "CP收入排行": {"table_id": "cpCard", "tabletype": "order_sort", "detail": "cpDetail","apiqdi":"queryordercp"},
            "区域收入排行": {"table_id": "areaCard", "tabletype": "order_sort", "detail": "areaDetail","apiqdi":"queryorderarea"},
        }
    Buttontext = "详情数据"

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="订购总览"]/..')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        super().pararms(**kwargs)
        self.buttontext = kwargs.get("buttontext", self.Buttontext)
        self.table_id = self.Pararm[self.buttontext]["table_id"]
        self.tabletype =self.Pararm[self.buttontext]["tabletype"]
        self.detail_id = self.Pararm[self.buttontext].get("detail")
        self.dlfile = kwargs.get("dlfile", "订购总览.xlsx")
        self.apiqdi = kwargs.get("apiqdi", self.Pararm[self.buttontext].get("apiqdi", None))
        self.text = "查询"
        self.down_text = {"by": "id", "value": self.table_id}

    def get_home_code(self):
        """ 获取code 供请求详情页使用"""


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
        self.search_time_type()
        self.click_serach()
        self.move_detaildata()
        self.get_data()

class Order订购总览详情(Order订购总览):
    Pararm2 =\
        {

            "单片收入排行": {"table_id": "singleOrderTable","dlfile":"订购总览-单片排行.xlsx","apiqdi":"queryordersingledetail"},
            "产品包收入排行": {"table_id": "productPackageOrderTable", "dlfile":"订购总览-产品包排行.xlsx","apiqdi":"queryorderpackagedetail"},
            "CP收入排行": {"table_id": "cpOrderTable", "dlfile":"订购总览-CP排行.xlsx", "apiqdi": "queryordercpdetail"},
            "区域收入排行": {"table_id": "areaOrderTable","dlfile":"订购总览-区域排行.xlsx","apiqdi":"queryorderareadetail"},
        }

    def _first(self,**kwargs):
        super()._first(**kwargs)
        self.f_search()
        self.look_排行()

    @getparamnow
    def pararms2(self, **kwargs):
        super().pararms(**kwargs)
        self.buttontext = kwargs.get("buttontext", self.Buttontext)
        self.table_id = self.Pararm2[self.buttontext]["table_id"]
        self.dlfile = self.Pararm2[self.buttontext]["dlfile"]
        self.apiqdi = self.Pararm2[self.buttontext]["apiqdi"]
        self.down_text = {"by": "id", "value": self.table_id}
        self.text = ""

    def f2_search(self, **kwargs):
        """查看的流程"""
        self.pararms2(**kwargs)
        self.get_data_datil()
        self._before(**kwargs)
        self.pararms2(**kwargs)
        self.checktext(2, element=getattr(self, "text", ""))
        self.getsysereorlog("start")
        self.change_time(pull_spanid="select2-changetime-container", pull_ulid="select2-changetime-results")
        self.move_detaildata()
        self.get_tablefirstdata()

class Order订购总览C3(Order订购总览):

    Pararm = \
        {
            "订购人数": {"table_id": "orderUserInfo", "tabletype": "order_count", "apiqdi": "queryc3ordercards"},
            "订购次数": {"table_id": "orderCountInfo", "tabletype": "order_count", "apiqdi": "queryc3ordercards"},
            "订购金额": {"table_id": "orderAmountInfo", "tabletype": "order_count", "apiqdi": "queryc3ordercards"},
            "订购冠军": {"table_id": "orderChampionDiv", "tabletype": "order_mvp", "apiqdi": "queryc3ordertopn"},
            "详情数据": {"table_id": "orderSumTable", "dlfile": "订购总览.xlsx", "apiqdi": "queryc3ordersum",
                     "tabletype": "get_tablefirstdata"},
            "单片收入排行": {"table_id": "singleCard", "tabletype": "order_sort", "detail": "singleDetail",
                       "apiqdi": "queryc3ordersingle"},
            "产品包收入排行": {"table_id": "productPackageCard", "tabletype": "order_sort", "detail": "productPackageDetail",
                        "apiqdi": "queryc3orderpackage"},
            "CP收入排行": {"table_id": "cpCard", "tabletype": "order_sort", "detail": "cpDetail", "apiqdi": "queryc3ordercp",
                       },
            "区域收入排行": {"table_id": "areaCard", "tabletype": "order_sort", "detail": "areaDetail","apiqdi": "queryc3orderarea"},
        }

    def _first(self, **kwargs):
        OrderBase._first(self, **kwargs)
        """"""
        self.checktext(1, element="订购总览C3")
        self.exement('//*[@id="menu"]//a/span[text()="订购分析"]/parent::*/parent::*/ul//span[text()="订购总览C3"]/parent::*')
        self.frame_change()

class Order订购总览详情C3(Order订购总览详情,Order订购总览C3):
    Pararm2 = \
        {

            "单片收入排行": {"table_id": "singleOrderTable", "dlfile": "订购总览C3-单片排行.xlsx", "apiqdi": "queryc3ordersingledetail"},
            "产品包收入排行": {"table_id": "productPackageOrderTable", "dlfile": "订购总览C3-产品包收入排行.xlsx",
                        "apiqdi": "queryc3orderpackagedetail"},
            "CP收入排行": {"table_id": "cpOrderTable", "dlfile": "订购总览C3-CP排行.xlsx", "apiqdi": "queryc3ordercpdetail"},
            "区域收入排行": {"table_id": "areaOrderTable", "dlfile": "订购总览C3-区域排行.xlsx", "apiqdi": "queryc3orderareadetail"},
        }

    def _first(self, **kwargs):
        Order订购总览C3._first(self,**kwargs)
        self.f_search()
        self.look_排行()


class Order退订明细( OrderBase ):

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="退订明细"]/..')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "noOrderDetailTable")
        self.dlfile = kwargs.get("dlfile", "退订明细.xlsx")
        self.apiqdi = kwargs.get("apiqdi", "queryorderunsubscribe")
        self.text = "查询"

    def get_home_code(self):
        """ 获取code 供请求详情页使用"""

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
        self.getsysereorlog( "start" )
        self.search_time_type()
        self.click_serach()
        self.move_detaildata()
        self.get_tablefirstdata()


class Order退订明细C3(Order退订明细):


    def _first(self, **kwargs):
        OrderBase._first(self,**kwargs)
        self.checktext(1,element="退订明细C3")
        self.exement('//*[@id="menu"]//a/span[text()="订购分析"]/parent::*/parent::*/ul//span[text()="退订明细C3"]/parent::*')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "noOrderDetailTable")
        self.dlfile = kwargs.get("dlfile", "退订明细.xlsx")
        self.apiqdi = kwargs.get("apiqdi", "queryc3orderunsubscribe")
        self.text = "查询"

class Order订购明细( OrderBase ):

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.checktext(2,element="订购明细")
        self.exement('//*[@id="menu"]//a/span[text()="订购明细"]/..')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "realTable")
        self.dlfile = kwargs.get("dlfile", "订购分析-订购明细.xlsx")
        self.apiqdi = kwargs.get("apiqdi", "queryorderdetail")
        self.text = "查询"

    def get_home_code(self):
        """ 获取code 供请求详情页使用"""

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
        self.page_type()
        self.click_serach()
        self.move_detaildata()
        self.get_tablefirstdata()



class Order单点订购( OrderBase ):

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="单点订购"]/..')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "singleTable")
        self.dlfile = kwargs.get("dlfile", "单点订购.xlsx")
        self.apiqdi = kwargs.get("apiqdi", "queryordersinglepoint")
        self.text = "查询"
        self.lists_page = kwargs.get("list_page", ["包月", "包年", "包季度", "包半年"])


class Order单点订购详情(Order单点订购):

    Pararm=\
        {
        "时段订购": {"table_id": "timeTable", "dlfile": "按次订购日期数据详情.xlsx", "apiqdi": "queryalluserinfo"},
        "区域分布": {"table_id": "areaDistributionTable", "dlfile": "按次订购区域分布数据.xlsx", "apiqdi": "queryordersinglepointarea"},
        "类型分布": {"table_id": "typeTable", "dlfile": "按次订购类型分布数据.xlsx", "apiqdi": "queryordersinglepointtype"},
        "单片订购": {"table_id": "monolithicTable", "dlfile": "按次订购单片订购数据.xlsx", "apiqdi": "queryordersinglepointdetail"},
        "支付方式": {"table_id": "paymentTable", "dlfile": "按次订购支付方式数据.xlsx", "apiqdi": "queryuseronlinefourmin"},
        "价格分析": {"table_id": "priceAnalyzeTable", "dlfile": "按次订购价格分析数据.xlsx", "apiqdi": "queryordersingleprice"},
        }


    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.f_search()
        self.look()

    @getparamnow
    def pararms2(self, **kwargs):
        """设置参数"""
        self.pararms(**kwargs)
        self.buttontext = kwargs.get("buttontext", "时段订购")
        self.table_id = kwargs.get("table_id", self.Pararm[self.buttontext]["table_id"])
        self.dlfile = kwargs.get("dlfile", self.Pararm[self.buttontext]["dlfile"])
        self.apiqdi = kwargs.get("apiqdi", self.Pararm[self.buttontext]["apiqdi"])
        self.text = self.buttontext




class Order包月订购( OrderBase ):

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="包月订购"]/..')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "monthTable")
        self.dlfile = kwargs.get("dlfile", "包月订购.xlsx")
        self.apiqdi = kwargs.get("apiqdi", "queryordersinglepoint")
        self.text = "查询"
        self.lists_page = kwargs.get("list_page", ["包月", "包年", "包季度", "包半年"] )


class Order包月订购详情(Order包月订购):

    Pararm=\
        {
        "时段订购": {"table_id": "timeTable", "dlfile": "按次订购日期数据详情.xlsx", "apiqdi": "queryalluserinfo"},
        "区域分布": {"table_id": "areaDistributionTable", "dlfile": "按次订购区域分布数据.xlsx", "apiqdi": "queryordersinglepointarea"},
        "类型分布": {"table_id": "typeTable", "dlfile": "按次订购类型分布数据.xlsx", "apiqdi": "queryordersinglepointtype"},
        "单片订购": {"table_id": "monolithicTable", "dlfile": "按次订购单片订购数据.xlsx", "apiqdi": "queryordersinglepointdetail"},
        "支付方式": {"table_id": "paymentTable", "dlfile": "按次订购支付方式数据.xlsx", "apiqdi": "queryuseronlinefourmin"},
        "价格分析": {"table_id": "priceAnalyzeTable", "dlfile": "按次订购价格分析数据.xlsx", "apiqdi": "queryordersingleprice"},
        }


    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.f_search()
        self.look()

    @getparamnow
    def pararms2(self, **kwargs):
        """设置参数"""
        self.pararms(**kwargs)
        self.buttontext = kwargs.get("buttontext", "时段订购")
        self.table_id = kwargs.get("table_id", self.Pararm[self.buttontext]["table_id"])
        self.dlfile = kwargs.get("dlfile", self.Pararm[self.buttontext]["dlfile"])
        self.apiqdi = kwargs.get("apiqdi", self.Pararm[self.buttontext]["apiqdi"])
        self.text = self.buttontext


class Order包年订购(OrderBase):

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.exement('//*[@id="menu"]//a/span[text()="包年订购"]/..')
        self.frame_change()

    @getparamnow
    def pararms(self, **kwargs):
        """设置参数"""
        super().pararms(**kwargs)
        self.table_id = kwargs.get("table_id", "yearTable")
        self.dlfile = kwargs.get("dlfile", "包年订购.xlsx")
        self.apiqdi = kwargs.get("apiqdi", "queryordersinglepoint")
        self.text = "查询"
        self.lists_page = kwargs.get("list_page", ["包月", "包年", "包季度", "包半年"] )


class Order包年订购详情(Order包年订购):

    Pararm=\
        {
        "时段订购": {"table_id": "timeTable", "dlfile": "按次订购日期数据详情.xlsx", "apiqdi": "queryalluserinfo"},
        "区域分布": {"table_id": "areaDistributionTable", "dlfile": "按次订购区域分布数据.xlsx", "apiqdi": "queryordersinglepointarea"},
        "类型分布": {"table_id": "typeTable", "dlfile": "按次订购类型分布数据.xlsx", "apiqdi": "queryordersinglepointtype"},
        "单片订购": {"table_id": "monolithicTable", "dlfile": "按次订购单片订购数据.xlsx", "apiqdi": "queryordersinglepointdetail"},
        "支付方式": {"table_id": "paymentTable", "dlfile": "按次订购支付方式数据.xlsx", "apiqdi": "queryuseronlinefourmin"},
        "价格分析": {"table_id": "priceAnalyzeTable", "dlfile": "按次订购价格分析数据.xlsx", "apiqdi": "queryordersingleprice"},
        }

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.f_search()
        self.look()

    @getparamnow
    def pararms2(self, **kwargs):
        """设置参数"""
        self.pararms(**kwargs)
        self.buttontext = kwargs.get("buttontext", "时段订购")
        self.table_id = kwargs.get("table_id", self.Pararm[self.buttontext]["table_id"])
        self.dlfile = kwargs.get("dlfile", self.Pararm[self.buttontext]["dlfile"])
        self.apiqdi = kwargs.get("apiqdi", self.Pararm[self.buttontext]["apiqdi"])
        self.text = self.buttontext


if __name__ == "__main__":
    obj=Order订购总览()
    obj.Buttontext="订购冠军"
    obj._begin()
    obj.f_search()
    # obj.check_web_api()

