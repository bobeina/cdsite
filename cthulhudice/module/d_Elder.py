# -*-coding:utf-8 -*-
from cthulhudice.models import Chat,PC,Counter,GameInfo,Round


'''
Elder Sign
– You gain 1 Sanity from Cthulhu. If there are no
Sanity tokens in the middle of the table, you get nothing.
实际使用参数：(gid, caster)
'''
def d_Elder(gid, caster,victim, flag, ot):#(gid, caster, victim, flag):
    r = {}
    g = GameInfo.objects.get(pk=gid)
    
    #10.30
    actor = caster
    
    c = PC.objects.get(player=actor)
    dc = 0
    if g.cthulhuSanity > 0:
        g.cthulhuSanity = g.cthulhuSanity -1
        c.sanity = c.sanity +1
        g.save(update_fields = ["cthulhuSanity"])
        c.save(update_fields=["sanity"])
        dc = 1
    else:
        dc = 0
    
    # check game/round statue
    pclist = []
    pclist.append( {"pid":actor, "sanity":c.sanity, "ds":dc} )
    r = {
        "rid":0,
        "rollFlag":flag,
        "dice":"Elder",
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
