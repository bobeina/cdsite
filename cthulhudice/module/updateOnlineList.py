# -*-coding:utf-8 -*-
import datetime

from django.utils import simplejson
from cthulhudice.models import Chat,PC,Counter,GameInfo,Round

from debugLog import debugLog
from get_client_ip import get_client_ip

'''
    update online pc list
'''
def updateOnlineList(request):
    try:
        pc = PC.objects.get(player_id=request.user.id)
    except:
	pc = PC()

        pc.player_id = request.user.id
        pc.active_time = datetime.datetime.now()
        pc.ip = get_client_ip(request)
        pc.gameStatue = 0
        pc.sanity = 3
	pc.save()
	return True

    ip = get_client_ip(request)
    at = datetime.datetime.now()
    data_dic = {'ip':ip, 'active_time':at}
    pc.save(update_fields=data_dic)
    return True
