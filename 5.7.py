#!/usr/bin/python
#coding=utf-8

girls = ['alice', 'bernice', 'clarice']
boys = ['chris', 'arnold', 'bob', 'dddd', 'xxx']

# print [b+'='+g for b in boys for g in girls if b[0] == g[0]]

letterGirls = {}

for girl in girls:
    letterGirls.setdefault(girl[0], []).append(girl)


# print [b+'+'+g for b in boys for g in letterGirls[b[0]]]
# 
print [b + '+' for b in boys if letterGirls.get(b[0])]

def parrot(voltage, state='a stiff', action='voom', type='Norwegian Blue', *test):
    print "-- This parrot wouldn't", action,
    print "if you put", voltage, "Volts through it."
    print "-- Lovely plumage, the", type
    print "-- It's", state, "!"

parrot(1000, ('asdfdasf'))
# parrot(action = 'VOOOOOM', voltage = 1000000)
# parrot('a thousand', state = 'pushing up the daisies')
# parrot('a million', 'bereft of life', 'jump')

