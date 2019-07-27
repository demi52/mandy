__author__ = "luxu"

import unittest
import ddt
from lib.funcslib import Ioput
from flow.idmp.搜索推荐.scripts import 搜索
__author__ = "luxu"


class Test_语音搜索服务接口(搜索, unittest.TestCase):

    def test_1直播搜索节目列表接口(self,
             url="http://{{idpURL}}/idpvoice/searchchannel?name={{name}}&start={{start}}&count={{count}}"):
        """ 6.1	直播搜索节目列表接口"""
        Ioput.function_name(self.__class__.__name__)
        try:
            self.execute_test(url=url)
            self.get_text_value(kone="subject")
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertTrue(self.datalist1, "键 subject 无内容")

    def test_2回看搜索节目列表接口(self,
             url="http://{{snm_idpVoice}}/idpvoice/searchschedule?name={{name}}&channelname={{name}}"):
        """ 6.2回看搜索节目列表接口"""
        Ioput.function_name(self.__class__.__name__)
        try:
            self.execute_test(url=url)
            self.get_text_value(kone="subject")
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertTrue(self.datalist1, "键 subject 无内容")

    def test_3点播搜索节目列表接口(self,
             url="http://{{snm_idpVoice}}/idpvoice/searchvod?name=战狼二"):
        """ 6.3点播搜索节目列表接口"""
        Ioput.function_name(self.__class__.__name__)
        try:
            self.execute_test(url=url)
            self.get_text_value(kone="subject")
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertTrue(self.datalist1, "键 subject 无内容")


if __name__ == "__main__":
    pass
