#cwThread.py

"""
通用API
author:slg
date:2022/9/10
"""

import os
import threading
import logging

if __name__ == '__main__':
    import multiprocessing
    import image_utils as comAPI
else:
    import sys
    sys.path.append("..")
    import image_utils.common as comAPI

# 同步base thread，具体业务需重载todo_request
class cwThread(threading.Thread):
    """ user thread class """
    def __init__(self, out_queue, repeat_count=1):
        """
        同步请求基础线程
        :param out_queue: 结果输出队列
        :param repeatCount: API线程内重复请求次数
        """
        threading.Thread.__init__(self)
        self._out_queue = out_queue
        self._repeat_count = repeat_count
        self._name = "PID-" + str(os.getpid()) + "-TID-" + str(threading.currentThread().ident) #线程识别号
        self._exitflag = False
        self._url = ""
        self._imagelist = []
        self._debug = False
        self._log_level = logging.INFO
        self._log_dict = {}

    def run(self):
        self.showlog(logging.INFO, "开始线程")

        if self._repeat_count < 0:
            # 一直循环下去
            while not self.exitflag:
                ret = self.todo_request()
                if not ret:
                    break
        else:
            index = 0
            while index < self._repeat_count and (not self.exitflag):
                ret = self.todo_request()
                if not ret:
                    break
                else:
                    index = index + 1

        self.showlog(logging.INFO, "退出线程")

    # 运行自定义请求任务, 重载一下实现具体任务
    # return: bool类型
    def todo_request(self):
        self.showlog(logging.INFO, "需要重载todo_request()，实现实际功能")
        return True

    # 保存log，保持日志到multiprocessing.JoinableQueue()
    def showlog(self, level, title,  *args):
        """
        :param level: level 等级
        :param title: 内容描述
        :param args: 不定个数的结果
        :return:
        """
        if level <= self._log_level and self._out_queue != None:
            self._log_dict.clear()
            self._log_dict["title"] = self._name + " " + title

            if len(args) > 0:
                for content in args:
                    self._condition_obj.acquire()
                    try:
                        if self._debug:
                            print(self._name + " " + title + " " + str(content))
                        else:
                            self._log_dict["content"] = content
                            self._out_queue.put(self._log_dict)
                            self._condition_obj.notify_all()
                    finally:
                        self._condition_obj.release()
            else:
                self._condition_obj.acquire()
                try:
                    if self._debug:
                        print(self._name + " " + title)
                    else:
                        self._out_queue.put(self._log_dict)
                        self._condition_obj.notify_all()
                finally:
                    self._condition_obj.release()

    # 加载文件
    def loadimagefiles(self, file, splitcount=0, index=0):
        """
        :param file: 图片文件或文件夹
        :param splitcount: 拆分个数，表示查询到的文件列表拆分子列表的个数，0表示不拆分，file是文件夹时才有效
        :param index: 获取子列表的索引，从0开始，index < splitcount才合法，，file是文件夹时才有效
        :return ：本次加载图片到列表文件个数， -1表示异常或参数错误
        """
        if os.path.isfile(file):
            # 单个文件
            if comAPI.is_image_file(file):
                self._imagelist.append(file)
                return 1
            else:
                return 0
        elif os.path.isdir(file):
            #文件夹
            ls = comAPI.folders_list_images(file)
            if len(ls) < 0:
                return 0
            if splitcount == 0:
                # 不拆分
                self._imagelist = self._imagelist + ls
                return len(ls)
            elif splitcount >= 1 and index>= 0 and index < splitcount:
                sublists = comAPI.round_robin_sublists(ls, splitcount)
                self._imagelist = self._imagelist + sublists[index]
                return len(sublists[index])
            else:
                # splitcount参数异常
                return -1
        else:
            return -1

    # Exit Flag
    @property
    def exitflag(self):
        """ Get Exit Thread Flag"""
        return self._exitflag

    def set_exit(self, is_exit):
        """ Set Exit Thread Flag"""
        self._exitflag = is_exit


    @property
    def loglevel(self):
        return self._log_level

    def set_log_level(self, level):
        self._log_level = level

    # API URL
    @property
    def url(self):
        return self._url

    def set_url(self, url):
        self._url = url


    def set_condition(self, condition_obj):
        self._condition_obj = condition_obj

    def set_out_queue(self, out_queue):
        self._out_queue = out_queue


    def set_debug(self, isdebug):
        self._debug = isdebug


if __name__ == '__main__':
    outQueue = multiprocessing.JoinableQueue()
    condition_obj = multiprocessing.Condition()
    testObj = cwThread(outQueue, 2)
    testObj.set_condition(condition_obj)
    testObj.loadimagefiles("d:\\id.jpg")
    testObj.set_debug(False)
    testObj.start()
    testObj.join()