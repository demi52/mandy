__autor__ = "鲁旭"

from flow.biportal.homepage import HomePage
from lib.funcslib import Ioput
Ioput.input("file", "homepage")
from lib.testsam import *
file = Ioput.output("file")

class CaseSample首页(FunctionSample):
    for f in Get.out(file, "detail"):
        exec("""
def test_{0}(self):
   Ioput.function_name(self.__class__.__name__)
   self.首页_table({1})
               """.format(f.get("buttontext"), f)
             )


Test1 = type("Test首页", (CaseSample首页,), {"obj": HomePage})

if __name__ == "__main__":
    pass