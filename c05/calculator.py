#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys, os, csv, configparser, datetime
from getopt import getopt
from multiprocessing import Process, Queue

class Args(object):
    
    def __init__(self):
        try:
            opts = getopt(sys.argv[1:],'C:c:d:o:h',['help'])[0]
            
        except:
            print('Parameter Error')
            sys.exit()
        args = dict(opts)
        
        for opt,arg in opts:
            if opt in ('-h','--help'):
                print('Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata')
                sys.exit()
            if opt in ('-C',):
                
                city = args['-C']                         
            else:
                
                city = 'DEFAULT'
         
        self.config_file = args['-c']
        self.user_file = args['-d']
        self.out_file = args['-o']
        self.city = args['-C']
class Config(Args):

    def get_config(self):
        config_d = {}
        
        if os.path.exists(self.config_file):
            config=configparser.ConfigParser()
            config.read(self.config_file)
            
            section = self.city.upper()
            
            
            if (section not in config.sections()) and (section != 'DEFAULT'):
                print('Parameter Error')
                sys.exit()
            JiShuL = config.getfloat(section,'jishul')
            
            JiShuH = config.getfloat(section,'jishuh')
            
            YangLao = config.getfloat(section,'yanglao')
            YiLiao = config.getfloat(section,'yiliao')
            ShiYe = config.getfloat(section,'shiye')
            GongShang = config.getfloat(section,'gongshang')
            GongJiJin = config.getfloat(section,'gongjijin')
            ShengYu = config.getfloat(section,'shengyu')
            config_d['JiShuL'] = JiShuL
            config_d['JiShuH'] = JiShuH
            config_d['YangLao'] = YangLao
            config_d['YiLiao'] = YiLiao
            config_d['ShiYe'] = ShiYe
            config_d['GongShang'] = GongShang
            config_d['GongJiJin'] = GongJiJin
            config_d['ShengYu'] = ShengYu
            
            return config_d
            
        else:
            print('Parameter Error')


class UserData(Args):
    
    def __init__(self):
        super(UserData,self).__init__()
        self.queue1 = Queue()
        self.queue2 = Queue()

    def get_userdata(self):

        user_file = self.user_file
        if os.path.exists(user_file) == False:
            print('Parameter Error')
            sys.exit()
        
        with open(user_file,'r') as f:
            for line in f:
            
                gonghao = line.split(',')[0]
                gongzi = line.split(',')[1]
                user_data = {'gonghao':gonghao,'gongzi':gongzi}
                self.queue1.put(user_data)
                

    def calculate(self):        
        config = Config().get_config()
        JiShuL = int(config['JiShuL'])
        JiShuH = int(config['JiShuH'])
        YangLao = config['YangLao']
        YiLiao = config['YiLiao']
        ShiYe = config['ShiYe']
        GongShang = config['GongShang']
        GongJiJin = config['GongJiJin']
        ShengYu = config['ShengYu']
        
        while True:
            try:
                user_data = self.queue1.get(timeout=1)
                       
                gonghao = user_data['gonghao']
                gongzi = int(user_data['gongzi'])
                

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
                
                s_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                gongzi_item = '{},{},{:.2f},{:.2f},{:.2f},{}'.format(gonghao,gongzi,shebao,shui,gongzi_f,s_datetime)
                
                self.queue2.put(gongzi_item)

            except:
                
                break
        
            
    def WriteToFile(self):
        while True:
            try:
                gongzi_item = self.queue2.get(timeout=1)
                
                with open(self.out_file, 'a') as f:
                     f.write(gongzi_item+os.linesep)
            except:
                break
    
    def main(self):
        Process(target=self.get_userdata).start()
        Process(target=self.calculate).start()
        Process(target=self.WriteToFile).start()


if __name__ == '__main__':
    user_data = UserData()
    user_data.main()
