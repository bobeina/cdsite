# -*-coding:utf-8 -*-
from cthulhudice.models import Chat,PC,Counter,GameInfo,Round

from django.utils import simplejson
import json

from ifPCInGame import ifPCInGame
from get_client_ip import get_client_ip

'''
public
@desc online players list
return a list
'''
def getPcList(request):
    uid = request.user.id
    found = False
    gameID = ifPCInGame(uid)
    if gameID == 0:
        return simplejson.dumps([])
    
    try:
        p = PC.objects.get(player_id=uid) 
        if p:
            found = True
    except:
        pass
    
    ip = get_client_ip(request)
    
    if not found: 
        ol = PC()
        
        ol.player_id = uid
        ol.ip = ip
        ol.sanity = 3
        ol.save()
    
    ols = PC.objects.filter( Q(gameStatue=gameID) )

    olplayers = []
    for player in ols:
        nick = User.objects.get(pk=player.player_id).username 
        olplayers.append({'id':player.player_id, 
                          'player':nick,
                          'sanity':player.sanity
                          })
    r = simplejson.dumps(olplayers)
    return r