from config.conf import BI_protal as bi

class BaseData:
    class Tabletype:
        """详情 日报、 周报、 月报"""
        test_day = {"tt": "day", "casename": "日报"}
        test_week = {"tt": "week", "casename": "周报"}
        test_month = {"tt": "month", "casename": "月报"}

    class Time:
        """首页 日报、 周报、 月报"""
        test_day = {"starttime": bi.starttime, "endtime": bi.endtime, "timetype": "day", "casename": "日报"}
        test_week = {"starttime": bi.weekstarttime, "endtime": bi.weekendtime, "timetype": "week", "casename": "周报"}
        test_month = {"starttime": bi.month_starttime, "endtime": bi.month_endtime, "timetype": "month", "casename": "月报"}

    class Usertype:
        test1 = {"user_index": "1"}
        test2 = {"user_index": "2"}
        test3 = {"user_index": "3"}
        test4 = {"user_index": "4"}
        test5 = {"user_index": "5"}
        test6 = {"user_index": "6"}
        test7 = {"user_index": "7"}
        test8 = {"user_index": "8"}



    class Datetime:
        test1 = {"time_index": "1"}
        test2 = {"time_index": "2"}

class Public:
    """通用基本"""
    class Home:
        class Homepage(BaseData):
            class Detail:
                test1 = {"buttontext": "开机率"}
                test2 = {"buttontext": "在线用户数"}
                test3 = {"buttontext": "全网用户数"}
                test4 = {"buttontext": "曲线图"}

    class User:
        """一级菜单  用户分析"""
        class Useractive(BaseData):
            """用户分析 -- 用户活跃"""
            class Detail:
                test1 = {"buttontext": "时段数据", "casename": "时段数据"}
                test2 = {"buttontext": "区域分布", "casename": "区域分布"}
                test3 = {"buttontext": "用户类型", "casename": "用户类型"}

        class Userdevelop(BaseData):
            """
             用户分析 --  用法发展
            """
            class Detail:
                test1 = {"buttontext": "区域分布", "casename": "区域分布"}
                test2 = {"buttontext": "用户类型", "casename": "用户类型"}

        class Usernowtime(BaseData):
            """用户分析 -- 用户实时数据"""

            class Other:
                test1 = {"buttontext": "全网用户"}
                test2 = {"buttontext": "当前在线用户"}
                test3 = {"buttontext": "开机率"}
                test4 = {"buttontext": "24小时内最高在线用户数"}
                test5 = {"buttontext": "在线用户使用功能"}
                test6 = {"buttontext": "在线用户类型分布"}

        class Userview(BaseData):
            """用户分析 -- 用户收视"""

            class Detail:
                test1 = {"buttontext": "区域分布", "casename": "区域分布"}
                test2 = {"buttontext": "用户类型", "casename": "用户类型"}
                test3 = {"buttontext": "时段数据", "casename": "时段数据"}

        class Usercount(BaseData):
            """
             用户分析 --  用户统计
            """
            class Usertypedata:
                test1 = {"buttontext": "全网用户数据", }
                test2 = {"buttontext": "UIOS用户数据",}
                test3 = {"buttontext": "C3用户数据", }

            class Detail:
                test1 = {"buttontextdetail": "区域分布", "casename": "区域分布"}
                test2 = {"buttontextdetail": "用户类型", "casename": "用户类型"}

        class UserSurvey(BaseData):
            """用户收视概况"""
            class Tabletype():
                test_year = {"tt": "year", "casename": "年报"}
                test_week = {"tt": "week", "casename": "周报"}
                test_month = {"tt": "month", "casename": "月报"}

            class Time:
                """首页 日报、 周报、 月报"""
                test_year = {"starttime": bi.year_starttime, "endtime": bi.year_endtime, "timetype": "year", "casename": "年报"}
                test_week = getattr(BaseData.Time, "test_week", {"starttime": bi.month_starttime, "endtime": bi.month_endtime, "timetype": "month", "casename": "月报"})
                test_month = getattr(BaseData.Time, "test_month", {"starttime": bi.weekstarttime, "endtime": bi.weekendtime, "timetype": "week", "casename": "周报"})

            class Viewtable:
                test1 = {"buttontext":"收视时长分布"}
                test2 = {"buttontext": "收视次数分布"}
                test3 = {"buttontext": "详情数据表"}

        class VersionCount(BaseData):
            """版本统计"""
            class Tabletype(BaseData.Tabletype):
                """详情 日报、 周报、 月报"""
                test_year = {"tt": "year", "casename": "年报"}

            class Time(BaseData.Time):
                """首页 日报、 周报、 月报"""
                test_year = {"starttime": bi.year_starttime, "endtime": bi.year_endtime, "timetype": "year", "casename": "年报"}

            class Detail:
                test1 = {"buttontext": "详情页", "casename": "详情页"}

        class SpecialCount(BaseData):
            """特殊统计C3"""
            class Usertypedata:
                test1 = {"buttontext": "频道厂商详情列表", }
                test2 = {"buttontext": "订购详情列表", }
                test3 = {"buttontext": "支付详情列表", }
                test4 = {"buttontext": "活跃用户详情列表", }
                test5 = {"buttontext": "用户统计列表", }

    class Channel:
        """
        频道分析
        """
        class Channellive(BaseData):
            """
            直播分析  --
                        直播频道，回看频道，时移频道"""

            class Channel:
                test1 = {"list_page": "全网频道", "groupcode":None}
                test2 = {"list_page": "高清频道", "groupcode":"1"}
                test3 = {"list_page": "CCTV频道", "groupcode":"2"}
                test4 = {"list_page": "BTV频道", "groupcode":"3"}
                test5 = {"list_page": "卫视频道", "groupcode":"4"}
                test6 = {"list_page": "体验频道", "groupcode":"5"}
                test7 = {"list_page": "精品节目", "groupcode":"7"}
                test8 = {"list_page": "测试频道", "groupcode":"8"}
                test9 = {"list_page": "少儿频道", "groupcode":"9"}

            class Detail:
                test0 = {"buttontext": "时段对比", "casename": "时段对比"}
                test1 = {"buttontext": "时段收视", "casename": "时段收视"}
                test2 = {"buttontext": "区域分布", "casename": "区域分布"}
                test3 = {"buttontext": "节目收视", "casename": "节目收视"}

        class ChannelTstv(BaseData):

            class Channel:
                test1 = {"list_page": "全网频道", "groupcode": None}
                test2 = {"list_page": "高清频道", "groupcode": "1"}
                test3 = {"list_page": "CCTV频道", "groupcode": "2"}
                test4 = {"list_page": "BTV频道", "groupcode": "3"}
                test5 = {"list_page": "卫视频道", "groupcode": "4"}
                test6 = {"list_page": "体验频道", "groupcode": "5"}
                test7 = {"list_page": "精品节目", "groupcode": "7"}
                test8 = {"list_page": "测试频道", "groupcode": "8"}
                test9 = {"list_page": "少儿频道", "groupcode": "9"}

            class Detail:
                test1 = {"buttontext": "时段收视", "casename": "时段收视"}
                test2 = {"buttontext": "区域分布", "casename": "区域分布"}
                test3 = {"buttontext": "节目收视", "casename": "节目收视"}


        class Channelmin(BaseData):
            """
            频道分析
                分钟收视"""

            class Time:
                test_day = getattr(BaseData.Time, "test_day", {"starttime": bi.starttime, "endtime": bi.endtime, "timetype": "day", "casename": "日报"})

            class Tabletype:
                test_day = getattr(BaseData.Tabletype, "test_day", {"tt": "day", "casename": "日报"})

            class Detail:
                test1 = {"buttontext": "时段收视", "casename": "时段收视"}


        class Channelnowtime(BaseData):
            """
            频道分析
                频道实时数据"""

            class Other:
                test1 = {"buttontext": "频道在线用户"}
                test2 = {"buttontext": "直播在线用户"}
                test3 = {"buttontext": "回看在线用户"}
                test4 = {"buttontext": "时移在线用户"}
                test5 = {"buttontext": "频道实时在线人数曲线图"}
                test6 = {"buttontext": "回看实时在线人数曲线图"}
                test7 = {"buttontext": "频道分组在线用户"}
                test8 = {"buttontext": "频道收视类型分布"}

            class Channel:
                test1 = {"buttontext": "全网频道", "groupcode": None}
                test2 = {"buttontext": "高清频道", "groupcode": "1"}
                test3 = {"buttontext": "CCTV频道", "groupcode": "2"}
                test4 = {"buttontext": "BTV频道", "groupcode": "3"}
                test5 = {"buttontext": "卫视频道", "groupcode": "4"}
                test6 = {"buttontext": "体验频道", "groupcode": "5"}
                test7 = {"buttontext": "精品节目", "groupcode": "7"}
                test8 = {"buttontext": "测试频道", "groupcode": "8"}
                test9 = {"buttontext": "少儿频道", "groupcode": "9"}


            class Detail:
                test1 = {"buttontext": "时段收视"}

    class Order:
        """
        订购分析
        """
        class Orderall(BaseData):
            """订购总览"""

            class Tabletype(BaseData.Tabletype):
                test_year = {"tt": "year", "casename": "年"}

            class Time(BaseData.Time):
                test_year = {"starttime": bi.year_starttime, "endtime": bi.year_endtime, "timetype": "year", "casename": "年报"}


            class Other:

                test1 = {"buttontext": "详情数据"}
                test2 = {"buttontext": "订购次数"}
                test3 = {"buttontext": "订购金额"}
                test4 = {"buttontext": "订购冠军"}
                test5 = {"buttontext": "订购人数"}
                test6 = {"buttontext": "单片收入排行"}
                test7 = {"buttontext": "产品包收入排行"}
                test8 = {"buttontext": "CP收入排行"}
                test9 = {"buttontext": "区域收入排行"}

            class Detail:

                test1 = {"buttontext": "单片收入排行"}
                test2 = {"buttontext": "产品包收入排行"}
                test3 = {"buttontext": "CP收入排行"}
                test4 = {"buttontext": "区域收入排行"}

        class Ordercycle(BaseData):
            """订购分析
                    周期订购"""
            class Page:
                test1 = {"list_page": ["包月", "包年", "包季度", "包半年"], "casename": "全部"}
                # test2 = {"list_page": ["包月"], "casename": "包月"}
                # test3 = {"list_page": ["包年"], "casename": "包年"}
                # test4 = {"list_page": ["包季度"], "casename": "包季度"}
                # test5 = {"list_page": ["包半年"], "casename": "包半年"}
                # test6 = {"list_page": ["包月", "包年"], "casename": "包月包年"}
                # test7 = {"list_page": ["包季度", "包半年"], "casename": "包季度包半年"}

            class Detail:
                test1 = {"buttontext": "时段订购", "casename": "时段订购"}
                test2 = {"buttontext": "区域分布", "casename": "区域分布"}
                test3 = {"buttontext": "类型分布", "casename": "类型分布"}
                test4 = {"buttontext": "支付方式", "casename": "支付方式"}
                test5 = {"buttontext": "价格分析", "casename": "价格分析"}

        class Ordersingle(BaseData):

            """按次订购"""

            class Detail:
                test1 = {"buttontext": "时段订购", "casename": "时段订购"}
                test2 = {"buttontext": "区域分布", "casename": "区域分布"}
                test3 = {"buttontext": "类型分布", "casename": "类型分布"}
                test4 = {"buttontext": "单片订购", "casename": "单片订购"}
                test5 = {"buttontext": "支付方式", "casename": "支付方式"}
                test6 = {"buttontext": "价格分析", "casename": "价格分析"}


    class Vod:
        """点播分析"""
        class Vodcolumn(BaseData):

            """栏目分析"""

            class Detail:
                test1 = {"buttontext": "时段数据", "casename": "时段数据"}
                test2 = {"buttontext": "子级栏目", "casename": "子级栏目"}
                test3 = {"buttontext": "节目收视", "casename": "节目收视"}
                test4 = {"buttontext": "区域分布", "casename": "区域分布"}

        class Vodnowtime(BaseData):
            """实时数据"""

            class Other:
                test1 = {"buttontext": "点播在线用户"}
                test2 = {"buttontext": "曲线"}
                test3 = {"buttontext": "栏目TOP5"}
                test4 = {"buttontext": "提供商TOP5"}
                test5 = {"buttontext": "导演TOP5"}
                test6 = {"buttontext": "演员TOP5"}
                test7 = {"buttontext": "年份TOP5"}

            class Channel:
                test1 = {"buttontext": "栏目"}
                test2 = {"buttontext": "提供商"}
                test3 = {"buttontext": "导演"}
                test4 = {"buttontext": "演员"}
                test5 = {"buttontext": "年份"}

            class Detail:
                # test0 = {"buttontext0": "二级栏目"}
                test1 = {"buttontext0": "时段收视"}
                test2 = {"buttontext0": "节目收视"}
                test3 = {"buttontext0": "区域收视"}

        class Vodprogram(BaseData):
            """节目信息"""
            class Detail:
                test1 = {"buttontext": "时段收视", "casename": "时段收视"}
                test2 = {"buttontext": "子节目收视", "casename": "子节目收视"}
                test3 = {"buttontext": "路径分析", "casename": "路径分析"}
                test4 = {"buttontext": "区域分布", "casename": "区域分布"}

        class Vodtag(BaseData):
            """内容标签"""
            class Program:
                test1 = {"program": "提供商"}
                test2 = {"program": "导演"}
                test3 = {"program": "演员"}
                test4 = {"program": "年份"}

            class Detail:
                test1 = {"buttontext": "时段数据", "casename": "时段数据"}
                test2 = {"buttontext": "节目收视", "casename": "节目收视"}
                test3 = {"buttontext": "区域分布", "casename": "区域分布"}

        class Vodemedia(BaseData):
            """媒资数据"""
            class Other:
                test1 = {"buttontext": "底量", }
                test2 = {"buttontext": "增加量", }
                test3 = {"buttontext": "删除量", }

            class Detail:
                test1 = {"buttontext2": "单剧集", }
                test2 = {"buttontext2": "连续剧", }
                test3 = {"buttontext2": "提供商", }

    class Epg:
        """EPG分析"""
        class Epg智能(BaseData):

            class Column:
                test1 = {"list_page": "推荐"}
                test2 = {"list_page": "直播"}
                test3 = {"list_page": "电影"}
                test4 = {"list_page": "热剧"}
                test5 = {"list_page": "少儿"}
                test6 = {"list_page": "综艺"}
                test7 = {"list_page": "新闻"}
                test8 = {"list_page": "4K"}
                test9 = {"list_page": "爱学"}
                test10 = {"list_page": "爱玩"}
                test11 = {"list_page": "精选"}
                test12 = {"list_page": "广东"}
                test13 = {"list_page": "活动"}

            class Detail:
                test1 = {"buttontext": "时段收视", "casename": "时段收视"}
                test2 = {"buttontext": "节目收视", "casename": "节目收视"}
                test3 = {"buttontext": "区域分布", "casename": "区域分布"}
                test4 = {"buttontext": "类型分布", "casename": "类型分布"}

        class HDreal(BaseData):
            """高清实时数据"""

            class Column:
                test1 = {"list_page": "推荐", }
                test2 = {"list_page": "直播", }
                test3 = {"list_page": "电影", }
                test4 = {"list_page": "热剧", }
                test5 = {"list_page": "少儿", }
                test6 = {"list_page": "综艺", }
                test7 = {"list_page": "新闻", }
                test8 = {"list_page": "4K", }
                test9 = {"list_page": "爱学", }
                test10 = {"list_page": "爱玩", }
                test11 = {"list_page": "精选", }
                test12 = {"list_page": "广东", }
                test13 = {"list_page": "活动", }

    class CountData:
        """结算数据"""

        class CDdatil(BaseData):
            class Detail:
                test1 = {"buttontext": "全量明细", "casename": "全量明细"}
                test2 = {"buttontext": "更新量明细", "casename": "更新量明细"}
                test3 = {"buttontext": "热榜明细", "casename": "热榜明细"}
                test4 = {"buttontext": "订购指标", "casename": "订购指标"}

    class Title:
        class TitleParser(BaseData):
            pass

    class Business:
        """运营分析"""
        class ProgramOrder(BaseData):
            """节目订购"""

        class PeriodOrder(BaseData):
            """订购时段分析C3"""
            class Time(BaseData.Time):
                test_year = getattr(BaseData.Time, "test_year", {"starttime": bi.year_starttime, "endtime": bi.year_endtime, "timetype": "year", "casename": "年报"})

            class Tabletype(BaseData.Tabletype):
                test_year = getattr(BaseData.Tabletype, "test_year", {"tt": "year", "casename": "年报"})

            class Detail:
                test1=dict()

        class BusinessSurvey(BaseData):
            class Time:
                test_week = getattr(BaseData.Time, "test_week", {"starttime": bi.weekstarttime, "endtime": bi.weekendtime, "timetype": "week", "casename": "周报"})
                test_month = getattr(BaseData.Time, "test_month", {"starttime": bi.month_starttime, "endtime": bi.month_endtime, "timetype": "month", "casename": "月报"})
                test_year = getattr(BaseData.Time, "test_year", {"starttime": bi.year_starttime, "endtime": bi.year_endtime, "timetype": "year", "casename": "年报"})

class BeiJing(Public):
    class Epg(Public.Epg):
        """EPG分析"""

        class Epg智能(Public.Epg.Epg智能):

            class Column:
                test1 = {"list_page": "点播"}
                test2 = {"list_page": "精品"}
                test3 = {"list_page": "专题"}
                test4 = {"list_page": "首页"}
                test5 = {"list_page": "聚精彩"}

        class HDreal(Public.Epg.HDreal):
            """高清实时数据"""
            class Column:
                test1 = {"list_page": "点播"}
                test2 = {"list_page": "精品"}
                test3 = {"list_page": "专题"}
                test4 = {"list_page": "首页"}
                test5 = {"list_page": "聚精彩"}



class NanChuan(Public):
    pass

    class Order(Public.Order):
        """
        订购分析
        """
        class Order单点(BaseData):
            """订购分析
                    单点订购"""

            class Detail:
                test1 = {"buttontext": "时段订购", "casename": "时段订购"}
                test2 = {"buttontext": "区域分布", "casename": "区域分布"}
                test3 = {"buttontext": "类型分布", "casename": "类型分布"}
                test4 = {"buttontext": "单片订购", "casename": "单片订购"}
                test5 = {"buttontext": "支付方式", "casename": "支付方式"}

        class Order包年(BaseData):
            """订购分析
                    包年订购"""

            class Detail:
                test1 = {"buttontext": "时段订购", "casename": "时段订购"}
                test2 = {"buttontext": "区域分布", "casename": "区域分布"}
                test3 = {"buttontext": "类型分布", "casename": "类型分布"}
                test5 = {"buttontext": "支付方式", "casename": "支付方式"}

        class Order包月(BaseData):
            """按次订购"""
            class Detail:
                test1 = {"buttontext": "时段订购", "casename": "时段订购"}
                test2 = {"buttontext": "区域分布", "casename": "区域分布"}
                test3 = {"buttontext": "类型分布", "casename": "类型分布"}
                test5 = {"buttontext": "支付方式", "casename": "支付方式"}

    class Channel(Public.Channel):

        class Channellive(Public.Channel.Channellive):
            """
            直播分析  --
                        直播频道，回看频道，时移频道"""
            class Channel:
                test1 = {"list_page": "全网频道"}
                test2 = {"list_page": "广东省台"}
                test3 = {"list_page": "卫视频道"}
                test4 = {"list_page": "央视频道"}
                test5 = {"list_page": "地市频道"}
                test6 = {"list_page": "中数频道"}
                test7 = {"list_page": "轮播频道"}
                test8 = {"list_page": "标清"}
                test9 = {"list_page": "高清"}
                test10 = {"list_page": "超清"}
                test11 = {"list_page": "其他"}

        class Channelnowtime(Public.Channel.Channelnowtime):
            """
            频道分析
                频道实时数据"""

            class Channel:
                test0 = {"buttontext": "频道总览"}
                test1 = {"list_page": "全网频道"}
                test2 = {"list_page": "广东省台"}
                test3 = {"list_page": "卫视频道"}
                test4 = {"list_page": "央视频道"}
                test5 = {"list_page": "地市频道"}
                test6 = {"list_page": "中数频道"}
                test7 = {"list_page": "轮播频道"}
                test8 = {"list_page": "标清"}
                test9 = {"list_page": "高清"}
                test10 = {"list_page": "超清"}
                test11 = {"list_page": "其他"}

class All(NanChuan):
    pass





if __name__ == "__main__":

    c=eval("NanChuan")
    name=[n for n in dir(c) if not n.startswith("__")]
    path=[]
    for x in name:
        classname=eval("""{0}.{1}""" .format("NanChuan",x))
        classlist = [n for n in dir(classname) if not n.startswith("__")]
        for y in classlist:
            path.append("%s.%s.%s" %("NanChuan",x,y))

    print(path)
    path="#".join(path)
    import re
    x=re.compile(r"[^#]+%s"%("Channellive")).findall(path)[0]
    print(x)
    cn=eval("%s.%s" %(x,"Time"))
    # print(cn.__dict__)
    name3 = [n for n in dir(cn) if not n.startswith("__")]
    print(name3)
    print([eval("%s.%s" %("cn",v)) for v in name3])