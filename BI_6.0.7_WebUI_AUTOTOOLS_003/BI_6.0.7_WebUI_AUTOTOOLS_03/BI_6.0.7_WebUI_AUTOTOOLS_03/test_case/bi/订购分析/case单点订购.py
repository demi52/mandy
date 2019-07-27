__author__ = "luxu"
from lib.funcslib import Ioput
Ioput.input("file",  r"order单点.ini")
from lib.testsam import *
from flow.biportal.orderbase import Order单点订购, Order单点订购详情
file=Ioput.output("file")

class CaseSample首页(FunctionSample):
    for f in Get.out(Ioput.output("file"), "time"):
        exec("""
def test_{0}(self):
   Ioput.function_name(self.__class__.__name__)
   self.首页_table({1})
               """.format(f.get("casename"), f)
             )

class CaseSample详情(FunctionSample):
    for f in Get.out(Ioput.output("file"), "detail"):
        exec("""
def test_{0}(self):
    Ioput.function_name(self.__class__.__name__)
    self.详情_table({1})
            """.format(f.get("casename"), f)
             )

Test1=type("Test单点订购_首页", (CaseSample首页,), {"obj":Order单点订购})

# Test2 = type("Test单点订购详情_日",(CaseSample详情,), {"obj":Order单点订购详情,"time_type":"day"})

file=Ioput.output("file")
for c in Get.out(file, "tabletype"):
    exec("""
class Test单点订购详情_{0}(CaseSample详情):

        obj=Order单点订购详情
        timetype="{1}"

    """.format(c.get("casename"), c.get("tt"))
         )



if __name__ == "__main__":
    unittest.main()


if __name__ == "__main__":
    pass