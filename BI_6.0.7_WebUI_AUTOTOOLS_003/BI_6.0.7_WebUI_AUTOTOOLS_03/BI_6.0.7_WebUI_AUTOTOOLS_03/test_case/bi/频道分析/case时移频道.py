from config.conf import Suite

__author__ = "luxu"
from lib.funcslib import Ioput
Ioput.input("file", r"channellive")
from lib.testsam import *
from flow.biportal.channelbase import Channel时移频道
file = Ioput.output("file")

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


Test1=type("Test时移频道_首页", (CaseSample首页,), {"obj":Channel时移频道})

# class CaseSample详情(FunctionSample):
#     for f in Get.out(Ioput.output("file"), "detail"):
#         exec("""
# def test_{0}(self):
#     Ioput.function_name(self.__class__.__name__)
#     self.详情_table({1})
#             """.format(f.get("casename"), f)
#              )



# for c in Get.out(file, ("tabletype", "channel")):
#     exec("""
# class Test回看频道详情_{0}_{2}(CaseSample详情):
#
#         obj=Channel回看频道详情
#         timetype="{1}"
#         movetype="{2}"
#
#     """.format(c.get("casename"), c.get("tt"), c.get("list_page"))
#          )


if __name__ == "__main__":
    unittest.main()

