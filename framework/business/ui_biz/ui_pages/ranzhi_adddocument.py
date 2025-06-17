# -*- coding:utf8 -*- #
#-----------------------------------------------------------------------------------
# ProjectName:   ranzhi_test
# FileName:     ranzhi_adddocument
# Author:      shilingang
# Datetime:    2021/3/5 10:49
# Description:
#-----------------------------------------------------------------------------------
from time import sleep
from pages.ranzhi_login import LoginPage


class Ranzhi_Add_Document(LoginPage):
    def add_document(self,sort,user,group,file_type,title,type_url,type_text,keywords,digest,
                     attach_path,attach_title,private=0,library="第一个文档库"):
        attach_path=[] if attach_path=='' else attach_path.split(',')
        attach_title=[] if attach_title=='' else attach_title.split(',')
        self.driver.get('http://127.0.0.1/ranzhi/doc/doc-alllibs-custom.html')
        # sleep(2)
        self.switch_to_frame ("i,iframe-4")
        # 选择文档库
        self.click('x,//*[@id="libList"]//a[@title="%s"]'%library)
        # 点击创建
        self.click('x,//*[@id="menuActions"]/a')
        # 添加文档信息
        if sort!='':
            self.click('x,//*[@id="module"]/option[%s]'%sort)
        if private==1:
            # 私密
            self.click('i,private')
        else:
            # 公开
            # 授权用户
            if user != '':
                self.click (r'x,//*[@id="users_chosen"]/ul/li/input')
                self.click ('x,//*[@id="users_chosen"]/div/ul/*[text()="%s"]'%user)
            # 授权分组
            if group != '':
                self.driver.find_element_by_xpath('//*[contains(text(),"%s")]'%group).find_element_by_tag_name('input').click()
        if file_type=="文档" or file_type==0 or file_type=='':
            self.click('i,typetext')
            if type_text != '':
                # 进入文本框架，填写文本,退出文本框架
                self.switch_to_frame ("i,ueditor_0")
                self.send_keys('x,/html/body',type_text)
                self.driver.switch_to.parent_frame ()
        elif file_type == "链接" or file_type == 1:
            # 链接url
            self.click ('i,typeurl')
            self.send_keys('i,url',type_url)
        # 其他内容
        if title!='':
            self.send_keys('i,title',title)
        self.send_keys('i,keywords',keywords)
        self.send_keys('i,digest',digest)

        # 处理多个附件

        # 循环添加附件框
        len_attach=max(len(attach_title),len(attach_path))
        if len_attach>2:
            for i in range(len_attach-2):
                self.click('x,//*[@id="fileBox1"]/tbody/tr/td[3]/a/i')

        # 循环添加附件与标题
        i = 0
        j = 0
        k = 1
        z=1
        while i<len(attach_path):
            index1=str(i+1)
            # 从第3个附件框地址不同
            if i>1 :
                k=i
                index1=1
            self.send_keys('x,//*[@id="fileBox%s"][%s]/tbody/tr/td[1]/div/input'%(index1,k),attach_path[i])
            # sleep(10)
            i+=1
        while j<len(attach_title):
            index2 = str (j + 1)
            # 从第3个附件框地址不同
            if j>1 :
                z=j
                index2=1
            self.send_keys('x,//*[@id="fileBox%s"][%s]/tbody/tr/td[2]/input'%(index2,z),attach_title[j])
            j+= 1
        # 保存
        self.click('i,submit')




if __name__ == '__main__':
    a=Ranzhi_Add_Document()
    a.login_ranzhi ("admin", "123456")
    a.add_document(4,'admin','管理员','链接','私密3','文档url','正文','关键字','摘要',
                  "",
                  "日志文件1,日志文件2,日志文件1,日志文件2,日志文件1,日志文件2")

    sleep(10)
    # a.quit()