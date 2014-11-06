# -*-coding:utf-8 -*-
from cthulhudice.models import Chat,PC,Counter,GameInfo,Round

from debugLog import debugLog
from ifPCInGame import ifPCInGame
from getCrntDicePC import getCrntDicePC
from isNextCaster import isNextCaster
from getLastRound import getLastRound
from createNewRound import createNewRound

# 判断当前是否该玩家投骰：若非，判断当前投骰玩家是否超时
# 未超时：PCTURN = True RollToken = True
# 当前轮超时但是当前uid为下一个投骰者：PCTURN = False RollToken = True
#     r["RollTurnInfo"]["crntPC"]= uid
def checkPCTurn(uid):
    try:
        gid = ifPCInGame(uid)
    except Exception,data:
        es = str(Exception)+":"+str(data)
        debugLog("   check PCTurn() ifPCInGame:"+es)
        
    r = {"PCTURN":False,"RollToken":False, "rndID":-1, "gid": gid}
    
    if gid <=0:
        return r

    try:
        tmpDicePC = getCrntDicePC(gid)
        r["RollTurnInfo"] = tmpDicePC
    except Exception,data:
        es = str(Exception)+":"+str(data)
        debugLog("check PCTurn () line 38:"+es)
        return r

    #无论是否超时，只要当前是该玩家投骰则返回True
    if r["RollTurnInfo"]["crntPC"]==uid:
        r["PCTURN"]=True
        r["RollToken"]=True
        return r
    elif r["RollTurnInfo"]["overtime"]==True:
        
        #非uid投骰，且当前超时：
        #  检查下一个投骰者是否uid
        nextpc = isNextCaster(uid,gid)
        
        #    若是则设置当前轮状态，生成新轮，并返回新生成的轮信息
        ##if uid == nextpc:
        if nextpc["found"]:
            r["RollToken"]=True
            # set crnt turn statue;
            rnd = getLastRound(gid)
            rnd.roundStatue = 1
            rnd.save(update_fields=["roundStatue"])
            # generate new turn;
            createNewRound(nextpc["rcntPC"],gid)
            r["rndID"]=rnd.id
            return r
    else:
        return r
    return r
