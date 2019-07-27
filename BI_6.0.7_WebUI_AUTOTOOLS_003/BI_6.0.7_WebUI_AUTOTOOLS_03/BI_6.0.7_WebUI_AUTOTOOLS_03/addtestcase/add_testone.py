#encoding='utf-8'
#author='鲁旭'
import unittest

from test_case.bi.用户分析.case用户发展 import *
from test_case.bi.用户分析.case用户活跃 import *
from test_case.bi.用户分析.case用户活跃C3 import *
from test_case.bi.订购分析.case周期订购C3 import *
from test_case.bi.订购分析.case按次订购 import *
from test_case.bi.频道分析.case回看频道 import *


def suite():
    """
    添加测试类、函数
    :return:
    """
    suite=unittest.TestSuite()
    loader = unittest.TestLoader()
    # suite.addTest(loader.loadTestsFromTestCase(Test用户发展详情))

    # suite.addTest(TestUserDevelop("test_outxlsx_user"))
    return suite

if __name__ == "__main__":
    print(list(iter(suite())))
    # print(len(["x" for i in suite()]))
    pass
    # print(dir())