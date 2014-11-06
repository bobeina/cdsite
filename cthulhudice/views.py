#coding=utf-8
from django.shortcuts import render
from django.db.models import Q

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from models import Chat, PC, Counter, GameInfo, Round #OnlinePC
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson
import json
import time
import datetime
import re

from django.views.decorators.csrf import csrf_protect

#..........................
import sys
sys.path.append("/your/directory/cdsite/cthulhudice/module")

from debugLog import debugLog
from insertMsg import insertMsg
from getLastRound import getLastRound
from updateOnlineList import updateOnlineList
from findPCInList import findPCInList
from get_client_ip import get_client_ip
from getCrntDicePC import getCrntDicePC
from queryCrntRound import queryCrntRound
from getCrntRoundStatue import getCrntRoundStatue
from ifPCInGame import ifPCInGame
from createGame import createGame
from checkOblation import checkOblation
from isNextCaster import isNextCaster
from checkPCTurn import checkPCTurn
from createNewRound import createNewRound
from getGameStatue import getGameStatue
from getGIRNDByUid import getGIRNDByUid
from joinGame import joinGame
from ifGameAvailable import ifGameAvailable

from startGame import startGame
from ifMad import ifMad
from switch import switch

from d_Cthulhu import d_Cthulhu
from d_Tentacle import d_Tentacle
from d_Yellow import d_Yellow
from d_Elder import d_Elder
from d_Eye import d_Eye

from ifGameOver import ifGameOver
from findNextCaster import findNextCaster
from roll import roll
from eye_choose import eye_choose

from quitGame import quitGame
from getPcList import getPcList


#..........................

intervalSeconds = 180


'''
public
@desc 页面载入或者刷新的时候，重置记录指针为0
@return 
'''

@login_required
@csrf_protect
def loadpage(request):
    try:
        sn = int(Chat.objects.order_by('-id')[0].id) 
    except:
	sn = 0

    request.session['record_offset'] = sn
    return render(request,'chat/chat.html',{'sn':sn})
    

'''
public
@desc 简单的控制添加和查询
'''
@csrf_protect
def chat(request):
    try:
        if request.method == 'POST':
	    return say(request)
        elif request.method == 'GET':
            return chatAllLog(request)
        else:
	    return HttpResponse('access deny')
    except Exception, e:
	import sys
	fp = open("/tmp/djangolog.txt",'a')
	fp.write("\nException : [")
	err = sys.exc_info()
	sa = ""
	for i in err:
	    sa = sa + str(i)
	fp.write(sa)
	fp.write("]\n")
	fp.close()
        
    return HttpResponse(simplejson.dumps({'success':True}), mimetype = 'application/json')
        
'''
public
@desc 删除对应的记录
'''
def chatDelete(request,delete_id):
    Chat.objects.get(id=delete_id).delete()
    record_offset = request.session.get('record_offset')
    request.session['record_offset'] = record_offset - 1
    return HttpResponse(simplejson.dumps({'success':True}), mimetype = 'application/json')



    
'''
public
@desc 保存用户的消息到数据库中
@param POST中的，username和content
'''
def say(request):
    req =simplejson.loads(request.body)
    content = req['content']
    cmd = req['cmd']
    target = req['target']
    uid = request.user.id
    
    
    if not cmd:
        return HttpResponse(simplejson.dumps({'success':False}), mimetype = 'application/json')

    chat = Chat()
    pattern1 = re.compile(r'<')
    content_t = re.sub(pattern1, '&lt;', content)

    pattern2 = re.compile(r'>')
    content_t = re.sub(pattern2, '&gt;', content_t)

    chat.username_id = request.user.id

    #................................................................
    if cmd == "chat":
        insertMsg(content_t,uid,datetime.datetime.now(),cmd,-1,'pub',ifPCInGame(uid))
	return HttpResponse(simplejson.dumps({'success':True}), mimetype = 'application/json')

    #..............................OK..................................
    if cmd == "GPCL":   #get pc list
	bValue = updateOnlineList(request)
	target_t = uid 
	content_t = getPcList(request)
	insertMsg( content_t, request.user.id, datetime.datetime.now(),"OLPC",uid,"pri",ifPCInGame(uid))
	return HttpResponse(simplejson.dumps({'success':True}), mimetype = 'application/json')

    #..............................OK..................................
    if cmd == "CRTG":   # create game
        bValue = updateOnlineList(request)
        
        g = createGame(uid, get_client_ip(request))

        debugLog("CRTG: createGame() return value="+str(g))
        
        if g["gid"]>0: 
            try:
                grinfo = getGIRNDByUid(uid, request.user.username)
                rCRTG = insertMsg( simplejson.dumps(grinfo),uid, datetime.datetime.now(), "CRTG", uid, "pri", g["gid"])
            except Exception,data:
                debugLog("CRTG error:"+str(Exception)+":"+str(data))
                
        else:
            rCRTG = insertMsg( g["errmsg"],uid, datetime.datetime.now(), "CRTG", uid, "pri", -1)
        
        return HttpResponse(simplejson.dumps({'success':True}), mimetype = 'application/json')

    #..............................OK..................................
    if cmd == "JOIN":   # join game
        jGid = req['gid']
        bValue = updateOnlineList(request)
        
        jg = joinGame(int(jGid), uid, get_client_ip(request))
        
        if jg =="":
	    grinfo = getGIRNDByUid(uid, request.user.username)
            insertMsg( simplejson.dumps(grinfo), uid, datetime.datetime.now(),"JOIN",0,"gam",jGid)
        else:
            insertMsg( "", uid, datetime.datetime.now(),"JOIN",uid,"pri",0)
        return HttpResponse(simplejson.dumps({'success':True}), mimetype = 'application/json')

    #.............................nearly.OK..................................
    if cmd == "STRT":   # start game
        crntGid = ifPCInGame(uid)
        
        if crntGid >0:
            sg = startGame(crntGid)
            
            if sg["errmsg"]:
                insertMsg( sg["errmsg"], uid, datetime.datetime.now(),"STRT",target_t,"pri",0)
                return HttpResponse(simplejson.dumps({'success':False}), mimetype = 'application/json')

            grin = getGIRNDByUid(uid, request.user.username)
            
            try:
	        if len(grin)>0:
		    insertMsg(simplejson.dumps(grin), uid, datetime.datetime.now(), "STRT", 0, "gam",grin["gid"] )
		else:
		    return HttpResponse(simplejson.dumps({'success':False}), mimetype = 'application/json')
            except Exception,data:
		debugLog("STRT error:"+str(Exception)+":"+str(data))
        return HttpResponse(simplejson.dumps({'success':True}), mimetype = 'application/json')

    #................................................................
    if cmd == "QRRD":   # query game round
        return HttpResponse(simplejson.dumps({'success':True}), mimetype = 'application/json')

    #................................................................
    if cmd == "ROLL":   # roll dice ( with target )
        # 获取发送者及游戏状态，决定是否可投骰，产生投骰结果，修改游戏及玩家状态，插入消息并返回
        
        #是否以自己为目标
        if target == uid:
	    return HttpResponse(simplejson.dumps({'success':True}), mimetype = 'application/json')

        iValue = ifPCInGame(uid)
        
        if iValue >0:
            gstatue = getGameStatue(iValue)
            if gstatue:
                if gstatue==2 :
                    gturn = checkPCTurn(uid)
                    
                    if gturn["RollToken"]:
                        try:
                            rollValue = roll(request,target,iValue,gturn["rndID"],gturn)#gturn["RollTurnInfo"]["gFlag"])
                        except Exception,data:
                            debugLog("call roll() error:"+str(Exception)+":"+str(data))
                            return HttpResponse(simplejson.dumps({'success':False}), mimetype = 'application/json')

                        
                        if rollValue["errmsg"] == '':
                            del rollValue["errmsg"]
                            del rollValue["info"]["rtime"] 
                            
                            ct = simplejson.dumps(rollValue)
                            dt = datetime.datetime.now()
                            
                            insertMsg( ct, uid, dt, "ROLL", target,"gam", gturn["gid"]) #gid
                            return HttpResponse(simplejson.dumps({'success':True}), mimetype = 'application/json')
                        else:
                            try:
                                insertMsg( simplejson.dumps(rollValue["errmsg"]) , uid, datetime.datetime.now(), "ROLL", 0,"pri",gturn["gid"]) #gid
                            except Exception,data:
                                debugLog("ROLL: insertMsg error: "+str(Exception)+":"+str(data))
        return HttpResponse(simplejson.dumps({'success':False}), mimetype = 'application/json')

    #................................................................
    if cmd == "EYE":   # 处理PC指定投骰结果 ***str2json: 未定***
        gid = ifPCInGame(uid)
        if gid !=0:
            gstatue = getGameStatue(gid)
            if gstatue >-1:
                gturn = checkPCTurn(uid)
                
                if gturn["RollToken"]:
                    if gturn["RollTurnInfo"]["grStatue"]==3 or gturn["RollTurnInfo"]["grStatue"]==4:
                        try:
			    eyeValue = eye_choose(uid, content_t, gturn)
			except Exception,data:
			    debugLog("EYE: eye_choose() error: "+str(Exception)+":"+str(data))
			    
                        if eyeValue["errmsg"]=="":
			    del eyeValue["errmsg"]
			    try:
			        c = simplejson.dumps(eyeValue)
			        
			        insertMsg(c, uid, datetime.datetime.now(), "EYE", eyeValue["target"],"gam",gid)
			    except Exception,data:
			        debugLog("EYE: insertMsg error: "+str(Exception)+":"+str(data))
			else:
			    insertMsg(simplejson.dumps(eyeValue["errmsg"]), uid, datetime.datetime.now(), "EYE", target,"pri",gid)
        return HttpResponse(simplejson.dumps({'success':True}), mimetype = 'application/json')

    #..............................OK..................................
    if cmd == "QRGI":   # 获取游戏状态
        bValue = updateOnlineList(request)
	grinfo = getGIRNDByUid(uid, request.user.username)
	rgiUser = uid
        nowTime = datetime.datetime.now()
        
        if len(grinfo)>0:
            try:
                info = simplejson.dumps(grinfo)
            except Exception,data:
                es = str(Exception)+":"+str(data)
                debugLog("QRGI: error msg = "+es )
            
            try:
	        insertMsg(info, rgiUser, nowTime, "QRGI", rgiUser, "pri",grinfo["gid"] )
	    except Exception,data:
	        debugLog("QRGI: insertMsg error: "+str(Exception)+":"+str(data))
        else:
            insertMsg("", rgiUser, nowTime, "QRGI", rgiUser, "pri",0)
            debugLog("QRGI: no grinfo  0.0")
        return HttpResponse(simplejson.dumps({'success':True}), mimetype = 'application/json')

    #................................................................
    if cmd == "QUIT":
        try:
	    q = quitGame(uid)
	except Exception,data:
	    debugLog("QUIT: quitGame() error: "+str(Exception)+":"+str(data))
	
	gid = q["gid"]
        if q["errmsg"]=="" and gid >0:
	    del q["gid"]
	    del q["errmsg"]
	    try:
	        insertMsg( simplejson.dumps(q), uid, datetime.datetime.now(), "QUIT", 0,"gam",gid )
	        
	        if q["owner"]=="F":
		    insertMsg( simplejson.dumps(q), uid, datetime.datetime.now(), "QUIT", uid,"pri",gid )
	    except Exception,data:
	        debugLog("QUIT: insertMsg() error: "+str(Exception)+":"+str(data))
	    return HttpResponse(simplejson.dumps({'success':True}), mimetype = 'application/json')
	    
    
    #................................................................
    
    return HttpResponse(simplejson.dumps({'success':False}), mimetype = 'application/json')


'''
public
@desc 根据session中的record_offset的数值获取以该数值为起始的所有记录
@return 返回对应的对象的字典形式
'''

def chatAllLog(request):
    if 'record_offset' in request.session:
        record_offset = request.session.get('record_offset')
    else:
        record_offset = 0
        request.session['record_offset'] = 0
    uid = request.user.id

    gameID = ifPCInGame(uid)
    
    pcGstatue = PC.objects.get(player_id=uid)
    if gameID <= 0 and pcGstatue.gameStatue==0 :
        chatList = Chat.objects.filter( Q(cmdType="pub") |
                                          Q(cmdType="sys") |
                                          Q(cmdType="ano") |
                                          Q(cmdType="pri", target = uid),#target=request.user.username),
                                          Q(id__gt=record_offset) )
    else:
        chatList = Chat.objects.filter( Q(cmdType="pub") |
                                    Q(cmdType="sys") |
                                    Q(cmdType="ano") |
                                    Q(cmdType="gam", gid=gameID) |
                                    Q(cmdType="gam", gid=pcGstatue.gameStatue) |
                                    Q(cmdType="pri", target = uid ),#target=request.user.username),
                                    Q(id__gt=record_offset) )
    
    chatlist_dict = []
    request.session['record_offset'] = len(chatList) + record_offset
    for chat in chatList:
	nick = User.objects.get(pk=chat.username_id).username

        chatlist_dict.append({'id':chat.id,
			      'content':chat.content,
                              'username_id': nick,
                              'date':str(chat.date).split('.')[0],
			      'cmd':chat.cmd,
			      'cmdType': chat.cmdType,
			      'target': chat.target,
                              'gid': chat.gid
                              })
    if gameID <= 0 and pcGstatue.gameStatue>0 :
        pcGstatue.gameStatue = 0
        pcGstatue.save(update_fields=['gameStatue'])

    return HttpResponse(simplejson.dumps(chatlist_dict), mimetype = 'application/json')



    
'''
def ifRoundEnd():
    return
    
'''
