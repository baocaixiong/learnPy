#!/usr/bin/env python
# coding: utf-8

class Model(object):
    class Meta:
        def getName(self):
            return '张明'
    def getMeta(self):
        return self.Meta

    def testMethod(self):
        pass

    def hah(self):
        print 'nihao'
    testMethod.name = 'testMethod'
    testMethod.method = hah

m = Model()
# 神奇
# print m.getMeta()().getName()

print m.testMethod.method(m)


def hahh():
    pass

hahh.name = 'hahh'

print hahh.name