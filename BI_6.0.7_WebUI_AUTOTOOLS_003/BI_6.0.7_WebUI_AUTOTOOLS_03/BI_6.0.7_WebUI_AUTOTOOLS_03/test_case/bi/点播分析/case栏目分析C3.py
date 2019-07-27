from config.conf import Suite

__autor__ = "鲁旭"
__author__ = "luxu"
from flow.biportal.vodbase import *
from lib.funcslib import Ioput
Ioput.input("file", "vodcolumn.ini")
from lib.testsam import *
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

        if Suite.keyword and (f.get("casename") == "子级栏目" or f.get("casename") == "节目收视"):
            exec("""
def test_{0}_关键字搜索(self):
    Ioput.function_name(self.__class__.__name__)
    self.d_keyword({1})
          """.format(f.get("casename"), f))


Test1=type("Test栏目分析C3首页", (CaseSample首页,), {"obj":Vod栏目分析C3})


for c in Get.out(file, "tabletype"):
    exec("""
class Test栏目分析详情C3_{0}(CaseSample详情):

        obj=Vod栏目分析详情C3
        timetype="{1}"

    """.format(c.get("casename"), c.get("tt")))



if __name__ == "__main__":
    unittest.main()



if __name__ == "__main__":
    pass