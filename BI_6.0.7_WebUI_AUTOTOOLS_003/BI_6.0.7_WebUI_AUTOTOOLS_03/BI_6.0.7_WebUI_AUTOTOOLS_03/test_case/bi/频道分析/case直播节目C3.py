from config.conf import Suite
from lib.funcslib import Ioput
Ioput.input("file", "channellive.ini")
from lib.testsam import *
from flow.biportal.channelbase import *
file=Ioput.output("file")


class CaseSample首页(FunctionSample):
    for f in Get.out(Ioput.output("file"), "time"):

        if Suite.table_data:
            exec("""
def test_{0}__表格数据(self):
   Ioput.function_name(self.__class__.__name__)
   self.首页_table({1})
               """.format(f.get("casename"), f)
             )

        if Suite.xlsx_data:
            exec("""
def test_{0}_导出数据(self):
   Ioput.function_name(self.__class__.__name__)
   self.首页_xlsx({1})
               """.format(f.get("casename"), f)
                )

        if Suite.keyword:
            exec("""
def test_{0}_关键字搜索(self):
   Ioput.function_name(self.__class__.__name__)
   self.h_keyword({1})
               """.format(f.get("casename"), f)
     )


Test1=type("Test直播节目C3_首页", (CaseSample首页,), {"obj":Channel直播节目C3})

if __name__ == "__main__":
    pass