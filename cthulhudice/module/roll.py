#-*-coding:utf-8 -*-
from cthulhudice.models import Chat,PC,Counter,GameInfo,Round

import random
import datetime

from django.utils import simplejson

from debugLog import debugLog
from ifMad import ifMad
from switch import switch
from ifGameOver import ifGameOver
from findNextCaster import findNextCaster
from createNewRound import createNewRound
from getCrntDicePC import getCrntDicePC
from getLastRound import getLastRound


'''
attFlag: 当前行动为攻击/反击
'''
def roll(request, target, gid, cRound, turnFlg):
    debugLog("roll() begin aaa")
    uid = request.user.id
    
    attFlag = turnFlg["RollTurnInfo"]["grStatue"]
    
    r = {"errmsg":""}
    targetStatue = ifMad(target)
    
    if targetStatue["errmsg"]=="":
        mad = targetStatue["mad"]
    else:
        r["errmsg"] = targetStatue["errmsg"]
        return r
    if mad and attFlag==0:
	r["errmsg"] = "target mad" #u"目标已疯，不能进行此操作。"
        return r
    else:
        # 生成骰数
	num = random.randint(0,11)
	#num = 9
	
        # 根据骰数决定对应操作
        diceIndex =["Cthulhu","Yellow","Tentacle","Tentacle","Yellow","Yellow","Yellow","Yellow","Elder","Eye","Tentacle","Tentacle"]

        debugLog("roll()  randint: diceNum="+str(num)+" dice="+str(diceIndex[num]) )
        debugLog("roll() *** attFlag="+str(attFlag))

        #设置攻击及受害者
        if attFlag==0:
            caster = uid
            victim = target
        elif attFlag == 1:
            lastRnd = getLastRound(gid)
            caster = lastRnd.victim
            victim = lastRnd.caster
        else:
            r["errmsg"] = "unknow"
            return r
        
        r["target"] = victim
        
        if not turnFlg["PCTURN"]:
            ot = True
        else:
            ot = False
            
        # 进行相应操作：扣除被伤害者相应神智/...等
        va = {"dice":diceIndex[num],
              "gid":gid,
              "caster":caster,
              "victim":victim,
              "flag":attFlag,
              "overtime":ot
              }
        rvalue = switch(va)
        
        if len(rvalue)==0:
            return r
        rvalue["rid"] = cRound

	rnd_list = Round.objects.filter(gameID=gid).order_by('-id')[:1]
	t_rnd = rnd_list[0]
        
        rvalue["rollFlag"] = attFlag

        #更新
        if attFlag==0:
	    if diceIndex[num]!="Eye":
	        rvalue["pTurn"] = target
	    else:
	        rvalue["pTurn"] = caster
            t_rnd.casterDice = num
            t_rnd.fbTimeBegin = datetime.datetime.now()
            t_rnd.victim = target
            t_rnd.save(update_fields=['casterDice','victim','fbTimeBegin'])
        elif attFlag == 1:
            t_rnd.victimDice = num
            t_rnd.save(update_fields=['victimDice'])

            # 若本轮结束则更新本轮；
            if diceIndex[num]!="Eye":
	        # 游戏结束：sanity<1的人有5个；查找是否有获胜者；返回数据格式：
	        gameover = ifGameOver(gid)
	        if gameover>=0:
		    rvalue["gameover"]=1
		    rvalue["winner"]=gameover
		    game = GameInfo.objects.get(pk=gid)
		    game.statue = 0
		    game.winner = gameover
		    game.save(update_fields=['statue','winner'])
		else:
		    rvalue["gameover"]=0
		    
		    #查找下一个玩家，开启下一回合（轮）
		    nextCaster = findNextCaster(gid)
		    newrid = createNewRound(nextCaster,gid)
		    
		    rvalue["crntRid"] = newrid
		    rvalue["pTurn"] = nextCaster
		    rvalue["rtime"] = datetime.datetime.now()
		    rvalue["rFlag"] = 1
            else:
	        rvalue["pTurn"] = uid
	        rvalue["rollFlag"] = attFlag+3
        else:
            pass
	    
        r["info"] = rvalue

    return r
