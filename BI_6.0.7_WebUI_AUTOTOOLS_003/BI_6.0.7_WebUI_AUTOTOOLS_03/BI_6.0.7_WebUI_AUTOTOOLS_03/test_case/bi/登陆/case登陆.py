__author__ = "luxu"

import ddt
import unittest
from lib.funcslib import Ioput, getdata
from flow.biportal.script登陆 import Land


@ddt.ddt
class TestLand(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """"""
        cls.sample = Land()
        cls.sample._begin()

    def tearDown(self):
        """"""
        self.sample._after()

    @ddt.data(*getdata("land.ini", "land"))
    def test_land(self, kwargs):
        """登陆页面"""
        Ioput.function_name(self.__class__.__name__, getdata("land.ini", "land").index(kwargs)+1)
        try:
            self.sample.f_land( **kwargs )
            self.assertIn("管理员", self.sample.driver.page_source)
        except Exception as e:
            self.assertTrue("",e)


if __name__ == "__main__":
    unittest.main()
