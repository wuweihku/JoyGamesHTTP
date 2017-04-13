#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'WUWEI'

import unittest
from test_interface_case import TestInterfaceCase
from datastruct import DataStruct

global test_data
test_data = DataStruct()

class  RunCase:
    '''运行测试用例'''
    def __init__(self):
        pass

    # 运行测试用例函数
    # runner
    def run_case(self, runner, run_mode, run_case_list, db_conn, http):
        global test_data
        self.http = http

        # 1 == run_mode
        # 运行全部用例
        if 1 == run_mode:
            db_cursor = db_conn.cursor()
            # 获取用例个数
            db_cursor.execute('SELECT count(case_id)  FROM test_data')
            test_case_num = db_cursor.fetchone()[0]
            db_cursor.close()

            # 循环执行测试用例
            for case_id in range(1, test_case_num+1):
                db_cursor = db_conn.cursor()
                db_cursor.execute('SELECT http_method, request_name, request_url, request_param, test_method, test_desc, response_expectation FROM test_data WHERE case_id = %s',(case_id,))
                # 记录数据
                tmp_result = db_cursor.fetchone()
                test_data.case_id = case_id
                test_data.http_method = tmp_result[0]
                test_data.request_name = tmp_result[1]
                test_data.request_url = tmp_result[2]
                test_data.request_param = tmp_result[3]
                test_data.test_method = tmp_result[4]
                test_data.test_desc = tmp_result[5]
                test_data.response_expectation = tmp_result[6]
                test_data.result = ''
                test_data.reason = ''
                
                try:
                    query = ('INSERT INTO test_result(case_id, http_method, request_name, request_url,request_param, test_method, test_desc, result, reason) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)')
                    data = (test_data.case_id,test_data.http_method,test_data.request_name, test_data.request_url,test_data.request_param, test_data.test_method, test_data.test_desc,test_data.result, test_data.reason)
                    db_cursor.execute(query, data)
                    db_cursor.execute('commit')

                except Exception as e:
                    print('%s' % e)
                    db_cursor.execute('rollback')

                test_suite = unittest.TestSuite()
                # methodName即test_data.test_method,也就是目标测试方法test_interface_case，而非http_method get or post
                # test_data = DataStruct(),自定义数据结构对象
                # http即ConfigHttp生成的http对象
                # db_cursor即GetDB生成的对象的数据库连接句柄
                # 根据数据库的一条条case，生成测试用例套件
                test_suite.addTest(TestInterfaceCase(test_data.test_method, test_data, http, db_cursor))
                runner.run(test_suite)
                db_cursor.close()
        
        # 0 == run_mode
        # 运行指定条目用例
        # [3,5,7]，运行case_id为3/5/7的这三条用例
        elif 0 == run_mode:
            for case_id in run_case_list:
                db_cursor = db_conn.cursor()    
                db_cursor.execute('SELECT http_method, request_name, request_url, request_param, test_method, test_desc, response_expectation FROM test_data WHERE case_id = %s',(case_id,))
                # 记录数据
                tmp_result = db_cursor.fetchone()
                test_data.case_id = case_id
                test_data.http_method = tmp_result[0]
                test_data.request_name = tmp_result[1]
                test_data.request_url = tmp_result[2]
                test_data.request_param = tmp_result[3]
                test_data.test_method = tmp_result[4]
                test_data.test_desc = tmp_result[5]
                test_data.response_expectation = tmp_result[6]
                test_data.result = ''
                test_data.reason = ''

                try:
                    query = ('INSERT INTO test_result(case_id, http_method, request_name, request_url, request_param, test_method, test_desc, result, reason) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)')
                    data = (test_data.case_id,test_data.http_method,test_data.request_name, test_data.request_url,test_data.request_param, test_data.test_method, test_data.test_desc,test_data.result, test_data.reason)
                    db_cursor.execute(query, data)
                    db_cursor.execute('commit')

                except Exception as e:
                    print('%s' % e)
                    db_cursor.execute('rollback')

                test_suite = unittest.TestSuite()
                test_suite.addTest(TestInterfaceCase(test_data.test_method, test_data, http, db_cursor))
                runner.run(test_suite)
                db_cursor.close()
        
        # 2 == run_mode
        # 运行指定范围用例
        # [3,10]运行case_id 从3到10的用例
        else:
            min = int(run_case_list[0])
            max = int(run_case_list[1])+1
            for case_id in range(min,max):
                db_cursor = db_conn.cursor()    
                db_cursor.execute('SELECT http_method, request_name, request_url, request_param, test_method, test_desc, response_expectation FROM test_data WHERE case_id = %s',(case_id,))
                # 记录数据
                tmp_result = db_cursor.fetchone()
                test_data.case_id = case_id
                test_data.http_method = tmp_result[0]
                test_data.request_name = tmp_result[1]
                test_data.request_url = tmp_result[2]
                test_data.request_param = tmp_result[3]
                test_data.test_method = tmp_result[4]
                test_data.test_desc = tmp_result[5]
                test_data.response_expectation = tmp_result[6]
                test_data.result = ''
                test_data.reason = ''

                try:
                    query = ('INSERT INTO test_result(case_id, http_method, request_name, request_url, request_param, test_method, test_desc, result, reason) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)')
                    data = (test_data.case_id,test_data.http_method,test_data.request_name, test_data.request_url,test_data.request_param, test_data.test_method, test_data.test_desc,test_data.result, test_data.reason)
                    db_cursor.execute(query, data)
                    db_cursor.execute('commit')

                except Exception as e:
                    print('%s' % e)
                    db_cursor.execute('rollback')

                test_suite = unittest.TestSuite()
                test_suite.addTest(TestInterfaceCase(test_data.test_method, test_data, http, db_cursor))
                runner.run(test_suite)
                db_cursor.close()

            

