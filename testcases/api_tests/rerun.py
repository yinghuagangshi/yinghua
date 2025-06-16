#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author:  slg
@Time: 2022/10/13 11:00
@File: rerun.py
"""
import json
import re
import traceback
import os
import subprocess
import sys

def get_json_files(directory):
    '''
    指定报告路径, 获取其中的json格式的报告
    :param directory:
    :return:
    '''
    json_list = []
    dirs = os.listdir(directory)
    if len(dirs) > 0:
        for dir in dirs:
            if dir.endswith('.json'):
                json_list.append(os.path.join(directory, dir))
    return json_list


def get_rerun_cases(file_path):
    '''
    从json报告中,获取需要重跑的用例
    :param file_path:
    :return:
    '''
    rerun_cases = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            strF = f.read()
            datas = json.loads(strF)
            f.close()
        tests = datas['report']['tests']
        # 获取执行失败的测试用例
        for test in tests:
            if test['outcome'] == 'error' or test['outcome'] == 'fail':
                rerun_cases.append(re.findall(r'(.+?)\[', test['name'])[0])
    except Exception:
        print(traceback.format_exc())
    return rerun_cases


def get_command_list(directory):
    '''
    根据需要重跑的用例生成执行命令. 一个json文件一个命令.
    :param json_list:
    :return:
    '''
    json_list = get_json_files(directory)
    if len(json_list) > 0:
        commond_list = []
        for json_file in json_list:
            case_list = get_rerun_cases(json_file)
            file_name = json_file.split(os.sep)[-1]
            rerun_report_html_name = directory + os.sep + 'rerun' + os.sep + file_name + '-rerun.html'
            rerun_report_json_name = directory + os.sep + 'rerun' + os.sep + file_name + '-rerun.json'
            #rerun_report_json_name = re.findall('(.+?)/*.json', json_file)[0] + '-rerun.json'
            command = 'pytest -s -v --html=' + rerun_report_html_name + ' --json=' + rerun_report_json_name
            for case in case_list:
                command = command + ' ' + case
            commond_list.append(command)
        return True,commond_list
    else:
        return False, []


def run_cases(commond_list):
    '''
    运行需重跑的用例
    :param commond_list:
    :return:
    '''
    for commond in commond_list:
        p = subprocess.Popen(commond, stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if err.decode('utf-8') == '':
            print('命令:' + commond + ' 执行成功.')
        else:
            print('命令: ' + commond + ' 执行失败.')


if __name__ == "__main__":

    #运行方式: 传参或使用默认report_dir
    #传参方式: rerun.py "D:\Automation\test1\af-bat-api\reports"
    if len(sys.argv) > 1:
        report_dir = sys.argv[1]
    else:
        # 如果没有给文件传参, 请把report_dir改为需要二次运行失败用例的报告所在目录
        report_dir = "/data/autotest/report/api/is-ocean-api"

    flag, command_list = get_command_list(report_dir)
    print(command_list)
    if flag and len(command_list) < 1:
        print('没有失败用例需要重跑.')
    elif not flag:
        print('当前目录没有找到json文件.')
    else:
        run_cases(command_list)

