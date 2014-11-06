# -*-coding:utf-8 -*-
from cthulhudice.models import Chat,PC,Counter,GameInfo,Round
import datetime

from ifPCInGame import ifPCInGame
from ifGameAvailable import ifGameAvailable
from debugLog import debugLog
from get_client_ip import get_client_ip

def joinGame(gid, uid, ip):
    errmsg = ''

    # check player's statue and if in a game - and jump to current game if there's any
    iValue = ifPCInGame(uid)
    if iValue>0:
        errmsg = "already in a game!"
        return errmsg

    g = ifGameAvailable(gid)
    
    if g["gameAvailable"]:
        if g["statue"] == 1:
            # check how many players in game
            num = PC.objects.filter(gameStatue=gid)#.count()

            if len(num) < 6:
                # modify creators' game statue
                try:
                    ol = PC.objects.get(player_id = uid)
                    ol.active_time = datetime.datetime.now()
                    ol.ip = ip
                    ol.gameStatue = gid
                    ol.sanity = 3
                    ol.save(update_fields=["ip","active_time","gameStatue","sanity"])
                except Exception,data:
                    ol = PC()
                    ol.player_id = uid
                    ol.active_time = datetime.datetime.now()
                    ol.ip = ip
                    ol.gameStatue = gid
                    ol.sanity = 3
                    ol.save()

                return errmsg
            else:
                errmsg = "You cannot join the game!"
        else:
            errmsg = "You cannnot join the game!"
    else:
        errmsg = "Game does not exist!"
    return errmsg
