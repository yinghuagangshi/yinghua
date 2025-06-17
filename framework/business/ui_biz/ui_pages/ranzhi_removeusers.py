# -*- coding:utf8 -*- #
#-----------------------------------------------------------------------------------
# ProjectName:   auto_test
# FileName:     ranzhi_removeusers
# Author:      shilingang
# Datetime:    2021/2/27 16:10
# Description:
#-----------------------------------------------------------------------------------
from time import sleep
from pages.ranzhi_login import LoginPage


class Remove_users(LoginPage):
    def remove_users(self,times=1):
        self.driver.get("http://127.0.0.1/ranzhi/sys/user-admin.html")
        # 进入iframe框架
        self.switch_to_frame('i,iframe-superadmin')
        for i in range(times):
            self.click( "s,body > div > div > div > div.col-md-10 > div > div > table > tbody > tr:last-child > td.operate > a.deleter")
            self.driver.switch_to.alert.accept()
            sleep(0.5)

if __name__ == '__main__':
    a=Remove_users("f")
    a.login_ranzhi ("admin", "123456")
    a.remove_users(15)