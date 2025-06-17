# This is a multi process Python script.
# author: slg
# date: 2022/9/10
import json
import multiprocessing
import queue
import os
import time
from pathlib import Path
#import affinity #for linux
# need pip install pypiwin32 #for windows
# import win32process
# import win32api
import psutil
import platform
from framework.core.concurrent import optionRequest
from framework.core.runners.systemMonitor import SystemMonitor
from framework.core.runners.algorithm_metrics import  AlgorithmMetrics

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
    def __init__(self, condition_obj, outQueue,label_file_path=None):
        multiprocessing.Process.__init__(self)
        self._outQueue = outQueue
        self._condition_obj = condition_obj
        self.exit = multiprocessing.Event()

        self.last_monitor_time = 0  # 最后监控时间记录
        # 统计数据结构
        self.stats = {
            "total_requests": 0,
            "success_requests": 0,
            "failed_requests": 0,
            "request_times": []
        }

        # 算法指标统计
        self.algorithm_metrics = AlgorithmMetrics(label_file_path) if label_file_path else None

    def shutdown(self):
        self.exit.set()
        print("WriteLogProcess Shutdown")

    def update_stats(self, result_dict):
        """更新请求统计数据"""
        if "content" in result_dict:
            self.stats["total_requests"] += 1
            content = result_dict["content"]
            if content.get("result", False):
                self.stats["success_requests"] += 1
                if "time_span" in content and content.get("status") == 200:
                    self.stats["request_times"].append(content["time_span"])
            else:
                self.stats["failed_requests"] += 1

            # 更新算法指标
            if self.algorithm_metrics:
                self.algorithm_metrics.update(content)

    def get_performance_summary(self):
        """获取性能摘要"""
        summary = {
            "success_rate": 0,
            "avg_time": 0,
            "min_time": 0,
            "max_time": 0,
            "throughput": 0
        }

        if self.stats["request_times"]:
            total_time = sum(self.stats["request_times"])
            avg_time = total_time / len(self.stats["request_times"])

            summary.update({
                "success_rate": self.stats["success_requests"] / self.stats["total_requests"] * 100,
                "avg_time": avg_time,
                "min_time": min(self.stats["request_times"]),
                "max_time": max(self.stats["request_times"]),
                "throughput": self.stats["total_requests"] / self.monitor.get_summary()["total_time"] if
                self.monitor.get_summary()["total_time"] > 0 else 0
            })

        # 增加算法指标
        if self.algorithm_metrics:
            summary["algorithm_metrics"] = self.algorithm_metrics.get_summary()

        return summary


    def run(self):
        self.monitor = SystemMonitor()  # 系统监控类

        print("开始保存log进程" )
        project_root = Path(__file__).parents[3]
        logs_dir = project_root / "logs"
        log_file = logs_dir / ("pineapple_" + time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) + ".log")
        perf_file = logs_dir / ("performance_" + time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) + ".json")

        with open(log_file, 'a', encoding='utf-8') as f, open(perf_file, 'a', encoding='utf-8') as pf:
            while not self.exit.is_set():
                try:
                    # 定期记录系统资源使用情况
                    current_time = time.time()
                    if current_time - self.last_monitor_time >= 5:
                        monitor_data = self.monitor.update()
                        pf.write(json.dumps({"type": "monitor", "data": monitor_data}) + "\n")
                        pf.flush()
                        self.last_monitor_time = current_time

                    # 处理请求日志
                    result_dict = self._outQueue.get(timeout=3)
                    if result_dict:
                        # 结构化日志记录
                        showText = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " " + str(result_dict)
                        f.write(json.dumps(showText) + "\n")
                        f.flush()

                        # 更新性能统计
                        self.update_stats(result_dict)
                        pf.write(json.dumps({"type": "request", "data": result_dict}) + "\n")
                        pf.flush()

                    self._outQueue.task_done()
                except queue.Empty as e:
                    time.sleep(1)
                    #self._condition_obj.wait()

            # 测试结束，写入总结数据
            summary = {
                "resource_usage": self.monitor.get_summary(),
                "performance": self.get_performance_summary(),
                "request_stats": self.stats
            }

            pf.write(json.dumps({"type": "summary", "data": summary}) + "\n")
            pf.flush()

            # 摘要输出
            print("\n=== 性能测试摘要 ===")
            print(f"总请求数: {self.stats['total_requests']}")
            print(f"成功请求: {self.stats['success_requests']}")
            print(f"失败请求: {self.stats['failed_requests']}")
            print(f"成功率: {summary['performance']['success_rate']:.2f}%")
            print(f"平均响应时间: {summary['performance']['avg_time']:.3f}秒")
            print(f"最小响应时间: {summary['performance']['min_time']:.3f}秒")
            print(f"最大响应时间: {summary['performance']['max_time']:.3f}秒")
            print(f"吞吐量: {summary['performance']['throughput']:.2f} 请求/秒")
            print(f"平均CPU使用率: {summary['resource_usage']['avg_cpu']:.1f}%")
            print(f"峰值CPU使用率: {summary['resource_usage']['max_cpu']:.1f}%")
            print(f"平均内存使用: {summary['resource_usage']['avg_memory']:.2f}MB")
            print(f"峰值内存使用: {summary['resource_usage']['max_memory']:.2f}MB")
            print(f"总测试时间: {summary['resource_usage']['total_time']:.2f}秒")

            # 算法指标输出
            if self.algorithm_metrics:
                alg_metrics = summary['performance'].get('algorithm_metrics', {})
                if alg_metrics:
                    print("\n=== 算法指标 ===")
                    print(f"精确率(Precision): {alg_metrics.get('precision', 0):.4f}")
                    print(f"召回率(Recall): {alg_metrics.get('recall', 0):.4f}")
                    print(f"F1分数: {alg_metrics.get('f1_score', 0):.4f}")
                    print(f"平均IoU: {alg_metrics.get('avg_iou', 0):.4f}")
                    print(f"真正例(TP): {alg_metrics.get('true_positives', 0)}")
                    print(f"假正例(FP): {alg_metrics.get('false_positives', 0)}")
                    print(f"假反例(FN): {alg_metrics.get('false_negatives', 0)}")

        print("WriteLogProcess exited!")


class WorkProcess(multiprocessing.Process):
    def __init__(self, request_type, index, condition_obj, outQueue, **args):
        multiprocessing.Process.__init__(self)
        self._condition_obj = condition_obj
        self._outQueue = outQueue
        self._request_type = request_type
        self.args = args

        # 绑定到对应的CPU, 需要考虑防止超出CPU数量
        # process_count = args["process_count"]
        physical_cores = psutil.cpu_count(logical=False) or psutil.cpu_count(logical=True)
        index = index % physical_cores
        self.cpu_mask = 1<<index

    def run(self):
        # 绑定到对应的CPU
        try:
            if platform.system() == "Windows":
                import win32process
                import win32api
                win32process.SetProcessAffinityMask(win32api.GetCurrentProcess(),self.cpu_mask)
            elif platform.system() == "Linux":
                try:
                    import affinity
                    affinity.set_process_affinity_mask(os.getpid(), self.cpu_mask)
                except ImportError:
                    # 回退到Python原生方法
                    os.sched_setaffinity(os.getpid(), [bin(self.cpu_mask).count('1') - 1])
            else:
                print(f"警告：不支持的操作系统 {platform.system()}，跳过CPU绑定")
        except PermissionError:
            print("错误：没有足够的权限设置CPU亲和性")
        except Exception as e:
            print(f"设置CPU亲和性失败: {e}")

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
    :param label_file: 标签文件路径(可选)
    """
    thread_count = args["thread_count"]
    if thread_count < 1:
        print("参数不合法")
        return None

    # 信息接收queue
    outQueue = multiprocessing.JoinableQueue()
    process_pool = []

    process_count = psutil.cpu_count(logical=False) or psutil.cpu_count(logical=True)
    if args["process_count"] > 0:
        process_count = args["process_count"]
    args["process_count"] = process_count

    print("进程数量：" + str(process_count) + " 总线程数量：" + str(process_count*thread_count))

    condition_obj = multiprocessing.Condition()
    logProcess = WriteLogProcess(condition_obj, outQueue,args.get("label_file"))
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

    print("main exit，测试完成")


if __name__ == '__main__':
    args = {} #参数字典
    request_type = "OCR"

    args["process_count"] = -1  # 进程数，-1采用默认CPU内核数
    args["thread_count"] = 2    # 每个进程内部创建线程数
    args["repeat_count"] = 1    # 一个线程内部重复请求次数
    args["is_async"] = True    # http异步请求还是同步请求

    if request_type == "OCR":
        args["url"] = "http://localhost:5000/ocr/carplate"
        args["image_files"] = r"E:\自动化\auto_2025\yinghua\data\ai_perf\images"  #目录或单张图片
        args["label_file"] = r"E:\自动化\auto_2025\yinghua\data\ai_perf\labels\labels.txt"
    else:
        args["url"] = "http://localhost:5000/sso/oauth/token"
        args["appkey"] = "67b05ab60d4e4e329bcc5db895e9e620"
        args["appsecret"] = "0630402006ba4ac6aaa003b8abb6e9c3"

    StartMultiRequest(request_type, **args)