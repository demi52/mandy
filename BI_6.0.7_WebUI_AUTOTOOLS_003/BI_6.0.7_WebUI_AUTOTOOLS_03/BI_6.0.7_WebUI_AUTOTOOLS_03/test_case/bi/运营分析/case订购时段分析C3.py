from config.conf import Suite

__author__ = "luxu"
from lib.funcslib import Ioput
Ioput.input("file",  r"PeriodOrder")
from lib.testsam import *
from flow.biportal.businessbase import Business订购时段分析C3 ,Business订购时段分析详情C3
file = Ioput.output("file")

class CaseSample首页(FunctionSample):
    for f in Get.out(file,  "time"):
        if Suite.table_data:
            exec("""
def test_{1}__表格数据(self):
    Ioput.function_name(self.__class__.__name__)
    self.首页_table({0})
               """.format(f, f.get("casename")))

        if Suite.xlsx_data:
            exec("""
def test_{1}_导出数据(self):
    Ioput.function_name(self.__class__.__name__)
    self.首页_table({0})
               """.format(f, f.get("casename")))

        if Suite.keyword:
            exec("""
def test_{1}_导出数据(self):
    Ioput.function_name(self.__class__.__name__)
    self.h_keyword({0})
               """.format(f, f.get("casename")))


class CaseSample详情(FunctionSample):
    for f in Get.out(Ioput.output("file"), "Detail"):
        if Suite.table_data:
            exec("""
def test_{0}__表格数据(self):
    Ioput.function_name(self.__class__.__name__)
    self.详情_table({1})
            """.format(f.get("casename",""), f)
             )
        if Suite.xlsx_data:
            exec("""
def test_{0}_导出数据(self):
    Ioput.function_name(self.__class__.__name__)
    self.详情_xlsx({1})
            """.format(f.get("casename", ""), f))

        if Suite.keyword:
            exec("""
def test_{0}_关键字搜索(self):
    Ioput.function_name(self.__class__.__name__)
    self.d_keyword({1})
            """.format(f.get("casename", ""), f))


Test1=type("Test订购时段分析C3_首页", (CaseSample首页,), {"obj":Business订购时段分析C3})


for c in Get.out(file, "tabletype",):
    exec("""
class Test订购时段分析详情C3_{0}(CaseSample详情):

        obj=Business订购时段分析详情C3
        timetype="{1}"
    """.format(c.get("casename"), c.get("tt"), )
         )


if __name__ == "__main__":
    unittest.main()