#!/usr/bin/env python
#coding: utf-8

import sys, re
# from util import * 
# from handlers import *
# from rules import *

class Parser(object):
    '''
    A Parser reads a text file, applying rules and controlling a handler
    '''
    def __init__(self, handler):
        self.handler = handler
        self.rules = []
        self.filters = []

    def addRule(self, rule):
        self.rule.append(rule)

    def addFilter(self, pattern, name):
        def filter(block, handler):
            return re.sub(pattern, handler.sub(name), block)

        self.filters.append(filter)

    def parse(self, file):
        self.handler.start('document')
        for block in self.filters:
            