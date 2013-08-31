#!/usr/bin/env python
#coding: utf-8

import re, urllib2, time, sys, Queue, threading, jieba, chardet
from BeautifulSoup import BeautifulSoup
from os import path

DEEP = 1000 # 深度?

PATH = path.abspath(path.join(path.dirname('MySpider.py'))) + '/temp/'
print PATH
urlQueue = Queue.Queue()

class MySpider(threading.Thread):
    def __init__(self, writeFile=False):
        threading.Thread.__init__(self)
        self.writeFile = writeFile

    def run(self):
        currUrl = urlQueue.get()
        while currUrl:
            html = self.getContents(currUrl)
            self.parseUrl(html)
            self.getKeyWords(html)
            if self.writeFile:
                self.wirteToFile(html, currUrl)

    def parseUrl(self, html):
        reUrl = re.compile(r'<\s*[Aa]{1}\s+[^>]*?[Hh][Rr][Ee][Ff]\s*=\s*[\"\']?([^>\"\']+)[\"\']?.*?>')
        urls = reUrl.findall(html)
        for url in urls:
            if len(url) > 10 and url.find('javascript') == -1:
                # 长度>10，并且不包含javascript字样
                urlQueue.put(url)

    def getContents(self, url):
        try:
            url = urllib2.quote(url.split('#')[0].encode('utf-8'), safe="%/:=&?~#+!$,;'@()*[]")
            req = urllib2.urlopen(url)
            res = req.read()
            code = chardet.detect(res)['encoding']
            return res
        except urllib2.HTTPError, e:
            print e.code
            return None
        except urllib2.URLError, e:
            print str(e)
            return None

    def wirteToFile(self, html, url):
        print PATH + str(time.time()) + '.html'
        fp = file(PATH + str(time.time()) + '.html', 'w')
        fp.write(html)
        fp.close()

    def getKeyWords(self, html):
        code = chardet.detect(html)['encoding']
        if code == 'ISO-8859-2':
            html = html.decode('gbk', 'ignore').encode('utf-8', 'ignore')

        soup = BeautifulSoup(html, fromEncoding='utf-8')
        titleTag = soup.title
        titleKeyWord = titleTag.contents[0]
        # self.cutWords(titleKeyWord)

    def cutWords(self, content):
        res = jieba.cut_for_search(content)
        res = '\n'.join(res)
        keyWords = file(PATH + 'cutKeyWors.txt', 'w')
        keyWords.write(res)
        keyWords.close()


if __name__ == '__main__':
    startUrl = 'http://www.baidu.com'
    
    urlQueue.put(startUrl)
    threadSum = 2

    for i in range(0, threadSum):
        mySpider = MySpider(True)
        mySpider.start()

