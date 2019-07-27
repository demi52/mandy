from flow.idmp.搜索推荐.scripts import 搜索
from test_case.idmp.搜索推荐.case import Base
from lib.funcslib import Ioput
import ddt
import unittest
__author__ = "luxu"

data1=["http://idpURL/idp/search?userid=07514000663&q=QQ",
        "http://idpURL/idp/search?userid=07514000663&q=QQ&start=0&count=20&sdonly=0&column=001&sdonly=0",
        "http://idpURL/idp/search?userid=07514000663&q=QQ&start=2&count=19&sdonly=0&column=002&sdonly=0",
        "http://idpURL/idp/search?userid=07514000663&q=t&start=0&count=21&sdonly=0&column=003&sdonly=0",
       ]

data3=["http://api.utstarcom.cn/idp/hotsearchtopn?type=d&count=20&sdonly=0&userid=123456&start=0",
        "http://api.utstarcom.cn/idp/hotsearchtopn?type=w&count=20&sdonly=0&userid=123456&start=0",
        "http://api.utstarcom.cn/idp/hotsearchtopn?type=m&count=20&sdonly=0&userid=123456&start=0",

        ]


@ddt.ddt
class Test_搜索服务接口(搜索, unittest.TestCase):

    @ddt.data(*data1)
    def test_1节目名_演员_导演关键字混合搜索接口(self,
             url="http://idpURL/idp/search?userid=123456&q=QQ&start=0&count=20&sdonly=0&column=001"):

        Ioput.function_name(self.__class__.__name__,casennumber=data1.index(url))
        try:
            self.execute_test(url=url)
            self.get_text_value(kone="subject", ktwo="column",repeat=True)
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertTrue( self.datalist1, "键 subject 无内容")
            self.assertEqual(self.search_url("column"), self.datalist2[0])


    def test_2用户选用搜索节目采集接口(self,
            url="http://{{idpURL}}/idp/setvalidsearchitem?mc=0000&userid=123456&hdflag=2&searchkey=x"):
        """ 5.2	用户选用搜索节目采集接口"""
        Ioput.function_name(self.__class__.__name__)
        try:
            self.execute_test(url=url)
            self.get_text_value(kone="code")
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertEqual(self.datalist1, 0, "键 subject 无内容")

    @ddt.data(*data3 )
    def test_3热搜节目排行接口(self, url="http://api.utstarcom.cn/idp/hotsearchtopn?type=w&count=20&sdonly=0&userid=123456&start=0"):
        """          5.3	热搜节目排行接口"""
        Ioput.function_name(self.__class__.__name__,casennumber=data3.index(url))
        try:
            self.execute_test(url=url)
            self.get_text_value(kone="subject", ktwo="column",repeat=True)
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertTrue( self.datalist1, "键 subject 无内容")

    def test_4用户搜索历史接口_1(self, url="http://api.utstarcom.cn/idp/getusersearchlist?userid=1234"):
        """          5.4	用户搜索历史接口"""
        Ioput.function_name( self.__class__.__name__ )
        try:
            self.executeapi(url="http://{{idpURL}}/idp/setvalidsearchitem?mc=0000&userid=123456&hdflag=2&searchkey=x")
            self.execute_test(url=url)
            self.get_text_value( kone="subject")
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertTrue(self.datalist1, "未查到数据")



    def test_4用户搜索历史接口_2(self, url="http://api.utstarcom.cn/idp/getusersearchlist?userid=123456&opt=reset"):
        """          5.4	用户搜索历史接口"""
        Ioput.function_name(self.__class__.__name__)
        try:
            self.execute_test(url=url)
            self.get_text_value( kone="code" )
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertEqual(self.datalist1, 0, "键 subject 无内容" )

    def test_4用户搜索历史接口_3(self, url="http://api.utstarcom.cn/idp/getusersearchlist?userid=1234"):
        """          5.4	用户搜索历史接口"""
        Ioput.function_name( self.__class__.__name__ )
        try:
            self.executeapi( url="http://{{idpURL}}/idp/setvalidsearchitem?mc=0000&userid=123456&hdflag=2&searchkey=x")
            self.executeapi(url="http://api.utstarcom.cn/idp/getusersearchlist?userid=123456&opt=reset")
            self.execute_test(url=url)
            self.get_text_value( kone="subject")
        except AssertionError as a:
            self.assertTrue( "", "返回结果text非字典  %s" % a )
        else:
            self.assertEqual( self.datalist1,[], "未查到数据" )


    def test_5多维度搜索接口_1(self,  url="http://api.utstarcom.cn/idp/multisearch?userid=123456&column=001"):
        """          5.5	多维度搜索接口"""
        Ioput.function_name( self.__class__.__name__ )
        try:
            self.execute_test(url=url)
            self.get_text_value(kone="subject", ktwo="column", repeat=True)
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertTrue( self.datalist1, "键 subject 无内容")
            self.assertEqual(self.search_url("column"), self.datalist2[0])

    def test_5多维度搜索接口_2(self, url="http://api.utstarcom.cn/idp/multisearch?title=我们&userid=123456"):
        """          5.5	多维度搜索接口"""
        Ioput.function_name( self.__class__.__name__ )
        try:
            self.execute_test(url=url)
            self.get_text_value(kone="subject", ktwo="title", repeat=True)
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertTrue( self.datalist1, "键 subject 无内容")
            self.assertIn(self.search_url("title"), self.datalist2[0])

    def test_5多维度搜索接口_3(self, url="http://api.utstarcom.cn/idp/multisearch?directors=姬棹馨&userid=123456"):
        """          5.5	多维度搜索接口"""
        Ioput.function_name( self.__class__.__name__ )
        try:
            self.execute_test(url=url)
            self.get_text_value(kone="subject", ktwo="directors", repeat=True)
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertTrue( self.datalist1, "键 subject 无内容")
            self.assertIn(self.search_url("directors"), self.datalist2[0])

    def test_5多维度搜索接口_4(self, url="http://api.utstarcom.cn/idp/multisearch?&userid=123456&casts=李菲儿"):
        """          5.5	多维度搜索接口"""
        Ioput.function_name( self.__class__.__name__)
        try:
            self.execute_test(url=url)
            self.get_text_value(kone="subject", ktwo="casts", repeat=True)
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertTrue( self.datalist1, "键 subject 无内容")
            self.assertIn(self.search_url("casts"), self.datalist2[0])




if __name__ == "__main__":
    pass
