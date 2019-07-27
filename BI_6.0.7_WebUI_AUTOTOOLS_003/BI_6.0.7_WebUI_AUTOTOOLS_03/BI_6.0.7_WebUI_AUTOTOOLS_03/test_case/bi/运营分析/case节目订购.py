from config.conf import Suite

__author__ = "luxu"
from lib.funcslib import Ioput
Ioput.input("file",  r"ProgramOrder")
from lib.testsam import *
from flow.biportal.businessbase import Business节目订购
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
def test_{1}_关键字搜索(self):
    Ioput.function_name(self.__class__.__name__)
    self.h_keyword({0})
            """.format(f, f.get("casename")))


Test1 = type("Test节目订购_首页", (CaseSample首页,), {"obj": Business节目订购})



if __name__ == "__main__":
    unittest.main()