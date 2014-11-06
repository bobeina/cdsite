# -*-coding:utf-8 -*-
from cthulhudice.models import Chat,PC,Counter,GameInfo,Round

import datetime

from queryCrntRound import queryCrntRound
from getCrntRoundStatue import getCrntRoundStatue
from debugLog import debugLog

intervalSeconds = 180
'''
 验证当前游戏应投骰玩家及是否超时，返回应投骰玩家ID
@ gFlag: 0:caster未投 1: caster已投 2:victim已投 3:等待caster选择 4: 等待victim选择
返回值 crntPC = -1 时，当前轮状态为结束或等待返回
'''
def getCrntDicePC(gid):
    r = {"overtime":False,"crntPC":-1,"gFlag":0, "grStatue":-1}

    #获取当前玩家所在游戏及当前轮
    r["gFlag"] = queryCrntRound(gid)

    rnd = r["gFlag"]

    #获取当前轮状态
    grDict = getCrntRoundStatue(rnd)

    grstatue = grDict["grStatue"]
    r["grStatue"] = grstatue

    if grstatue == 0 or grstatue == 3:
         s = datetime.datetime.now() - rnd["attTime"]
         r["crntPC"] = rnd["caster"]
         if s.seconds >intervalSeconds:
             r["overtime"] = True
             return r
    else:
        if grstatue == 1 or grstatue == 4:
             s = datetime.datetime.now() - rnd["fbTime"]
             r["crntPC"] = rnd["victim"]
             if s.seconds >intervalSeconds:
                r["overtime"] = True
                return r
    return r
