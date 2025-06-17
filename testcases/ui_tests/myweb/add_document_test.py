# -*- coding:utf8 -*- #
#-----------------------------------------------------------------------------------
# ProjectName:   ranzhi_test
# FileName:     add_document_test
# Author:      shilingang
# Datetime:    2021/3/6 14:18
# Description:
#-----------------------------------------------------------------------------------
import time
import unittest
import warnings
from parameterized import parameterized

from pages.ranzhi_adddocument import Ranzhi_Add_Document
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


class Add_Document_Test(unittest.TestCase):
    # 获取数据
    case_data_sucess=read_excel(ReadIni().get_path('add_document_path'),'adduser_document_sucess')
    case_data_fail=read_excel(ReadIni().get_path('add_document_path'),'adduser_document_fail')
    # print(case_data_sucess)
    # 获取日志
    log=log_output (ReadIni ().log_path () + r'add_document.log')

    # 打开与关闭浏览器、登录管理员账户
    @classmethod
    def setUpClass(self) :
        warnings.simplefilter("ignore",ResourceWarning)
        # 数据库
        self.mysql_connect=Mysql_Operation ()
        self.mysql_connect.connect_mysql()
        # 打开浏览器
        self.document_driver=Ranzhi_Add_Document("c")
        # 登录用户
        self.document_driver.login_ranzhi ('admin', '123456')
        self.log.info ("用户已登录")
    @classmethod
    def tearDownClass(self) :
        time.sleep (3)
        self.document_driver.quit()

    # 添加成功用例
    @parameterized.expand(case_data_sucess)
    # @unittest.skip
    def test_add_sucess(self,num,sort,user,group,file_type,title,type_url,type_text,keywords,digest,
                        attach_path,attach_title,private):
        try:
            # 添加用户
            self.document_driver.add_document(sort,user,group,file_type,title,type_url,type_text,keywords,digest,
                     attach_path,attach_title,private)
            # 数据库断言
            time.sleep(1)
            sql='select title from oa_doccontent where title="%s"'%title
            realtitle =self.mysql_connect.execute_mysql(sql)[0][0]
            self.assertEqual(realtitle,title,"与预期不一致")
            self.log.info ("添加成功用例：[编号%s]执行成功" % (num))
        except:
            t=time.strftime('%Y%m%d_%H%M%S')
            self.document_driver.get_screenshot_as_file(read_ini.ReadIni().screenshot_path()+t+'.png')
            self.log.error("添加成功用例：[编号%s]执行失败"%(num))
            raise AssertionError("添加成功用例：[编号%s]执行失败"%(num))

    # 添加失败用例
    @parameterized.expand(case_data_fail)
    # @unittest.skip
    def test_add_fail(self,num,sort,user,group,file_type,title,type_url,type_text,keywords,digest,
                        attach_path,attach_title,private,ele,expect_text):
        try:
            # 添加文档
            self.document_driver.add_document (sort, user, group, file_type, title, type_url, type_text, keywords, digest,
                                      attach_path, attach_title, private)
            # 断言
            real_text=self.document_driver.get_text(ele)
            # print(real_text)
            self.assertEqual(real_text,expect_text,"与预期不一致")
            self.log.info ("添加失败用例：[编号%s]执行成功" % (num))
        except:
            t=time.strftime('%Y%m%d_%H%M%S')
            self.document_driver.get_screenshot_as_file(read_ini.ReadIni().screenshot_path()+t+'.png')
            self.log.error("添加失败用例：[编号%s]执行失败" % (num))
            raise AssertionError("添加失败用例：[编号%s]执行失败"%(num))
if __name__ == '__main__':
    unittest.main()