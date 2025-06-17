# -*- coding:utf8 -*- #
#-----------------------------------------------------------------------------------
# ProjectName:   pro_ranzhi_25
# FileName:     get_path
# Author:      MingFeiyang
# Datetime:    2021-03-02 16:56
# Description:
#-----------------------------------------------------------------------------------
import os

def get_file_path(path):

    # 获取当前文件的绝对路径
    file_path = os.path.dirname(__file__)
    pro_name = path.split("/")[0]
    # 分割绝对路径，找到项目之前的路径
    before_ptah = file_path.split(pro_name)[0]
    # 拼接路径
    # all_path = str(before_ptah) + path
    all_path = os.path.join(before_ptah,path)
    return all_path

if __name__ == '__main__':
    print(get_file_path(r'ranzhi_test'))


