# -*-coding:utf-8 -*-
from cthulhudice.models import Chat,PC,Counter,GameInfo,Round

from getLastRound import getLastRound
from findPCInList import findPCInList

# 查找下一个攻击者
def findNextCaster(gid):
    # 获取当前轮开始时间
    rnd = getLastRound(gid)

    game = GameInfo.objects.get(pk = gid)
    pl = game.pclist.split(",")
    bi = findPCInList(rnd.caster,pl)
    if bi == -1:
        return -1

    if bi+1>=len(pl):
        index = 0
    else:
        index = bi+1
    return int(pl[index])
