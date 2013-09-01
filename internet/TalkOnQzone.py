#!/usr/bin/env python
# coding: utf-8

import urllib2
import cookielib
import urllib
import hashlib
import gzip
import time
import random
import os


class TalkOnQzone(object):
    # 默认协议头
    DefaultHeaders = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E)",
        "Accept-Language": "zh-cn",
        "Accept-Encoding": "gzip;deflate",
        "Connection": "keep-alive",
        "Referer": "http://qzone.qq.com"
    }

    appid = "15000101"

    def __init__(self):
        self.cookies = cookielib.CookieJar()
        cookiePro = urllib2.HTTPCookieProcessor(self.cookies)
        urllib2.install_opener(urllib2.build_opener(cookiePro))

    def md5(self, string):
        try:
            string = string.encode("utf-8")
        finally:
            return hashlib.md5(string).hexdigest().upper()

    def hexchar2bin(self, num):
        arry = bytearray()
        for i in range(0, len(num), 2):
            arry.append(int(num[i:i + 2], 16))
        return arry

    def Getp(self, password, verifycode):
        hashpasswd = self.md5(password)
        I = self.hexchar2bin(hashpasswd)
        H = self.md5(I + bytes(verifycode[2]))
        G = self.md5(H + verifycode[1].upper())
        return G

    # QQ空间GTK算法
    def GetGtk(self, skey):
        HashId = 5381
        skey = skey.strip()
        for i in range(0, len(skey)):
            HashId = HashId + HashId * 32 + ord(skey[i])
        gtk = HashId & 2147483647
        return gtk

    # 取cookies对应值
    def GetCookie(self, name):
        for cookie in self.cookies:
            if cookie.name == name:
                return cookie.value

    # GET访问
    def Get(self, url, headers):
        req = urllib2.Request(url=url, headers=headers)
        ret = urllib2.urlopen(req)

        encoding = ret.info().getheader("Content-Encoding")
        if encoding and encoding.find('gzip'):
            f = gzip.decompress(ret.read())
            res = f.decode("utf-8")
        else:
            res = ret.read()

        return res

    # POST访问
    def Post(self, url, postdata, headers):
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

    # 验证码处理
    def GetVerifyCode(self, uin):
        check = self.Get(
            "http://check.ptlogin2.qq.com/check?regmaster=&uin=%s&appid=%s&r=%s" %
            (uin, self.appid, random.Random().random()), self.DefaultHeaders)
        verify = eval(check.split("(")[1].split(")")[0])
        verify = list(verify)
        if verify[0] == "1":
            img = "http://captcha.qq.com/getimage?uin=%s&aid=%s&%s" % (
                uin, self.appid, random.Random().random())
            with open("verify.jpg", "wb") as f:
                rr = urllib2.Request(url=img, headers=self.DefaultHeaders)
                f.write(urllib2.urlopen(rr).read())
            os.popen("./verify.jpg")
            verify[1] = raw_input(
                "需要输入验证码，请输入打开的图片\"verify.jpg\"中的验证码：\n").strip()
        return verify

    # QQ登录
    def Login(self, uid, password, verifycode):
        p = self.Getp(password, verifycode)
        url = r"http://ptlogin2.qq.com/login?ptlang=2052&u=" + str(uid) + r"&p=" + p + r"&verifycode=" + str(verifycode[1]) + r"&css=http://imgcache.qq.com/ptcss/b2/qzone/15000101/style.css&mibao_css=m_qzone&aid=" + str(
            self.appid) + r"&u1=http%3A%2F%2Fimgcache.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone&ptredirect=1&h=1&from_ui=1&dumy=&fp=loginerroralert&action=2-14-13338&g=1&t=1&dummy="
        self.DefaultHeaders.update({"Referer": url})
        res = self.Get(url, self.DefaultHeaders)
        if res.find("登录成功") != -1:
            tempstr = eval(res.split("(")[1].split(")")[0])
            tempstr = list(tempstr)
            print("\n昵称：" + tempstr[5] + "，登录成功！")
        elif res.find("验证码不正确") != -1:
            print("验证码错误，请重新登录")
            res = self.GetVerifyCode(uid)
            res = self.Login(uin, password, res)
        elif res.find("帐号或密码不正确，请重新输入") != -1:
            uin = raw_input("请输入QQ号码:\n").strip()
            print("请输入QQ密码:")
            password = raw_input("请输入QQ密码:").strip()
            res = self.GetVerifyCode(uid)
            res = self.Login(uin, password, res)
        return res

    def Shuo(self, text, uin, gtk):
        postdata = {'code_version': '1', 'con': text, 'feedversion': '1', 'format': 'fs', 'hostuin': str(uin), 'qzreferrer': 'http://user.qzone.qq.com/' + str(
            uin), 'richtype': '', 'richval': '', 'special_url': '', 'subrichtype': '', 'syn_tweet_verson': '1', 'to_sign': '0', 'to_tweet': '0', 'ugc_right': '1', 'ver': '1', 'who': '1'}
        res = self.Post(
            "http://taotao.qq.com/cgi-bin/emotion_cgi_publish_v6?g_tk=%s" %
            (gtk), postdata, self.DefaultHeaders)
        if res.find(text) != -1:
            print("恭喜，说说发表成功！")


if __name__ == '__main__':
    print '仿写From comeheres'
    talkOnQzone = TalkOnQzone()
    uid = input('请输入QQ号码: ')
    password = raw_input("请输入QQ密码:").strip()
    res = talkOnQzone.GetVerifyCode(uid)
    talkOnQzone.Login(uid, password, res)

    skey = talkOnQzone.GetCookie("skey")
    if skey:
        gtk = talkOnQzone.GetGtk(skey)

    if gtk:
        text = raw_input("请输入说说内容:\n").strip()
        talkOnQzone.Shuo(text, uid, gtk)
