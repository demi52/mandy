import json

from requests import ReadTimeout

__author__ = "luxu"
r"""flow\biportal\用户分析\change.py  进入用户分析"""

import os
import re
import time
import random
import requests
from lib.funcslib import log, parserxlsx, Ioput, exef, get_token
from config.conf import BI_protal as bt, LOG, BI_protal
from flow.biportal.script登陆 import Land
from lib.listen import ListenServerLog


class Base(Land):

    excute_status = dict()
    time_type = "day"
    down_text = {"by": "xpath", "value": '//span[text()="导出数据"]'}
    Times = {
        "day": {"starttime": bt.starttime, "endtime": bt.endtime, "datatype": "D"},
        "week": {"starttime": bt.weekstarttime, "endtime": bt.weekendtime, "datatype": "W"},
        "month": {"starttime": bt.month_starttime, "endtime": bt.month_endtime, "datatype": "M"},
        "year": {"starttime": bt.year_starttime, "endtime": bt.year_endtime, "datatype": "Y"},
            }
    url_api = r"%squery" % bt.remote_server_url
    secsiono = {"1": "t", "2": "m", "3": "u"}[bt.secsion]

    def _first(self, **kwargs):
        super()._first(**kwargs)
        self.f_land(**kwargs)

    @exef()
    def getsysereorlog(self, status):

        """
        获取服务端日志
        :param status:
        :return:
        """
        ListenServerLog().searchqdi(status=status, qdi=self.apiqdi)

    def checktext(self, num=1, element=""):
        """校验文本在页面是否存在"""
        log().debug("校验文本在页面是否存在")
        now = True
        for i in range(0, bt.wait_time+5):
            page = self.driver.page_source
            if element in page:
                now = False
                break
            time.sleep(1)
        if now:
            assert False, "\"{0}\" 不在当前页面".format(element)
        elif not now and num == 1:
            log().debug(" '%s' 在当前页，环境校验成功，next，" % element)

    def __before(self):
        pass

    def _before(self,**kwargs):
        """测试函数前环境不通过，重新准备一次环境"""
        if Ioput.output("pathstatus") == "exit":
            text = "setupClass 不通过，当前用例判为失败： {0}".format(Ioput.output("patherror"))
            log().critical(text)
            assert False, text
        log().debug("前置环境校验通过,next")
        try:
           self.checktext(1, element=getattr(self, "text", ""))
        except Exception as e:
            log().error(" %s 准备清空浏览器缓存，重置环境一次 ：%s" % (self.text, e))
            try:
                self._last()
            except:
                self._first()
            else:
                self._first()
            if "详情" in self.__class__.__name__ and getattr(self,"buttontext", None) != "子级栏目":
                self.pararms2(**kwargs)
                self.get_data_datil()



    def pararms(self, **kwargs):
        """设置参数"""
        log().debug("%s" % kwargs)
        self.timetype = kwargs.get("timetype", self.time_type)
        self.starttime = self.Times[self.timetype].get("starttime", bt.starttime)
        self.endtime = self.Times[self.timetype].get("endtime", bt.endtime)
        self.apidatatype = self.Times[self.timetype].get("datatype","D")
        self.user_index = kwargs.get("user_index", "1")

        self.table_id = kwargs.get("table_id", "userDevelopTable")
        self.dlfile = kwargs.get("dlfile", "用户发展数据.xlsx")
        self.apiqdi = kwargs.get("apiqdi", "queryOffLineUserDevelop")
        self.text = "实时数据"


    def frame_change(self, index=-1):
        """切换frame页"""
        log().debug("开始切换frame")
        self.driver.switch_to.frame(self.driver.find_elements_by_tag_name("iframe")[index])
        log().info("change to %s sucess " % "frame ")

    def _set_time_day(self):
        """日报"""
        log().debug("日报")
        try:
            self.exement("day", "id")
        except AssertionError as a:
            if "分钟收视" not in self.__class__.__name__ :
                raise  AssertionError(a)

        starttime = self.starttime
        endtime = self.endtime
        sy = starttime.split("-")[0]
        sm = str(int(starttime.split("-")[1]) - 1)
        ey = endtime.split("-")[0]
        em = str(int(endtime.split("-")[1]) - 1)
        self.exement("starttime","id")
        self.exement('//*[@class="layui-laydate"]//*[@lay-type="year"]')
        self.exement('//*[@class="layui-laydate"]//*[@lay-ym="%s"]' % sy)
        self.exement('//*[@class="layui-laydate"]//*[@lay-type="month"]')
        self.exement('//*[@class="layui-laydate"]//*[@lay-ym="%s"]' % sm)
        self.exement('//*[@class="layui-laydate"]//*[@lay-ymd="%s"]' % starttime)

        self.exement("endtime", "id")
        self.exement('//*[@class="layui-laydate"]//*[@lay-type="year"]')
        self.exement('//*[@class="layui-laydate"]//*[@lay-ym="%s"]' % ey)
        self.exement('//*[@class="layui-laydate"]//*[@lay-type="month"]')
        self.exement('//*[@class="layui-laydate"]//*[@lay-ym="%s"]' % em)
        self.exement('//*[@class="layui-laydate"]//*[@lay-ymd="%s"]' % endtime)

    def _excuteasert(self):
        #excute_status={"key":self.kws,"status":"None、pass、fail"}
        status=self.excute_status
        if not status or self.excute_status["key"] != self.kws:
            status = {"key": self.kws, "status": None}

        if status  and ( status.get("status",None) == None or status.get("key",None)):
           """初始未运行，准备运行"""

        elif "key" in status and status.get("status",None) == "pass":
            """初始运行成功，跳过"""

        elif "key" in status and status.get("status", None) == "fail":
             """初始运行失败，跳过，且终止后续操作"""

    def _set_time_week(self):
        """月报"""
        log().debug("周报")
        self.exement('//*[@id="week"]')
        self.exement('//*[@id="select2-starttime-container"]')
        self.exement('//*[@id="select2-starttime-results"]//li[text()="{0}"]'.format(self.starttime))

        self.exement('//*[@id="select2-endtime-container"]')
        self.exement('//*[@id="select2-endtime-results"]//li[text()="{0}"]'.format(self.endtime))

    def _set_time_month(self):
        log().debug("月报")
        self.exement('//*[@id="month" and @data-value="M"]')
        starttime = self.starttime
        endtime = self.endtime
        sy = starttime.split("-")[0]
        sm = str(int( starttime.split("-")[1]) - 1)
        ey = endtime.split("-")[0]
        em = str(int(endtime.split("-")[1]) - 1)
        self.exement("starttime", "id")
        self.exement('//*[@class="layui-laydate"]//*[@lay-type="year"]')
        self.exement('//*[@class="layui-laydate-content"]//*[@lay-ym="%s"]' % sy)
        self.exement('//*[@class="layui-laydate-content"]//*[@lay-ym="%s"]' % sm)
        self.exement('//*[@class="layui-laydate"]//span[text()="确定"]')

        self.exement("endtime", "id")
        self.exement('//*[@class="layui-laydate"]//*[@lay-type="year"]')
        self.exement('//*[@class="layui-laydate"]//*[@lay-ym="%s"]' % ey)
        self.exement('//*[@class="layui-laydate"]//*[@lay-ym="%s"]' % em)
        self.exement('//*[@class="layui-laydate"]//span[text()="确定"]')

    def _set_time_year(self):
        log().debug("年报")
        self.exement('//*[@data-value="Y"]')
        starttime = self.starttime
        endtime = self.endtime
        sy = starttime.split("-")[0]
        ey = endtime.split("-")[0]
        self.exement("starttime", "id")
        self.exement('//*[@class="layui-laydate-content"]//*[@lay-ym="%s"]' % sy)
        self.exement('//*[@class="layui-laydate"]//span[text()="确定"]')

        self.exement("endtime", "id")
        self.exement('//*[@class="layui-laydate"]//*[@lay-ym="%s"]' % ey)
        self.exement('//*[@class="layui-laydate"]//span[text()="确定"]')

    def search_time_type(self):
        """设置时间"""
        log().debug("开始点击时间")
        if self.timetype == "day":
            self._set_time_day()

        elif self.timetype == "week":
            self.starttime = self.starttime.split(":")[1]
            self.endtime = self.endtime.split(":")[1]
            self._set_time_week()

        elif self.timetype == "year":
            self._set_time_year()

        elif self.timetype == "month":
            self._set_time_month()
        log().info("set starttime  sucess,starttime=%s  endtime=%s" % (self.starttime, self.endtime))

    def _pull_down(self, spanid, ulid, index):
        """下拉框"""
        self.exement(spanid, "id")
        elem = '//ul[@id="%s"]/li[%s]' % (ulid, index)
        self.exement(elem)

    @exef()
    def change_user(self, pull_spanid="select2-userGroupSelect-container", pull_ulid="select2-userGroupSelect-results"):
        """切换用户"""
        log().debug("选择用户类型")
        self._pull_down(spanid=pull_spanid, ulid=pull_ulid, index=self.user_index)


    def click_channel(self):
        """点击频道，栏目等"""
        try:
            self.alltime=2
            self.wait_element("groupToggle", "id")
        except AssertionError as e:
            log().info("无下拉展开按钮")
        else:
            buteenttype = self.driver.find_element_by_xpath('//*[@id="%s"]/i' % "groupToggle").get_attribute("class")
            if buteenttype.endswith("down"):
                self.exement("groupToggle", "id")
        finally:
            self.alltime=BI_protal.wait_ele

        if "实时数据频道" in self.__class__.__name__:
            time.sleep(2)
        log().debug(self.channel)
        self.checktext(1, element=self.channel)
        self.exement('//*[@id="{1}"]//*[text()="{0}"]'.format(self.channel, self.groupid))


    def click_serach(self):
        """点击查询"""
        self.exement("searchButton", "id")
        if "内容标签" in self.__class__.__name__:
            time.sleep(0.001)
        log().info("click 查询 sucess")

    def outxlsx(self):
        """清理旧的xlsx文件，并下载新的xlsx"""
        log().debug("导出数据")
        rootdir = bt.downloadpath
        files = "\n" + "\n".join(os.listdir(rootdir)) + "\n"
        fileheader = os.path.splitext(self.dlfile)[0]
        needfile=re.compile(r"(?<=\n)%s.*?\.xlsx(?=\n)" % fileheader).findall(files)
        #删除已经存在的
        [os.remove(r"%s\%s" % (rootdir, file)) for file in needfile]
        log().debug("clean old file  sucess  old file is '%s'" % needfile)
        #下载
        Daochu=self.driver.find_elements_by_xpath('//span[text()="导出数据"]')

        count_daochu=len(list(iter(Daochu)))
        if count_daochu == 1:
            self.exement('//span[text()="导出数据"]')
        elif count_daochu > 1:
            self.exement('//*[@id="%s%s"]/span[text()="导出数据"]' % (self.table_id, "DaoChu"))

    def getxlsxcontent(self,  timeout=20):
        """解析xlsx"""
        log().debug("解析XLSX")
        dlfile = self.dlfile
        absfile = r"%s\%s" % (bt.downloadpath, dlfile)
        starttime = time.time()
        while True:
            """等待文件下载"""
            if os.path.exists(absfile):
                log().info("download %s   ---  sucess " % (dlfile))
                self.xlsxcontent = parserxlsx(absfile)
                log().info("{1} content is \n {0}".format(self.xlsxcontent[0:20], self.dlfile))
                break
            elif time.time() - starttime >= timeout:
                    raise AssertionError("download %s fail not found in  %s" % (dlfile, absfile))
            time.sleep(1)

    @exef(LOG.screenhost)
    def move_detaildata(self):
        """上下移动，截屏"""
        log().debug("滚动到屏幕顶部")
        """滚动到屏幕底部获取详情数据，并截屏"""
        scroll_top_js = "window.scrollTo(0,0);"  #顶端
        scroll_end_js = "window.scrollTo(0,document.body.scrollHeight);" #底部
        scroll_view_js = "arguments[0].scrollIntoView();" #指定元素
        time.sleep(0.2)
        ele_top = ""
        classname = self.__class__.__name__
        if hasattr(self, "text") and self.text == "查询":
            ele_top = self.driver.find_elements_by_id("searchButton")
        elif hasattr(self, "p") and self.p == "groupToggle":
            ele_top = self.driver.find_elements_by_id("groupToggle")
        elif hasattr(self, "up_text"):
            ele_top = self.driver.find_elements(**self.up_text)
        elif "详情" in classname:
            try:
                ele_top = self.driver.find_elements_by_id("nameTitle")
            except:
                ele_top = self.driver.find_elements_by_id("select2-changetime-container")
        if ele_top:
            self.driver.execute_script(scroll_view_js, ele_top[0])  # 移动到 顶端
        name = os.path.splitext(self.dlfile)[0]+"表"
        self.screenhost_to_report(alt=name+"header", name=name+"header")

        log().debug("滚动到屏幕底部")
        eledown = self.driver.find_elements(**self.down_text)
        if eledown:
            self.driver.execute_script(scroll_view_js, eledown[0])  #移动到指定元素 底部

    def _get_tabledata(self, tablenum="1", getlines=3):
        """获取表数所有据"""
        alldata = []
        lines = 0
        getphoto=True
        name = os.path.splitext(self.dlfile)[0] + "表"
        for ele in self.ele_tables:
            """轮询多张表"""
            classname = ele.get_attribute("class")
            if classname in ["table-left", "table-middle"]:
                ele_tr_string = '//*[@id="%s"]/div[@class="%s"]//table[%s]//tr' % (self.table_id, classname, tablenum)
                if getphoto:
                    self.screenhost_to_report(alt=name + "data", name=name + "data")
                    getphoto = False
                eletrs_0 = '%s[1]' % ele_tr_string
                log().debug(eletrs_0)

                try:
                    self.wait_element(eletrs_0, "xpath")
                except AssertionError as ae:
                    log().error(" {0} 无数据，终止后续操作".format(self.table_id))
                    self.getsysereorlog("end")
                    raise AssertionError(" {1},{0} 无数据，终止后续操作".format(self.table_id, ae))
                else:
                    ele_trs = self.driver.find_elements_by_xpath(ele_tr_string)
                    # 数据总行数
                    lines = len(list(iter(ele_trs)))
                    linedata = []
                    lastline = 1
                    for i in range(1, lines+1):
                        tds_element_text = '%s[%s]/td' % (ele_tr_string, i)
                        tds_element_text_num1 = '%s[%s]/td[1]' % (ele_tr_string, i)
                        self.wait_element(tds_element_text_num1, "xpath")
                        tds = self.driver.find_elements_by_xpath(tds_element_text)
                        texts = []
                        for m in tds:
                            text_number = 0
                            while True:
                                try:
                                    texts.append(m.text)
                                except:
                                    time.sleep(0.1)
                                    text_number += 1
                                    if text_number >= 50:
                                        raise TimeoutError("表格元素的文本加载超时,未加载")
                                else:
                                    break
                        linedata.append(texts)
                        lastline += 1
                        if lastline >= getlines:
                            break
                    alldata.append(linedata)

         #多表数据整合
        outdata = []
        for i in alldata[0]:
            n = []
            for y in alldata:
                n += y[alldata[0].index(i)]
            del n[0]
            outdata.append(n)
        self.web_alldatt=outdata
        return lines, outdata

    def get_tablehead(self):

        """获取详情数据的表头"""
        self.head_lines, self.table_head_list = self._get_tabledata("1")
        log().info("tables head  is  %s" % self.table_head_list)

    def get_tablefirstdata(self):
        """获取详情数据的第一行"""
        log().debug(self.table_id)
        self.wait_element(self.table_id, "id")
        self.ele_Table = self.exement(self.table_id, "id", "getele")  #self.driver.find_element_by_id(self.table_id)
        self.ele_tables = self.ele_Table.find_elements_by_xpath('//div[starts-with(@class,"table-")]')
        self.data_lines, self.table_firstline_list = self._get_tabledata("2")
        log().info("table content is  %s" % self.table_firstline_list)

    def look(self):
        """点击第一条的查看，切入详情页"""
        log().debug("点击‘查看’，进入详情页")
        """点击查看，并切换到frame"""
        try:
            self.ele_Table.find_elements_by_xpath('//a[text()="查看"]')[0].click()
        except:
            log().error("详情数据表中，无数据")
            raise AssertionError("无数据")
        self.driver.switch_to.parent_frame()
        self.frame_change(-1)

    def click_type(self):
        log().debug("详情页点击类型按钮")
        """点击查看的类型"""
        self.exement('//*[@id="navigationChange"]//a[text()="{0}"]'.format(self.buttontext))

    @exef()
    def change_time(self, pull_spanid="select2-changetime-container", pull_ulid="select2-changetime-results"):
        log().debug("下拉框选择时间")
        """下拉框中选择时间"""
        self._pull_down( spanid=pull_spanid, ulid=pull_ulid, index=self.time_index)

    def keyword_search(self, ):
        """关键字搜索"""
        data = self.table_firstline_list
        name1 = [i[0] for i in data]

        number = 0
        while True:
            """随机关键字"""
            randomnamepice = random.choice(name1)
            sindex = random.randint(0, len(randomnamepice))
            eindex = random.randint(0, len(randomnamepice))
            if sindex < eindex:
                keyword = randomnamepice[sindex:eindex]
                break
            elif number >= 100:
                """100次不合法 置空"""
                keyword = ""
                break
            number += 1

        log().debug("keyword is {0}".format(keyword))
        kw_ele_id = "%sSearch" % self.table_id
        self.exement(elements=kw_ele_id, ele_type="id", parms=keyword)
        data = self._get_tabledata(tablenum="2", getlines=20)[1]
        log().debug("after search keywords {0}".format(data))
        self.screenhost_to_report(alt="关键字搜索", name="关键字搜索")
        for i in data:
            if keyword not in i[0]:
                raise AssertionError("关键字 : \"%s\" %s 在查询的结果中不存在" % (keyword, i))

    def h_keyword_search(self, **kwargs):
        """首页关键字搜索"""
        self.f_search(**kwargs)
        self.keyword_search()

    def d_keyword_search(self, **kwargs):
        """详情页关键字搜索 """
        self.f2_search(**kwargs)
        self.keyword_search()

    def request_time(self):
        """首页请求时间"""
        stime_list = re.compile(r"[-:/]").split(self.starttime)[0:3]
        etime_list = re.compile(r"[-:/]").split(self.endtime)[0:3]
        stime_list = [int(i) for i in stime_list]
        etime_list = [int(i) for i in etime_list]

        if self.apidatatype in ("D", "W"):
            start_time = "{0}{1:0>2d}{2:0>2d}".format(*stime_list)
            end_time = "{0}{1:0>2d}{2:0>2d}".format(*etime_list)

        elif self.apidatatype == "M":
            start_time = "{0}{1:0>2d}01".format(*stime_list)
            end_time = "{0}{1:0>2d}01".format(*etime_list)

        elif self.apidatatype == "Y":
            start_time = "{0}0101".format(*stime_list)
            end_time = "{0}0101".format(*etime_list)

        self.start_time=start_time
        self.end_time=end_time

    def get_home_code(self):
        """ 获取code 供请求详情页使用"""
        code = [x["SUMDATE"] for x in self.datatext][0]
        self.request_code = code.replace("-", "")

    def request_data_home(self):
        """构造首页请求数据"""
        start_time = self.start_time
        end_time = self.end_time
        self.data = \
            {
                "qdi": self.apiqdi,
                "starttime": start_time,
                "begintime": start_time,
                'begindate': start_time,
                "endtime": end_time,
                "enddate": end_time,
                "datetype": self.apidatatype,
                "rootcategoryid": None,
                "groupcode": getattr(self, "groupcode", None),
                "hours": "00:00-00:59",
                "token": self.token,
                "tagid":None,
                "vspid":"1",
                "selectdate": getattr(self, "request_code", None),
                "channelcode":getattr(self, "request_code", None),
                "sysid": getattr(self,"secsiono","u"),
                "userid": "test1",
            }
        if  getattr(self, "movetype","") == "全网频道":
            self.data["groupcode"] = None
        log().debug("requests 'url, data' \t {1},{0}".format(self.data, self.url_api))

    def api_result(self):
        """发送请求并返回数据"""
        headr = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                 }
        try:
            res = requests.post(self.url_api, data=self.data, headers=headr, timeout=bt.wait_ele-4)
            text = eval(res.text)
        except NameError:
            """str>>dict"""
            text = json.loads(res.text)
        except ReadTimeout as e:
            """Timeout"""
            self.e=e
            text = dict()
            self.datatext = list()
            log().error(e)
        self.datatext=text.get("subject", [])[0:2]

        log().info("result subject data is {1}\t ".format(text, self.datatext))
        if self.datatext:
            Ioput.input("datatext", self.datatext)
        else:
            raise AssertionError(r"statplatform5 output not data ,test stop \n[error :{0}] \n request data is: {1}".format(getattr(self, "e", None), self.data))

    @get_token
    def get_data_home(self):
        """请求首页数据"""
        self.request_time()
        self.request_data_home()
        self.api_result()
        self.get_home_code()


    def get_data_datil(self):

        self.request_data_home()
        self.api_result()


    def check_web_api(self):
        """验证前后端数据准确性"""
        if getattr(self, "datatext", None) and getattr(self, "web_alldatt", None):
            for num in range(0, min([len(self.datatext), len(self.web_alldatt)])):
                api_numdata=self.datatext[num]
                ui_numdata=self.web_alldatt[num]
                cache_api = { self.__washdata(i) for i in api_numdata.values() if self.__washdata(i)}
                cache_ui = { self.__washdata(i) for i in ui_numdata if self.__washdata(i)}
                if str(num+1) in cache_ui:
                    cache_ui.remove(str(num+1))
                # assert cache_ui.issubset(cache_api), r"页面数据与后台数据不同 ui={0}\t stapfrom={1}。。{2}".format(cache_ui, cache_api,num)
                    diff=cache_ui.difference(cache_api)
                    if len(diff)>=2:
                        raise AssertionError(r"页面数据与后台数据不同 ui={0}\t stapfrom={1}。。{2}".format(cache_ui, cache_api,num))

    def __washdata(self, s):
        s = str(s).strip()
        if s.endswith("%"):
            """百分数转换"""
            res = re.compile(r"\d+\.\d+(?=%)").findall(s)
            if res:
                result = str(int(float(res[0]) / 100))
            else:
                result = str()
        elif "." in s:
            try:
                result = str(int(float(s)))
            except:
                result = ""
        elif "," in s:
            result = s.replace(",", "")
        elif s == "查看" or s == "-":
            result = ""
        elif s.startswith("+"):
            result = s.replace("+", "")
        else:
            result = s

        result = re.compile("\s+").sub(" ", result)
        return result


    def dict_update(self, dictobject, key, value):
        """key存在则更新,不存在在，不做操作"""
        if isinstance(dictobject, dict) and key in dictobject:
            dictobject[key] = value
        return dictobject




class Base实时数据():

    def order_count(self):
        """订购总览 饼图统计"""
        patten='//*[@id="%s"]/div' % self.table_id
        self.wait_element('%s[1]' % patten)
        ele_table = self.driver.find_elements_by_xpath(patten)
        log().debug("{1}  {0} content == {2}".format(self.table_id, patten, ele_table))
        name = self.buttontext
        self.screenhost_to_report(alt=name, name=name)
        if not ele_table:
            log().error("表 {0} 无数据 end".format(self.table_id))
            self.getsysereorlog("end")
            raise AssertionError("表 {0} 无数据 end".format(self.table_id))
        alldata=[]
        for i in ele_table:
            patten2 = '{0}[{1}]'.format(patten,ele_table.index(i)+1)
            log().debug(patten2)
            text=[]
            text1=self.driver.find_element_by_xpath('{0}/p[1]'.format(patten2)).text
            """切除中文"""
            text.append(re.compile(r'[\u4e00-\u9fa5]+').sub("",text1))
            log().debug('{0}/p[1]\t{1}'.format(patten2,self.driver.find_element_by_xpath('{0}/p[1]'.format(patten2)).text))
            text2=self.driver.find_element_by_xpath('{0}/p[2]'.format(patten2)).text
            """保留中文"""
            text += re.compile(r'[\u4e00-\u9fa5]+').findall(text2)
            log().debug('{0}/p[2]\t{1}'.format(patten2,self.driver.find_element_by_xpath('{0}/p[2]'.format(patten2)).text))
            text.append(self.driver.find_element_by_xpath('{0}/p[2]/label'.format(patten2)).text)
            log().debug('{0}/p[2]/label\t{1}'.format(patten2,self.driver.find_element_by_xpath('{0}/p[2]/label'.format(patten2)).text))
            alldata.append(text)
        self.web_alldatt = alldata
        log().info("{0} content \n {1}".format(self.table_id, alldata))
        return alldata

    def order_sort(self):
        """订购总览4排行"""
        patten = '//*[@id="%s"]/tr' % self.table_id
        self.wait_element('%s[1]' % patten)
        eletrs_table = self.driver.find_elements_by_xpath(patten)
        log().debug("{1}  {0} content == {2}".format(self.table_id, patten, eletrs_table))
        name = self.buttontext
        self.screenhost_to_report(alt=name, name=name)
        if not eletrs_table:
            log().error("表 {0} 无数据 end".format(self.table_id))
            self.getsysereorlog("end")
            raise AssertionError("表 {0} 无数据 end".format(self.table_id))
        tr_text = []
        for tr in range(len(eletrs_table)):
            patten_tr='{0}[{1}]/td'.format(patten,tr+1)
            eletds_table = self.driver.find_elements_by_xpath(patten_tr)
            td_text=[]
            for td in range(len(eletds_table)):
                patten_td = '{0}[{1}]'.format(patten_tr, td + 1)
                log().debug(("tds", patten_td))
                td_text.append(self.driver.find_element_by_xpath(patten_td).text)
            tr_text.append(td_text)
        self.web_alldatt = tr_text
        log().info("{0} content \n {1}".format(self.table_id, tr_text))
        return tr_text

    def order_mvp(self):
        """订购总览，订购冠军"""
        patten = '//*[@id="%s"]//tbody/tr' % self.table_id
        self.wait_element('%s[1]' % patten)
        eletrs_table = self.driver.find_elements_by_xpath(patten)
        log().debug("{1}  {0} content == {2}".format(self.table_id, patten, eletrs_table))
        name = self.buttontext
        self.screenhost_to_report(alt=name, name=name)
        if not eletrs_table:
            log().error("表 {0} 无数据 end".format(self.table_id))
            self.getsysereorlog("end")
            raise AssertionError("表 {0} 无数据 end".format(self.table_id))

        tr_text = []
        for tr in range(len(eletrs_table)):
            patten_tr='{0}[{1}]/td'.format(patten,tr+1)
            eletds_table = self.driver.find_elements_by_xpath(patten_tr)
            td_text=[]
            for td in range(len(eletds_table)):
                patten_td = '{0}[{1}]'.format(patten_tr, td + 1)
                log().debug(("tds", patten_td))
                text_0=self.driver.find_element_by_xpath(patten_td).text
                text_0=re.compile(r":|元\(金额\)|null").sub("",text_0)
                td_text.append(text_0)
            tr_text.append(td_text)
        self.web_alldatt = tr_text
        log().info("{0} content \n {1}".format(self.table_id, tr_text))
        return tr_text

    def order_top5(self):
        """top5"""
        patten='//*[@id="{0}"]/div[1]/canvas'.format(self.table_id)
        self.wait_element('%s[1]' % patten)
        elements = self.driver.find_elements_by_xpath('//*[@id="{0}"]/div[1]/canvas'.format(self.table_id))
        if not elements:
            log().error("表 {0} 无数据 end".format(self.table_id))
            self.getsysereorlog("end")
            raise AssertionError("表 {0} 无数据 end".format(self.table_id))

    def count_user(self):
        """"""
        self.wait_element(self.table_id, "id")
        element = self.driver.find_element_by_id(self.table_id)
        text = element.text
        if text == "0" or text == "0%":
            log().error("表 {0} 无数据 end".format(self.table_id))
            self.getsysereorlog("end")
            raise AssertionError("表 {0} 无数据 end".format(self.table_id))

    def get_data(self):
        name = getattr(self, self.tabletype)
        name()

    def look_排行(self):
        log().debug("点击‘更多’，进入详情页")
        """点击查看，并切换到frame"""
        self.driver.find_element_by_id(self.detail_id).click()
        self.driver.switch_to.parent_frame()
        self.frame_change(-1)


class ReqData(object):

    def dict_update(self, dictobject, key, value):
        """key存在则更新,不存在在，不做操作"""
        if isinstance(dictobject, dict) and key in dictobject:
            dictobject[key] = value
        return dictobject

    def request_data_home(self):
        start_time = self.start_time
        end_time = self.end_time
        data_tuple = re.compile(r"(\w+):(.+)").findall(self.data_str)
        data = {x.strip(): y.strip() for x, y in data_tuple}

        data = self.dict_update(data, "starttime", start_time)
        data = self.dict_update(data, "endtime", end_time)
        data = self.dict_update(data, "token", self.token)
        # data = self.dict_update(data, "qdi",self.apiqdi)
        data = self.dict_update(data, "datetype", self.apidatatype)
        data = self.dict_update(data, "sysid", getattr(self, "secsiono", "u"))
        data = self.dict_update(data, "userid","test1")
        data = self.dict_update(data, "positioncode", getattr(self, "request_code", None))
        data = self.dict_update(data, "hour", getattr(self, "request_code", None))
        self.data=data
        log().debug("requests 'url, data' \t {1},{0}".format(self.data, self.url_api))


if __name__ == "__main__":
    p = Base()
    p.time_type = "day"
    p.pararms()
    p.request_data_home()
    p.get_data_home()



