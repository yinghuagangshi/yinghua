# cwRequests.py

"""
通用API
author:slg
date:2022/9/10
"""

import requests
import time

# 同步base http request
class cwRequests:
    """ http request api """
    def __init__(self):
        # _result_data各字段介绍
        """
        result：请求结果boolean类型
        time_span：请求时长，单位为秒
        message：错误信息描述
        data：API请求返回值
        """
        self._result_data = {}
        self._result_data["result"] = False
        self._result_data["time_span"] = 0

    # get，统计响应时间
    def get(self, url, json_data, json_headers):
        self._result_data["result"] = False
        preTime = time.time()

        try:
            r = requests.get(url, timeout=30, data=json_data, headers=json_headers, allow_redirects=False)
            self._result_data['status'] = r.status_code
            if r.status_code == requests.codes.ok:
                self._result_data["result"] = True
                self._result_data["data"] = r.json()
            else:
                self._result_data["message"] = str(r);
        except requests.exceptions.ConnectionError as ece:  # 未知的服务器
            self._result_data["message"] = "Connection Error:" + str(ece)
        except requests.exceptions.Timeout as et:
            self._result_data["message"] = "Timeout Error:" + str(et)
        except requests.exceptions.RequestException as e:
            self._result_data["message"] = "Some Ambiguous Exception:" + str(e)
        except requests.exceptions.ConnectTimeout as e:  # 连接超时
            self._result_data["message"] = "ConnectTimeout Error:" + str(e)
        except requests.exceptions.ReadTimeout as e:  # 连接、读取超时
            self._result_data["message"] = "ReadTimeout Error:" + str(e)
        except requests.exceptions.ProxyError as e:  # 代理连接不上
            self._result_data["message"] = "Proxy Error:" + str(e)
        except:
            self._result_data["message"] = "未知错误"
            r.raise_for_status()
        finally:
            curTime = time.time()

        #self._result_data["time_span"] = '{:.3f}'.format(curTime - preTime)
        self._result_data["time_span"] = round(curTime - preTime, 3)
        return self._result_data["result"]


    # post，统计响应时间
    def post(self, url, json_data, json_headers):
        self._result_data["result"] = False
        preTime = time.time()

        try:
            r = requests.post(url, timeout=30, data=json_data, headers=json_headers, allow_redirects=False)
            self._result_data['status'] = r.status_code
            if r.status_code == requests.codes.ok:
                self._data = r.json()
                self._result_data["result"] = True
                self._result_data["data"] = r.json()
            else:
                self._result_data["message"] = str(r)
        except requests.exceptions.ConnectionError as ece:  # 未知的服务器
            self._result_data["message"] = "Connection Error:" + str(ece)
        except requests.exceptions.Timeout as et:
            self._result_data["message"] = "Timeout Error:" + str(et)
        except requests.exceptions.RequestException as e:
            self._result_data["message"] = "Some Ambiguous Exception:" + str(e)
        except requests.exceptions.ConnectTimeout as e:  # 连接超时
            self._result_data["message"] = "ConnectTimeout Error:" + str(e)
        except requests.exceptions.ReadTimeout as e:  # 连接、读取超时
            self._result_data["message"] = "ReadTimeout Error:" + str(e)
        except requests.exceptions.ProxyError as e:  # 代理连接不上
            self._result_data["message"] = "Proxy Error:" + str(e)
        except:
            self._result_data["message"] = "未知错误"
            r.raise_for_status()
        finally:
            curTime = time.time()

        self._result_data["time_span"] = round(curTime - preTime, 3)
        return self._result_data["result"]

    def get_data(self):
        return self._result_data

    def set_data(self, data):
        self._result_data["data"] = data

    def get_error(self):
        return self._result_data["message"]

    def set_error(self, msg):
        self._result_data["message"] = msg


if __name__ == '__main__':
    json_data = {'img': 'aaaaaa'}
    json_headers = {'content-type': "application/json"}
    url = "http://localhost:5000/ocr/idcard"
    testObj = cwRequests()
    ret = testObj.get(url, json_data, json_headers)
    print(testObj.get_data())