from config.conf import Suite

__author__ = "luxu"
from lib.funcslib import Ioput
Ioput.input("file",  r"ordersingle")
from lib.testsam import *
from flow.biportal.orderbase import *
file=Ioput.output("file")

class CaseSample首页(FunctionSample):
    for f in Get.out(Ioput.output("file"), "time"):
        if Suite.table_data:
            exec("""
def test_{0}__表格数据(self):
   Ioput.function_name(self.__class__.__name__)
   self.首页_table({1})
               """.format(f.get("casename"), f))

        if Suite.xlsx_data:
            exec("""
def test_{0}_导出数据(self):
   Ioput.function_name(self.__class__.__name__)
   self.首页_xlsx({1})
               """.format(f.get("casename"), f))

        if Suite.keyword:
            exec("""
def test_{0}_关键字搜索(self):
    Ioput.function_name(self.__class__.__name__)
    self.h_keyword({1})
           """.format(f.get("casename"), f))


class CaseSample详情(FunctionSample):
    for f in Get.out(Ioput.output("file"), "detail"):
        if Suite.table_data:
            exec("""
def test_{0}__表格数据(self):
    Ioput.function_name(self.__class__.__name__)
    self.详情_table({1})
            """.format(f.get("casename"), f))

        if Suite.xlsx_data:
            exec("""
def test_{0}_导出数据(self):
    Ioput.function_name(self.__class__.__name__)
    self.详情_xlsx({1})
            """.format(f.get("casename"), f))

        if Suite.keyword and f.get("casename") in ["区域分布", "单片订购"]:
            exec("""
def test_{0}_关键字搜索(self):
    Ioput.function_name(self.__class__.__name__)
    self.d_keyword({1})
            """.format(f.get("casename"), f))


Test1 = type("Test按次订购C3_首页", (CaseSample首页,), {"obj":Order按次订购C3})


for c in Get.out(file, "tabletype"):
    exec("""
class Test按次订购C3详情_{0}(CaseSample详情):

        obj=Order按次订购详情C3
        timetype="{1}"

    """.format(c.get("casename"), c.get("tt"))
         )





if __name__ == "__main__":
    unittest.main()
