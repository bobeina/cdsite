# -*-coding:utf-8 -*-
from cthulhudice.models import Chat,PC,Counter,GameInfo,Round

# 返回值
# 0: 已结束，无人获胜; -1: 未结束 uid: 已结束，返回获胜者uid
def ifGameOver(gid):
    counter = 0
    winner = -1
    allpc = PC.objects.filter(gameStatue=gid)
    for pc in allpc:
        if pc.sanity >0:
            counter = counter +1
            winner = pc.player_id
        if counter >1:
            return -1
    if counter == 0:
        return 0
    return winner
