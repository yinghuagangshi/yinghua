#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Time: 2022/8/17 9:06 上午
@File:  PostgreSQLActionLib.py
@Author:  slg
"""
import psycopg2
import psycopg2.extras
import json


class PostgreSQLActionLib(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self, host_name, user_name, pwd, db_name, port_id):
        # connect
        self.host_name = host_name
        self.user_name = user_name
        self.pwd = pwd
        self.db_name = db_name
        self.port_id = port_id
        try:
            self.con = psycopg2.connect(host=self.host_name, user=self.user_name, password=self.pwd
                                        , database=self.db_name, port=self.port_id)
        except psycopg2.DatabaseError as e:
            print("数据库连接失败: {}".format(str(e)))
        self.cur = self.con.cursor()

    def __del__(self):
        self.cur.close()
        self.con.close()

    def delete_sql(self, execute_sql):
        self.cur.execute(execute_sql)
        self.con.commit()

    def query(self, sql):
        print("sql: {}".format(sql))
        cur_json = self.con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur_json.execute(sql)
        all_rows = cur_json.fetchall()
        return all_rows

    def query_data(self,sql):
        print("sql: {}".format(sql))
        cur_json = self.con.cursor()
        cur_json.execute(sql)
        all_rows = cur_json.fetchall()
        return all_rows
