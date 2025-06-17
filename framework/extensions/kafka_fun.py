import os
import random
from typing import Optional, Dict, Any, Union, List
from kafka import KafkaConsumer, KafkaProducer
from loguru import logger
from framework.utils.get_ini import Conf


class KafkaClient:
    """
    通用的Kafka客户端类，支持生产者和消费者功能

    功能特点：
    1. 同时支持生产者和消费者模式
    2. 配置分层管理（默认配置 > 配置文件 > 用户参数）
    3. 自动资源清理
    4. 敏感信息保护
    5. 类型注解支持
    """

    # 默认消费者配置
    DEFAULT_CONSUMER_CONFIG = {
        'auto_offset_reset': 'earliest',
        'enable_auto_commit': False,
        'session_timeout_ms': 30000,
        'max_poll_interval_ms': 300000,
        'group_id': lambda: f'group-{random.randint(1000, 999999999)}'
    }

    # 默认生产者配置
    DEFAULT_PRODUCER_CONFIG = {
        'acks': 'all',
        'retries': 3,
        'compression_type': 'gzip',
        'max_in_flight_requests_per_connection': 1
    }

    def __init__(self,
                 bootstrap_servers: Optional[Union[str, List[str]]] = None,
                 **client_config: Dict[str, Any]):
        """
        初始化Kafka客户端

        :param bootstrap_servers: Kafka服务器地址(默认为配置文件的kafka.url)
        :param client_config: 全局配置（同时适用于生产者和消费者）
        """
        # 合并配置（优先级: 直接参数 > 配置文件 > 默认值）
        self.bootstrap_servers = (
                bootstrap_servers
                or Conf().get_str('kafka', 'url')
                or 'localhost:9092'
        )

        # 全局共享配置
        self.base_config = {
            'bootstrap_servers': self.bootstrap_servers,
            **self._load_security_config(),
            **client_config
        }

        self._producer = None
        self._consumers = []

    def _load_security_config(self) -> Dict[str, Any]:
        """从配置加载安全认证信息"""
        security_config = {}

        # 如果有安全配置
        if Conf().get_bool('kafka', 'enable_sasl', False):
            security_config.update({
                'security_protocol': Conf().get_str('kafka', 'security_protocol', 'SASL_PLAINTEXT'),
                'sasl_mechanism': Conf().get_str('kafka', 'sasl_mechanism', 'SCRAM-SHA-256'),
                'sasl_plain_username': Conf().get_str('kafka', 'sasl_username', ''),
                'sasl_plain_password': Conf().get_str('kafka', 'sasl_password', '')
            })

        return security_config

    def get_consumer(self,
                     topics: Union[str, List[str]],
                     **consumer_config: Dict[str, Any]) -> KafkaConsumer:
        """
        获取Kafka消费者实例

        :param topics: 要订阅的主题（单个或多个）
        :param consumer_config: 消费者专属配置
        :return: 配置好的KafkaConsumer实例
        """
        # 处理动态默认值（如随机group_id）
        resolved_config = {}
        for k, v in self.DEFAULT_CONSUMER_CONFIG.items():
            resolved_config[k] = v() if callable(v) else v

        # 合并配置（优先级: 方法参数 > 全局配置 > 默认配置）
        config = {
            **resolved_config,
            **self.base_config,
            **consumer_config
        }

        try:
            consumer = KafkaConsumer(
                *([topics] if isinstance(topics, str) else topics),
                **config
            )
            self._consumers.append(consumer)
            return consumer
        except Exception as e:
            logger.error(f'创建消费者失败: {e}')
            raise

    def get_producer(self, **producer_config: Dict[str, Any]) -> KafkaProducer:
        """
        获取Kafka生产者实例

        :param producer_config: 生产者专属配置
        :return: 配置好的KafkaProducer实例
        """
        if self._producer is None:
            try:
                config = {
                    **self.DEFAULT_PRODUCER_CONFIG,
                    **self.base_config,
                    **producer_config
                }
                self._producer = KafkaProducer(**config)
            except Exception as e:
                logger.error(f'创建生产者失败: {e}')
                raise

        return self._producer

    def produce(self,
                topic: str,
                value: Union[str, bytes],
                key: Optional[Union[str, bytes]] = None,
                **kwargs):
        """
        生产消息（便捷方法）

        :param topic: 目标主题
        :param value: 消息内容
        :param key: 消息键（可选）
        """
        producer = self.get_producer()
        if isinstance(value, str):
            value = value.encode('utf-8')
        if key and isinstance(key, str):
            key = key.encode('utf-8')

        future = producer.send(topic, value=value, key=key, **kwargs)
        return future.get(timeout=10)  # 同步等待发送结果

    def close(self):
        """关闭所有Kafka连接"""
        if self._producer:
            self._producer.close()
            self._producer = None

        for consumer in self._consumers:
            consumer.close()

        self._consumers.clear()
        logger.info('已关闭所有Kafka连接')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# 使用示例
if __name__ == '__main__':
    # 基本用法
    with KafkaClient() as client:
        # 消费者
        consumer = client.get_consumer('test_topic')
        for msg in consumer:
            print(f"收到消息: {msg.value.decode()}")

        # 生产者
        producer = client.get_producer()
        producer.send('test_topic', value=b'Hello Kafka')

        # 或者使用便捷方法
        client.produce('test_topic', 'Another message')

    # 带认证的用法
    secure_client = KafkaClient(
        bootstrap_servers='kafka1:9092,kafka2:9092',
        security_protocol='SASL_SSL',
        sasl_mechanism='SCRAM-SHA-512',
        ssl_cafile='/path/to/ca.pem'
    )