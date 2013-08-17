#!/usr/bin/env python3
#coding: utf-8

__author__ = 'zhangming'

import sys
import socket
import urllib.request, urllib.parse, urllib.error
import gzip
import http.cookiejar
import time

print(urllib.__file__)
class HttpTest:
    def __init__(self, timeout=10, addHeader=True):
        socket.setdefaulttimeout(timeout)

        self.__opener = urllib.request.build_opener()
        urllib.request.install_opener(self.__opener)

        if addHeader: self.addHeaders()

    def __error(self, e):
        """错误处理"""
        print(e)

    def addHeaders(self):
        """添加默认的headers"""
        self.__opener.addHeaders = [('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'),
                                    ('Connection', 'keep-alive'),
                                    ('Cache-Control', 'no-cache'),
                                    ('Accept-Language:', 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3'),
                                    ('Accept-Encoding', 'gzip, deflate'),
                                    ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')]

    def __decode(self, webPage, charset):
        if webPage.startwith(b'\x1f\x8b'):
            return gzip.decompress(webPage).decode(charset)
        else:
            return webPage.decode(charset)

    def addCookieJar(self):
        """为self.__opener添加 cookie handler"""
        cj = http.cookiejar.CookieJar()
        self.__opener.add_handler = (urllib.request.HTTPCookieProcessor(cj))

    def addProxy(self, host, type='http'):
        """设置代理"""
        proxy = urllib.request.ProxyHandler({type: host})
        self.__opener.add_handler(proxy)

    def addAuth(self, url, user, pwd):
        """添加认证"""
        pwdMessage = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        pwdMessage.add_password(None, url, url, passwd=pwd)
        auth = urllib.reuqest.HTTPBasicAuthHandler(pwdMessage)
        self.__opener.add_handler(auth)
    def get(self, url, params={}, headers={}, charset='UTF-8'):
        """HTTP GET 方法"""
        if params:
            url += '?' + urllib.parse.urlencode(params)
        request = urllib.request.Request(url)
        for (k, v) in headers.items():
            request.add_header(k, v)

        try:
            response = urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:
            return self.__error(e)
        else:
            return self.__decode(response.read(), charset)

    def post(self, url, params={}, headers={}, charset='UTF-8'):
        params = urllib.parse.urlencode(params)
        request = urllib.request.Request(url, data=params.encode(charset)) # 带 data 参数的 request 被认为是 POST 方法。
        for (k, v) in headers.items():
            request.add_header(k, v)
        try:
            response = urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:
            self.__error(e)
        else:
            return self.__decode(response.read(), charset=charset)

    def download(self, url, saveFile):
        """下载文件或者网页"""
        header_gzip = None

        for header in self.__opener.addHeaders:
            if 'Accept-Encoding' in header:
                header_gzip = header
                self.__opener.addHeaders.remove(header)

        __perLen = 0

        def reporthook(a, b, c):
            if c > 1000000:
                nonlocal __perLen
                per = (100.0 * a *b ) / c
                if per > 100: per = 100
                per = '{:.2f}%'.format(per)
                print('\b'*__perLen, per, end='')     # 打印下载进度百分比
                sys.stdout.flush()
                __perLen = len(per)+1
        print('--> {}\t'.format(url), end='')

        try:
            urllib.request.urlretrieve(url, savefile, reporthook)   # reporthook 为回调钩子函数，用于显示下载进度
        except urllib.error.HTTPError as e:
            self.__error(e)
        finally:
            self.__opener.addHeaders.append(header_gzip)
            print()

if __name__ == '__main__':
    ht = HttpTest()
    ht.addCookieJar()

    # 为了隐私，把有些关键字隐藏了哦！
    ht.get('https://www.oschina.net/home/login?goto_page=http%3A%2F%2Fwww.oschina.net%2F')
    ht.post(url = 'https://www.oschina.net/action/user/hash_login',
            params = {'email': '****@foxmail.com',
                      'pwd': 'e4a1425583d37fcd33b9*************',   #密码哈希，Firefox开发工具抓取的
                      'save_login': '1'}
    )
    ht.get('http://www.oschina.net/')
    ht.post(url = 'http://www.oschina.net/action/tweet/pub',
            params = {'user_code': '8VZTqhkJOqhnuugHvzBtME4***********',
                      'user': '102*****',
                      'msg': '大家在动弹什么？ via:(python3, urllib) ->{t}'.format(t = time.ctime())}
    )

