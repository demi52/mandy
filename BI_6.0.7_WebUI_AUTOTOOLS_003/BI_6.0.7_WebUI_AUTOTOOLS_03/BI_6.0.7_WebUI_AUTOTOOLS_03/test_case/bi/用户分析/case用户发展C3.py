from config.conf import Suite

__author__ = "luxu"
from lib.funcslib import Ioput
Ioput.input("file", r"userdevelop.ini")
from lib.testsam import *
from flow.biportal.userbase import User用户发展C3, User用户发展详情C3
file = Ioput.output("file")


class CaseSample首页(FunctionSample):
    """构造测试用例"""
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

Test1=type("Test用户发展C3_首页", (CaseSample首页,), {"obj": User用户发展C3})

# Test2 = type("Test用户发展详情C3_日",(CaseSample详情,), {"obj": User用户发展详情C3, "time_type":"day"})

for c in Get.out(file, "tabletype"):
    exec("""
class Test用户发展C3详情_{0}(CaseSample详情):

    obj=User用户发展详情C3
    timetype="{1}"

    """.format(c.get("casename"), c.get("tt"))
         )


if __name__ == "__main__":
    print(dir())
