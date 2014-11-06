# -*-coding:utf-8 -*-

# 在列表中查找特定pc
def findPCInList(uid,pclist):
    for i in range(0,len(pclist)):
        if uid == int(pclist[i]):
            return i
    return -1
