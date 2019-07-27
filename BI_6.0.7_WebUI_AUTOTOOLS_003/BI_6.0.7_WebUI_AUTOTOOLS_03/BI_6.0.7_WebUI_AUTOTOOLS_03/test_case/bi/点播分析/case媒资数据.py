from config.conf import Suite

__author__ = "luxu"
from lib.funcslib import Ioput
Ioput.input("file",  r"Vodemedia")
from lib.testsam import *
from flow.biportal.vodbase import Vod媒资数据, Vod媒资数据详情
file=Ioput.output("file")

class CaseSample首页(FunctionSample):
    for f in Get.out(Ioput.output("file"), ("time", "Other")):
        if Suite.table_data:
            exec("""
def test_{0}_{2}__表格数据(self):
   Ioput.function_name(self.__class__.__name__)
   self.首页_table({1})
               """.format(f.get("casename"), f, f.get("buttontext"))
             )

        if Suite.xlsx_data:
            exec("""
def test_{0}_{2}_导出数据(self):
   Ioput.function_name(self.__class__.__name__)
   self.首页_xlsx({1})
               """.format(f.get("casename"), f, f.get("buttontext")))

        if Suite.keyword:
            exec("""
def test_{0}_{2}_关键字搜索(self):
    Ioput.function_name(self.__class__.__name__)
    self.首页_xlsx({1})
               """.format(f.get("casename"), f, f.get("buttontext")))


class CaseSample详情(FunctionSample):
    for f in Get.out(file, "Detail"):
        if Suite.table_data:
            exec("""
def test_{0}__表格数据(self):
    Ioput.function_name(self.__class__.__name__)
    self.详情_table({1})
            """.format(f.get("buttontext2"), f))


        if Suite.xlsx_data:
            exec("""
def test_{0}_导出数据(self):
    Ioput.function_name(self.__class__.__name__)
    self.d_keyword({1})
            """.format(f.get("buttontext2"), f))

        if Suite.keyword:
            exec("""
def test_{0}_关键字搜索(self):
    Ioput.function_name(self.__class__.__name__)
    self.d_keyword({1})
            """.format(f.get("buttontext2"), f))


Test1=type("Test媒资数据首页", (CaseSample首页,), {"obj": Vod媒资数据})


for c in Get.out(file, ("tabletype", "Other")):
    exec("""
class Test媒资数据详情_{0}_{2}(CaseSample详情):

        obj=Vod媒资数据详情
        timetype="{1}"
        movetype="{2}"

    """.format(c.get("casename"), c.get("tt"), c.get("buttontext")))



if __name__ == "__main__":
    unittest.main()
