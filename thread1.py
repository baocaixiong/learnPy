#!/usr/bin/python
#-*- encoding: utf-8 -*-
import thread, time
count = 0
def threadTest():
    print '你好'
    global count                                                         
    for i in xrange(10000):
        count += 1
for i in range(10):
    thread.start_new_thread(threadTest, ())
time.sleep(3)
print count