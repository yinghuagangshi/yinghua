# -*- coding:utf8 -*- #
#-----------------------------------------------------------------------------------
# ProjectName:   ranzhi_test
# FileName:     adduser_test
# Author:      shilingang
# Datetime:    2021/3/4 11:14
# Description:
#-----------------------------------------------------------------------------------
import time
import unittest
import warnings
from parameterized import parameterized

from pages.ranzhi_addusers import AddUserPage
from pages.ranzhi_login import LoginPage
from utils import read_ini
from utils.log_output import log_output
from utils.mysql_operation import Mysql_Operation
from utils.read_data import read_yaml
from utils.read_excel import read_excel
from utils.read_ini import ReadIni
import pymysql
from utils.read_json import read_json


class Adduser_test(unittest.TestCase):
    # 获取数据
    case_data_sucess=read_excel(ReadIni().get_path('adduser_path'),'adduser_sucess')
    case_data_fail=read_excel(ReadIni().get_path('adduser_path'),'adduser_fail')
    # 获取日志
    log=log_output (ReadIni ().log_path () + r'ranzhi_adduser.log')
    # 打开与关闭浏览器、登录管理员账户
    @classmethod
    def setUpClass(self) :
        # 数据库
        self.mysql_connect=Mysql_Operation ()
        self.mysql_connect.connect_mysql()
        warnings.simplefilter("ignore",ResourceWarning)
        # 打开浏览器
        self.adduser_driver=AddUserPage("c")
        # 登录用户
        self.adduser_driver.login_ranzhi ('admin', '123456')
        self.log.info ("用户已登录")
    @classmethod
    def tearDownClass(self) :
        # self.mysql_connect.close()
        time.sleep(3)
        self.adduser_driver.quit()
    # 添加成功用例
    @parameterized.expand(case_data_sucess)
    # @unittest.skip
    def test_adduser_sucess(self,num,user_name, real_name,pwd1,pwd2,email,gender,dept,role):
        try:
            # 添加用户
            self.adduser_driver.add_user(user_name,real_name,pwd1,pwd2,email,gender,dept,role)
            # 断言
            time.sleep(1)
            realname =self.mysql_connect.execute_mysql('select account from sys_user where account="%s"'%user_name)[0][0]
            # realname=self.adduser_driver.get_add_username()
            self.assertEqual(realname,user_name,"与预期不一致")
            self.log.info ("添加成功用例：[编号%s]执行成功" % (num))
        except:
            t=time.strftime('%Y%m%d_%H%M%S')
            self.adduser_driver.get_screenshot_as_file(read_ini.ReadIni().screenshot_path()+t+'.png')
            self.log.error("添加成功用例：[编号%s]执行失败"%(num))
            raise AssertionError("添加成功用例：[编号%s]执行失败"%(num))
    # 添加失败用例
    @parameterized.expand(case_data_fail)
    # @unittest.skip
    def test_adduser_fail(self,num,user_name, real_name,pwd1,pwd2,email,gender,dept,role,locator,expect_text):
        try:
            # 添加用户
            self.adduser_driver.add_user(user_name,real_name,pwd1,pwd2,email,gender,dept,role)
            # 断言
            # time.sleep(2)
            real_text=self.adduser_driver.get_text('i,%s'%locator)
            # print(real_text)
            self.assertEqual(real_text,expect_text,"与预期不一致")
            self.log.info ("添加失败用例：[编号%s]执行成功" % (num))
        except:
            t=time.strftime('%Y%m%d_%H%M%S')
            self.adduser_driver.get_screenshot_as_file(read_ini.ReadIni().screenshot_path()+t+'.png')
            self.log.error("添加失败用例：[编号%s]执行失败" % (num))
            raise AssertionError("添加失败用例：[编号%s]执行失败"%(num))
if __name__ == '__main__':
    unittest.main()