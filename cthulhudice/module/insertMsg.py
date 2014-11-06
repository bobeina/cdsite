# -*-coding:utf-8 -*-
import datetime
from cthulhudice.models import Chat,PC,Counter,GameInfo,Round

#from debugLog import debugLog

'''
public
向消息列表中插入数据
'''
def insertMsg(content,sender,date,cmd,target,cmdType,gid):
    errmsg = ""
    chat = Chat()
    chat.content = content
    chat.username_id = sender
    chat.date = datetime.datetime.now()
    chat.cmd = cmd
    chat.cmdType = cmdType
    chat.target = target
    chat.gid = gid
    chat.save()
    return True
