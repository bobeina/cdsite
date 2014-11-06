# -*-coding:utf-8 -*-
from cthulhudice.models import Chat,PC,Counter,GameInfo,Round

from debugLog import debugLog

# 获取游戏最后一轮并置有效标志
def getLastRound(gid):
    try:
        rnd = Round.objects.filter(gameID=gid).order_by('-id')[0]
    except:
        return 
    return rnd
