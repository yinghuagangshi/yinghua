# -*- coding:utf8 -*- #
#-----------------------------------------------------------------------------------
# ProjectName:   ranzhi_test
# FileName:     send_email
# Author:      shilingang
# Datetime:    2021/3/4 10:17
# Description:
#-----------------------------------------------------------------------------------
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class SendEmail:
    def send_emails(self,report_path,receiver):
        try:
            # 配置服务器信息
            # 服务器
            smtp = "smtp.qq.com"
            # 端口
            port = "25"
            # port = "465"
            # 登录用户
            sender = "1125116689@qq.com"
            # 配置邮箱的授权码
            pwd = 'yvqfvssudyhcigcc'
            # 配置接收用户

            # 创建邮件对象,设置邮件发送信息
            msg = MIMEMultipart()
            msg["from"] = sender  # 由谁发送
            msg["to"] = receiver  # 发送给谁
            msg["subject"] = "石林钢_添加用户测试报告"    # 主题
            # 读取报告内容
            with open(report_path,mode="rb") as report:
                body = report.read().decode(encoding="utf8")

            # 写正文
            mime_text = MIMEText(body, "html", "utf8")
            msg.attach(mime_text)
            # 添加附件
            att = MIMEText(body, "base64", "utf8")
            att['Content-Type'] = 'application/octet-stream' # 表示可以添加附件
            att["Content-Disposition"] = "attachment;filename = %s" % report_path
            msg.attach(att)

            # 发送邮件
            smtp1 = smtplib.SMTP()
            # 连接服务器：服务器和端口号
            smtp1.connect(smtp,port)
            # print('连接成功')
            # 登录：用来用户名和授权码
            smtp1.login(sender,pwd)
            # print("登录成功")
            # 发送 ：发送给谁，多个接收人分割成列表
            smtp1.sendmail(sender,receiver.split(";"),msg.as_string())
            print("邮件发送成功")
        except Exception as e:
            print("邮件发送失败")
            raise

if __name__ == '__main__':
    SendEmail().send_emails(r'C:\Users\ranzhi_test\result\report\ranzhitest2021_03_04_10_01_42.html','shilingang111@163.com')