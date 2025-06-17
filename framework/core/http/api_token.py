#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import random
import requests
import string
import sys
import time
from loguru import logger
from sm3md5encoder import Encode

from control import GLOBAL_USERINFO
from get_conf import Conf


class ApiFun():
    '''
    该模块主要是用于接口的公用方法
    '''
    _host = Conf().get_str('developer_center', 'url')
    _get_token = Conf().get_str('login', 'get_token')

    def __init__(self):
        self.userKey = GLOBAL_USERINFO["appKey"]
        self.Secret = GLOBAL_USERINFO["appSecret"]
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.userKey,
            'client_secret': self.Secret
        }

        # 获取token
        # print(data)
        ac_token = requests.post(url=self._host + self._get_token, data=data).json()['access_token']
        # 13位时间戳
        timestamp = str(int(time.time() * 1000))
        # 随机字符串
        nonce = ''.join(random.sample(string.ascii_letters + string.digits, 32))
        # 客户端秘钥
        appkey = self.Secret
        # 获取sgin
        sgin = Encode.SM3(timestamp + nonce + ac_token + appkey)
        # 拼接
        self.path = f'?token={ac_token}&timestamp={timestamp}&nonce={nonce}&sign={sgin}'
        # print(self.path)

    def send_post(self, path, data):
        url = self._host + path + self.path
        logger.info(f'开始发送post请求')
        logger.info(f'请求url:{url}，请求参数：{data}')
        try:
            res = requests.post(url=url, json=data,headers={"Content-Type":"application/json"})

        except Exception as e:
            logger.error('请求发送失败')
            raise e
        else:
            logger.info(f'响应结果为：{res.json()}')
            return res.json()



