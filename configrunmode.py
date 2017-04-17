#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'WUWEI'

import configparser

class ConfigRunMode:
    '''从配置文件中读取运行模式'''
    
    # 传入配置文件
    def __init__(self, ini_file):
        config = configparser.ConfigParser()

        config.read(ini_file)

        try:
            self.run_mode = config['RUNCASECONFIG']['runmode']
            # 将str转为int
            self.run_mode = int(self.run_mode)

            self.case_list = config['RUNCASECONFIG']['case_id']
            # 把字符串类型的list转换为list
            self.case_list = eval(self.case_list) 
        
            if 0 == self.run_mode:
                print('[RUNCASECONFIG] runmode = %d，运行指定条目用例:%s\n'%(self.run_mode,config['RUNCASECONFIG']['case_id']))
            elif 1 == self.run_mode:
                print('[RUNCASECONFIG] runmode = %d，运行全部用例\n'%self.run_mode)
            else:
                print('[RUNCASECONFIG] runmode = %d，运行指定范围用例:%s\n'%(self.run_mode,config['RUNCASECONFIG']['case_id']))
        
        except Exception as e:
            print('%s', e)
  
    def get_run_mode(self):
        return self.run_mode

    def get_case_list(self):
        return  self.case_list

