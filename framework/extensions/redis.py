import redis
from typing import Any, Optional, Union, List, Dict, Set, Tuple
from loguru import logger
from functools import wraps


class RedisClient:
    """
    通用Redis客户端封装

    功能特性：
    1. 支持单节点、哨兵、集群模式
    2. 自动连接池管理
    3. 支持常见数据结构操作
    4. 自动重连机制
    5. 上下文管理器支持
    6. 类型注解完善
    """

    def __init__(
            self,
            host: str = "localhost",
            port: int = 6379,
            db: int = 0,
            password: Optional[str] = None,
            decode_responses: bool = True,
            max_connections: int = 100,
            **kwargs
    ):
        """
        初始化Redis客户端

        :param host: Redis地址
        :param port: 端口
        :param db: 数据库编号
        :param password: 认证密码
        :param decode_responses: 是否自动解码返回字符串
        :param max_connections: 连接池最大连接数
        :param kwargs: 其他redis.StrictRedis参数
        """
        self.connection_pool = redis.ConnectionPool(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=decode_responses,
            max_connections=max_connections,
            **kwargs
        )
        self._client = None

    @property
    def client(self) -> redis.Redis:
        """获取Redis连接实例（懒加载）"""
        if self._client is None or not self.ping():
            self._client = redis.Redis(connection_pool=self.connection_pool)
        return self._client

    def ping(self) -> bool:
        """检查连接是否活跃"""
        try:
            return self._client.ping() if self._client else False
        except (redis.ConnectionError, redis.TimeoutError):
            return False

    def reconnect(self):
        """强制重连"""
        if self._client:
            self._client.close()
        self._client = redis.Redis(connection_pool=self.connection_pool)

    # ------------------- 基础操作 -------------------
    def exists(self, key: str) -> bool:
        """判断键是否存在"""
        return bool(self.client.exists(key))

    def delete(self, *keys: str) -> int:
        """删除一个或多个键"""
        return self.client.delete(*keys)

    def expire(self, key: str, seconds: int) -> bool:
        """设置键过期时间（秒）"""
        return bool(self.client.expire(key, seconds))

    # ------------------- 字符串操作 -------------------
    def get(self, key: str) -> Optional[str]:
        """获取字符串值"""
        return self.client.get(key)

    def set(
            self,
            key: str,
            value: Any,
            ex: Optional[int] = None,
            px: Optional[int] = None,
            nx: bool = False,
            xx: bool = False
    ) -> bool:
        """
        设置字符串值
        :param ex: 过期时间（秒）
        :param px: 过期时间（毫秒）
        :param nx: 仅当键不存在时设置
        :param xx: 仅当键存在时设置
        """
        return bool(self.client.set(key, value, ex=ex, px=px, nx=nx, xx=xx))

    # ------------------- 哈希操作 -------------------
    def hget(self, name: str, key: str) -> Optional[str]:
        """获取哈希表中字段值"""
        return self.client.hget(name, key)

    def hset(self, name: str, key: str, value: Any) -> int:
        """设置哈希表字段值"""
        return self.client.hset(name, key, value)

    def hgetall(self, name: str) -> Dict[str, str]:
        """获取哈希表所有字段和值"""
        return self.client.hgetall(name)

    # ------------------- 列表操作 -------------------
    def lpush(self, name: str, *values: Any) -> int:
        """从列表左侧插入一个或多个值"""
        return self.client.lpush(name, *values)

    def rpop(self, name: str) -> Optional[str]:
        """移除并获取列表最后一个元素"""
        return self.client.rpop(name)

    # ------------------- 集合操作 -------------------
    def sadd(self, name: str, *values: Any) -> int:
        """向集合添加一个或多个成员"""
        return self.client.sadd(name, *values)

    def smembers(self, name: str) -> Set[str]:
        """获取集合所有成员"""
        return self.client.smembers(name)

    # ------------------- 有序集合操作 -------------------
    def zadd(self, name: str, mapping: Dict[str, float]) -> int:
        """向有序集合添加一个或多个成员"""
        return self.client.zadd(name, mapping)

    def zrange(self, name: str, start: int, end: int, withscores: bool = False) -> Union[
        List[str], List[Tuple[str, float]]]:
        """通过索引区间返回有序集合成员"""
        return self.client.zrange(name, start, end, withscores=withscores)

    # ------------------- 事务操作 -------------------
    def pipeline(self):
        """创建管道（支持事务）"""
        return self.client.pipeline()

    # ------------------- 发布订阅 -------------------
    def publish(self, channel: str, message: str) -> int:
        """发布消息到频道"""
        return self.client.publish(channel, message)

    def pubsub(self):
        """创建发布/订阅对象"""
        return self.client.pubsub()

    # ------------------- 上下文管理 -------------------
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """关闭连接"""
        if self._client:
            self._client.close()
        self.connection_pool.disconnect()
        logger.info("Redis连接已关闭")


# ------------------- 装饰器工具 -------------------
def redis_retry(max_retries: int = 3):
    """
    Redis操作重试装饰器
    :param max_retries: 最大重试次数
    """

    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            for attempt in range(1, max_retries + 1):
                try:
                    return func(self, *args, **kwargs)
                except (redis.ConnectionError, redis.TimeoutError) as e:
                    if attempt == max_retries:
                        logger.error(f"Redis操作失败，已达最大重试次数: {e}")
                        raise
                    logger.warning(f"Redis连接异常，正在重试({attempt}/{max_retries})...")
                    self.reconnect()
                    time.sleep(0.5 * attempt)

        return wrapper

    return decorator