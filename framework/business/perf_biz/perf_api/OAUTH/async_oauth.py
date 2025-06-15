# async_oauth.py
"""
异步请求认证
author:heye
"""

import uuid
from urllib import parse
from time import time
import sys
sys.path.append("..")
import common.common as comAPI
import common.cwAsyncRequests as http
if __name__ == '__main__':
    import cryptSMx as crypt
else:
    import OAUTH.cryptSMx as crypt


class oauth(http.cwRequests):
    #异步请求
    async def get_token(self, url, appkey, appsecret):
        payload_1 = {'grant_type': 'client_credentials', 'client_id': appkey, 'client_secret': appsecret}
        json_str = parse.urlencode(payload_1)  #生成一个符合 URL 查询字符串格式的字符串：如 key1=value1&key2=value2
        return await self.post(url, json_str)

    def get_access_param(self, access_token, appSecret):
        _time = str(round(time() * 1000))
        _nonce = str(uuid.uuid1()).replace('-', '')   #uuid1()基于当前时间戳和主机MAC地址生成唯一的随机字符串
        _sign = crypt.sm3_hash(_time + _nonce + access_token + appSecret)
        encrypt_params = {
            'access_token': access_token,
            'timestamp': _time,
            'nonce': _nonce,
            'sign': _sign
        }
        self.set_data(encrypt_params)
        return True
