from config.conf import Suite

__author__ = "luxu"
from lib.funcslib import Ioput
Ioput.input("file",  r"orderall")
from flow.biportal.orderbase import Order订购总览, Order订购总览详情
from lib.testsam import *
file = Ioput.output("file")

class CaseSample首页(FunctionSample):
    for f in Get.out(Ioput.output("file"), ("time","other")):
        if Suite.table_data:
            exec("""
def test_{0}_{2}__表数据(self):
   Ioput.function_name(self.__class__.__name__)
   self.首页_table({1})
               """.format(f.get("casename"), f,f.get("buttontext"))
             )
        if Suite.xlsx_data and f.get("buttontext", None) == "详情数据":
            exec("""
def test_{0}_{2}_导出数据(self):
   Ioput.function_name(self.__class__.__name__)
   self.首页_xlsx({1})
               """.format(f.get("casename"), f, f.get("buttontext")))

        if Suite.keyword and f.get("buttontext", None) == "详情数据":
            exec("""
def test_{0}_{2}_关键字搜索(self):
    Ioput.function_name(self.__class__.__name__)
    self.h_keyword({1})
               """.format(f.get("casename"), f, f.get("buttontext")))


class CaseSample详情(FunctionSample):

    if Suite.table_data:
        exec("""
def test_排行详情__表格数据(self):
    Ioput.function_name(self.__class__.__name__)
    self.详情_table({})
            """)

    if Suite.xlsx_data:
            exec("""
def test_排行详情_导出数据(self):
    Ioput.function_name(self.__class__.__name__)
    self.详情_xlsx({})
            """)

    if Suite.keyword:
        exec("""
def test_排行详情_关键字搜索(self):
    Ioput.function_name(self.__class__.__name__)
    self.d_keyword({})
            """)


Test1 = type("Test订购总览_首页", (CaseSample首页,), {"obj":Order订购总览})

for c in Get.out(file, ("tabletype","detail")):
    exec("""
class Test订购总览详情_{0}_{2}(CaseSample详情):

        obj=Order订购总览详情
        timetype="{1}"
        Buttontext = "{2}"
    """.format(c.get("casename"), c.get("tt"),c.get("buttontext"))
         )



if __name__ == "__main__":
    unittest.main()


