#!/usr/bin/env python 
# coding: utf8

def d1(func):
    def _():
        return func
    return _

def d2(func):
    return func()


@d2
@d1
def d3(url):
    print url
    return '张明'

print d3('http://www.baidu.com')


aa = [1, 2, 3]

bb = [x for x in aa if x >= 2]

print bb
import os
import sys

print sys.path[0]

import time

print int(time.time()), type(time.localtime())

import datetime

print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

print str(datetime.datetime.today()).rsplit('.', 1)[0]