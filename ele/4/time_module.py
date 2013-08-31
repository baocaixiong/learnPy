#!/usr/bin/env python
#coding: utf-8

import time

print time.localtime() #返回当前时间的9个状态元组
print time.time() #当时时间戳
print time.gmtime() #UTC事件的9个状态元组
print time.ctime() #返回一个本地的可读的时间
print time.mktime(time.localtime()) #根据9个时刻返回时间戳
print time.strftime('%a %b', time.localtime())
print time.asctime(time.localtime())
print time.strptime('2009-03-20 11:45', '%Y-%m-%d %H:%M')