#!/usr/bin/env python
#coding: utf-8

import re

def trim(string, replace = ' '):
    try:
        string + ''

        return re.sub(r'^\s*((?:[\S\s]*\S)?)\s*$', r'\1', string)
    except:
        raise TypeError('is not a string')


print   '  asdfasd        '
print trim('  xxx          123')


# import os
# print os.environ

from os import path

print path.abspath(path.join(path.dirname('trim.py'), path.pardir))