#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'WUWEI'

'''负责管理测试用例对应的测试方法,相关的数据处理'''

import  unittest

# 测试用例(组)类
class ParametrizedTestCase(unittest.TestCase):
    '''DB中的测试用例request_param通过此类得以参数化parametrized'''
    def __init__(self, methodName='runTest', test_data=None, http=None, db_cursor=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        # test_data = DataStruct(),datastruct.py里定义的数据结构
        self.test_data = test_data
        # http/https
        self.http = http
        # 数据库句柄
        self.db_cursor = db_cursor

class TestInterfaceCase(ParametrizedTestCase):
    def setUp(self):
        pass

    # 测试接口
    def test_interface_case(self):
       # 根据被测接口的实际情况，合理的添加HTTP头
       # header = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       # 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:29.0) Gecko/20100101 Firefox/29.0'
       #    }
       # self.http.set_header(header)
        #  self.http是globalconfig.py里面self.http = ConfigHttp('../config/http_conf.ini')实例化的对象
        response = self.http.get(self.test_data.request_url,  self.test_data.request_param)
        if {} == response:
            self.test_data.result = 'Error'
            try:
                # 更新结果表中的用例运行结果
                self.db_cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s', (self.test_data.result, self.test_data.case_id))
                self.db_cursor.execute('commit')
            except Exception as e:
                print('%s' % e)
                self.db_cursor.execute('rollback')
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


