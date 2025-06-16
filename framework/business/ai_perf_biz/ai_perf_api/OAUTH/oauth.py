"""
@User:  slg
@Time: 2021/8/27
"""
import uuid
from urllib import parse
import time
import sys
sys.path.append("..")
import common.cwRequests as httpRequests
if __name__ == '__main__':
    import cryptSMx as crypt
else:
    import OAUTH.cryptSMx as crypt

class oauth(httpRequests.cwRequests):
    def get_token(self, url, appkey, appsecret):
        # 返回dict类型
        HEADERS = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
        payload_1 = {'grant_type': 'client_credentials', 'client_id': appkey, 'client_secret': appsecret}
        data = parse.urlencode(payload_1)
        self.post(url, data, HEADERS)
        return self.get_data()

    def get_access_param(self, access_token, appSecret):
        _time = str(round(time.time() * 1000))
        _nonce = str(uuid.uuid1()).replace('-', '')
        _sign = crypt.sm3_hash(_time + _nonce + access_token + appSecret)
        encrypt_params = {
            'access_token': access_token,
            'timestamp': _time,
            'nonce': _nonce,
            'sign': _sign
        }
        self.set_data(encrypt_params)
        return True

    def get_access_paramEx(self, url, appkey, appsecret):
        result_data = self.get_token(url, appkey, appsecret)
        if result_data["result"]:
            data = result_data["data"]
            self.get_access_param(data["access_token"], appsecret)
            return True
        else:
            return False

# for test
if __name__ == '__main__':
    sso = oauth()
    url = "http://developercenter-tf-test.cloudwalk.work/sso/oauth/token"
    ret = sso.get_access_paramEx(url, "67b05ab60d4e4e329bcc5db895e9e620", "0630402006ba4ac6aaa003b8abb6e9c3")
    if ret:
        print(sso.get_data())
    else:
        print(sso.get_error())