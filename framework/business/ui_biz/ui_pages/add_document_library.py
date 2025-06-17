# -*- coding:utf8 -*- #
#-----------------------------------------------------------------------------------
# ProjectName:   ranzhi_test
# FileName:     add_document_library
# Author:      shilingang
# Datetime:    2021/3/6 12:56
# Description:
#-----------------------------------------------------------------------------------
from pages.ranzhi_login import LoginPage


class Ranzhi_Add_Document_Library(LoginPage):
    def add__library(self,type,name,user,group,private=0):
        # 进入文档
        self.driver.get (r'http://127.0.0.1/ranzhi/doc/doc-alllibs-custom.html')
        # 进入iframe框架
        self.switch_to_frame ("i,iframe-4")
        # 点击添加
        self.click("i,createButton")

        # 添加文档信息
        if type=='项目文档库':
            self.click('x,//*[@id="libType"]/option[2]')
        self.send_keys("i,name",name)

        if private==1:
            # 私密
            self.click('i,private')
        else:
            # 公开
            # 授权用户
            self.click (r'x,//*[@id="users_chosen"]/ul/li/input')
            self.click ('x,//*[@id="users_chosen"]/div/ul/*[text()="%s"]'%user)
            # 授权分组
            self.driver.find_element_by_xpath('//*[contains(text(),"%s")]'%group).find_element_by_tag_name('input').click()
        self.click('i,submit')


if __name__ == '__main__':
    a = Ranzhi_Add_Document_Library()
    a.login_ranzhi ("admin", "123456")
    a.add__library('自定义文档','第二个文档库','admin','管理员')
