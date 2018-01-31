#!usr/bin/env python

import sys, csv, os

class Config():

    def __init__(self,config_file):
        config_list = []
        with open(config_file,'r') as f:
            lines = f.readlines()

            for line in lines:
                if len(line)>1:
                    config_item = line.split('=')
                    for i in range(0,len(config_item)):
                        config_item[i] = config_item[i].strip()
                    config_list.append(config_item)
            
        self.config = dict(config_list)
     
    def get_config(self,kw):
        return float(self.config[kw])
        
        
class UserDate():
    
    def __init__(self,user_file,out_file):
        with open(user_file,'r') as f:
            reader = csv.reader(f)
            d=dict(list(reader))
            
        self.userdate = d
        self.out_file = out_file
        self.config = None

    def calculator(self):
        l = []
        for key in self.userdate.keys():
            gonghao = key
            gongzi = int(self.userdate[key])
            JiShuL = self.config.get_config('JiShuL')
            JiShuH = self.config.get_config('JiShuH')
            YangLao = self.config.get_config('YangLao')
            YiLiao = self.config.get_config('YiLiao')
            ShiYe = self.config.get_config('ShiYe')
            GongShang = self.config.get_config('GongShang')
            ShengYu = self.config.get_config('ShengYu')
            GongJiJin = self.config.get_config('GongJiJin')
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

            shui = (gongzi-shebao-3500)*rate -a

            gongzi_f = gongzi-shebao-shui
            s = '{gonghao},{gongzi},{shebao},{shui},{gongzi_f}'.format(gonghao=gonghao,
                           gongzi=gongzi,shebao=format(shebao,'.2f'),
                           shui=format(shui,'.2f'),gongzi_f=format(gongzi_f,'.2f'))
            l.append(s)
        return l

    def dumtofile(self):
        l = self.calculator()
        with open(self.out_file, 'w') as f:
            for i in l:
                f.write(i+os.linesep)





if __name__ == '__main__':

    try:
        args = sys.argv[1:]
        config_file = args[args.index('-c')+1]
        user_file = args[args.index('-d')+1]
        out_file = args[args.index('-o')+1]
        
        config = Config(config_file)
        userdate = UserDate(user_file=user_file,out_file=out_file)
        userdate.config=config
        userdate.dumtofile()
    except:
        print('Parameter Error')
