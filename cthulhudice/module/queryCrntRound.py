# -*-coding:utf-8 -*-
from cthulhudice.models import Chat,PC,Counter,GameInfo,Round

#from debugLog import debugLog

def queryCrntRound(gid):
    if gid>0:
        try:
            r = Round.objects.filter(gameID=gid).order_by('-id')[0]
        except Exception,data:
            return {}

        rValue =  {"gid":r.gameID_id,
                   "round":r.roundNum,
                   "caster":r.caster,
                   "victim":r.victim,
                   "attTime":r.attackTimeBegin,
                   "fbTime":r.fbTimeBegin,
                   "cDice":r.casterDice,
                   "vDice":r.victimDice,
                   "roundStatue":r.roundStatue
                   }

        return rValue
    return {}
