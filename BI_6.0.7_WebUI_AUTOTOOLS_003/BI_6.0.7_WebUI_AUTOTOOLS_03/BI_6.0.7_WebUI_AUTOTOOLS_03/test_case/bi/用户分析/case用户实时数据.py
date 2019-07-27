__autor__ = "鲁旭"

from lib.funcslib import Ioput
Ioput.input("file", "usernowtime")
from lib.testsam import *
from flow.biportal.userbase import *
file=Ioput.output("file")

class CaseSample首页(FunctionSample):
    for f in Get.out(Ioput.output("file"), "other"):
        exec("""
def test_{0}(self):
   Ioput.function_name(self.__class__.__name__)
   self.首页_table({1})
               """.format(f.get("buttontext"), f)
             )

Test2 = type("Test用户实时数据",(CaseSample首页,), {"obj":User实时数据})


if __name__ == "__main__":
    print(dir())
