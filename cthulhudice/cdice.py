#coding=utf-8
#import re
import random

class RollCthulhuDice():
    def __init__(self, name):
        self.diceIndex =["Cthullu","Yellow","Tentacle","Tentacle","Yellow","Yellow","Yellow","Yellow","Elder","Eye","Tentacle","Tentacle"]



from distutils import log

def stateA(s):
    #log.warn('stateA called')
    print "stateA called: s=",s

def stateB():
    log.warn('stateB called')

def stateC():
    log.warn('stateC called')

def stateDefault():
    log.warn('stateDefault called')


cases = {'a':stateA, 'b':stateB, 'c':stateC}

def switch(case):
    if case in cases:
        cases[case]()
    else:
        stateDefault()

def test():
    switch('b')
    switch('c')
    switch('a')
    switch('x')

test()
