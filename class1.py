#!/usr/bin/env python
#-*-coding: utf-8 -*-
import sys


class Page(object):
    page = None

    def __init__(self):
        print 'create new instance'

    def setPage(self, page):
        self.page = page
        return self

    def getPage(self):
        return self.page

class SubPage(Page):
    pass


print SubPage().setPage(10).getPage()