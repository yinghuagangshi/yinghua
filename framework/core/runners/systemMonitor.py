import time
import psutil
import os

class SystemMonitor:
    """系统资源监控类"""

    def __init__(self):
        self.start_time = time.time()
        self.cpu_usage = []
        self.memory_usage = []
        self.network_io = []
        self.disk_io = []
        self.process = psutil.Process(os.getpid())

    def update(self):
        """更新监控数据"""
        # CPU使用率
        cpu_percent = psutil.cpu_percent(interval=1)
        # 内存使用
        memory_info = self.process.memory_info()
        memory_mb = memory_info.rss / (1024 * 1024)  # 转换为MB
        # 网络IO
        net_io = psutil.net_io_counters()
        # 磁盘IO
        disk_io = psutil.disk_io_counters()

        # 记录数据
        self.cpu_usage.append(cpu_percent)
        self.memory_usage.append(memory_mb)
        self.network_io.append({
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv
        })
        self.disk_io.append({
            'read_bytes': disk_io.read_bytes,
            'write_bytes': disk_io.write_bytes
        })

        return {
            "timestamp": time.time(),
            "cpu_percent": cpu_percent,
            "memory_mb": memory_mb,
            "network_io": net_io,
            "disk_io": disk_io,
            "elapsed_time": time.time() - self.start_time
        }

    def get_summary(self):
        """获取资源使用摘要"""
        if not self.cpu_usage:
            return {}

        # 计算网络和磁盘IO增量
        net_diff = 0
        disk_diff = 0
        if len(self.network_io) > 1:
            net_diff = self.network_io[-1]['bytes_sent'] - self.network_io[0]['bytes_sent']
        if len(self.disk_io) > 1:
            disk_diff = self.disk_io[-1]['read_bytes'] - self.disk_io[0]['read_bytes']

        return {
            "avg_cpu": sum(self.cpu_usage) / len(self.cpu_usage),
            "max_cpu": max(self.cpu_usage),
            "avg_memory": sum(self.memory_usage) / len(self.memory_usage),
            "max_memory": max(self.memory_usage),
            "network_bytes_sent": net_diff,
            "disk_bytes_read": disk_diff,
            "total_time": time.time() - self.start_time,
            "monitor_interval": len(self.cpu_usage)
        }