# oauthThread.py
"""
request thread
多线程内部开启http同步请求
"""

import logging
import sys
sys.path.append("..")
import common.cwThread as  thread_module
if __name__ == '__main__':
    import multiprocessing
    import oauth as auth
else:
    import OAUTH.oauth as auth


class authThread(thread_module.cwThread):
    _appkey = ""
    _appsecret = ""

    def todo_request(self):
        # 身份认证
        result = True
        authObj = auth.oauth()

        self.showlog(logging.INFO, "开启请求")

        result = authObj.get_access_paramEx(self.url, self._appkey, self._appsecret)
        if not result:
            self.showlog(logging.ERROR, "请求错误", authObj.get_error())
        else:
            self.showlog(logging.INFO, "请求结果", authObj.get_data())
        return result

    def set_account(self, appkey, appsecret):
        self._appkey = appkey
        self._appsecret = appsecret

#for test
if __name__ == '__main__':
    appkey = "67b05ab60d4e4e329bcc5db895e9e620"
    appsecret = "0630402006ba4ac6aaa003b8abb6e9c3"
    outQueue = multiprocessing.JoinableQueue()
    condition_obj = multiprocessing.Condition()
    myThread = authThread(outQueue, 2 )
    myThread.set_condition(condition_obj)
    myThread.set_account(appkey, appsecret)
    myThread.set_url("http://developercenter-tf-test.cloudwalk.work/sso/oauth/token")
    myThread.set_debug(True)
    myThread.start()
    myThread.join()