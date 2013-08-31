#!/usr/bin/env python
#coding: utf-8

import re


def data():
    data = []
    def match(line):
        def changeType(value):
            try:
                return int(value)
            except:
                return float(value)

        reg = re.compile(r'^(\d{4})\s+?(\d{1,2})\s+?(\d+?\.\d+?)\s+?(\d+?\.\d+?)\s+?(\d+?\.\d+?)')
        matchReg = reg.match(line)
        if matchReg:
            temp = [matchReg.group(1), matchReg.group(2), matchReg.group(3), matchReg.group(4), matchReg.group(5)]
            newTemp = map(changeType, temp)

            return tuple(newTemp)
        else:
            return False
    with open('/home/zhangming/python/ele/2/Predict.txt', 'r') as file:
        for line in file.readlines():
            matchData = match(line)
            if matchData:
                data.append(matchData)
            else:
                continue;

    return data