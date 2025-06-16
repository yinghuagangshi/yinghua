#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Time: 2022/8/17 9:07 上午
@File:  MySQLActionLib.py
@Author:  slg
"""
import pymysql
import time


class MySQLAction(object):
    def __init__(self, host_name, user_name, pwd, db_name, port_id):
        # connect
        self.host_name = host_name
        self.user_name = user_name
        self.pwd = pwd
        self.db_name = db_name
        self.port_id = port_id
        try:
            self.conn = pymysql.connect(host=self.host_name, user=self.user_name, password=self.pwd
                                        , db=self.db_name, port=self.port_id, local_infile=1)
        except pymysql.DatabaseError as e:
            print("connect error: {}".format(str(e)))
        # create cursor
        self.cur = self.conn.cursor()

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def query_return_dict(self, execute_sql):
        cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        re = cursor.execute(execute_sql)
        all_rows = cursor.fetchall()
        time.sleep(0.5)
        return all_rows

    def query_sql(self, execute_sql):
        result = self.cur.execute(execute_sql)
        self.commit_data()
        return result

    def delete_sql(self, execute_sql):
        self.cur.execute(execute_sql)
        self.conn.commit()

    def execute_script(self, sql_file):
        try:
            with open(sql_file, encoding='utf-8', mode='r') as f:
                # 读取整个sql文件，以分号切割。[:-1]删除最后一个元素，也就是空字符串
                sql_list = f.read().split(';')[:-1]
                for x in sql_list:
                    # 判断包含空行的
                    if '\n' in x:
                        # 替换空行为1个空格
                        x = x.replace('\n', ' ')

                    # 判断多个空格时
                    if '    ' in x:
                        # 替换为空
                        x = x.replace('    ', '')

                    # sql语句添加分号结尾
                    sql_item = x + ';'
                    self.cur.execute(sql_item)
            self.commit_data()
        except Exception as ex:
            self.conn.rollback()

    def commit_data(self):
        self.conn.commit()
