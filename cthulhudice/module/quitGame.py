# -*-coding:utf-8 -*-
import datetime
from cthulhudice.models import Chat,PC,Counter,GameInfo,Round

from ifPCInGame import ifPCInGame
from debugLog import debugLog

'''
quit game
'''

def quitGame(uid):
    r = {"errmsg":"","gid":0, "owner":"F", "pc":uid}  #False

    iValue = ifPCInGame(uid)
    if iValue>0:
        game = GameInfo.objects.get(pk=iValue)
        if game.statue ==1:
	    if game.creator_id == uid:
	        game.statue = 0
	        game.save(update_fields=['statue'])
	        r["owner"]="T"  #True
	    else:
	        pc = PC.objects.get(player_id=uid)
	        pc.gameStatue = 0
	        pc.save(update_fields=['gameStatue'])
	    r["gid"]=iValue
	    r["pc"]=uid
	else:
	    r["errmsg"]="not waiting"
    return r;