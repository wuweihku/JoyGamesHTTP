#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'WUWEI'

from confighttp import ConfigHttp
from configrunmode import ConfigRunMode
from getdb import GetDB

class Global:
    '''负责配置的全局初始化，包括ConfigHttp、GetDB、ConfigRunMode'''
    
    def __init__(self):
        # 读取并配置接口服务器IP，端口等信息,生成self.http对象
        # 由ConfigHttp类实例化的http对象，都直接用类中的方法和属性
        # 方法get/post等，可扩展
        # 属性protocol/host/port/headers
        self.http = ConfigHttp('./config/http_conf.ini')

        # 读取并配置数据库服务器IP，端口等信息，生成self.db对象
        # self.db的可用方法有get_conn,返回数据库连接句柄进行后续操作
        # DATABASE是db_config.ini里的section名
        self.db = GetDB('./config/db_config.ini', 'DATABASE')
        
        # 读取运行模式配置，生成self.run_mode_config对象
        # self.run_mode_config对象的可用方法有get_run_mode、get_case_list
        self.run_mode_config = ConfigRunMode('./config/run_case_config.ini')

    # 返回http对象,包含各种可操作属性和方法 
    def get_http(self):
        return self.http

    # 返回db对象连接句柄
    def get_db_conn(self):
        return self.db.get_conn()

    # 获取运行模式配置
    def get_run_mode(self):
        return self.run_mode_config.get_run_mode()

    # 获取需要单独运行的用例列表
    def get_run_case_list(self):
        return self.run_mode_config.get_case_list()

    # 释放资源
    def clear(self):
        # 关闭数据库连接
        self.db.get_conn().close()



