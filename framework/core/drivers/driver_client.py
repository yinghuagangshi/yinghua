from selenium import webdriver
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class Base:
    def __init__(self,browser="c",url='http://127.0.0.1/ranzhi/sys/user-login.html'):
        # 传入浏览器类型
        if browser == "Chrome" or browser == "c" or browser == "C":
            self.driver = webdriver.Chrome()
        elif browser == "Firefox"or browser == "f" or browser == "F":
            self.driver = webdriver.Firefox()
        else:
            raise NameError("请输入正确的浏览器类型")
        # 隐式等待
        # self.driver.implicitly_wait(30)
        # 打开网址
        self.driver.get(url)
        # 最大化窗口
        self.driver.maximize_window()

    def selector_to_locator(self, selector):
        """
        把selector("i,account")转换成locator(By.ID,"account")
        :param selector: selector("i,account")
        :return:
        """
        selector_by = selector.split(",")[0].strip()
        selector_value = selector.split(",")[1].strip()
        if selector_by == "i" or selector_by == "id":
            locator = (By.ID, selector_value)
        elif selector_by == "n" or selector_by == "name":
            locator = (By.NAME, selector_value)
        elif selector_by == "l" or selector_by == "link_text":
            locator = (By.LINK_TEXT, selector_value)
        elif selector_by == "p" or selector_by == "partial_link_text":
            locator = (By.PARTIAL_LINK_TEXT, selector_value)
        elif selector_by == "t" or selector_by == "tag_name":
            locator = (By.TAG_NAME, selector_value)
        elif selector_by == "c" or selector_by == "class_name":
            locator = (By.CLASS_NAME, selector_value)
        elif selector_by == "s" or selector_by == "css_selector":
            locator = (By.CSS_SELECTOR, selector_value)
        elif selector_by == "x" or selector_by == "xpath":
            locator = (By.XPATH, selector_value)
        else:
            raise TypeError("请输入正确的定位方式")
        return locator

    def get_element(self, selector):
        """
        定位到元素
        :param selector:
        :return:
        """
        locator = self.selector_to_locator(selector)
        # ele = self.driver.find_element(*locator)  # locator == (By.ID,"value")
        ele = WebDriverWait(self.driver,20,1).until(EC.presence_of_element_located(locator))
        return ele

    def send_keys(self, selector, text):
        """
        输入内容
        :param selector:
        :param text: 需要输入的内容
        :return:
        """
        ele=self.get_element(selector)
        ele.clear()
        ele.send_keys(text)

    def click(self, selector):
        """
        对元素进行点击
        :param selector:
        :return:
        """
        self.get_element(selector).click()

    def switch_to_frame(self,selector):
        """
        进入iframe框架
        :param selector:
        :return:
        """
        locator = self.get_element(selector)
        # self.driver.switch_to.frame(locator)
        WebDriverWait(self.driver,20,1).until(EC.frame_to_be_available_and_switch_to_it(locator))

    def select_by_index(self,selector,num):
        """
        select下拉框通过索引定位
        :param selector:
        :param num:
        :return:
        """
        Select(self.get_element(selector)).select_by_index(num)

    def select_by_value(self,selector,value):
        """
        select下拉框通过value值定位
        :param selector:
        :param value:
        :return:
        """
        Select(self.get_element(selector)).select_by_value(value)

    def select_by_visible_text(self,selector,text):
        """
        select下拉框通过文本定位
        :param selector:
        :param text:
        :return:
        """
        Select(self.get_element(selector)).select_by_visible_text(text)

    def two_locator(self,selector1,selector2):
        """
        二次定位,随机选择下拉框
        :param selector1:
        :param selector2:
        :return:
        """
        locator1 = self.selector_to_locator(selector1)
        locator2 = self.selector_to_locator(selector2)
        # 随机点击
        ele = self.driver.find_element(*locator1).find_elements(*locator2)
        random.choice(ele).click()
    def second_locator(self,selector1,selector2):
        """
        二次定位,随机选择下拉框
        :param selector1:
        :param selector2:
        :return:
        """
        locator1 = self.selector_to_locator(selector1)
        locator2 = self.selector_to_locator(selector2)
        return self.driver.find_element(*locator1).find_element(*locator2)

    def get_text(self,selector):
        """
        获取文本
        :param selector:
        :return:
        """
        return self.get_element(selector).text
    def get_screenshot_as_file(self,picture_name):
        """
        截图
        :return:
        """
        return self.driver.get_screenshot_as_file(picture_name)

    def quit(self):
        """
        杀进程
        :return:
        """
        self.driver.quit()

if __name__ == '__main__':
    Base().get_screenshot_as_file(r'C:\Users\ranzhi_test\config\screenshot\a.png')