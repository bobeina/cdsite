# -*-coding:utf-8 -*-
from cthulhudice.models import Chat,PC,Counter,GameInfo,Round


'''
实际使用参数：gid
'''
def d_Cthulhu(gid, caster,victim, flag, ot):
    r = {}
    counter = 0
    allpc = PC.objects.filter(gameStatue=gid)
    pclist = []
    for pc in allpc:
        if pc.sanity >0:
            pc.sanity = pc.sanity -1
            pc.save(update_fields=['sanity'])
            counter = counter +1
            pclist.append( {"pid":pc.player.id, "sanity":pc.sanity, "ds":-1} )
    try:
        game = GameInfo.objects.get(pk = gid)
        game.cthulhuSanity = game.cthulhuSanity +counter

        r = {"rid":0,
             "rollFlag":flag,
	     "dice":"Cthulhu",
	     "ps":pclist,
	     "cs":game.cthulhuSanity,
	     "overtime":0,
	     "crntRid":0,
	     "pTurn":0,
	     "rtime":"",
	     "rFlag": 0,
	     "gameover":0,
	     "winner": 0
	     }
        game.save(update_fields=['cthulhuSanity'])
                             
    except:
        return r
    return r
