#!/usr/bin/env python
# coding:utf8

import json 


a = {'a': 'aa', 'b': 'bb', 'c': 'cc'}
b = ['aa', 'bb', 'cc', 'dd', {'a': 'aa', 'b': 'bb', 'c': 'cc'}]

print type(json.dumps(b))
print json.dumps(b)

import random

print random.choice(b)
import sys
reload(sys)
sys.setdefaultencoding('utf8')


print random.choice(u"学习Python")