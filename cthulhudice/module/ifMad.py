# -*-coding:utf-8 -*-
from cthulhudice.models import Chat,PC,Counter,GameInfo,Round

def ifMad(target):
    r = {"errmsg":"", "mad":False}
    try:
        pc = PC.objects.get(player_id=target)
        if pc.sanity <= 0:
            r["mad"] = True
    except:
        r["errmsg"] = u"unknow error!"
    return r
