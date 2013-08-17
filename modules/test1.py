#!/usr/bin/env python
#coding: utf-8

import sys

sys.path.append('/home/zhangming/python/modules/subModules');

import hello

#hello = reload(hello)

# print sys.path_importer_cache

# for i in sys.path_importer_cache:
#     print i
print dir(hello), hello.__doc__

import copy

# print copy.__all__
# print hello.__file__
# 
for i in sys.argv:
    print i

import os 
#print os.environ
#os.system('ls -al')
#
#os.system('/usr/bin/firefox')

