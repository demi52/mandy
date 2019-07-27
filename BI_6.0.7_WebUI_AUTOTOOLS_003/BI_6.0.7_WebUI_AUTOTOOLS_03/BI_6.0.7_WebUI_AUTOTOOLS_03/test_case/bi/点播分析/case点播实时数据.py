from config.conf import Suite

__author__ = "luxu"
from lib.funcslib import Ioput
Ioput.input("file",  r"vodnowtime")
from lib.testsam import *
from flow.biportal.vodbase import   Vod实时数据频道 ,Vod实时数据频道总览, Vod实时数据频道详情
file=Ioput.output("file")

class CaseSample首页总览(FunctionSample):
    for f in Get.out(file,  "other"):
        exec("""
def test_{0}(self):
   Ioput.function_name(self.__class__.__name__)
   self.首页_table({1})
               """.format(f.get("buttontext"), f)
             )

class CaseSample首页(FunctionSample):
    for f in Get.out(file, "channel"):
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
   self.首页_table({1})
               """.format(f.get("buttontext"), f))
        if Suite.keyword:
            exec("""
def test_{0}_媒资数据(self):
    Ioput.function_name(self.__class__.__name__)
    self.h_keyword({1})
               """.format(f.get("buttontext"), f))



class CaseSample详情(FunctionSample):
    for f in Get.out(Ioput.output("file"), "Detail",):

        if Suite.table_data:
            exec("""
def test_{0}__表格数据(self):
    Ioput.function_name(self.__class__.__name__)
    self.详情_table({1})
            """.format(f.get("buttontext0"), f)
             )

        if Suite.xlsx_data:
            if f.get("buttontext0",None) != "时段收视":
                exec("""
def test_{0}_导出数据(self):
    Ioput.function_name(self.__class__.__name__)
    self.详情_xlsx({1})
            """.format(f.get("buttontext0"), f))

        if Suite.keyword and f.get("buttontext0") == "节目收视" :
            exec("""
def test_{0}_关键字搜索(self):
    Ioput.function_name(self.__class__.__name__)
    self.d_keyword({1})
            """.format(f.get("buttontext0"), f))




Test1 = type("Test点播实时频道总览", (CaseSample首页总览,), {"obj": Vod实时数据频道总览})
Test2 = type("Test点播实时频道", (CaseSample首页,), {"obj": Vod实时数据频道})



for c in Get.out(file, "channel"):
    exec("""
class Test点播频道实时数据详情_{0}(CaseSample详情):

        obj=Vod实时数据频道详情
        Channel="{0}" 
        
    """.format(c.get("buttontext"))
         )

def test_二级栏目__表格数据(self):
    Ioput.function_name(self.__class__.__name__)
    self.详情_table({"buttontext0": "二级栏目"})

def test_二级栏目_导出数据(self):
    Ioput.function_name(self.__class__.__name__)
    self.详情_xlsx({"buttontext0": "二级栏目"})

def test_二级栏目_关键字搜索(self):
    Ioput.function_name(self.__class__.__name__)
    self.d_keyword({"buttontext0": "二级栏目"})

if Suite.table_data:
    setattr(Test点播频道实时数据详情_栏目, "test_二级栏目__表格数据", test_二级栏目__表格数据)
if Suite.xlsx_data:
    setattr(Test点播频道实时数据详情_栏目, "test_二级栏目_导出数据", test_二级栏目_导出数据)
if Suite.keyword:
    setattr(Test点播频道实时数据详情_栏目, "test_二级栏目_导出数据", test_二级栏目_关键字搜索)



if __name__ == "__main__":
    unittest.main()
