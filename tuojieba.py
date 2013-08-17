#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib2
import re
import sys
from threading import Thread
import time
import random
import hashlib

class tieba(object):
    
    url = None
    dirPath = None
    __md5 = None

    def __init__(self):
        self.url = "http://tieba.baidu.com/f?kw=%BD%E3%CD%D1&tp=0&pn="
        self.dirPath = "/tmp/tieba/"
        self.__md5 = hashlib.md5()

    def getImages(self, page):
        url = self.url + str(page*50)
        req = urllib2.Request(url)
        res = urllib2.urlopen(url)
        html = res.read()
        rc = '<img src="[^"]*" original="[^"]*"  bpic="([^"]*)"[^>]*\/>'
        html = re.findall(rc, html, re.MULTILINE | re.DOTALL)
        return html

    def saveImg(self, images):
        for i in images:
            rand = str(random.randint(1, 10000)) + i
            self.__md5.update(rand)
            fname = self.__md5.hexdigest()
            fname = self.dirPath + fname + ".jpg"

            req = urllib2.Request(i)
            res = urllib2.urlopen(i)
            pic = res.read()

            f = open(fname, "wb");
            f.write(pic);
            f.close()

class catch(Thread):
    startPage = None
    endPage = None

    def __init__(self, start, end):
        Thread.__init__(self)
        self.startPage = start
        self.endPage = end
        
    def run(self):
        loop = range(self.startPage, self.endPage + 1)
        for i in loop:
            t = tieba()
            imgs = t.getImages(i)
            t.saveImg(imgs)
            print "get page %d success" % i
            sys.stdout.flush()

if __name__ == '__main__':
    maxPage = 500
    threadSum = 50
    if threadSum > maxPage:
        threadSum = maxPage
    urlCount = maxPage / threadSum
    
    for i in range(0, threadSum):
        c = catch(i * urlCount, (i + 1)* urlCount - 1)
        c.start()