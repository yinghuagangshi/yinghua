# async_multiThread.py
"""
request thread
线程内异步调用http
"""

import logging
import sys
sys.path.append("..")
import common.cwAsyncThread as thread_module1

if __name__ == '__main__':
    import multiprocessing
    import async_ocr as ocr
else:
    import OCR.async_ocr as ocr

# 继承异步Thread类，todo_request调用异步ocr
class ocrThread(thread_module1.cwThread):
    #重载
    def todo_request(self):
        ocrObj = ocr.ocr(self._client)

        self.showlog(logging.INFO, "开启请求识别")

        for f in self._imagelist:
            # 创建协程
            coroutine = ocrObj.read(self._url, f)
            super().add_coroutine(coroutine)

        return True

#for test
if __name__ == '__main__':
    outQueue = multiprocessing.JoinableQueue()
    condition_obj = multiprocessing.Condition()
    myThread = ocrThread(outQueue, 2)
    myThread.set_url("http://10.128.162.176:32345/ocr/idcard")
    myThread.loadimagefiles("D:\\id.jpg")
    myThread.set_condition(condition_obj)
    myThread.set_debug(True)
    myThread.start()
    myThread.join()