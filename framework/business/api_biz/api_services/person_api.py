#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author:  chaozhongze
@Time: 2021/10/18
@File: person_api
"""
from comm.api_fun import ApiFun
from comm.get_conf import Conf


class PersonApi():
    '''
    行人行为接口
    '''
    _roi_set = Conf().get_str('task_api', 'person_roi')
    _task_set = Conf().get_str('task_api', 'person_set')
    _task_del = Conf().get_str('task_api', 'person_del')

    def person_roi_api(self, data):
        '''
        头肩解析roi设置
        :param data:
        :return:
        '''
        path = self._roi_set
        res = ApiFun().send_post(path, data)
        return res

    def person_set_api(self, data):
        '''
        设置头肩解析任务
        :param: data
        :return:
        '''
        path = self._task_set
        res = ApiFun().send_post(path, data)
        return res

    def person_del_api(self, data):
        '''
        删除头肩解析任务
        :param data:
        :return:
        '''
        path = self._task_del
        res = ApiFun().send_post(path, data)
        return res