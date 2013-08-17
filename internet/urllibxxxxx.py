#!/usr/bin/env python
#coding: utf-8

# import urllib
# response = urllib.urlopen('http://www.baidu.com/')
# html = response.read()

# print html


from urllib import urlopen

import re

p = re.compile(r'<a[^>]+href\s*=\s*[\"\']?([^\"\' ]+)[\"\']?.*?\>([\w\W]*?)\<\/a>?')

text = urlopen('http://www.python.org/community/jobs/').read()

#print text
for url, name in p.findall(text):
    print '%s (%s)' % (name, url)