from time import sleep

from utils.base import Base


class LoginPage(Base):
    def login_ranzhi(self,user,pwd):
        # driver = Base('c')
        # 填写用户名和密码
        self.send_keys("i,account", user)
        self.send_keys("i,password", pwd)
        # 点击登录按钮
        self.click("i,submit")
        sleep(2)
    def logout_ranzhi(self):
        # self.driver.get("http://127.0.0.1/ranzhi/sys/user-admin.html")
        self.click("l,签退")
    # 获得登录信息
    def get_real_name(self):
        return self.get_text("s,#mainNavbar > div > ul:nth-child(1) > li > a")
    def get_fail_text(self):
        return self.get_text('s,body > div.bootbox.modal.fade.bootbox-alert.in > div > div > div.modal-body > div')
    def login_fail_confirm(self):
        self.click('s,body > div.bootbox.modal.fade.bootbox-alert.in > div > div > div.modal-footer > button')

if __name__ == '__main__':
    a=LoginPage(browser="c")
    a.login_ranzhi("admin","123456")
    # print(a.get_fail_text())
    # a.login_fail_confirm()
    # a.logout_ranzhi()