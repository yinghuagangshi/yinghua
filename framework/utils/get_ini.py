#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author:  chaozhongze
@Time: 2021/09/01
@File: get_conf
"""
import os
from configparser import ConfigParser
from loguru import logger


class Conf():
    # 配置文件路径
    _conf_path = os.path.dirname(os.path.dirname(__file__)) + '/conf/config.ini'

    def __init__(self, encoding="utf8"):
        """
        初始化
        :param filename: 配置文件名
        :param encoding: 文件编码方式
        """
        filename = self._conf_path
        self.encoding = encoding
        # 创建一个文件解析对象，设为对象的conf
        self.conf = ConfigParser()
        # 使用解析器对象，加载配置文件中的内容
        self.conf.read(filename, encoding)

    def get_str(self, section, option):
        """
        读取数据
        :param section: 配置块
        :param option: 配置项
        :return: 对应配置项的数据
        """
        try:
            result = self.conf.get(section, option)
        except Exception as e:
            logger.error('配置文件读取失败')
            raise e
        else:
            return result
