from config.conf import Suite

__autor__ = "鲁旭"

from lib.funcslib import Ioput
Ioput.input("file", "VersionCount")
from lib.testsam import *
from flow.biportal.userbase import User版本统计,   User版本统计详情
file = Ioput.output("file")

class CaseSample首页(FunctionSample):
    for f in Get.out(Ioput.output("file"), "time"):
        if Suite.table_data:
            exec("""
def test_{0}__数据表格(self):
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


class CaseSample详情(FunctionSample):
    for f in Get.out(Ioput.output("file"), "detail"):
        if Suite.table_data:
            exec("""
def test_{0}__数据表格(self):
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

Test1=type("Test版本统计_首页", (CaseSample首页,), {"obj":User版本统计})


for c in Get.out(file, "tabletype"):
    exec("""
class Test版本统计详情页_{0}(CaseSample详情):

        obj=User版本统计详情
        timetype="{1}"

    """.format(c.get("casename"), c.get("tt"))
         )


if __name__ == "__main__":
    print(dir())