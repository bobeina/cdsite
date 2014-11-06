# -*-coding:utf-8 -*-
from cthulhudice.models import Chat,PC,Counter,GameInfo,Round


def ifGameAvailable(gid):
    flag = False
    gs = -1
    try:
        gStatue = GameInfo.objects.get(pk = gid)
        if gStatue:
            flag = True
            gs = gStatue.statue
    except:
            pass
    rdict = {"gameAvailable":flag,"statue":gs}
    return rdict
