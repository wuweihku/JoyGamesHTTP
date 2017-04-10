#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'WUWEI'

class DataStruct:
    '''
    定义结构体，接收从测试数据库testdb 中test_data 表读取的测试数据,记录要写入测试报告的数据
    表： test_data Field Information:
    case_id : 用例编号
    http_method : get or post
    request_name : 接口名称，一般是接口文档的描述 
    request_url ：请求的地址
    request_param ：请求的参数
    test_method ：目标测试函数
    response_expectation：期望
    test_desc：测试case描述

    '''
    def __init__(self):
        self.case_id = 0       #用例ID
        self.http_method = ''  #接口http方法
        self.request_name = '' #接口名
        self.request_url = ''  #接口请求url
        self.request_param = ''#请求参数
        self.test_method = ''  #测试方法
        self.test_desc = ''    #测试用例描述
        self.result = ''       #测试结果
        self.response_expectation = '' #断言预期
        self.reason = ''       #失败原因

