from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import time



class WaitElement():

    def __call__(self, driver=None):
        if "/" not in self.elementstr:
            if self.driver.find_element_by_id(self.elementstr):
                return True
            else:
                return False
        else:
            if self.driver.find_element_by_xpath(self.elementstr):
                return True
            else:
                return False

    def wait_element(self, elementstr='//*[@id="js_love_url"]', alltime=10, seq=0.5):
        self.elementstr = elementstr
        WebDriverWait(self.driver, alltime, 0.5).until(self)

    def one(self):
        driver = webdriver.Chrome()
        self.driver=driver
        driver.implicitly_wait(60)
        time_start = time.time()
        driver.get('https://www.163.com/')

        # driver.find_element_by_id('js_love_url').click()
        self.wait_element("js_love_url")
        time_end = time.time()
        print('access time is : ', time_end - time_start)
        time.sleep(2)
        driver.quit()


WaitElement().one()


