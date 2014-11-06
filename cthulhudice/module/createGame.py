# -*-coding:utf-8 -*-
import datetime
from cthulhudice.models import Chat,PC,Counter,GameInfo,Round

from checkOblation import checkOblation
from ifPCInGame import ifPCInGame
from debugLog import debugLog
from get_client_ip import get_client_ip

'''
create game
'''

def createGame(uid, ip):
    r = {"errmsg":"","gid":0}
    
    # check items
    bValue1 = checkOblation(uid)
    iValue = ifPCInGame(uid)

    if bValue1 and iValue==0:
        gi = GameInfo()
        
        gi.cthulhuSanity = 0
        gi.pclist = str(uid)
        gi.winner = -1
        gi.statue = 1
        gi.createTime = datetime.datetime.now()
        gi.creator_id = uid
        gi.save()
        try:
            crntgame = GameInfo.objects.filter(creator_id=uid).order_by('-id')[:1]
            if len(crntgame)==0:
                r["errmsg"] = "create game fail."
                return r
            gid = crntgame[0]
            r["gid"] = gid.id
        except:
            r["errmsg"] = "create game fail."
            return r
        
        # modify creators' game statue
        try:
            ol = PC.objects.get(player_id = uid)
            ol.active_time = datetime.datetime.now()
            ol.ip = ip
            ol.gameStatue = gid.id
            ol.sanity = 3

            ol.save(update_fields=['ip','active_time','gameStatue','sanity'])
        except:
            ol = PC()
            ol.player_id = uid
            ol.active_time = datetime.datetime.now()
            ol.ip = ip
            ol.gameStatue = gid.id
            ol.sanity = 3
            ol.save()
        return r
    if iValue>0:
        r["errmsg"] = "already in a game!"
        r["gid"] = iValue
    if not bValue1:
        r["errmsg"] = "not enough oblation!"
    
    return r
