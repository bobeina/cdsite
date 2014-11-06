# -*-coding:utf-8 -*-
from cthulhudice.models import Chat,PC,Counter,GameInfo,Round


from debugLog import debugLog

def ifPCInGame(uid):
    inGameFlag = False

    try:
        pcstatue = PC.objects.get(player_id=uid)
        
        if pcstatue.gameStatue > 0:
            inGameFlag = True
        else:
            return 0
    except Exception,data:
        return -2

    if inGameFlag:
        try:
            ginfo = GameInfo.objects.get(pk = pcstatue.gameStatue)
            if ginfo.statue >0:
                return ginfo.id
        except Exception,data:
            es = str(Exception)+":"+str(data)
            debugLog("ifPCInGame() get gameinfo: "+str(Exception)+":"+str(data))
            return -3
    return 0
