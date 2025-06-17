# -*- coding:utf8 -*- #
#-----------------------------------------------------------------------------------
# ProjectName:   auto_test
# FileName:     ranzhi_addusers
# Author:      shilingang
# Datetime:    2021/2/27 14:16
# Description:
#-----------------------------------------------------------------------------------
from time import sleep
import datetime
import random
from pages.ranzhi_login import LoginPage
from utils.read_data import read_yaml


class AddUserPage(LoginPage):
    # 元素定位路径
    yaml_data=read_yaml(r'C:\Users\ranzhi_test\config\config_data.yaml')

    def add_users(self, user_name, real_name, pwd, email,times=1):
        """
        批量添加用户
        :param user_name:
        :param real_name:
        :param pwd:
        :param email:
        :param times:
        :return:
        """
        # 进入添加成员
        self.get_element(self.yaml_data['AddUserPage']['wait_login'])
        self.driver.get(self.yaml_data['AddUserPage']['add_page'])
        # 进入iframe框架
        self.switch_to_frame(self.yaml_data['AddUserPage']['iframe'])
        for i in range(1, times+1):
            # 引入微秒，来随机
            tt = datetime.datetime.now().microsecond
            # 填写信息：
            self.send_keys("i,account", user_name + str(tt))  # 用户名
            self.send_keys("i,realname", real_name + str(tt))  # 真实姓名
            # self.find_element_by_id('genderm').click() # 选择性别
            sex = ["genderm", "genderf"]
            self.click('i,%s' % random.choice(sex))
            # 二次定位,定位部门
            self.two_locator('i,dept', 't,option')
            # 二次定位,定位角色
            self.two_locator('i,role', 't,option')
            # 添加密码，重复密码
            self.send_keys('i,password1', pwd)
            self.send_keys('i,password2', pwd)
            # 添加邮箱
            self.send_keys('i,email', email + "{}@qq.com".format(tt))
            # 点击保存按钮
            self.click('i,submit')
            # 输入页数
            sleep(2)
            self.send_keys('i,_pageID', "100")
            # 点击GO
            self.click('i,goto')
            # 定位用户名
            realname_ele = 'body > div > div > div > div.col-md-10 > div > div > table > tbody > tr:last-child > td:nth-child(3)'
            # 获取用户名文本
            sleep(1)
            actual_name = self.get_text('s,%s' % realname_ele)
            assert actual_name == user_name + str(tt)
            print("断言成功，实际结果是：{},期望结果是：{}".format(actual_name, user_name + str(tt)))
            # 点击添加成员
            self.click('x,/html/body/div/div/div/div[1]/div/div[2]/a[1]')

    def add_user(self, user_name, real_name,pwd1,pwd2,email,gender='',dept='',role=''):
        """
        添加单个用户
        :param user_name:
        :param real_name:
        :param pwd:
        :param email:
        :param times:
        :return:
        """
        # 进入添加成员
        self.driver.get(r'http://127.0.0.1/ranzhi/sys/user-create.html')
        # 进入iframe框架
        self.switch_to_frame(self.yaml_data['AddUserPage']['iframe'])

        # 填写必要用户信息
        if user_name!='':
            self.send_keys("i,account", user_name)  # 用户名
        if real_name != '':
            self.send_keys("i,realname", real_name )  # 真实姓名
        # 添加密码，重复密码
        if pwd1 != '':
            self.send_keys('i,password1', pwd1)
        if pwd2 != '':
            self.send_keys('i,password2', pwd2)
        # 添加邮箱
        if email != '':
            self.send_keys('i,email', email)

        # 非必填信息
        if gender=='':
            pass
        elif gender=="男":
            self.click ('i,genderm' )
        elif gender=="女":
            self.click ('i,genderf' )
        if dept!='':
            # 二次定位部门
            self.select_by_visible_text('i,dept', r'/%s'%dept)
        if role != '':
            # 二次定位角色
            self.select_by_visible_text('i,role', role)
        # 点击保存按钮
        self.click('i,submit')
        # sleep(5)
    def get_add_username(self):
        # 挑转到最后一页
        sleep (1)
        self.send_keys ('i,_pageID', "100")
        self.click ('i,goto')
        # 定位用户名
        realname_ele = 'body > div > div > div > div.col-md-10 > div > div > table > tbody > tr:last-child > td:nth-child(3)'
        # 获取用户名文本
        sleep (1)
        return self.get_text ('s,%s' % realname_ele)


if __name__ == '__main__':
    a=AddUserPage()
    a.login_ranzhi ("admin", "123456")
    a.add_user('',"slg",'123456','123456','slg115@qq.email',"男","4","人事")
    # print(a.get_add_username())
