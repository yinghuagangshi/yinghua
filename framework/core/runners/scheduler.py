from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger


class TestScheduler:
    def __init__(self):
        self.sched = BlockingScheduler()
        self.interval_jobs = {}

    def add_interval_job(self, func, interval_seconds, job_id=None, timezone='Asia/Shanghai'):
        """添加定时执行任务
        Args:
            func: 要执行的函数
            interval_seconds: 执行间隔(秒)
            job_id: 任务ID(用于后续管理)
            timezone: 时区设置
        """
        job = self.sched.add_job(
            func,
            trigger=IntervalTrigger(seconds=interval_seconds),
            timezone=timezone
        )
        if job_id:
            self.interval_jobs[job_id] = job
        return job

    def start_schedule(self):
        """启动定时调度器"""
        self.sched.start()

    def remove_job(self, job_id):
        """移除定时任务"""
        if job_id in self.interval_jobs:
            self.sched.remove_job(self.interval_jobs[job_id].id)
            del self.interval_jobs[job_id]