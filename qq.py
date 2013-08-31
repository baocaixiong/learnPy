#鱼C工作室 - comeheres 练习作品  博客地址：http://www.8zata.com
from urllib import parse,request
from http import cookiejar
import time
import random
import hashlib
import msvcrt
import os
import gzip

#登录参数之一
appid = "15000101"

#默认协议头
DefaultHeaders = {
            "Accept":"*/*",
            "User-Agent":"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E)",
            "Accept-Language":"zh-cn",
            "Accept-Encoding":"gzip;deflate",
            "Connection":"keep-alive",
            "Referer":"http://qzone.qq.com"
}

#登录和发表说说需要cookies，此处设置自动处理cookies
cj = cookiejar.LWPCookieJar()
cookies = request.HTTPCookieProcessor(cj)
opener  = request.build_opener(cookies)

#密码输入，cmd命令行下运行显示*号
def pwd_input():  
    chars = [] 
    while True:
        try:
            newChar = msvcrt.getch().decode(encoding="utf-8")
        except:
            return input("【温馨提醒：当前未在cmd命令行下运行，密码输入无法隐藏】:\n")
        if newChar in "\r\n":            
             break 
        elif newChar == "\b":
             if chars:  
                 del chars[-1] 
                 msvcrt.putch("\b".encode(encoding="utf-8"))
                 msvcrt.putch( " ".encode(encoding="utf-8"))
                 msvcrt.putch("\b".encode(encoding="utf-8"))                 
        else:
            chars.append(newChar)
            msvcrt.putch("*".encode(encoding="utf-8"))
    return ("".join(chars) )

#QQ登录加密算法
def md5(string):
    try:
        string = string.encode("utf-8")
    finally:
        return hashlib.md5(string).hexdigest().upper()

def hexchar2bin(num):
    arry = bytearray()
    for i in range(0, len(num), 2):
        arry.append(int(num[i:i+2],16))
    return arry

def Getp(password,verifycode):
    hashpasswd = md5(password) 
    I = hexchar2bin(hashpasswd)
    H = md5(I + bytes(verifycode[2], encoding="ISO-8859-1"))
    G = md5(H + verifycode[1].upper())
    return G

#QQ空间GTK算法
def GetGtk(skey):
    HashId = 5381
    skey = skey.strip()
    for i in range(0, len(skey)):
        HashId = HashId + HashId * 32 + ord(skey[i])
    gtk = HashId & 2147483647
    return gtk

#取cookies对应值
def GetCookie(name):
    for cookie in cj:
        if cookie.name == name:
            return cookie.value

#GET访问
def Http(url,headers):
    rr = request.Request(url=url, headers=headers)
    with opener.open(rr) as fp:
        if fp.info().get("Content-Encoding") == 'gzip':
            f = gzip.decompress(fp.read())
            res = f.decode("utf-8")
        else:
            res = fp.read().decode("utf-8")
    return res

#POST访问
def Post(url,postdata,headers):
    if postdata:
        postdata = parse.urlencode(postdata).encode("utf-8")
    rr = request.Request(url=url,headers=headers,data=postdata)
    with opener.open(rr) as fp:
        if fp.info().get("Content-Encoding") == "gzip":
            f = gzip.decompress(fp.read())
            res = f.decode("utf-8")
        else:
            res = fp.read().decode("utf-8")
    return res

#验证码处理
def GetVerifyCode():
    check = Http("http://check.ptlogin2.qq.com/check?regmaster=&uin=%s&appid=%s&r=%s"%(uin,appid,random.Random().random()),DefaultHeaders)
    verify =  eval(check.split("(")[1].split(")")[0])
    verify = list(verify)
    if verify[0] == "1":
        img = "http://captcha.qq.com/getimage?uin=%s&aid=%s&%s"%(uin,appid,random.Random().random())
        with open("verify.jpg","wb") as f:
            rr = request.Request(url=img, headers=DefaultHeaders)
            f.write(opener.open(rr).read())
        os.popen("verify.jpg")
        verify[1] = input("需要输入验证码，请输入打开的图片\"verify.jpg\"中的验证码：\n").strip()
    return verify

#QQ登录
def Login(uid,password,verifycode):
    p = Getp(password,verifycode)
    url = "http://ptlogin2.qq.com/login?ptlang=2052&u="+uid+"&p="+p+"&verifycode="+verifycode[1]+"&css=http://imgcache.qq.com/ptcss/b2/qzone/15000101/style.css&mibao_css=m_qzone&aid="+appid+"&u1=http%3A%2F%2Fimgcache.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone&ptredirect=1&h=1&from_ui=1&dumy=&fp=loginerroralert&action=2-14-13338&g=1&t=1&dummy="
    DefaultHeaders.update({"Referer":url})
    res = Http(url,DefaultHeaders)
    if res.find("登录成功") != -1:
        tempstr =  eval(res.split("(")[1].split(")")[0])
        tempstr = list(tempstr)
        print("\n昵称："+tempstr[5]+"，登录成功！")
    elif res.find("验证码不正确") != -1:
        print("验证码错误，请重新登录")
        res = GetVerifyCode()
        res = Login(uin,password,res)
    elif res.find("帐号或密码不正确，请重新输入") != -1:
        uin = input("请输入QQ号码:\n").strip()
        print("请输入QQ密码:") 
        password = pwd_input().strip()
        res = GetVerifyCode()
        res = Login(uin,password,res)
    return res

#发表说说
def Shuo(text,uin,gtk):
    postdata = {'code_version' : '1', 'con' : text, 'feedversion' : '1', 'format' : 'fs', 'hostuin' : uin , 'qzreferrer' : 'http://user.qzone.qq.com/'+uin, 'richtype' : '', 'richval' : '', 'special_url' : '', 'subrichtype' : '', 'syn_tweet_verson' : '1', 'to_sign' : '0', 'to_tweet' : '0', 'ugc_right' : '1', 'ver' : '1', 'who' : '1'}
    res = Post("http://taotao.qq.com/cgi-bin/emotion_cgi_publish_v6?g_tk=%s"%(gtk),postdata,DefaultHeaders)
    if res.find(text) != -1:
        print("恭喜，说说发表成功！")    

print("【鱼C工作室 - comeheres 练习作品】\n【博客地址：http://www.8zata.com】\n")
uin = input("请输入QQ号码:\n").strip()
print("请输入QQ密码:") 
password = pwd_input().strip()
res = GetVerifyCode()
Login(uin,password,res)

if cj:
    skey = GetCookie("skey")
    if skey:
        gtk = GetGtk(skey)

if gtk:
    text = input("请输入说说内容:\n").strip() 
    Shuo(text,uin,gtk)

