#!/usr/bin/env python
# coding: utf-8

from os import path
import urllib2
import cookielib
import hashlib
import gzip
import json
import urllib
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

SELF_PATH = path.abspath(path.join(path.dirname('')))


class Music163Error(IOError): pass

class DownloadMusic163(object):

    '''
    登陆163云音乐之后从登陆的用户的收藏中将歌曲找出，然后
    下载其中的音乐
    '''

    defaultHeaders = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36",
        "Accept-Language": "zh-cn",
        "Accept-Encoding": "gzip;deflate",
        "Connection": "keep-alive",
        "Referer": "http://music.163.com/"
    }

    loginUrl = "http://music.163.com/api/login/"
    playListUrl = 'http://music.163.com/api/playlist/detail'
    userMusicListUrl = 'http://music.163.com/api/user/playlist/'

    def __init__(self):
        self.cookies = cookielib.CookieJar()
        cookiePro = urllib2.HTTPCookieProcessor(self.cookies)
        urllib2.install_opener(urllib2.build_opener(cookiePro))
        self.userInfo = None
        self.mp3List = []

    def hasPassword(self, password):
        '''密码为md5加密'''
        return hashlib.md5(password).hexdigest()

    def get(self, url, headers):
        req = urllib2.Request(url=url, headers=headers)
        ret = urllib2.urlopen(req)

        encoding = ret.info().getheader("Content-Encoding")
        if encoding and encoding.find('gzip'):
            f = gzip.decompress(ret.read())
            res = f.decode("utf-8")
        else:
            res = ret.read()

        return res

    def post(self, url, postdata={}, headers={}):
        '''
        POST访问
        '''
        if postdata:
            postdata = urllib.urlencode(postdata).encode("utf-8")
        req = urllib2.Request(url=url, headers=headers, data=postdata)
        ret = urllib2.urlopen(req)

        encoding = ret.info().getheader("Content-Encoding")
        if encoding and encoding.find('gzip'):
            f = gzip.decompress(ret.read())
            res = f.decode("utf-8")
        else:
            res = ret.read()

        return res

    def login(self, username, password):
        postdata = {
            'username': username,
            'password': self.hasPassword(password),
            'rememberLogin': 'true'
        }
        loginRes = json.loads(self.post(self.loginUrl, postdata=postdata, headers=self.defaultHeaders))

        if loginRes['code'] == 200:
            print '登陆成功'
            self.loginRes = loginRes
        else:
            print '登陆失败'
            raise Music163Error

    def startPutMp3List(self):
        self.userInfo = self.loginRes['profile']
        print '欢迎您: ' + self.userInfo['nickname'] + '(' + str(self.userInfo['userId']) + ')'
        print '正在获取收藏列表...'
        userPlayList = self.getUserPlayList()
        
        for i in userPlayList:
            print '正在获得收藏: ' + i['name'] + ' 的歌曲'
            self.putMp3List(i['id'])
            
    def getUserPlayList(self):
        if self.userInfo != None:
            uid = self.userInfo['userId']
            queryDict = {'offset': '0', 'limit': '500', 'uid': uid}
            queryString = urllib.urlencode(queryDict).encode("utf-8")
            self.defaultHeaders.update({"Referer": 'http://music.163.com/my'})

            url = self.userMusicListUrl + '?' + queryString
            listJson = json.loads(self.get(url, headers=self.defaultHeaders))

            return listJson['playlist']
        else:
            raise Music163Error

    def putMp3List(self, listId):
        queryDict = {'id': listId, 'offest': '0', 'total': 'true', 'limit': '500'}

        url = self.playListUrl + '?' + urllib.urlencode(queryDict).encode("utf-8")
        print url
        listJson = json.loads(self.get(url, headers=self.defaultHeaders))

        for i in listJson['result']['tracks']:
            self.mp3List.append((i['name'], i['mp3Url']))

        

if __name__ == '__main__':
    dl163 = DownloadMusic163()
    threadSum = 50
    username = raw_input('请输入网易通行证号: ').strip()
    password = raw_input("请输入通行证密码: ").strip()
    try:
        dl163.login(username, password)
    except:
        pass
    else:
        dl163.startPutMp3List()
        for mp3 in dl163.mp3List:
            print '正在下载歌曲: ' + mp3[0]
            f = urllib2.urlopen(mp3[1])
            with open(mp3[0].decode('utf-8') + ".mp3", "wb") as file:
                file.write(f.read())

    
