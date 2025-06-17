# -*- coding:utf8 -*- #
#-----------------------------------------------------------------------------------
# ProjectName:   ranzhi_test
# FileName:     log_output
# Author:      shilingang
# Datetime:    2021/3/3 14:38
# Description:
#-----------------------------------------------------------------------------------
import logging

from utils.read_ini import ReadIni


def log_output(path):
    log=logging.Logger("ranzhi")
    # 日志格式  路径
    log_format=logging.Formatter("{%(asctime)s}[%(levelname)s]:%(message)s")
    fh=logging.FileHandler(path,encoding='utf8')
    # 应用格式
    fh.setFormatter(log_format)
    # 写入log日志
    log.addHandler(fh)

    return log

if __name__ == '__main__':
    log_output(ReadIni().log_path()+r'ranzhi.log').error("w")