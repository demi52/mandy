from config.conf import Suite

__author__ = "luxu"
from lib.funcslib import Ioput
Ioput.input("file",  r"CDdatil")
from lib.testsam import *
from flow.biportal.cdbase import CountData结算明细
file=Ioput.output("file")

class CaseSample首页(FunctionSample):

    for f in Get.out(file,  "Detail"):
        if Suite.table_data:
            exec("""
def test_{1}__表格数据(self):
   Ioput.function_name(self.__class__.__name__)
   self.首页_table({0})
               """.format(f, f.get("buttontext"))
             )
        if Suite.xlsx_data:
            exec("""
def test_{1}_导出数据(self):
   Ioput.function_name(self.__class__.__name__)
   self.首页_table({0})
               """.format(f, f.get("buttontext"))
         )

# class CaseSample详情(FunctionSample):
#     for f in Get.out(Ioput.output("file"), "Detail"):
#         exec("""
# def test_{0}(self):
#     Ioput.function_name(self.__class__.__name__)
#     self.详情_table({1})
#             """.format(f.get("casename"), f)
#              )

Test1=type("Test结算明细_首页", (CaseSample首页,), {"obj":CountData结算明细})


# for c in Get.out(file, ("tabletype", "Usertypedata")):
#     exec("""
# class Test用户统计详情_{0}_{2}(CaseSample详情):
#
#         obj=User用户统计详情
#         timetype="{1}"
#         Usertype="{2}"
#
#     """.format(c.get("casename"), c.get("tt"), c.get("buttontext"))
#          )


if __name__ == "__main__":
    unittest.main()