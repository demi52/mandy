from config.conf import Suite

__author__ = "luxu"
from lib.funcslib import Ioput
Ioput.input("file",  r"channelnowtime")
from lib.testsam import *
from flow.biportal.channelbase import Channel实时数据频道, Channel实时数据频道详情, Channel实时数据频道总览
file = Ioput.output("file")

class CaseSample首页总览(FunctionSample):
    for f in Get.out(file, ("time", "other")):
        exec("""
def test_{0}(self):
   Ioput.function_name(self.__class__.__name__)
   self.首页_table({1})
               """.format(f.get("buttontext"), f)
             )

class CaseSample首页(FunctionSample):
    for f in Get.out(file, ("time", "channel")):
        if Suite.table_data:
            exec("""
def test_{0}__表格数据(self):
   Ioput.function_name(self.__class__.__name__)
   self.首页_table({1})
               """.format(f.get("buttontext"), f)
             )

        if Suite.xlsx_data:
            exec("""
def test_{0}_导出数据(self):
   Ioput.function_name(self.__class__.__name__)
   self.首页_xlsx({1})
               """.format(f.get("buttontext"), f)
                 )

        if Suite.keyword:
            exec("""
def test_{0}_关键字搜索(self):
   Ioput.function_name(self.__class__.__name__)
   self.h_keyword({1})
               """.format(f.get("buttontext"), f)
     )

class CaseSample详情(FunctionSample):
    for f in Get.out(Ioput.output("file"), "detail"):
            exec("""
def test_{0}__表格数据(self):
    Ioput.function_name(self.__class__.__name__)
    self.详情_table({1})
            """.format(f.get("buttontext"), f)
             )


Test频道实时总览 = type("Test频道实时总览", (CaseSample首页总览,), {"obj": Channel实时数据频道总览})
Test频道实时频道 = type("Test频道实时频道", (CaseSample首页,), {"obj": Channel实时数据频道})

for c in Get.out(file, "channel"):

    if c.get("buttontext") == "全网频道":
        exec("""
class Test频道实时数据详情_{0}(CaseSample详情):
        obj=Channel实时数据频道详情
        Channel="{0}"
        group_codes=None

    """.format(c.get("buttontext"), c.get("groupcode"))
     )
    else:
        exec("""
class Test频道实时数据详情_{0}(CaseSample详情):
        obj=Channel实时数据频道详情
        Channel="{0}"
        group_codes="{1}"

    """.format(c.get("buttontext"),c.get("groupcode"))
         )



if __name__ == "__main__":
    unittest.main()
