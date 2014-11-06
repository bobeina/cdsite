# -*-coding:utf-8 -*-
from cthulhudice.models import Chat,PC,Counter,GameInfo,Round


from debugLog import debugLog

'''
Your target (whoever you were rolling against)
loses 1 Sanity to Cthulhu. Push one token to the middle of
the table.

flag: current rolling player is caster('C') or victim('V')
实际使用参数：(gid, caster, victim, flag)
'''
def d_Yellow(gid, caster,victim, flag, ot):
    r = {}

    #10.30
    attacker = caster
    target = victim
    
    v = PC.objects.get(player=target)
    dc = 0
    g = GameInfo.objects.get(pk=gid)
    if v.sanity>0:
        v.sanity = v.sanity -1
        dc = -1
        g.cthulhuSanity = g.cthulhuSanity +1
        g.save(update_fields = ['cthulhuSanity'])
        v.save(update_fields=['sanity'])

    pclist = []
    pclist.append( {"pid":target, "sanity":v.sanity, "ds":dc} )
    r = {
        "rid":0,
        "rollFlag":flag,
        "dice":"Yellow",
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
