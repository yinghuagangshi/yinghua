#cwAsyncRequests class
# http异步请求

import json
import time


# 异步base http request
class cwRequests:
    """ http request api """
    def __init__(self, client):
        """
        异步请求基础类
        :param client: ClientSession
        """
        self._client = client
        self._result_data = {}
        self._result_data["result"] = False
        self._result_data["time_span"] = 0

    #get
    async def get(self, url, json_str):
        self._result_data['result'] = False
        preTime = time.time()
        try:
            async with self._client.get(url, data = json_str, allow_redirects=False) as response:
                self._result_data['status'] = response.status
                if response.status == 200:
                    self._result_data['result'] = True
                    self._result_data['data'] = json.loads(await response.text())
                else:
                    self._result_data['message'] = str(response);
        except Exception as e:
            self._result_data['message'] = str(e)
            self._result_data['status'] = e.errno
        finally:
            self._result_data["time_span"] = round(time.time() - preTime, 3)
            json_data = json.dumps(self._result_data)
            return json_data

    # post
    async def post(self, url, json_str):
        self._result_data['result'] = False
        preTime = time.time()
        try:
            async with self._client.post(url, data = json_str, allow_redirects=False) as response:
                self._result_data['status'] = response.status
                if response.status == 200:
                    self._result_data['result'] = True
                    self._result_data['data'] = await response.text()
                else:
                    self._result_data['message'] = str(response);
        except Exception as e:
            self._result_data['message'] = str(e)
            self._result_data['status'] = e.errno
        finally:
            self._result_data["time_span"] = round(time.time() - preTime, 3)
            json_data = json.dumps(self._result_data)
            return json_data

    def get_data(self):
        return self._result_data

    def set_data(self, data):
        self._result_data["data"] = data

    def get_error(self):
        return self._result_data["message"]

    def set_error(self, msg):
        self._result_data["message"] = msg