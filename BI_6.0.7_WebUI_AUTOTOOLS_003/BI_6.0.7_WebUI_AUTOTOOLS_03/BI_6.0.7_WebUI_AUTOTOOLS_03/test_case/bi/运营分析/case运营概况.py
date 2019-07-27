from config.conf import Suite

__author__ = "luxu"
from lib.funcslib import Ioput
Ioput.input("file",  r"BusinessSurvey")
from lib.testsam import *
from flow.biportal.businessbase import Business运营概况
file = Ioput.output("file")

class CaseSample首页(FunctionSample):
    for f in Get.out(file,  "time"):
        if Suite.table_data:
            exec("""
def test_{1}__表格数据(self):
   Ioput.function_name(self.__class__.__name__)
   self.首页_table({0})
               """.format(f, f.get("casename"))
             )
        if Suite.xlsx_data:
            exec("""
def test_{1}_导出数据(self):
   Ioput.function_name(self.__class__.__name__)
   self.首页_table({0})
               """.format(f, f.get("casename"))
         )


Test1=type("Test运营概况_首页", (CaseSample首页,), {"obj":Business运营概况})





if __name__ == "__main__":
    unittest.main()