from config.conf import Suite

__autor__ = "鲁旭"

from lib.funcslib import Ioput
Ioput.input("file", "Epg智能")
from lib.testsam import *
from flow.biportal.epgbase import Epg标清EPG, Epg标清EPG详情
file=Ioput.output("file")

class CaseSample首页(FunctionSample):
    """创建待测试用例模板"""
    for f in Get.out(file, ("time", "Column")):
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

Test1=type("Test标清EPG_首页", (CaseSample首页,), {"obj":Epg标清EPG})


for c in Get.out(file, ("tabletype", "Column")):
    exec("""
class Test标清EPG详情_{0}_{2}(CaseSample详情):

        obj=Epg标清EPG详情
        timetype="{1}"
        movetype="{2}"

    """.format(c.get("casename"), c.get("tt"), c.get("list_page"))
         )


if __name__ == "__main__":
    print(dir())