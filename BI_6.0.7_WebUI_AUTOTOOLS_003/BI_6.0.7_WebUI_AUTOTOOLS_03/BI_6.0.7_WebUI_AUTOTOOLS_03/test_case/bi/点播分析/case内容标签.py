from config.conf import Suite

__author__ = "luxu"
from lib.funcslib import Ioput
Ioput.input("file",  r"vodtag")
from lib.testsam import *
from flow.biportal.vodbase import *
file=Ioput.output("file")

class CaseSample首页(FunctionSample):
    for f in Get.out(Ioput.output("file"), ("time", "program")):
        if Suite.table_data:
            exec("""
def test_{0}_{2}__表格数据(self):
   Ioput.function_name(self.__class__.__name__)
   self.首页_table({1})
               """.format(f.get("casename"), f,f.get("program")))

        if Suite.xlsx_data:
            exec("""
def test_{0}_{2}_导出数据(self):
   Ioput.function_name(self.__class__.__name__)
   self.首页_xlsx({1})
               """.format(f.get("casename"), f, f.get("program")))

        if Suite.keyword:
            exec("""
def test_{0}_{2}_关键字搜索(self):
   Ioput.function_name(self.__class__.__name__)
   self.h_keyword({1})
               """.format(f.get("casename"), f, f.get("program")))


class CaseSample详情(FunctionSample):
    for f in Get.out(file, "detail"):
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

        if Suite.keyword and (f.get("casename") == "节目收视" or f.get("casename") == "区域分布"):
            exec("""
def test_{0}_导出数据(self):
    Ioput.function_name(self.__class__.__name__)
    self.d_keyword({1})
            """.format(f.get("casename"), f))


Test1 = type("Test内容标签首页", (CaseSample首页,), {"obj": Vod内容标签})


for c in Get.out(file, ("tabletype", "program")):
    exec("""
class Test内容标签详情_{0}_{2}(CaseSample详情):

        obj=Vod内容标签详情
        timetype="{1}"
        Programtype="{2}"

    """.format(c.get("casename"), c.get("tt"), c.get("program"))
         )


if __name__ == "__main__":
    unittest.main()
