# -*-coding:utf-8 -*-
import datetime
from cthulhudice.models import Chat,PC,Counter,GameInfo,Round

from getLastRound import getLastRound
from findPCInList import findPCInList

def ifPCisCreator(uid,gid):
    r = {"errmsg": "", "value": False}
    
    try:
        game = GameInfo.objects.get(pk = gid, creator=uid)
	if game:
            r["value"] = True
    except:
        return r
    return r
