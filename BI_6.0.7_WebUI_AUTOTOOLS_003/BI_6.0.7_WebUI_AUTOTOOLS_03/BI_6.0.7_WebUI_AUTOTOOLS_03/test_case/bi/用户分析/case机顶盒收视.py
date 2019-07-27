__author__ = "luxu"
import unittest
from lib.funcslib import Ioput
from flow.biportal.userbase import User机顶盒收视

file = r"userdevelop.ini"


class TestUser机顶盒收视( unittest.TestCase ):

    @classmethod
    def setUpClass(cls):

        Ioput.function_name(cls.__name__)
        cls.sample = User机顶盒收视()
        # cls.sample.pararms()
        cls.sample._begin()

    @classmethod
    def tearDownClass(cls):
        cls.sample._last()


    def tearDown(self):
        """"""
        self.sample._after()

    def test_机顶盒收视_0_首页(self):
        Ioput.function_name(self.__class__.__name__)
        try:
            self.sample.f_search()
        except AssertionError as a:
            self.assertTrue("", a)
        else:
            self.assertGreaterEqual(self.sample.data_lines, 1, "未生成数据的tables,无数据")


    def test_机顶盒收视_1_导出数据_1(self):

        Ioput.function_name(self.__class__.__name__)
        try:
            self.sample.f_outxlsx()
        except AssertionError as a:
            self.assertTrue( "", a )
        else:
            self.assertGreaterEqual(len(self.sample.xlsxcontent), 2, "空表")
            # self.assertEqual(len(self.sample.xlsxcontent), self.sample.head_lines + self.sample.data_lines, "行数不同")
            # self.assertEqual(self.sample.xlsxcontent[1:], self.sample.table_firstline_list, "第一行数据不相同")




if __name__ == "__main__":
    unittest.main()
