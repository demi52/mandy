import os
import shutil
import time
import re
from HTMLReport import HTMLReport
from config.conf import BI_protal, report
from lib.funcslib import Ioput, log, CreatReportXlsx
from lib.listen import ListenServerLog as L
from selenium import webdriver
from addtestcase.addtestall_class import suite
import sys
import requests

__autor__ = "鲁旭"


class InitTest(CreatReportXlsx):

    x = 1
    @classmethod
    def stream(cls):
        allcase = set()
        sui = suite()
        print(type(sui), "type")
        suis = list(iter(sui))
        case = []
        case_id = 0
        for clss in suis:
            for fun in list(iter(clss)):
                case_id += 1
                print(" {:0>4d} \t %s".format(case_id,) % str(fun))
                allcase.add(str(fun))
                case.append(fun)
        print("校验重复", len(allcase))


    @classmethod
    def check(cls):
        try:
            L().searchqdi()
        except ConnectionRefusedError as c:
            log().error("监听程序未启动 %s" % c)
            sys.exit()

    @classmethod
    def start(cls):
        options = webdriver.ChromeOptions()
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': BI_protal.downloadpath}
        options.add_experimental_option('prefs', prefs)
        options.add_argument('log-level=3')

        cls.driver=webdriver.Chrome(executable_path=BI_protal.driver_path,chrome_options=options)
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(BI_protal.wait_time)
        Ioput.input(keys="driver", value=cls.driver)
        log().info("\t启动浏览器\t".center(80, "-"))

    @classmethod
    def _start2(cls):

        # chrome_driver = os.path.abspath(r"C:\software\chromedriver")
        # os.environ["webdriver.chrome.driver"] = chrome_driver
        chrome_capabilities = {
            "browserName": "chrome",                          # 浏览器名称
            "version": "",                                    # 操作系统版本
            "platform": "windows",                            # 平台，这里可以是windows、linux、andriod等等
            "javascriptEnabled": True,                        # 是否启用js
            # "webdriver.chrome.driver": chrome_driver
        }
        driver = webdriver.Remote("http://node_ip:5555/wd/hub", desired_capabilities=chrome_capabilities)
        # driver.set_window_size(1280,720)
        driver.get("http://www.baidu.com")
        print(driver.title)
        driver.quit()

    @classmethod
    def active(cls, suite=suite, report_name='index'):
        cls.stream()
        # cls.check()
        if os.path.exists(report()):
            shutil.rmtree(report())
        os.makedirs(report())
        os.makedirs(BI_protal.downloadpath)

        assert os.path.exists(BI_protal.driver_path), "chromedriver.exe  不存在"
        cls.start()
        HTMLReport.TestRunner(
                               # report_file_name='BI_6.0.7_BeiJing_3_13_2日报周报',
                               report_file_name=report_name,
                               output_path=report('report'),
                               title="BI-PORTAL 测试报告",
                               description="描述测试项目相关信息",
                               sequential_execution=True,
                               lang='cn'
                               ).run(suite())

    @classmethod
    def end(cls):
        driver = Ioput.output("driver")
        driver.quit()
        log().info("\t测试结束关闭浏览器\t".center(80, "-"))


if __name__ == "__main__":
    InitTest.stream()
    # InitTest.search_ui_api()
    # InitTest.write("index")

