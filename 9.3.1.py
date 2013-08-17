#!/usr/bin/env python
#coding: utf-8

def checkIndex(key):
    pass

class ArithmeticSequence(object):
    def __init__(self, start = 0, step = 1):
        """这里是注释"""
        self.start = start
        self.step = step
        self.change = {}

    def __getitem__(self, key):
        ArithmeticSequence.checkIndex(key)

        try:
            return self.change[key]
        except KeyError, e:
            return self.start + key*self.step

    def __setitem__(self, key, value):
        ArithmeticSequence.checkIndex(key)
        self.change[key] = value

    @staticmethod
    def checkIndex(key):
        '''这里是注释'''
        if not isinstance(key, (int, long)):
            raise TypeError('不是数字')
        if key < 0:
            raise IndexError

s = ArithmeticSequence(1, 2)

print s[4]