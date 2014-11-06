# -*-coding:utf-8 -*-
from cthulhudice.models import GameInfo


def getGameStatue(gid):
    try:
        g = GameInfo.objects.get(id=gid)
        return g.statue
    except:
        return
    return
