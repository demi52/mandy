from config.conf import Suite

__autor__ = "鲁旭"

from lib.funcslib import Ioput
Ioput.input("file", "HDreal")
from lib.testsam import *
from flow.biportal.epgbase import Epg标清实时数据
file=Ioput.output("file")

class CaseSample首页(FunctionSample):
    for f in Get.out(Ioput.output("file"), "Column"):
        if Suite.table_data:
            exec("""
def test_{0}__表格数据(self):
   Ioput.function_name(self.__class__.__name__)
   self.首页_table({1})
               """.format(f.get("list_page"), f)
             )
            if Suite.xlsx_data:
                exec("""
def test_{0}_导出数据(self):
   Ioput.function_name(self.__class__.__name__)
   self.首页_xlsx({1})
               """.format(f.get("list_page"), f)
             )

Test1=type("Test标清实时数据_首页", (CaseSample首页,), {"obj":Epg标清实时数据})







if __name__ == "__main__":
    print(dir())