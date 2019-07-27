import unittest

from flow.idmp.搜索推荐.scripts import Api_搜索推荐
from lib.funcslib import Ioput

__author__ = "luxu"


class Base( Api_搜索推荐, unittest.TestCase):

    def basefunc(self, url ="http://api.utstarcom.cn/idp/gettopn?type=v"):
        try:
            self.execute_test(url=url)
        except AssertionError as a:
            self.assertTrue("", "返回结果text非字典  %s" % a)
        else:
            self.assertTrue(self.text["subject"],"键 subject 无内容")
            # self.assertIn("subject", self.text, "无键  subject ")


class Test_推荐服务接口(Base):


    def test_1排行推荐_点播(self, url="http://api.utstarcom.cn/idp/gettopn?type=v"):
        """ 4.1 排行榜推荐点播
                """
        Ioput.function_name( self.__class__.__name__)
        self.basefunc( url=url )

    def test_1排行推荐_直播(self, url="http://api.utstarcom.cn/idp/gettopn?type=c"):
        """         4.1 排行榜推荐直播"""
        Ioput.function_name( self.__class__.__name__)
        self.basefunc( url=url )

    def test_1排行推荐_回看(self, url="http://api.utstarcom.cn/idp/gettopn?type=t"):
        """         4.1 排行榜推荐回看"""
        Ioput.function_name( self.__class__.__name__)
        self.basefunc( url=url )

    def test_1排行推荐_连续剧(self, url="http://api.utstarcom.cn/idp/gettopn?type=s"):
        """         4.1 排行榜推荐连续剧"""
        Ioput.function_name( self.__class__.__name__)
        self.basefunc( url=url )


    def test_2媒资相关性推荐接口(self,url="http://api.utstarcom.cn/idp/getsimilaritems?mc=02000000000000000000000000001389&userid=123456&count=2"):
        """         4.2 媒资相关性推荐接口"""
        Ioput.function_name( self.__class__.__name__ )
        self.basefunc( url=url )

    @unittest.skip("跳过")
    def test_3根据演员_导演获取影片数据接口(self, url="http://api.utstarcom.cn/idp/getInfoByRole?name=林青霞"):
        """4.3 根据演员_导演获取影片数据接口"""
        Ioput.function_name( self.__class__.__name__ )
        self.basefunc( url=url )

    def test_4南传九宫屏(self,url="http://api.utstarcom.cn/idp/getnewtopn?typeid=001"):
        """4.4 南传九宫屏"""
        Ioput.function_name( self.__class__.__name__ )
        self.basefunc( url=url )

    def test_5一级标签内容实时排行接口(self,url="http://api.utstarcom.cn/idp/getnewtopn?typeid=001"):
        """4.5	一级标签内容实时排行接口"""
        Ioput.function_name( self.__class__.__name__)
        self.basefunc( url=url )

    def test_6一级标签实时排行榜接口(self,url="http://api.utstarcom.cn/idp/gettypetopn"):
        """4.6 一级标签实时排行榜接口"""
        Ioput.function_name( self.__class__.__name__)
        self.basefunc( url=url )

    def test_7运营标签实时排行榜接口(self,url="http://api.utstarcom.cn/idp/getoptagtopn"):
        """4.7 运营标签实时排行榜接口"""
        Ioput.function_name( self.__class__.__name__)
        self.basefunc( url=url )

    def test_8猜你喜欢推荐接口(self,url="http://api.utstarcom.cn/idp/getuserrecmd?userid=123456"):
        """4.8	猜你喜欢推荐接口"""
        Ioput.function_name( self.__class__.__name__ )
        self.basefunc( url=url )

    def test_9直播推点播接口(self,url="http://api.utstarcom.cn/idp/getchannelrecmdvod?mc=02000000000000072017072100006618&userid=123456&count=2"):
        """4.9	直播推点播接口"""
        Ioput.function_name( self.__class__.__name__ )
        self.basefunc( url=url )

    def test_10实时推荐接口(self,url="http://api.utstarcom.cn/idp/getrtpersonar?userid=123456&timeslot=1"):
        """4.10	直播推点播接口"""
        Ioput.function_name( self.__class__.__name__ )
        self.basefunc( url=url )

    def test_11用户标签内容接口(self,url="http://api.utstarcom.cn/idp/getusertagdtl?userid=123456"):
        """4.11	用户标签内容接口"""
        Ioput.function_name( self.__class__.__name__ )
        self.basefunc(url=url)

class Test_搜索服务接口( Base ):

    def test_1节目名_演员_导演关键字混合搜索接口(self,url="http://{{idpURL}}/idp/search?userid=07514000663&q=QQ&start=0&count=20&sdonly=0&column=001"):
        """          5.1 排行榜推荐点播"""
        Ioput.function_name( self.__class__.__name__)
        self.basefunc(url=url)

    def test_2用户选用搜索节目采集接口(self,url="http://{{idpURL}}/idp/setvalidsearchitem?mc={{mc}}&userid={{userid}}&hdflag={{hdflag}}&searchkey={{searchkey}}"):
        """          5.2	用户选用搜索节目采集接口"""
        Ioput.function_name(self.__class__.__name__)
        self.basefunc(url=url)

    def test_3热搜节目排行接口(self,url="http://api.utstarcom.cn/idp/hotsearchtopn"):
        """          5.3	热搜节目排行接口"""
        Ioput.function_name( self.__class__.__name__ )
        self.basefunc( url=url)

    def test_4用户搜索历史接口(self,url="http://api.utstarcom.cn/idp/getusersearchlist?userid=1234&opt=reset"):
        """          5.4	用户搜索历史接口"""
        Ioput.function_name( self.__class__.__name__ )
        self.basefunc( url=url )
        
    def test_5多维度搜索接口(self,url="http://api.utstarcom.cn/idp/multisearch?title=<string>&userid=<string>"):
        """          5.5	多维度搜索接口"""
        Ioput.function_name( self.__class__.__name__ )
        self.basefunc( url=url )




if __name__ == "__main__":
   unittest.main()
