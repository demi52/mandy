import time

from selenium.webdriver.support.wait import WebDriverWait

from lib.driver import InitTest
__author__ = "luxu"
import os
from HTMLReport import AddImage
from selenium import webdriver
from config.conf import BI_protal, LOG
from lib.funcslib import log, Ioput




class Land:
    alltime = BI_protal.wait_ele
    sec_text = BI_protal.secsion

    def __call__(self, driver=None):
        if self.driver.find_element(by=self.element_type, value=self.elementstr):
            return True
        else:
            return False

    def wait_element(self, elementstr, element_type="xpath", seq=0.5):
        """显示等待"""
        self.elementstr = elementstr
        self.element_type = element_type
        log().info("轮询元素 %s : %s " % (self.element_type, self.elementstr))
        try:
            WebDriverWait(self.driver, self.alltime, seq).until(self)
        except:
            log().error("超时，timeout >= %s秒 元素 <%s : %s> 未加载；" % (self.alltime, element_type, elementstr))
            raise AssertionError("超时，timeout >= %s 元素 <%s : %s> 未加载；" % (self.alltime, element_type, elementstr))

    def _begin(self,**kwargs):
        """测试类开始前环境准备
        """
        try:
            Ioput.input("pathstatus", "next")
            self._first(**kwargs)
        except AssertionError as e:
            log().critical("准备环境缺少数据，或当前版本无此页面，后续用例均判定失败 ,ERROR : {0}".format(e))
            Ioput.input("pathstatus", "exit")
            Ioput.input("patherror", e)
            self._last()
        except Exception as e:
            self._last()
            Ioput.input("pathstatus", "next")
            log().error("异常终止：{0}".format(e))
        finally:
            self.screenhost_to_report(alt="前置环境", name="前置环境")

    def _first(self, **kwargs):
        __class__.pararms(self, **kwargs)
        if BI_protal.portal != "debug":
            self.driver = Ioput.output("driver")
        else:
            self.open()


    def _last(self):
        """测试类结束事物
        tearDown
        """
        # self.driver.quit()

    def __chose(self):
        self.driver.quit()

    def __before(self):

        """测试函数开始前事物"""
        try:
            self.driver.delete_all_cookies()
        except:
            try:
                self.__chose()
            except:
                InitTest.start()
                self.driver = Ioput.output("driver")
            else:
                InitTest.start()
                self.driver = Ioput.output("driver")


    def _after(self):
        """单个用例执行后操作"""
        log().info("{0} test end {0}\n".format("=" * 50))
        Ioput.input(keys="funcname", value="wait and init")


    def pararms(self, **kwargs):
        """当前测试类的所有参数"""
        self.url= BI_protal.url
        self.user = kwargs.get("user", BI_protal.user)
        self.password = kwargs.get("password", BI_protal.password)

    def open(self):
        """打开浏览器"""
        options = webdriver.ChromeOptions()
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': BI_protal.downloadpath}
        options.add_experimental_option('prefs', prefs)
        options.add_argument('log-level=3')
        self.driver = webdriver.Chrome(executable_path=BI_protal.driver_path,chrome_options=options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(BI_protal.wait_time)
        log().info("{0}启动浏览器{0}".format("*" * 40))

    def __landing(self):
        """登陆"""
        self.driver.get(self.url)
        self.exement("name", "id", self.user)
        self.exement("password", "id", self.password)
        self.exement("submit", "id")


    def change_sec(self):
        """电信、移动、联通节点选择"""
        self.wait_element('//*[@id="div-select"]/form/span/label', "xpath")
        sec_text = self.driver.find_element_by_xpath('//*[@id="div-select"]/form/span/label').text
        sec_text = sec_text.strip()
        log().debug((sec_text, type(sec_text)))
        d = {"中国电信": "1", "中国移动": "2", "中国联通": "3"}
        if d[sec_text] != self.sec_text:
            self.exement('//*[@id="div-select"]/form/span')
            time.sleep(0.5)
            self.exement('//*[@id="div-select"]/form/ul/li[%s]/a' % self.sec_text)
            time.sleep(0.5)
        log().info("landing  %s sucess , secaction %s" % (self.url, self.sec_text))


    def exement(self, elements, ele_type="xpath", parms=None):
        """xpath 获取元素封装方法
        """
        ele_type = ele_type.lower()
        self.wait_element(elementstr=elements, element_type=ele_type, seq=1)
        elements = self.driver.find_element(by=ele_type, value=elements)

        if parms =="getele":
            return elements

        if parms != None:
            elements.clear()
            elements.send_keys(parms)
        elif parms == None:
            elements.click()

    def screenhost_to_report(self, alt="登陆", name="登陆"):
        """截屏动作"""
        if  LOG.screenhost:
            photo = self.driver.get_screenshot_as_base64()
            AddImage(photo, alt=alt, name=name)
            log().debug("screenhost sucess %s " % alt)

    def f_land(self, **kwargs):
        __class__.pararms(self, **kwargs)
        self.__before()
        self.__landing()
        self.change_sec()
        if self.__class__ == __class__:
            self.screenhost_to_report()


if __name__ == "__main__":
    pass
    p=Land()
    p._first()
    p.f_land()




