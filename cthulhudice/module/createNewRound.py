# -*-coding:utf-8 -*-
import datetime
from cthulhudice.models import Chat,PC,Counter,GameInfo,Round

from debugLog import debugLog
from getLastRound import getLastRound

'''
创建新轮数据
'''
def createNewRound(caster,gid):
    #rnum = 0
    try:
        rnum = Round.object.filter(gameID = gid).count() +1
    except:
        rnum = 0
    
    if rnum ==0:
        casterID = caster
    
    gr = Round()    
    gr.gameID_id = gid
    gr.roundNum = rnum
    gr.caster = casterID
    gr.victim = -1
    gr.attackTimeBegin = datetime.datetime.now()
    gr.casterDice = -1
    gr.victimDice = -1
    gr.roundStatue = 0
    gr.save()
    rnd = getLastRound(gid)

    if rnd:
        return rnum

    return -1
