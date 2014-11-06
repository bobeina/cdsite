# -*-coding:utf-8 -*-
import datetime
from cthulhudice.models import Chat,PC,Counter,GameInfo,Round

from getLastRound import getLastRound
from findPCInList import findPCInList

# 是否超时
# 返回一个超时后可用的列表
def isNextCaster(uid,gid):
    r = {"errmsg": "", "found": False, "rcntPC":-1,"low":-1, "high":-1, "victim":False}
    # 获取当前轮开始时间
    rnd = getLastRound(gid)
    if rnd.fbTimeBegin:
        btime = rnd.fbTimeBegin
        #判断是否当前轮受害者
        if uid == rnd.victim:
            r["victim"] = True
            r["found"] = True
            return r
    else:
        btime = rnd.attackTimeBegin
    
    rt =  datetime.datetime.now() - btime
    border = rt.seconds/intervalSeconds
    pc_num = PC.objects.filter(gameStatue=gid).count()
    if border >=pc_num:	#6: #超时一轮，游戏结束
        r["errmsg"] = "overtime"
        return r   #
    else:
        game = GameInfo.objects.get(pk = gid)
        pl = game.pclist.split(",")
        bi = findPCInList(uid,pl)
        if bi == -1:
            r["errmsg"] = "no such pc"
            return r
        r["low"] = bi
        r["rcntPC"] = int(pl[bi])
        l = bi + border
        LA = len(pl)
        for i in range(bi,l):
            if i<LA:
                index = i
            else:
                index = (LA - i)*(-1)
            if int(pl[index]) == uid:
                r["found"] = True
                r["high"] = index
                return r
    return r
