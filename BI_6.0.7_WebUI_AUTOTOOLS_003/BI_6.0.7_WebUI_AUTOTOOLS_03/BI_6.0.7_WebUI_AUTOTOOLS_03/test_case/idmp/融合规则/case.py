__author__ = "luxu"

import ddt
import unittest
from lib.funcslib import log, getdata, Ioput as I
from flow.idmp.融合规则.script import Medial, GetC3Data


@ddt.ddt
class Test_idmp(unittest.TestCase):
    """idmp"""

    def setUp(self):
        """"""

    def tearDown(self):
        log().info("%s stop %s" % (" " * 60, " " * 60))

    @ddt.data(*getdata("data.txt","idpc"))
    def test_idpc(self, kwargs):
        """测试融合规则"""
        I.function_name(self.__class__.__name__, getdata("data.txt","idpc").index(kwargs)+1)
        try:
            obj=Medial(**kwargs)
            obj.execute_c2()
        except AssertionError as e:
            log().error(e)
            self.assertTrue("",e)
        else:
            self.assertEqual( obj.status, "pass" )


    def test_notc3(self):
        """未有C3数据时爬去扩展数据
        """
        I.function_name(self.__class__.__name__)
        try:
            obj=GetC3Data()
            obj.execute_notc3()
        except AssertionError as e:
            log().error(e)
            self.assertTrue("",e)
        else:
            self.assertEqual( obj.status, "pass" )

    def test_exitsc3(self):
        """已有C3数据时爬去扩展数据"""
        I.function_name(self.__class__.__name__)
        try:
            obj = GetC3Data()
            obj.execute_exitsc3()

        except AssertionError as e:
            log().error(e)
            self.assertTrue("")
        else:
            self.assertEqual( obj.status, "pass" )

    def test_c2c3(self):
        """未存在C3数据时，爬取扩展数据+融合数据"""
        I.function_name(self.__class__.__name__)
        try:
            obj = GetC3Data(**{'rule': [('YEAR', '1')]})
            obj.execute_c2c3()
        except AssertionError as e:
            log().error(e)
            self.assertTrue("")
        else:
            self.assertEqual( obj.status, "pass" )








