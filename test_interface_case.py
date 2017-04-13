#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'WUWEI'

'''负责管理测试用例对应的测试方法,相关的数据处理'''

import  unittest
import hashlib 

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
    
    # 需要一个函数，能够在发起请求前，对参数表的key-value进行再编辑
    # updatekey = 需要update的key，传str实参
    # updatevalue = 需要update的key所对应的value，传str实参
    def update_request_param_value(self, updatekey, updatevalue):
        
        # DataStruct类实例化出test_data对象
        # test_data有request_param属性，为str类型
        # 需要将self.test_data.request_param str转为dict类型
        request_param_dict = eval(self.test_data.request_param)
        request_param_dict[updatekey] = updatevalue
        self.test_data.request_param = str(request_param_dict)

    # 需要一个函数，能够便捷地获取参数表的key-value
    # needkey = 需要值的key，传str实参
    # return needvalue，返回你所需要的key-value
    def get_request_param_value(self, needkey):
        request_param_dict = eval(self.test_data.request_param)
        needkey = request_param_dict[needkey]
        return needkey

    # 提供一个便捷的md5函数，供生成signature
    # sign_data为需要被md5的值,传str实参
    def get_md5(self,sign_data):
        sign = hashlib.md5()
        sign.update(sign_data.encode('utf-8'))
        sign_md5_data = sign.hexdigest()
        return sign_md5_data



class TestInterfaceCase(ParametrizedTestCase):
    # 可以在此类中自定义测试场景描述函数
    # test_interface_case（）为我提供的通用函数
    # 当然，如果有需求，你也可以写一个test_downloadmovie_firstofall()函数，不管做什么事之前，都要求先下载一部电影
 
    
    def setUp(self):
        pass    
    
    # 测试接口
    def test_interface_case(self):
        # 测试场景描述函数
        # 可以进行参数表值调整,即self.test_data.request_param的再编辑
        # 利用update_request_param_value()更新参数表中的键值对
        # 利用get_request_param_value()获取参数表的指定key-value
        # 利用get_md5()获取signature等
        
        '''
        比如，我要用脚本生成每个case的signature字段值，代码段如下：
        appkey='f46806d675f16feae23b5c07d4a3c935'
        appID = self.get_request_param_value('appID')
        sign_data = appID + appkey
        sign_md5_data = self.get_md5(sign_data)
        self.update_request_param_value('signature',sign_md5_data)
        
        '''
        
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
            self.test_data.reason = str(e)
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
            self.assertEqual(int(response['code']), int(self.test_data.response_expectation))
            # 通过即Pass
            self.test_data.result = 'Pass'
        except AssertionError as e:
            print('%s' % e)
            self.test_data.result = 'Fail'
            # 记录失败原因
            self.test_data.reason = 'Raise Error:%s , Response:%s'%(e,response)
            print(self.test_data.reason)

        # 更新结果表中的用例运行结果
        # 同时还要更新test_result表里的request_param字段记录，update_request_param（）的行为要同步到报告中
        try:
            self.db_cursor.execute('UPDATE test_result SET request_param = %s WHERE case_id = %s', (self.test_data.request_param,self.test_data.case_id))
            self.db_cursor.execute('UPDATE test_result SET result = %s WHERE case_id = %s', (self.test_data.result, self.test_data.case_id))
            self.db_cursor.execute('UPDATE test_result SET reason = %s WHERE case_id = %s', (self.test_data.reason, self.test_data.case_id))
            self.db_cursor.execute('commit')
        except Exception as e:
            print('%s' % e)
            self.db_cursor.execute('rollback')

    def tearDown(self):
        pass


