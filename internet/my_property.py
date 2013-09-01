#!/usr/bin/env python
# coding: utf-8

class Page(object):
    def __init__(self):
        self.age = None

    def getAge(self):
        return self.age

    def setAge(self, age):
        self.age = age

    def test(self):
        print self.getAge()

class TestProperty(object):
    def __init__(self):
        self.__ha = 123

    def getHa(self):
        return self.__ha

    def setHa(self, value):
        self.__ha = value

    def deleteHa(self):
        del self.__ha

    ha = property(getHa, setHa, deleteHa, '')

class TestProperty1(object):
    def __init__(self):
        self.__ha = None

    @property
    def ha(self):
        return self.__ha

    @ha.setter
    def ha(self, value):
        self.__ha = value

    @ha.deleter
    def ha(self):
        del self.__ha

b = TestProperty1()

b.ha = 123
print b.ha