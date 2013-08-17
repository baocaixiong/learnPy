#!/usr/bin/env python
#coding: utf-8

class Page(object):
    def __init__(self):
        pass
    def __get(self):
        print 'private method'

page = Page()
page._Page__get()