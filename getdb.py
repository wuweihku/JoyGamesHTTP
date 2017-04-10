#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'WUWEI'

import configparser
import mysql.connector
import sys

class GetDB:
    '''配置数据库IP，端口等信息，获取数据库连接'''
    
    # ini_file是数据库配置文件
    # db是ini_file的section名，用于config[db]['host']
    def __init__(self, ini_file, db):
        config = configparser.ConfigParser()

        # 从配置文件中读取数据库服务器IP、域名，端口
        config.read(ini_file)
        self.host = config[db]['host']
        self.port = config[db]['port']
        self.user = config[db]['user']
        self.passwd = config[db]['passwd']
        self.db = config[db]['db']
        self.charset = config[db]['charset']

    # 使用GetDB生成对象后，用对象的get_conn返回数据库连接句柄进行后续操作
    def get_conn(self):
        # 尝试建立连接
        try:
            conn = mysql.connector.connect(host=self.host, port=self.port, user=self.user, password=self.passwd, database=self.db, charset=self.charset)
            return conn
        except Exception as e:
            print('%s', e)
            sys.exit()
