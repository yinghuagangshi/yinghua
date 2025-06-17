# ocrThread.py
"""
request thread
多线程内部开启http同步请求
"""

import logging
import sys
sys.path.append("..")
import framework.core.concurrent.cwThread as  thread_module

if __name__ == '__main__':
    import multiprocessing
    import ocr
else:
    import framework.business.ai_perf_biz.ai_perf_api.OCR.ocr as ocr

# 继承同步base thread，调用同步ocr
class ocrThread(thread_module.cwThread):
    def todo_request(self):
        # 识别身份证照
        result = True
        ocrObj = ocr.ocr()

        super().showlog(logging.INFO, "开启请求识别")

        for f in self._imagelist:
            result = ocrObj.read(self.url, f)
            if not result:
                self.showlog(logging.ERROR, "请求错误", ocrObj.get_error())
                continue
            else:
                super().showlog(logging.INFO, "识别结果", ocrObj.get_data())
        return result

#for test
if __name__ == '__main__':
    outQueue = multiprocessing.JoinableQueue()
    condition_obj = multiprocessing.Condition()
    myThread = ocrThread(outQueue, 2 )
    myThread.set_url("http://10.128.162.176:32345/ocr/idcard")
    myThread.loadimagefiles("D:\\id.jpg")
    myThread.set_condition(condition_obj)
    myThread.set_debug(True)
    myThread.start()
    myThread.join()