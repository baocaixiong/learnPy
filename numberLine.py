#!/usr/bin/env python
#coding: utf-8

import fileinput

for line in fileinput.input(inplace = True):
    line = line.rstrip()
    num = fileinput.lineno()
    print '%-50s # %2i' % (line, num)