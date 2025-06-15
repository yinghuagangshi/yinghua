#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author:  chaozhongze
@Time: 2021/11/16
@File: file_io
"""
import os


class Fileio():
    '''文件读写'''
    dir_path = os.path.dirname(os.path.dirname(__file__)) + '\\datas\\taskid'

    def write_data(self, file_name, taskid):
        '''写入文件'''
        file_path = self.dir_path + '\\' + file_name
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(taskid)
            f.close()

    def read_data(self, file_name):
        '''读取文件'''
        file_path = self.dir_path + '\\' + file_name
        with open(file_path, 'r', encoding='utf-8') as f:
            taskid = f.read()
            f.close()
            return taskid
