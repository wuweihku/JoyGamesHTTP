#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'WUWEI'

'''负责管理测试用例对应的测试方法,相关的数据处理'''

import  unittest

# 自定义RequestMethodError异常类，当请求到未支持的request method方法时raise
class RequestMethodError(Exception):
    def __init__(self, reason):
        self.reason = reason
    def __str__(self):
        return repr(self.reason)

# 测试用例(组)类
class ParametrizedTestCase(unittest.TestCase):
    '''DB中的测试用例request_param通过此类得以参数化parametrized'''
    # methodName即test_data.test_method,也就是目标测试方法test_interface_case，而非http_method get or post
    # 目前是统一用test_interface_case通用接口测试函数，对于比较复杂的测试流程，可以额外定义函数,支持拓展
    # test_data = DataStruct()，自定义数据结构对象
    # http即ConfigHttp生成的http对象
    # db_cursor即GetDB生成的对象的数据库连接句柄

    def __init__(self, methodName='runTest', test_data=None, http=None, db_cursor=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        self.test_data = test_data
        self.http = http
        self.db_cursor = db_cursor

class TestInterfaceCase(ParametrizedTestCase):
    def setUp(self):
        pass

    # 测试接口
    def test_interface_case(self):
        try:
            # 尝试向服务器发起请求
            # confighttp.py有做异常处理
            # 正常时返回return json_response
            # 异常时返回return {}并且抛出异常，异常可被这里捕获处理
            if self.test_data.http_method == 'GET':
                response = self.http.get(self.test_data.request_url,  self.test_data.request_param)
                
            elif self.test_data.http_method == 'POST':
                response = self.http.post(self.test_data.request_url,  str(self.test_data.request_param))
            
            else:
                # 尚未支持的request method，抛出自定义异常RequestMethodError
                raise RequestMethodError('Error - Unsupported Request Method ： %s' %self.test_data.http_method)                
        
        except Exception as e:
            # 异常的情况下
            self.test_data.result = 'Error'
            self.test_data.reason = str(e.reason)
            try:
                # 更新结果表中的用例运行结果
                # 更新结果表中的self.test_data.reason失败原因
                self.db_cursor.execute('UPDATE test_result SET result = %s, reason = %s WHERE case_id = %s', (self.test_data.result, self.test_data.reason ,self.test_data.case_id))
                self.db_cursor.execute('commit')
            # 操作数据库时发生异常
            except Exception as e:
                print('%s' % e)
                self.db_cursor.execute('rollback')
            # 这个return指尝试向服务器发起请求时发生异常，则做完上述异常处理后，直接return该次测试函数
            return



        try:
            # 读取数据库response_expectation，用于和接口请求返回码结果做比较
            self.assertEqual(response['code'], self.test_data.response_expectation, msg='返回code与预期response_expectation不匹配')
            # 通过即Pass
            self.test_data.result = 'Pass'
        except AssertionError as e:
            print('%s' % e)
            self.test_data.result = 'Fail'
            # 记录失败原因
            self.test_data.reason = '%s' % e

        # 更新结果表中的用例运行结果
        try:
            self.db_cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s', (self.test_data.result, self.test_data.case_id))
            self.db_cursor.execute('UPDATE test_result SET reason = %s WHERE case_id = %s', (self.test_data.reason, self.test_data.case_id))
            self.db_cursor.execute('commit')
        except Exception as e:
            print('%s' % e)
            self.db_cursor.execute('rollback')

    def tearDown(self):
        pass


