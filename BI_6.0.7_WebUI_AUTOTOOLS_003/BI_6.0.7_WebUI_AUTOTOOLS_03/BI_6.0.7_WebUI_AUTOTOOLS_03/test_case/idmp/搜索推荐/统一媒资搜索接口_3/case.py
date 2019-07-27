__author__ = "luxu"

import unittest
import ddt
from lib.funcslib import Ioput
from flow.idmp.搜索推荐.scripts import 搜索
__author__ = "luxu"


class Test_统一媒资接口(搜索, unittest.TestCase):

    def test_1统一媒资查询接口(self,
             url="http://api.utstarcom.cn/idp/mergedinfo?mc=<string>"):
        """ 3.1统一媒资查询接口"""
        Ioput.function_name(self.__class__.__name__)
        try:
            self.execute_test(url=url)
            self.get_text_value(kone="subject")
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertTrue(self.datalist1, "键 subject 无内容")

    def test_2媒资来源查询接口_1(self,url="http://api.utstarcom.cn/idp/mergedsource?mc=<string>"):
        """3.2媒资来源查询接口"""
        Ioput.function_name(self.__class__.__name__)
        try:
            self.execute_test(url=url)
            self.get_text_value(kone="subject")
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertTrue(self.datalist1, "键 subject 无内容")
    def test_2媒资来源查询接口_2(self,url="http://api.utstarcom.cn/idp/mergedsource?mc=<string>&s=c2"):
        """3.2媒资来源查询接口"""
        Ioput.function_name(self.__class__.__name__)
        try:
            self.execute_test(url=url)
            self.get_text_value(kone="subject")
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertTrue(self.datalist1, "键 subject 无内容")
    def test_2媒资来源查询接口_3(self,url="http://api.utstarcom.cn/idp/mergedsource?mc=<string>&s=douban"):
        """3.2媒资来源查询接口"""
        Ioput.function_name(self.__class__.__name__)
        try:
            self.execute_test(url=url)
            self.get_text_value(kone="subject")
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertTrue(self.datalist1, "键 subject 无内容")