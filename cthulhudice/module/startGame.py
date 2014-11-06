# -*-coding:utf-8 -*-
from cthulhudice.models import Chat,PC,Counter,GameInfo,Round

from debugLog import debugLog
from createNewRound import createNewRound

def startGame(gid):
    rvalue = {"errmsg":"", "pclist":[]}

    # find request.user.id created game id
    if gid <1:
        rvalue["errmsg"]="Game does not exist!"
        return rvalue

    # set game statue
    try:
        game = GameInfo.objects.get(pk=gid)
        
        if game.statue ==1:
            game.statue = 2
            allpc=PC.objects.filter(gameStatue=gid)
            pc_num = len(allpc)

            if pc_num<2:
                rvalue["errmsg"] = "not enough players!"
                return rvalue
            if pc_num>6:
                rvalue["errmsg"] = "too many players! please remove %d player(s)."%(len(pclist)-6)
                return rvalue

            # set players statue
            rvalue["pclist"] = ""
            tmpC = 0
            
            for pc in allpc:
                if tmpC ==0:
                    firstCaster = pc.player_id
                pc.sanity = 3

                #pc sequence

                #提醒：PClist部分作为投骰顺序数组保存，勿删除！
                #游戏信息使用get GIRNDByUid()获取
                
                tstr = str(pc.player_id)
                tmpC = tmpC + 1
                rvalue["pclist"] = rvalue["pclist"] + tstr
                if tmpC < pc_num:   #6:
                    rvalue["pclist"] = rvalue["pclist"] + ","

            createNewRound(firstCaster,gid)
            game.pclist = rvalue["pclist"]
            game.save(update_fields=['statue','pclist'])
    except Exception,data:
        debugLog("startGame():"+str(Exception)+":"+str(data))
        rvalue["errmsg"] = "cannot start the game!"

    return rvalue
