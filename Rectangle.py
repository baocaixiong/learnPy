#!/usr/bin/env python
#coding: utf-8

__metaclass__ = type
class Rectangle:
    def __init__(self):
        self.width = 0
        self.height = 0
    def setSize(self, size):
        self.width, self.height = size
        return self

    def getSize(self):
        return self.width, self.height

    size = property(getSize, setSize)#第一个参数是取值，第二个参数是赋值

r = Rectangle()
r.setSize((1, 2))
r.size = (1, 200)
print r.size 