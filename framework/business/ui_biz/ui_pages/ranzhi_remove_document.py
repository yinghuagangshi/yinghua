# -*- coding:utf8 -*- #
#-----------------------------------------------------------------------------------
# ProjectName:   ranzhi_test
# FileName:     ranzhi_remove_document
# Author:      shilingang
# Datetime:    2021/3/6 16:41
# Description:
#-----------------------------------------------------------------------------------
from time import sleep

from pages.ranzhi_login import LoginPage


class Ranzhi_Remove_Document(LoginPage):
    def remove_document(self,num):

        self.login_ranzhi ("admin", "123456")
        self.driver.get(r'http://127.0.0.1/ranzhi/doc/doc-browse-3.html')
        self.switch_to_frame ("i,iframe-4")

        for i in range (num):
            self.click('s,#docList > tbody > tr:first-child > td.actions > a.reloadDeleter')
            self.driver.switch_to_alert().accept()
            sleep(0.5)
            i+=1

if __name__ == '__main__':
    Ranzhi_Remove_Document().remove_document(10)