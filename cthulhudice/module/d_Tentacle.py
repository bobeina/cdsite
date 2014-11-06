# -*-coding:utf-8 -*-
from cthulhudice.models import Chat,PC,Counter,GameInfo,Round

from debugLog import debugLog

'''
The Caster takes 1 Sanity from the Victim, whether
the Caster or the Victim rolls the Tentacle. If the Caster is
mad when he attacks, he does not get to keep the stolen
Sanity. It goes to Cthulhu.

flag: current rolling player is caster('C') or victim('V')
需要一个 get round statue函数：用于获取当前投骰者是受害者或进攻者的状态字段
实际使用参数：(gid, caster, victim, flag)
'''
def d_Tentacle(gid, caster,victim, flag, ot):
    r = {}
    
    if flag == 0 or flag == 3:
        attacker = caster
        target = victim
    elif flag == 1 or flag == 4:
        attacker = victim
        target = caster
    else:
        return r

    try:
        v = PC.objects.get(player=target)
        c = PC.objects.get(player=attacker)
    except:
        return r

    dc = 0
    g = GameInfo.objects.get(pk=gid)
    if v.sanity>0:
        v.sanity = v.sanity - 1
	v.save(update_fields=['sanity'])
    if c.sanity > 0:
        c.sanity = c.sanity + 1
        dc = 1
        c.save(update_fields=['sanity'])
    else:
        g.cthulhuSanity = g.cthulhuSanity +1
        g.save(update_fields = ['cthulhuSanity'])
        
    pclist = []
    pclist.append( {"pid":caster, "sanity":c.sanity, "ds":dc} )
    pclist.append( {"pid":victim, "sanity":v.sanity, "ds":-1} )

    r = {
        "rid":0,
        "rollFlag":flag,
        "dice":"Tentacle",
        "ps":pclist,
        "cs":g.cthulhuSanity,
        "overtime":0,
        "crntRid":0,
        "pTurn":0,
        "rtime":"",
        "rFlag": 0,
        "gameover":0,
        "winner": 0
        }
    return r
