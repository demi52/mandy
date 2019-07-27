from config.conf import Suite

__author__ = "luxu"
from lib.funcslib import Ioput
Ioput.input("file",  r"channellive")
from lib.testsam import *
from flow.biportal.channelbase import *
file=Ioput.output("file")

class CaseSample首页(FunctionSample):
    for f in Get.out(file, ("time", "channel")):
        if Suite.table_data:
            exec("""
def test_{0}_{2}__表格数据(self):
   Ioput.function_name(self.__class__.__name__)
   self.首页_table({1})
               """.format(f.get("casename"), f, f.get("list_page"))
                )
        if Suite.xlsx_data:
            exec("""
def test_{0}_{2}_导出数据(self):
   Ioput.function_name(self.__class__.__name__)
   self.首页_xlsx({1})
               """.format(f.get("casename"), f, f.get("list_page"))
                 )
        if Suite.keyword:
            exec("""
def test_{0}_{2}_关键字搜索(self):
   Ioput.function_name(self.__class__.__name__)
   self.h_keyword({1})
               """.format(f.get("casename"), f, f.get("list_page"))
                 )

class CaseSample详情(FunctionSample):
    for f in Get.out(Ioput.output("file"), "detail"):
        if Suite.table_data:
            exec("""
def test_{0}__表格数据(self):
    Ioput.function_name(self.__class__.__name__)
    self.详情_table({1})
            """.format(f.get("casename"), f)
             )

        if Suite.xlsx_data:
            exec("""
def test_{0}_导出数据(self):
    Ioput.function_name(self.__class__.__name__)
    self.详情_xlsx({1})
                """.format(f.get("casename"), f)
                     )

        if Suite.keyword and f.get("casename") == "节目收视":
            exec("""
def test_{0}_关键字搜索(self):
    Ioput.function_name(self.__class__.__name__)
    self.d_keyword({1})
                """.format(f.get("casename"), f)
     )

Test1 = type("Test直播频道C3_首页", (CaseSample首页,), {"obj": Channel直播频道C3})


for c in Get.out(file, ("tabletype", "channel")):
    exec("""
class Test直播频道详情C3_{0}_{2}(CaseSample详情):

        obj=Channel直播频道详情C3
        timetype="{1}"
        movetype="{2}"
        group_codes="{3}"

    """.format(c.get("casename"), c.get("tt"), c.get("list_page"),c.get("groupcode"))
         )


if __name__ == "__main__":
    unittest.main()
