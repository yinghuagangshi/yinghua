# -*- coding:utf8 -*- #
#-----------------------------------------------------------------------------------
# ProjectName:   ranzhi_test
# FileName:     runner1
# Author:      shilingang
# Datetime:    2021/3/3 16:17
# Description:
#-----------------------------------------------------------------------------------
import time
import unittest

from unittestreport.HTMLTestRunnerNew import HTMLTestRunner

from utils.read_ini import ReadIni
from utils.send_email import SendEmail


class  RunnerTest_1:
    def runner_test(self,case_name,receiver='shilingang111@163.com'):
        # 创建测试套件
        suite = unittest.TestSuite()
        # 加载单个用例到测试套件中
        # 批量加载用例到测试套件中
        #第一种加载方式
        case_path = ReadIni().get_path('case_path')
        suite.addTests(unittest.TestLoader().discover(case_path,pattern=case_name))

        # 报告路径
        tt = time.strftime("%Y_%m_%d_%H_%M_%S")
        report_path = ReadIni().get_path('report_path') + r"ranzhitest{}.html".format(tt)
        # print(report_path)

        # 第一种测试套

        # 引入HTMLTestRunner
        report_data = open(report_path,mode="wb")
        html_runner = HTMLTestRunner(report_data,verbosity=2,title="然之测试报告",
                                     description="下面是详细的报告内容",tester="slg")
        # 运行测试套
        html_runner.run(suite)
        report_data.close()

        # 第二种测试套

    # 发送邮箱
        SendEmail ().send_emails(report_path,receiver)

if __name__ == '__main__':
    RunnerTest_1().runner_test('add_document_test.py','1366896160@qq.com')
