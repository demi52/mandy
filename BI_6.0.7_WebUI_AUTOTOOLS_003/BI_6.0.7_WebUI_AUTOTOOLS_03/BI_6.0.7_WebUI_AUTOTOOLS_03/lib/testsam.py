

__autor__ = "鲁旭"

import unittest
from lib.funcslib import Ioput, Get
if __name__== "__main__":
    Ioput.input("file", "userdevelop")


class FunctionSample(unittest.TestCase):

    timetype = "day"
    movetype = "高清"
    Buttontext="详情数据"
    Programtype="提供商"
    Channel = "高清"
    Usertype = "全网用户数据"
    obj = type
    group_codes= None
    if group_codes=="None" :
        group_codes=None


    @classmethod
    def setUpClass(cls):
        """"""
        Ioput.function_name(cls.__name__)
        cls.sample = cls.obj()
        cls.sample.time_type = cls.timetype
        cls.sample.movetype = cls.movetype
        cls.sample.Buttontext = cls.Buttontext
        cls.sample.programtype = cls.Programtype
        cls.sample.Channel = cls.Channel
        cls.sample.Usertype = cls.Usertype
        cls.sample.group_codes=cls.group_codes

        cls.sample._begin()

    @classmethod
    def tearDownClass(cls):
        cls.sample._last()

    def tearDown(self):
        self.sample._after()

    def 首页_xlsx(self,kwargs):
        try:
            self.sample.f_outxlsx(**kwargs)
        except AssertionError as a:
            self.assertTrue( "", a )
        else:
            self.assertGreaterEqual(len(self.sample.xlsxcontent),2 ,"‘导出数据’无内容")
            # self.assertEqual(len(self.sample.xlsxcontent), self.sample.head_lines + self.sample.data_lines, "行数不同")
            # self.assertEqual(self.sample.xlsxcontent[1], self.sample.table_firstline_list[1:-1], "第一行数据不相同")


    def 首页_table(self, kwargs):
        try:
            self.sample.f_search(**kwargs)
            self.sample.check_web_api()
        except AssertionError as a:
            self.assertTrue("", a)


    def 详情_xlsx(self, kwargs):
        """导出数据测试"""
        try:
            self.sample.f2_outxlsx(**kwargs)

        except AssertionError as a:
            self.assertTrue("", a)
        else:
            self.assertGreaterEqual(len(self.sample.xlsxcontent), 2, "‘导出数据’无内容")
            # self.assertGreaterEqual(len(self.sample.xlsxcontent), self.sample.head_lines + self.sample.data_lines, "行数不同")
            # self.assertEqual(self.sample.xlsxcontent[1], self.sample.table_firstline_list[1:], "第一行数据不相同")

    def 详情_table(self, kwargs):
        try:
            self.sample.f2_search(**kwargs)
            self.sample.check_web_api()
        except AssertionError as a:
            self.assertTrue("", a)


    def h_keyword(self,kwargs):
        """首页关键字搜索"""
        try:
            self.sample.h_keyword_search(**kwargs)
        except AssertionError as a:
            self.assertTrue("", a)

    def d_keyword(self, kwargs):
        """详情页关键字搜索"""
        try:
            self.sample.d_keyword_search(**kwargs)
        except AssertionError as a:
            self.assertTrue("", a)

# class CaseSample首页(FunctionSample):
#     for f in Get.out(Ioput.output("file"), "time"):
#         exec("""
# def test_{0}(self):
#    Ioput.function_name(self.__class__.__name__)
#    self.首页_table({1})
#                """.format(f.get("casename"), f)
#              )
#
# class CaseSample详情(FunctionSample):
#     for f in Get.out(Ioput.output("file"), "detail"):
#         exec("""
# def test_{0}(self):
#     Ioput.function_name(self.__class__.__name__)
#     self.详情_table({1})
#             """.format(f.get("casename"), f)
#              )



if __name__ == "__main__":
        pass