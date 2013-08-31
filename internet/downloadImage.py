#!/usr/bin/env python
# coding: utf-8

class Page(object):
    def __init__(self):
        self.age = 12

    def getAge(self):
        return self.age

    def setAge(self, age):
        self.age = age

    def test(self):
        print self.getAge()

page = Page()
page.test()