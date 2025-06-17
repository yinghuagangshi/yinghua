#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from framework.core.http.http_client import api
from framework.utils.get_ini_conf import Conf
from logger import logger

device_pages = Conf().get_str('device_api', 'camera_list')

@api.mark(module='ocean')
@api.http.post(path=device_pages)
def deviceid(data):
    '''
    相机管理列表获取设备id
    '''
    return dict(json=data)
