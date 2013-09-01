#coding: utf-8


import os 
import sys
from os import path


sys.path.insert(0, path.abspath(path.join(path.dirname('test.py'))) + '/tornado')

print sys.path
import tornado

print tornado.__file__

