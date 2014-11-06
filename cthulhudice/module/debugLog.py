# -*-coding:utf-8 -*-
import datetime
import re


def debugLog(txt):
    fp = open("/tmp/cthulhudice.log",'a')
    dt = datetime.datetime.now()
    s = "["+dt.strftime('%c')+"]"+txt+"\n"
    fp.write(s)
    fp.close()
    return 
