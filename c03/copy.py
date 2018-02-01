#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys, os, csv
from getopt import getopt

class Args(object):
    
    def __init__(self):
        try:
            opts = getopt(sys.argv[1:],'c:d:o:')[0]
        except:
            print('Parameter Error')
            sys.exit()
        if len(opts) != 3:
            print("Parameter Error")
            sys.exit()
        else:            
            args = dict(opts)
            self.config_file = args['-c']
            self.user_file = args['-d']
            self.out_file = args['-o']
            

class Config(Args):

    def get_config(self):
        config = {}
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                config_lines = f.readlines()
            for config_line in config_lines:
                config[config_line.split('=')[0].strip()] = float(config_line.split('=')[1].strip())
            return config
        else:
            print('Parameter Error')


class UserData(Args):

    def get_userdata(self):
        user_file = self.user_file
        if os.path.exists(user_file) == False:
            print('Parameter Error')
            sys.exit()
        
        with open(user_file,'r') as f:
            reader = csv.reader(f)
            user_datas = list(reader)
            
        return user_datas

    def calculate(self):        
        config = Config().get_config()
        JiShuL = config['JiShuL']
        JiShuH = config['JiShuH']
        YangLao = config['YangLao']
        YiLiao = config['YiLiao']
        ShiYe = config['ShiYe']
        GongShang = config['GongShang']
        GongJiJin = config['GongJiJin']
        ShengYu = config['ShengYu']

        gongzi_list = []
        user_datas = self.get_userdata()
        for user_data in user_datas:
            gonghao = user_data[0]
            gongzi = int(user_data[1])
            shebaolv = YangLao+YiLiao+ShiYe+GongShang+ShengYu+GongJiJin
            if gongzi < JiShuL:
                shebao = JiShuL*shebaolv
            elif gongzi >=JiShuL and gongzi <=JiShuH:
                shebao = gongzi*shebaolv
            else:
                shebao = JiShuH*shebaolv
            
            n = gongzi-3500
            if n<=0:
                rate = 0
                a = 0
            elif n>0 and n<=1500:
                rate = 0.03
                a = 0
            elif n>1500 and n<=4500:
                rate = 0.1
                a = 105
            elif n>4500 and n<=9000:
                rate = 0.2
                a = 555
            elif n>9000 and n<=35000:
                rate = 0.25
                a = 1005
            elif n>35000 and n<=55000:
                rate = 0.3
                a = 2755
            elif n>55000 and n<=80000:
                rate = 0.35
                a = 5505
            elif n>80000:
                rate = 0.45
                a = 13505
            shui = (gongzi-shebao-3500)*rate - a
            if gongzi <=3500:
                shui = 0
            
            gongzi_f = gongzi-shebao-shui
            gongzi_item = '{},{},{:.2f},{:.2f},{:.2f}'.format(gonghao,gongzi,shebao,shui,gongzi_f)
            gongzi_list.append(gongzi_item)
        
        return gongzi_list
            
    def WriteToFile(self):
        l = self.calculate()
        with open(self.out_file, 'w') as f:
            for i in l:
                f.write(i+os.linesep)

if __name__ == '__main__':
    user_data = UserData()
    user_data.WriteToFile()