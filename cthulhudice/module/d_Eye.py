# -*-coding:utf-8 -*-
from cthulhudice.models import Chat,PC,Counter,GameInfo,Round


'''
实际使用参数：(gid, caster)
'''
def d_Eye(gid, caster,victim, flag, ot):#(gid, caster, victim, flag):
    r = {
        "rid":0,
        "rollFlag":flag,
        "dice":"Eye",
        "ps":[],
        "cs":0,
        "overtime":0,
        "crntRid":0,
        "pTurn":0,
        "rtime":"",
        "rFlag": 0,
        "gameover":0,
        "winner": 0
        }
    return r
