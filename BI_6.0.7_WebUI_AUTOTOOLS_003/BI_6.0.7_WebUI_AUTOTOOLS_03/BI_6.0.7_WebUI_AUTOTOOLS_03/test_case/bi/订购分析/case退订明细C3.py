import ddt
import unittest

from config.conf import Suite
from lib.funcslib import Ioput
from flow.biportal.orderbase import Order退订明细C3

datafile = r"ordercycle.ini"
@ddt.ddt
class Test退订明细C3_首页(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        Ioput.function_name(cls.__name__, )
        cls.sample = Order退订明细C3()
        cls.sample._begin()

    @classmethod
    def tearDownClass(cls):
        cls.sample._last()


    def tearDown(self):
        self.sample._after()


    if Suite.table_data:
        def test__表格数据(self, ):
            Ioput.function_name(self.__class__.__name__,)
            try:
                self.sample.f_search()
            except AssertionError as a:
                self.assertTrue( "", a )
            else:
                self.assertGreaterEqual(self.sample.data_lines, 1, "未生成数据的tables,无数据")

    if Suite.xlsx_data:
        def test_导出数据(self, ):
            Ioput.function_name(self.__class__.__name__,)
            try:
                self.sample.f_outxlsx()
            except AssertionError as a:
                self.assertTrue( "", a )
            else:
                self.assertGreaterEqual(len(self.sample.xlsxcontent), 2, "‘导出数据’无内容")