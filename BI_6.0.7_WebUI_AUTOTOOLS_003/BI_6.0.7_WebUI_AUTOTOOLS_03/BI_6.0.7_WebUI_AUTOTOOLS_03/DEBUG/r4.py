import xlwt

from DEBUG.r5 import parserxlsx
from config.conf import backage

d="日报"
w="周报"
m="月报"
y="年报"
o="导出数据"
z="曲线图"
t="表格数据"
s="关键字搜索"
u=["用户分析",]

two={
    "用户分析111":{
        "收视概况":[[d,w,y],["首页",],[o,t,"收视时长分布","收视次数分布"]],
        "收视概况C3":[[d,w,y],["首页",],[o,t,"收视时长分布","收视次数分布"]],
        "用户画像":[[""],["首页"],[o,t,s]],  #["用户信息","用户流水","用户消费"],
        "用户明细C3":[["首页",],["-"],[s,t,]],
        "特殊统计C3": [[d, w, m],["首页", ],["频道厂商详情列表","订购详情列表","订购详情列表","活跃用户详情列表"],  [o, t,z ,s]],
        "版本统计":[[d,w,y,m],["首页"],[o,t,]], #["详情页"],
        "用户发展":[[d,w,m],["首页"],[o,z,t]],
        "用户发展C3":[[d,w,m],["首页"],[o,z,t]],
        "用户收视":[[d,w,m],["首页"],[o,z,t]],
        "用户收视C3":[[d,w,m],["首页"],[o,z,t]],
        "用户活跃":[[d,w,m],["首页"],[o,z,t]],
        "用户活跃C3":[[d,w,m],["首页"],[o,z,t]],
        "机顶盒收视":[[""],["首页"],[o,t,z,s]],
        "用户统计":[[d,w,m],["首页"],["全网用户数据","UIOS用户数据","C3用户数据"],[o,z,t]],

        "实时数据":[["活跃用户数","当前在线用户","开机率","24小时最高在线用户","在线用户","全网在线用户类型分布",]],
    },
    "用户分析222": {
        "用户画像": [["详情页"], ["用户信息","用户流水","用户消费"], [o, t, s]],
        "版本统计": [[d, w, y, m], ["详情页"], [o, t, ]],  #
        "用户发展": [[d, w, m], ["详页情"],["区域分布","用户类型"], [o, z, t]],
        "用户发展3": [[d, w, m], ["详页情"],["区域分布","用户类型"], [o, z, t]],
        "用户收视": [[d, w, m], ["详情页"],["时段数据","区域分布","用户类型"], [o, z, t]],
        "用户收视C3": [[d, w, m], ["详情页"],["时段数据","区域分布","用户类型"], [o, z, t]],
        "用户活跃C3": [[d, w, m], ["详情页"],["时段数据","区域分布","用户类型"], [o, z, t]],
        "用户活跃": [[d, w, m], ["详情页"],["时段数据","区域分布","用户类型"], [o, z, t]],
        "用户统计": [[d, w, m],  ["全网用户数据", "UIOS用户数据", "C3用户数据"],["详情页"],["区域分布","用户类型"], [o, z, t]],
    },

    "频道分析111":{
        "直播频道":[[d,w,m],["全网频道","高清频道","CCTV频道","BTV频道","卫视频道","体验频道","精品节目","测试频道","少儿频道",],["首页"],[t,s,o,z]],
        "直播频道C3": [ [d, w, m],["全网频道", "高清频道", "CCTV频道", "BTV频道", "卫视频道", "体验频道", "精品节目", "测试频道", "少儿频道", ], ["首页"],
                 [t, s, o, z]],
        "回看频道": [ [d, w, m],["全网频道", "高清频道", "CCTV频道", "BTV频道", "卫视频道", "体验频道", "精品节目", "测试频道", "少儿频道", ], ["首页"],
                 [t, s, o, z]],
        "回看频道C3": [ [d, w, m],["全网频道", "高清频道", "CCTV频道", "BTV频道", "卫视频道", "体验频道", "精品节目", "测试频道", "少儿频道", ], ["首页"],
                   [t, s, o, z]],
        "直播节目": [[d, w, m],["首页"],  [t, s, o, z]],
        "直播节目C3": [[d, w, m],["首页"],  [t, s, o, z]],
        "回看节目": [[d, w, m],["首页"],  [t, s, o, z]],
        "回看节目C3": [[d, w, m],["首页"],  [t, s, o, z]],
        "时移频道":[[d,w,m],["全网频道","高清频道","CCTV频道","BTV频道","卫视频道","体验频道","精品节目","测试频道","少儿频道",],["首页"],[t,s,o,z]],
        "分钟收视": [["首页"], [""], [t, s, o, z]],
        "分钟收视": [["首页"], [""], [t, s, o, z]],
        "实时数据":[["频道总览"],["频道在线用户","直播在线用户","回看在线用户","时移在线用户","频道实时在线曲线图","回看实时在线曲线图","频道分组在线用户","频道收视类型分布"
                          ,"在线用户区域排名","在线用户性别分布","在线用户年龄分布"]],
        "实时数据111":[["全网频道", "高清频道", "CCTV频道", "BTV频道", "卫视频道", "体验频道", "精品节目", "测试频道", "少儿频道", ],["实时频道TOP20",t,o,s]],
        "实时数据222": [["全网频道", "高清频道", "CCTV频道", "BTV频道", "卫视频道", "体验频道", "精品节目", "测试频道", "少儿频道", ],["实时频道详情页"],["时段收视"],
                    [ t, z]]
    },
    "频道分析222": {
        "直播频道": [ [d, w, m],["全网频道", "高清频道", "CCTV频道", "BTV频道", "卫视频道", "体验频道", "精品节目", "测试频道", "少儿频道", ], ["详情页"],
                      ["时段对比","节目收视","时段收视","区域分布",]  ,[t, o, z],],
        "直播频道C3": [ [d, w, m],["全网频道", "高清频道", "CCTV频道", "BTV频道", "卫视频道", "体验频道", "精品节目", "测试频道", "少儿频道", ],["详情页"],
                    ["时段对比", "节目收视", "时段收视", "区域分布", ], [t, s, o, z]],
        "回看频道": [ [d, w, m],["全网频道", "高清频道", "CCTV频道", "BTV频道", "卫视频道", "体验频道", "精品节目", "测试频道", "少儿频道", ], ["详情页"],
                  [ "节目收视", "时段收视", "区域分布", ],     [t, s, o, z]],
        "回看频道C3": [ [d, w, m],["全网频道", "高清频道", "CCTV频道", "BTV频道", "卫视频道", "体验频道", "精品节目", "测试频道", "少儿频道", ] ,["详情页"],
                    ["节目收视", "时段收视", "区域分布", ],[t, s, o, z]],
        "分钟收视": [[""], [t, s, o, z],["首页"], ["时段收视"]],
        "分钟收视": [[""], [t, s, o, z], ["时段收视"]],
    },

    "点播分析222":{
        "栏目分析":[ [d, w, m],["详情页"],["时段数据","子级栏目","节目收视","区域分布",] , [t, s, o, z]],
        "内容标签": [[d, w, m],["提供商","导演","演员","年份"],["详情页"],["时段数据","节目收视","区域分布",], [t, s, o, z]],
        "节目信息":[ [d, w, m],["详情页"],["时段收视","子节目收视","路径分析","区域分布",], [t, s, o, z,]],
        "媒资数据": [ [d, w, m],["底量", "增加量", "删除量", ],["详情页"],["单剧集","连续剧","提供商"] ,[t, s, o, z]],
        "栏目分析C3":[ [d, w, m],["详情页"],["时段数据","子级栏目","节目收视","区域分布",] , [t, s, o, z]],
        "节目信息C3":[ [d, w, m],["详情页"],["时段收视","子节目收视","路径分析","区域分布",], [t, s, o, z,]],
    },
    "点播分析111":{
        "栏目分析":[ [d, w, m],["首页"], [t, s, o, z]],
        "内容标签": [[d, w, m],["提供商","导演","演员","年份"],["首页"], [t, s, o, z]],
        "节目信息":[ [d, w, m],["首页"], [t, s, o, z,"导出冷播节目"]],
        "媒资数据": [ [d, w, m],["底量", "增加量", "删除量", ],["首页"], [t, s, o, z]],
        "栏目分析C3": [ [d, w, m],["首页"], [t, s, o, z]],
        "节目信息C3":[ [d, w, m],["首页"], [t, s, o, z,"导出冷播节目"]],
        "实时数据":[["点播总览"],[z,"栏目TO5","提供商TO5","导演TO5","演员TO5","年份TO5",]],
        "实时数据222":[["栏目","提供商","导演","演员","年份",],["TOP20",t,s,o]],
        "实时数据333":[["提供商","导演","演员","年份",],["详情页"],["时段收视","节目收视","区域收视"],[t,z,o],],
        "实时数据333":[["栏目",],["详情页"],["时段收视","二级栏目","节目收视","区域收视"],[t,z,o],]
    },


    "EPG分析111":{
        "高清实时数据":[ ["首页"], [t, s, o,"页面数据UV" ]],
        "智能实时数据": [["首页"], [t, s, o, "页面数据UV"]],
        "标清实时数据": [["首页"], [t, s, o, "页面数据UV"]],
        "高清EPG": [[d, w, m],["首页"], [t, s, o, "页面数据UV"]],
        "智能EPG": [[d, w, m],["首页"], [t, s, o, "页面数据UV"]],
        "标清EPG": [[d, w, m],["首页"], [t, s, o, "页面数据UV"]],
    },

    "EPG分析222": {
        "高清EPG": [[d, w, m], ["详情页"],["时段收视","节目收视","区域分布","类型分布"], [t, z, o, ]],
        "智能EPG": [[d, w, m], ["详情页"],["时段收视","节目收视","区域分布","类型分布"], [t, z, o, ]],
        "标清EPG": [[d, w, m], ["详情页"], ["时段收视","节目收视","区域分布","类型分布"],[t, z, o, ]],
    },
}










def out(listdata=two):
    alllist=[]
    for x  in listdata :   # x:用户分析
        print(x)
        for y in two[x]:     #y:收视概况
            print(y)
            list_all = two[x][y]   #z:list
            temp = list_all[0]
            for i in list_all[1:]:
                cache = []
                for xu in i:
                    for lu in temp:
                        cache.append("%s_%s" % (lu, xu))
                temp = cache
            temp=["%s_%s_%s" % (x,y,gg)  for gg in temp]
            # print(len(temp), temp)

            # alllist = alllist+copy.deepcopy(temp)
            alllist = alllist + temp
    k=[h.replace("111","").replace("222","").replace("333","") for h in alllist]
    k.sort()
    return k


m=out()
m2=[ [i.split("_")[0],i.split("_")[1],i] for i in m]

m2=[]
allc=["",0]
onec=["",0]
twoc=["",0]
# m=x+m
# print(m)
for i in m:
    r=i.split("_")
    allc[1] += 1

    onec[1] +=1
    twoc[1] +=1

    if r[0] !=onec[0]:
        onec[1] =1
        onec[0] = r[0]
    if r[1] !=twoc[0]:
        twoc[1] =1
        twoc[0] = r[1]

    caseid=" {:0>4d} ".format(allc[1])
    oneid=" {:0>4d} ".format(onec[1])
    twoid = " {:0>4d} ".format(twoc[1])
    m2.append([caseid, r[0],r[1] ,"验证：%s" % i])
m2.insert(0,["用例编号","一级页面","二级页面","用例标题"])

x=parserxlsx(r"D:\case.xlsx")
m2=m2+x
for i in m2:
    print(i)


def write(input=m2,outxlsx_path="aaa3.xls"):

    workbook = xlwt.Workbook()  # Create workbook
    worksheet = workbook.add_sheet('My sheet')

    pattern_yellow = xlwt.Pattern()  # Create the pattern
    pattern_yellow.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
    pattern_yellow.pattern_fore_colour = 5  # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...
    style_yellow = xlwt.XFStyle()  # Create the pattern
    style_yellow.pattern = pattern_yellow  # Add pattern to style

    pattern_green = xlwt.Pattern()
    pattern_green.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern_green.pattern_fore_colour = 3
    style_Green = xlwt.XFStyle()  # Create the pattern
    style_Green.pattern = pattern_green  # Add pattern to style

    pattern_red = xlwt.Pattern()
    pattern_red.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern_red.pattern_fore_colour = 2
    style_Red = xlwt.XFStyle()  # Create the pattern
    style_Red.pattern = pattern_red  # Add pattern to style

    clor={"Pass":style_Green,"Fail":style_Red,"Error":style_yellow}

    datas=input

    row_count = len(datas)
    for row in range(0, row_count):
        col_count = len(datas[row])
        for col in range(0, col_count):
                worksheet.write(row, col, datas[row][col],)


    # worksheet.write(2, 5, 'Cell contents', style_Red)
    r'D:\Script\BI6.0.6_BI_PORTAL_003_version_6_综合\report\测试告.xls'
    outxlsx_path = r"D:\\%s" %(outxlsx_path)
    workbook.save(outxlsx_path)

write()
