# -*-coding:utf-8 -*-
from d_Cthulhu import d_Cthulhu
from d_Tentacle import d_Tentacle
from d_Yellow import d_Yellow
from d_Elder import d_Elder
from d_Eye import d_Eye


'''
v = { dice, gid, caster, victim, flag }
'''
def switch(v):
    diceProc = {"Cthulhu":d_Cthulhu,
                "Tentacle":d_Tentacle,
                "Yellow":d_Yellow,
                "Elder":d_Elder,
                "Eye":d_Eye
                }
    return diceProc.get(v["dice"])(v["gid"], v["caster"], v["victim"], v["flag"], v["overtime"])
