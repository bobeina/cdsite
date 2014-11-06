# -*-coding:utf-8 -*-
from django.utils import simplejson
from django.contrib.auth.models import User
from cthulhudice.models import Chat
from cthulhudice.models import PC,Counter,GameInfo,Round

from ifPCInGame import ifPCInGame
from debugLog import debugLog
from getGameStatue import getGameStatue
from getCrntDicePC import getCrntDicePC


# 获取当前PC所处的游戏及当前轮信息
def getGIRNDByUid(uid, nick):
    r = {}
    
    #获取PC状态，验证PC当前是否处于某个游戏中
    gid = ifPCInGame(uid)
    if gid>0:
        try:
            pl = PC.objects.filter(gameStatue=gid)
            gs = GameInfo.objects.get(pk=gid)

            #if pl.statue == 2:
            if gs.statue == 2 or gs.statue == 1:
                pclist = []
                for p in pl:
                    nick = User.objects.get(pk=p.player_id).username
                    pclist.append({"id":p.player_id,
                                   "player":nick,
                                   "sanity":p.sanity
                                   })

            if gs.statue == 2:
                rnd = Round.objects.filter(gameID=gid).order_by('-id')[0]

                rnd_id = rnd.id
                rnd_caster = rnd.caster
                rnd_victim = rnd.victim
                rnd_attackTimeBegin = rnd.attackTimeBegin
                rnd_fbTimeBegin = rnd.fbTimeBegin
                rnd_casterDice = rnd.casterDice
                rnd_victimDice = rnd.victimDice
                rnd_roundStatue = rnd.roundStatue

                act = getCrntDicePC(gid)
                
                if act["crntPC"] >0:
                    actor = act["crntPC"]
                else:
                    actor = -1
            
            else:
                rnd_id = 0
                rnd_caster = 0
                rnd_victim = 0
                rnd_attackTimeBegin = 0
                rnd_fbTimeBegin = 0
                rnd_casterDice = 0
                rnd_victimDice = 0
                rnd_roundStatue = 0
                actor = -1
            
            tempPL = simplejson.dumps(pclist)
            game = GameInfo.objects.get(pk=gid)

            d = game.createTime #
            st = d.strftime("%Y-%m-%d %H:%M:%S") #
            
            if rnd_fbTimeBegin:
                fbt = rnd_fbTimeBegin.strftime("%Y-%m-%d %H:%M:%S")
            else:
                fbt = "0"

            if rnd_attackTimeBegin:
                atime = rnd_attackTimeBegin.strftime("%Y-%m-%d %H:%M:%S")
            else:
                atime = 0
            
            r = {"nick":nick,
                 "actor":actor,
                 "gid":gid,
                 "cs":game.cthulhuSanity,
                 "statue":game.statue,
                 "ctime":st,
                 "creator":game.creator_id,
                 "winner":game.winner,
                 "ps":tempPL,
                 "rid":rnd_id,
                 "caster":rnd_caster,
                 "victim":rnd_victim,
                 "atime":atime,
                 "fbtime":fbt,
                 "cdice":rnd_casterDice,
                 "vdice":rnd_victimDice,
                 "rstatue":rnd_roundStatue
                 }
            debugLog("getGIRNDByUid() r = "+ str(r))
        except Exception,data:
            debugLog("getGIRNDByUid()"+str(Exception)+":"+str(data))
            return r

    rValue = r
    return rValue
