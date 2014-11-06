# -*-coding:utf-8 -*-
from cthulhudice.models import Chat,PC,Counter,GameInfo,Round

'''
获取当前轮状态：
0：caster未投；1：caster已投；2：victim已投（本轮结束）；

3：caster投出eye，等待caster指定结果
4：victim投出eye，等待victim指定结果
game为queryCrntRound()的返回值
'''
def getCrntRoundStatue(game):#(request):
    r = {"errmsg":'', "grStatue":-1}
    if game["roundStatue"]==1:
        #本轮已结束
        r["grStatue"] = 2
        return r

    #caster 未投
    if game["cDice"]==-1:
        r["grStatue"] = 0
        return r

    # 判断victim是否已投骰
    if game["vDice"]==9: #victim投出Eye，等待victim指定结果
        r["grStatue"] = 4
        return r
    
    if game["vDice"]==-1:
        if game["cDice"]==9:#caster投出Eye，等待caster指定结果
            r["grStatue"] = 3
        else:
            r["grStatue"] = 1
    else:
        r["grStatue"] =2
    return r
