# This is a multi process Python script.
# author: slg
# date: 2022/9/10
import json
import multiprocessing
import queue
import os
import time
#import affinity #for linux
# need pip install pypiwin32 #for windows
import win32process
import win32api
import optionRequest

"""
pip install pypiwin32
PACKAGE CONTENTS
    _win32sysloader
    _winxptheme
    mmapfile
    odbc
    perfmon
    servicemanager
    timer
    win2kras
    win32api
    win32clipboard
    win32console
    win32cred
    win32crypt
    win32event
    win32evtlog
    win32file
    win32gui
    win32help
    win32inet
    win32job
    win32lz
    win32net
    win32pdh
    win32pipe
    win32print
    win32process
    win32profile
    win32ras
    win32security
    win32service
    win32trace
    win32transaction
    win32ts
    win32wnet
    winxpgui
"""

class WriteLogProcess(multiprocessing.Process):
    def __init__(self, condition_obj, outQueue):
        multiprocessing.Process.__init__(self)
        self._outQueue = outQueue
        self._condition_obj = condition_obj
        self.exit = multiprocessing.Event()

    def shutdown(self):
        self.exit.set()
        print("WriteLogProcess Shutdown")

    def run(self):
        print("开始保存log进程" )
        root = os.getcwd()
        file_name = root + "\\pineapple" + time.strftime("%Y-%m-%d", time.localtime()) + ".log"
        f = open(file_name, 'a')

        count = 0
        min = 3600
        max = 0
        while not self.exit.is_set():
            try:
                dict = self._outQueue.get(timeout=3)
                if len(dict) > 0:
                    showText = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " " + str(dict)
                    print(showText)
                    f.write(showText + "\n")
                    f.flush()
                    # 统计分析数据
                    if "content" in dict:
                        con_dict = dict["content"]
                        if "result" in con_dict and con_dict["result"]:
                            if "time_span" in  con_dict and "status" in con_dict and con_dict["status"] == 200:
                                count = count + 1
                                if con_dict["time_span"] < min:
                                    min = con_dict["time_span"]
                                if con_dict["time_span"] > max:
                                    max = con_dict["time_span"]
                self._outQueue.task_done()
            except queue.Empty as e:
                time.sleep(1)
                #self._condition_obj.wait()
        f.close()

        print("count:" + str(count) + ", min time_span:" + str(min) + ", max time_span:" + str(max))

        print("WriteLogProcess exited!")


class WorkProcess(multiprocessing.Process):
    def __init__(self, request_type, index, condition_obj, outQueue, **args):
        multiprocessing.Process.__init__(self)
        self._condition_obj = condition_obj
        self._outQueue = outQueue
        self._request_type = request_type
        # 绑定到对应的CPU, 需要考虑防止超出CPU数量
        process_count = args["process_count"]
        index = index % process_count
        self._cpu = 1<<index
        self.args = args

    def run(self):
        # 绑定到对应的逻辑CPU，需要考虑超出CPU数量绑定失败以及自动匹配平台
        #windows
        win32process.SetProcessAffinityMask(win32api.GetCurrentProcess(), self._cpu)
        #linux
        # affinity.set_process_affinity_mask(os.getpid(), self._cpu)

        # 创建线程
        thread_pool = []
        for i in range(self.args["thread_count"]):
            myThread = optionRequest.choice(self._request_type, self._outQueue, self._condition_obj, **self.args)
            thread_pool.append(myThread)

        for t in thread_pool:
            t.start()
        for t in thread_pool:
            t.join()
        thread_pool.clear()

# 开启多进程多线程请求调用访问
def StartMultiRequest(request_type, **args):
    """
    开启多进程多线程请求调用访问
    :param request_type: 功能类别
    :param processCount: 进程数量， 默认-1，表示自动采用CPU内核数
    :param threadCount: 单进程内的线程数量，总线程数量是processCount * threadCount
    :param repeatCount: API线程内重复请求次数
    :param is_async:是否异步请求
    """
    thread_count = args["thread_count"]
    if thread_count < 1:
        print("参数不合法")
        return None

    # 信息接收queue
    outQueue = multiprocessing.JoinableQueue()
    process_pool = []

    process_count = multiprocessing.cpu_count()
    if args["process_count"] > 0:
        process_count = args["process_count"]
    args["process_count"] = process_count

    print("进程数量：" + str(process_count) + " 总线程数量：" + str(process_count*thread_count))

    condition_obj = multiprocessing.Condition()
    logProcess = WriteLogProcess(condition_obj, outQueue)
    logProcess.start()

    for i in range(process_count):
        p = WorkProcess(request_type, i, condition_obj, outQueue, **args)
        process_pool.append(p)

    for p in process_pool:
        p.start()
    for p in process_pool:
        p.join()
    process_pool.clear()

    print("工作进程完成工作")
    logProcess.shutdown()

    print("notify_all")
    condition_obj.acquire()
    condition_obj.notify_all()
    condition_obj.release()

    print("outQueue.join")
    outQueue.join()

    print("logProcess.join")
    logProcess.join()

    print("main exit")


if __name__ == '__main__':
    args = {} #参数字典
    request_type = "OAUTH"

    args["process_count"] = -1  # 进程数，-1采用默认CPU内核数
    args["thread_count"] = 8    # 每个进程内部创建线程数
    args["repeat_count"] = 1    # 一个线程内部重复请求次数
    args["is_async"] = True     # http异步请求还是同步请求

    if request_type == "OCR":
        args["url"] = "http://10.128.162.176:32345/ocr/idcard"
        args["image_files"] = "D:\\id.jpg"  #目录或单张图片
    else:
        args["url"] = "http://developercenter-tf-test.cloudwalk.work/sso/oauth/token"
        args["appkey"] = "67b05ab60d4e4e329bcc5db895e9e620"
        args["appsecret"] = "0630402006ba4ac6aaa003b8abb6e9c3"

    StartMultiRequest(request_type, **args)