from config.conf import Suite

__author__ = "luxu"
from lib.funcslib import Ioput
Ioput.input("file",  r"useractive.ini")
from flow.biportal.userbase import *
from lib.testsam import *
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

Test用户活跃=type("Test用户活跃_首页", (CaseSample首页,), {"obj": User用户活跃})

# Test用户活跃详情_日 = type("Test用户活跃详情_日",(CaseSample详情,), {"obj": User用户活跃详情, "time_type":"day"})

for c in Get.out(file, "tabletype"):
    exec("""
class Test用户活跃详情_{0}(CaseSample详情):

    obj=User用户活跃详情
    timetype="{1}"

    """.format(c.get("casename"), c.get("tt"))
         )



if __name__ == "__main__":
    pass