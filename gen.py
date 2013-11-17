#!/usr/bin/env python
#coding: utf-8

import os
import sys
import re
from os import path
reload(sys)
sys.setdefaultencoding('utf-8')

class Gen(object):
    def __init__(self, fileName):
        if not os.path.isfile(fileName):
            print u'不是一个文件'
            sys.exit()
        self.lines = []
        with open(fileName) as f:
            for line in f.readlines():
                line = line.strip()
                if self.getCheckLineReg().match(line):
                    self.lines.append(line)
                else:
                    print u'文件格式不对'
                    sys.exit()

        if len(self.lines) < 1:
            print u'文件不能为空'
            sys.exit()
        self.origin = {} # 作为每一行的元

    def parse(self):
        for line in self.lines:
            if 1:
                pass
            eLine = EveryLine(line)
            self.origin.update({eLine.name: eLine})
            


    def getCheckLineReg(self):
        '''获得验证每行验证的re'''
        return re.compile(r'^[A-Z]:\[[A-Z ]+\]$')

class EveryLine(object):
    def __init__(self, line):
        Str = line.split(':')
        self.depends = Str[1].strip('[]').split(' ')
        self.name = Str[0]


if __name__ == '__main__':
    gen = Gen('a.txt')
    gen.parse()
    for i in dir(re.compile(r'^[A-Z]:\[[A-Z ]+\]$').match('A:[B C]\n')):
        print i
    print re.compile(r'^[A-Z]:\[[A-Z ]+\]$').match('A:[B C]\n')
    