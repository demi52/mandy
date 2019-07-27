from config.conf import Suite

__autor__ = "鲁旭"

from lib.funcslib import Ioput
Ioput.input("file", "TitleParser")
from lib.testsam import *
from flow.biportal.titlebase import Title专区分析
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

Test1=type("Test专区分析_首页", (CaseSample首页,), {"obj":Title专区分析})




if __name__ == "__main__":
    print(dir())