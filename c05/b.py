import sys
import configparser

config=configparser.ConfigParser()
config.read('test.cfg')

v=config.getfloat('DEFAULT','JiShuL')
print(v)
