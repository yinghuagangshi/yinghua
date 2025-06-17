# -*- coding:utf8 -*- #
#-----------------------------------------------------------------------------------
# ProjectName:   auto_test
# FileName:     unittest
# Author:      shilingang
# Datetime:    2021/3/1 14:49
# Description:
#-----------------------------------------------------------------------------------
import time
import unittest
import warnings
from parameterized import parameterized
from pages.ranzhi_login import LoginPage
from utils import read_excel, get_path, read_ini
from utils.log_output import log_output
from utils.read_data import read_yaml
from utils.read_ini import ReadIni
import pymysql
from utils.read_json import read_json


class Login_test(unittest.TestCase):
    # 获取数据
    yaml_data=read_yaml(ReadIni().get_yaml_ele())
    log=log_output (ReadIni ().log_path () + r'ranzhi.log')
    # 打开浏览器
    @classmethod
    def setUpClass(self) :
        warnings.simplefilter("ignore",ResourceWarning)
        # 连接数据库
        self.ranzhi_connect=pymysql.connect(
            host='127.0.0.1',user='root',passwd='123456',
            database='ranzhi',port=3306,charset='utf8'
        )
        # 打开浏览器
        self.login_page=LoginPage("c")
    @classmethod
    def tearDownClass(self) :
        time.sleep(3)
        self.login_page.quit()
    # def setUp(self):
    #     warnings.simplefilter ("ignore", ResourceWarning)
    #     self.login_page = LoginPage ("c")
    #
    # def tearDown(self):
    #     self.login_page.logout_ranzhi ()
    #     self.login_page.quit ()
    # 用例1
    case_data1=read_excel.read_excel(yaml_data["Login_test"]["login_path"], yaml_data["Login_test"]["login_sucess_sheet"])
    # case_data1= read_json (r'C:\Users\ranzhi_test\config\login_case.json')['login_sucess']
    # case_data1 = read_yaml (r'C:\Users\ranzhi_test\config\login_case.yaml')['login_sucess']
    @parameterized.expand(case_data1)
    def test_login_sucess(self,user,pwd,expection,num):
        try:
            # 建立游标
            self.youbiao = self.ranzhi_connect.cursor ()
            # 执行sql
            self.youbiao.execute ('select deleted from sys_user where account="admin"')
            data_deleted = self.youbiao.fetchall ()[0][0]
            print ('账号状态：'+data_deleted)
            # 登录
            self.login_page.login_ranzhi(user, pwd)
            self.log.error("用例{}已登录".format(num))
            # 断言
            realname=self.login_page.get_real_name()
            self.assertEqual(realname,expection,"与预期不一致")
        except:
            raise AssertionError("用例编号%s执行失败"%(num))
            # print("处理异常")
        finally:
            # 签退
            self.login_page.logout_ranzhi ()
    # # 用例2
    case_data2=read_excel.read_excel(yaml_data["Login_test"]["login_path"], yaml_data["Login_test"]["login_fail_sheet"])
    @parameterized.expand(case_data2)
    # @unittest.skip
    def test_login_fail(self,user,pwd,expection,num):
        try:
            self.login_page.login_ranzhi(user, pwd)
            # 断言
            fail_text=self.login_page.get_fail_text()
            self.assertEqual(fail_text,expection,"与预期不一致")
        except:
            t=time.strftime('%Y%m%d_%H%M%S')
            self.login_page.get_screenshot_as_file(read_ini.ReadIni().screenshot_path()+t+'.png')
            raise AssertionError("用例编号%s执行失败"%(num))
        finally:
            # 点击确框
            self.login_page.login_fail_confirm()
if __name__ == '__main__':
    unittest.main()
    # a=Login_test()
    # t = time.strftime ('%Y%m%d_%H%M%S')
    # b=a.login_page.get_screenshot_as_file (read_ini.ReadIni ().screenshot_path () + '\\' + t)
    # print(b)
