import os
import psutil
import platform

def get_physical_cores():
    """返回物理 CPU 核心数量（忽略超线程）"""
    return psutil.cpu_count(logical=False)

def bind_process_to_physical_cpu(pid, physical_cpu_id):
    """
    将进程绑定到指定的物理 CPU 核心
    :param pid: 进程 ID
    :param physical_cpu_id: 物理核心编号（0, 1, 2, ...）
    """
    if platform.system() == "Linux":
        # Linux: 使用 cgroups 或 taskset 绑定
        try:
            # 方法 1: 直接设置亲和性（需要 root 权限）
            os.sched_setaffinity(pid, [physical_cpu_id])
        except PermissionError:
            # 方法 2: 通过 taskset 命令（推荐）
            os.system(f"taskset -pc {physical_cpu_id} {pid}")
    elif platform.system() == "Windows":
        # Windows: 使用位掩码绑定物理核心
        import win32process
        import win32api
        # 计算物理核心对应的位掩码
        cpu_mask = 1 << physical_cpu_id
        win32process.SetProcessAffinityMask(
            win32api.OpenProcess(win32process.PROCESS_ALL_ACCESS, False, pid),
            cpu_mask
        )
    else:
        raise NotImplementedError("Unsupported OS")

def get_cpu_topology():
    """返回逻辑 CPU 到物理核心的映射（用于调试）"""
    if not hasattr(psutil, "cpu_topology"):
        return {}
    return {cpu.id: cpu.physical_id for cpu in psutil.cpu_topology()}