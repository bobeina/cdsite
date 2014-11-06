#coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from cthulhudice.models import Chat,PC,Counter,GameInfo,Round

import datetime

from django.utils import simplejson

from checkPCTurn import checkPCTurn
from switch import switch
from ifGameOver import ifGameOver
from debugLog import debugLog
from findNextCaster import findNextCaster
from createNewRound import createNewRound

'''

'''
def eye_choose(uid, dice, turnFlg):
    r = {"errmsg":""}
    diceIndex = {"Cthulhu":0,"Yellow":1,"Tentacle":2,"Elder":8}
    
    if dice not in diceIndex:
        r["errmsg"]="no such dice"
        return r

    attFlag = turnFlg["RollTurnInfo"]["grStatue"]
    gid = turnFlg["gid"]
    
    try:
        rnd_list = Round.objects.filter(gameID=gid).order_by('-id')[:1]
    except Exception,data:
        debugLog("eye_choose() query Round fail: "+str(Exception)+":"+str(data))
        r["errmsg"]="query round error"
        return r

    t_rnd = rnd_list[0]
    
    if attFlag ==3:
        caster = uid
        target = t_rnd.victim
        victim = target
    elif attFlag ==4:
        target = t_rnd.caster
        caster = t_rnd.victim
        victim = target
    else:
        r["errmsg"]="round statue is not for eye"
        return r
    
    if not turnFlg["PCTURN"]:
        ot = True
    else:
        ot = False

    va = {"dice":dice,
          "gid":gid,
          "caster":caster,
          "victim":victim,
          "flag":attFlag-3,
          "overtime":ot
          }

    rvalue = switch(va)
    
    if len(rvalue)==0:
        return r

    rvalue["rid"] = turnFlg["rndID"]

    if attFlag==3:
        rvalue["pTurn"] = target
        rvalue["rollFlag"] = 0
        t_rnd.casterDice = diceIndex[dice]
        t_rnd.fbTimeBegin = datetime.datetime.now()
        t_rnd.victim = target
        t_rnd.save(update_fields=['casterDice','victim','fbTimeBegin'])
    else:
        t_rnd.victimDice = diceIndex[dice]
        t_rnd.save(update_fields=['victimDice'])
        
        #if game over
        gameover = ifGameOver(gid)
        if gameover>=0:
	    rvalue["gameover"]=1
	    rvalue["winner"]=gameover
	    game = GameInfo.objects.get(pk=gid)
	    game.statue = 0
	    game.winner = gameover
	    game.save(update_fields=['statue','winner'])
	    
	    # TODO:
	    # 清除各pc游戏标志
	else:
	    rvalue["gameover"]=0

	    nextCaster = findNextCaster(gid)
	    newrid = createNewRound(nextCaster,gid)
	    rvalue["crntRid"] = newrid
	    rvalue["pTurn"] = nextCaster
	    rvalue["rtime"] = datetime.datetime.now().strftime('%Y-%B-%d %H:%M:%S')
	    rvalue["rFlag"] = 1
	    rvalue["rollFlag"] = 1

    r["info"] = rvalue
    r["target"] = target
    
    return r