#cwAsyncThread.py

"""
异步请求的线程基类
author:slg
date:202w/9/10
"""

import multiprocessing
import logging
import asyncio
import json
from aiohttp import ClientSession

if __name__ == '__main__':
    import cwThread as  thread_module
else:
    import sys
    sys.path.append("..")
    import framework.core.concurrent.cwThread as  thread_module

# 异步base thread，继承同步base thread
class cwThread(thread_module.cwThread):
    """ user thread class """
    def __init__(self, out_queue, repeat_count):
        """
        异步请求基础线程
        :param out_queue: 结果输出队列
        :param repeatCount: API线程内重复请求次数
        """
        super().__init__(out_queue, repeat_count)
        # 协程task
        self._tasks = []
        self._client = None
        self._json_headers = {'content-type': "application/json"}

    # 用异步方法用作创建session
    async def create_session(self):
        return ClientSession(headers = self._json_headers)

    # 可以重载此函数，处理结果：协程内异常/正常结果需通过 done_callback 捕获，自动回调
    def done_callback(self, future):
        try:
            if future.exception():
                self.showlog(logging.ERROR, "抛出异常" )
            elif future.cancelled():
                self.showlog(logging.WARN, "请求被取消")
            else:
                if future.result() != None:
                    self.showlog(logging.INFO, "异步请求结果", json.loads(future.result()) )
                    # try:
                    #     result = json.loads(future.result())
                    # except ValueError as e:
                    #     self.showlog(logging.ERROR, "JSON解析失败", str(e))
                else:
                    self.showlog(logging.WARN, "异步请求结果为空")
        except Exception as e:  # 显式捕获连接重置错误
            self.showlog(logging.CRITICAL, f"回调处理发生意外错误: {str(e)}")

    #重写同步base thread类的run方法
    def run(self):
        self.showlog(logging.INFO, "开始线程")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        self._client = asyncio.get_event_loop().run_until_complete(self.create_session())

        if self._repeat_count < 0:
            # 一直循环下去
            while not self._exitflag:
                ret = self.todo_request()
                if not ret:
                    break
        else:
            index = 0
            while index < self._repeat_count and (not self._exitflag):
                ret = self.todo_request()
                if not ret:
                    break
                else:
                    index = index + 1

        #安全终止异步线程，确保任务完成且资源释放
        #无任务时的快速退出
        if len(self._tasks) < 1:
            self.showlog(logging.INFO, "task is empty")
            loop.run_until_complete(self._client.close())
            loop.run_until_complete(asyncio.sleep(3))
            loop.close()
            return
        # asyncio.wait()同时等待多个异步任务
        try:
            loop.run_until_complete(asyncio.wait(self._tasks))
        except KeyboardInterrupt as e:  # 捕获Ctrl+C信号,取消任务
            print(asyncio.Task.all_tasks())
            for task in asyncio.Task.all_tasks():
                print(task.cancel())
            loop.stop()
            loop.run_forever()   # 处理剩余事件（确保取消操作完成）
        finally:
            loop.run_until_complete(self._client.close())
            loop.run_until_complete(asyncio.sleep(3))
            loop.close()

        self.showlog(logging.INFO, "退出线程")

    #创建协程
    def add_coroutine(self, coroutine):
        #:param coroutine: 协程
        # Future表示未来某个时刻会完成的操作,Task是Future 的子类，专门用于包装协程并自动调度执行
        task = asyncio.ensure_future(coroutine)   #确保传入的对象是一个Task 或 Future
        task.add_done_callback( self.done_callback)   #添加完成回调
        self._tasks.append(task)

    def set_json_headers(self, json_headers):
        self._json_headers = json_headers


if __name__ == '__main__':
    outQueue = multiprocessing.JoinableQueue()
    condition_obj = multiprocessing.Condition()
    testObj = cwThread(outQueue, 2)
    testObj.set_condition(condition_obj)

    json_headers = {'content-type': "application/json"}
    testObj.set_json_headers(json_headers)
    testObj.loadimagefiles("d:\\id.jpg")
    testObj.set_debug(True)
    testObj.start()
    testObj.join()