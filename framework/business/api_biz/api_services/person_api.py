#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author:  slg
@Time: 2022/10/18
@File: person_api
"""
from framework.core.http.http_client import api
from framework.utils.get_ini_conf import Conf


class PersonApi():
    '''
    行人行为接口
    '''
    _roi_set = Conf().get_str('task_api', 'person_roi')
    _task_set = Conf().get_str('task_api', 'person_set')
    _task_del = Conf().get_str('task_api', 'person_del')


    @api.mark(module='ocean')
    @api.http.post(path=_roi_set)
    def person_roi_api(self, data):
        '''
        头肩解析roi设置
        :param data:
        :return:
        '''
        return dict(json=data)

    @api.mark(module='ocean')
    @api.http.post(path=_task_set)
    def person_set_api(self, data):
        '''
        设置头肩解析任务
        :param: data
        :return:
        '''
        return dict(json=data)

    @api.mark(module='ocean')
    @api.http.post(path=_task_del)
    def person_del_api(self, data):
        '''
        删除头肩解析任务
        :param data:
        :return:
        '''
        return dict(json=data)