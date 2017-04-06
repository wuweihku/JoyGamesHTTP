#!/usr/bin/env python
# -*- coding:utf-8 -*-


__author__ = 'WUWEI'

import urllib.request
import http.cookiejar
import urllib.parse
import json
import configparser

# 配置类
class ConfigHttp:
    ''' 配置要测试接口服务器的协议,ip、端口、域名等信息，封装http 请求方法，http 头设置等'''
    
    # 传入文件对象ini_file配置文件
    def __init__(self, ini_file):
        
        # 使用configparser配置库，生成config对象
        config = configparser.ConfigParser()

        # 从配置文件中读取接口服务器协议,IP、域名，端口
        config.read(ini_file)
        self.protocol = config['HTTP']['protocol']
        self.host = config['HTTP']['host']
        self.port = config['HTTP']['port']
        # 刚从文本读取进来的时候，是字符串str
        self.headers = config['HTTP']['headers']
        # 把字符串类型的dict转换为dict
        self.headers = eval(self.headers)

        # install cookie
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        urllib.request.install_opener(opener)

    def set_headers(self, headers):
        self.headers = headers

    def get_headers(self):
        return self.headers

    def set_protocol(self, protocol):
        self.protocol = protocol

    def get_protocol(self):
        return self.protocol

    def set_host(self, host):
        self.host = host

    def get_host(self):
        return self.host

    def set_port(self, port):
        self.port = port

    def get_port(self):
        return  self.port

    # 封装HTTP GET请求方法
    def get(self, url, params):
        # 将参数转为url编码字符串
        params = urllib.parse.urlencode(eval(params))
        url = str(self.protocol) + '://' + self.host + ':' + str(self.port)  + url + params 
        request = urllib.request.Request(url, headers=self.headers)

        try:
            response = urllib.request.urlopen(request)
            # decode函数对获取的字节数据进行解码
            response = response.read().decode('utf-8')
            # 将返回数据转为json格式的数据
            json_response = json.loads(response)
            return json_response
        except Exception as e:
            print('%s' % e)
            return {}

    # 封装HTTP POST请求方法
    def post(self, url, data):
        data = json.dumps(eval(data))
        data = data.encode('utf-8')
        url = str(self.protocol) + '://' + self.host + ':' + str(self.port)  + url
        
        try:
            request = urllib.request.Request(url, headers=self.headers)
            response = urllib.request.urlopen(request, data)
            response = response.read().decode('utf-8')
            json_response = json.loads(response)
            return json_response
        except Exception as e:
            print('%s' % e)
            return {}

    # 封装xxx请求方法
    # 比如delete、put等，甚至是socket


