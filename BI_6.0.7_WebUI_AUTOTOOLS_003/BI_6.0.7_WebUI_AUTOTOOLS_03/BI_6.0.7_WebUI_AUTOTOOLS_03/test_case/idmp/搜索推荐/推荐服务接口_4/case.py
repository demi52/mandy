import unittest
import ddt
from lib.funcslib import Ioput
from flow.idmp.搜索推荐.scripts import 搜索
from test_case.idmp.搜索推荐.case import Base

__author__ = "luxu"

class Test_推荐服务接口(搜索,unittest.TestCase):


    def test_1排行推荐_点播_1(self, url="http://api.utstarcom.cn/idp/gettopn?type=v"):
        """ 4.1 排行榜推荐点播
        "http://api.utstarcom.cn/idp/gettopn?type=v"
        """
        Ioput.function_name(self.__class__.__name__)
        try:
            self.execute_test(url=url)
            self.get_text_value(kone="subject")
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertTrue(self.datalist1, "键 subject 无内容")


    def test_1排行推荐_直播_2(self, url="http://api.utstarcom.cn/idp/gettopn?type=c&start=2&count=20"):
        """ 4.1 排行榜推荐直播"""
        Ioput.function_name(self.__class__.__name__)
        try:
            self.execute_test(url=url)
            self.get_text_value(kone="subject")
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertTrue(self.datalist1, "键 subject 无内容")

    def test_1排行推荐_回看_3(self, url="http://api.utstarcom.cn/idp/gettopn?type=t&start=0&count=19"):
        """         4.1 排行榜推荐回看"""
        Ioput.function_name(self.__class__.__name__)
        try:
            self.execute_test(url=url)
            self.get_text_value(kone="subject")
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertTrue(self.datalist1, "键 subject 无内容")

    def test_1排行推荐_连续剧_4(self, url="http://api.utstarcom.cn/idp/gettopn?type=s&start=0&count=21"):
        """ 4.1 排行榜推荐连续剧"""
        Ioput.function_name(self.__class__.__name__)
        try:
            self.execute_test(url=url)
            self.get_text_value(kone="subject")
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertTrue(self.datalist1, "键 subject 无内容")


    def test_2媒资相关性推荐接口_1(self,url="http://api.utstarcom.cn/idp/getsimilaritems?mc=09&userid=123456&count=2"):
        """4.2 媒资相关性推荐接口"""
        Ioput.function_name(self.__class__.__name__)
        try:
            self.execute_test(url=url)
            self.get_text_value(kone="subject")
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertTrue(self.datalist1, "键 subject 无内容")
            self.assertLessEqual(len(self.datalist1), int(self.search_url("count")))

    def test_2媒资相关性推荐接口_2(self,url="http://api.utstarcom.cn/idp/getsimilaritems?mc=09&userid=123456&count=19"):
        """4.2 媒资相关性推荐接口"""
        Ioput.function_name(self.__class__.__name__)
        try:
            self.execute_test(url=url)
            self.get_text_value(kone="subject")
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertTrue(self.datalist1, "键 subject 无内容")
            self.assertLessEqual(len(self.datalist1), int(self.search_url("count")))


    def test_3根据演员_导演获取影片数据接口(self, url="http://api.utstarcom.cn/idp/getInfoByRole?name=林青霞"):
        """4.3 根据演员_导演获取影片数据接口"""
        Ioput.function_name(self.__class__.__name__)
        try:
            self.execute_test(url=url)
            self.get_text_value(kone="subject")
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertTrue(self.datalist1, "键 subject 无内容")


    def test_4南传九宫屏_1(self,url="http://api.utstarcom.cn/idp/getscreen9?type=c&start=0&count=20"):
        """4.4 南传九宫屏"""
        Ioput.function_name(self.__class__.__name__)
        try:
            self.execute_test(url=url)
            self.get_text_value(kone="subject")
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertTrue(self.datalist1, "键 subject 无内容")

    def test_4南传九宫屏_2(self,url ="http://api.utstarcom.cn/idp/getscreen9?type=v&start=0&count=20"):
        """4.4 南传九宫屏"""
        Ioput.function_name(self.__class__.__name__)
        try:
            self.execute_test(url=url)
            self.get_text_value(kone="subject")
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertTrue(self.datalist1, "键 subject 无内容")

    def test_4南传九宫屏_3(self,url ="http://api.utstarcom.cn/idp/getscreen9?type=s&start=0&count=20"):
        """4.4 南传九宫屏"""
        Ioput.function_name(self.__class__.__name__)
        try:
            self.execute_test(url=url)
            self.get_text_value(kone="subject")
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertTrue(self.datalist1, "键 subject 无内容")

    def test_4南传九宫屏_4(self,url="http://api.utstarcom.cn/idp/getscreen9?type=c&start=0&count=10"):
        """4.4 南传九宫屏"""
        Ioput.function_name(self.__class__.__name__)
        try:
            self.execute_test(url=url)
            self.get_text_value(kone="subject")
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertTrue(self.datalist1, "键 subject 无内容")


    def test_5一级标签内容实时排行接口_1(self,url="http://api.utstarcom.cn/idp/getnewtopn?typeid=001&start=0&count=20&sdonly=1"):
        """4.5	一级标签内容实时排行接口"""
        Ioput.function_name(self.__class__.__name__)
        try:
            self.execute_test(url=url)
            self.get_text_value(kone="subject")
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertTrue(self.datalist1, "键 subject 无内容")

    def test_5一级标签内容实时排行接口_2(self,url="http://api.utstarcom.cn/idp/getnewtopn?typeid=002&start=0&count=19&sdonly=0"):
        """4.5	一级标签内容实时排行接口"""
        Ioput.function_name(self.__class__.__name__)
        try:
            self.execute_test(url=url)
            self.get_text_value(kone="subject")
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertTrue(self.datalist1, "键 subject 无内容")


    def test_6一级标签实时排行榜接口_1(self,url="http://api.utstarcom.cn/idp/gettypetopn?start=0&count=20&sdonly=1"):
        """4.6 一级标签实时排行榜接口"""
        Ioput.function_name(self.__class__.__name__)
        try:
            self.execute_test(url=url)
            self.get_text_value(kone="subject")
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertTrue(self.datalist1, "键 subject 无内容")
    def test_6一级标签实时排行榜接口_2(self,url="http://api.utstarcom.cn/idp/gettypetopn?start=0&count=10&sdonly=0"):
        """4.6 一级标签实时排行榜接口"""
        Ioput.function_name(self.__class__.__name__)
        try:
            self.execute_test(url=url)
            self.get_text_value(kone="subject")
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertTrue(self.datalist1, "键 subject 无内容")

    def test_7运营标签实时排行榜接口(self,url="http://api.utstarcom.cn/idp/getoptagtopn"):
        """4.7 运营标签实时排行榜接口"""
        Ioput.function_name(self.__class__.__name__)
        try:
            self.execute_test(url=url)
            self.get_text_value(kone="subject")
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertTrue(self.datalist1, "键 subject 无内容")

    def test_8猜你喜欢推荐接口(self,url="http://api.utstarcom.cn/idp/getuserrecmd?userid=123456"):
        """4.8	猜你喜欢推荐接口"""
        Ioput.function_name(self.__class__.__name__)
        try:
            self.execute_test(url=url)
            self.get_text_value(kone="subject")
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertTrue(self.datalist1, "键 subject 无内容")

    def test_9直播推点播接口(self,url="http://api.utstarcom.cn/idp/getchannelrecmdvod?mc=020&userid=123456&count=2"):
        """4.9	直播推点播接口"""
        Ioput.function_name(self.__class__.__name__)
        try:
            self.execute_test(url=url)
            self.get_text_value(kone="subject")
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertTrue(self.datalist1, "键 subject 无内容")

    def test_10实时推荐接口_1(self,url="http://api.utstarcom.cn/idp/getrtpersonar?userid=123456&timeslot=0"):
        """4.10	直播推点播接口"""
        Ioput.function_name(self.__class__.__name__)
        try:
            self.execute_test(url=url)
            self.get_text_value(kone="subject")
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertTrue(self.datalist1, "键 subject 无内容")

    def test_10实时推荐接口_2(self,url="http://api.utstarcom.cn/idp/getrtpersonar?userid=123456&timeslot=1"):
        """4.10	直播推点播接口"""
        Ioput.function_name(self.__class__.__name__)
        try:
            self.execute_test(url=url)
            self.get_text_value(kone="subject")
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertTrue(self.datalist1, "键 subject 无内容")

    def test_10实时推荐接口_3(self,url="http://api.utstarcom.cn/idp/getrtpersonar?userid=123456&timeslot=2"):
        """4.10	直播推点播接口"""
        Ioput.function_name(self.__class__.__name__)
        try:
            self.execute_test(url=url)
            self.get_text_value(kone="subject")
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertTrue(self.datalist1, "键 subject 无内容")


    def test_11用户标签内容接口(self,url="http://api.utstarcom.cn/idp/getusertagdtl?userid=123456"):
        """4.11	用户标签内容接口"""
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
