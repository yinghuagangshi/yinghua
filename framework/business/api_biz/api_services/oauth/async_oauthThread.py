# async_oauthThread.py
"""
request thread
多线程内部开启 http异步请求
author:heye
"""


import logging
import json
import sys
sys.path.append("..")
import common.cwAsyncThread as thread_module1

if __name__ == '__main__':
    import multiprocessing
    import async_oauth as auth
else:
    import OAUTH.async_oauth as auth


class authThread(thread_module1.cwThread):
    _appkey = ""
    _appsecret = ""

    #重载
    def todo_request(self):
        self._authObj = auth.oauth(self._client)

        self.showlog(logging.INFO, "开启请求")

        coroutine = self._authObj.get_token(self.url, self._appkey, self._appsecret)
        self.add_coroutine(coroutine)
        return True

    # 重载，需要处理结果数据
    def done_callback(self, future):
        if future.exception():
            self.showlog(logging.ERROR, "抛出异常" )
        elif future.cancelled():
            self.showlog(logging.WARN, "请求被取消")
        else:
            if future.result() != None:
                data = json.loads(future.result())
                if data['result']:
                    auth_data = json.loads(data['data'])
                    token = auth_data["access_token"]
                    self._authObj.get_access_param(token, self._appsecret)
                    result_data = self._authObj.get_data()
                    self.showlog(logging.INFO, "异步请求结果", result_data )
                else:
                    self.showlog(logging.INFO, "异步请求结果", data)
            else:
                self.showlog(logging.WARN, "异步请求结果为空")

    def set_account(self, appkey, appsecret):
        self._appkey = appkey
        self._appsecret = appsecret


#for test
if __name__ == '__main__':
    outQueue = multiprocessing.JoinableQueue()
    condition_obj = multiprocessing.Condition()
    myThread = authThread(outQueue, 2)
    myThread.set_condition(condition_obj)
    myThread.set_url("http://developercenter-tf-test.cloudwalk.work/sso/oauth/token")
    myThread.set_account("67b05ab60d4e4e329bcc5db895e9e620", "0630402006ba4ac6aaa003b8abb6e9c3")
    HEADERS = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
    myThread.set_json_headers(HEADERS)
    myThread.set_debug(True)
    myThread.start()
    myThread.join()