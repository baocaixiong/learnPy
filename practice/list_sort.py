#!/usr/bin/env python
#coding: utf-8

testList = [1, 4, 5 ,4, 16, 45, 23, 67, 45, 1, 16, 67, 33, 56, 56, 34]
# 三种方法删除列表中重复的元素及效率分析！

def methodOne(list):
    list.sort()
    lenList = len(list)
    lastItem = list[-1:][0]
    for i in range(lenList - 2, -1, -1):
        if list[i] == lastItem:
            list.remove(list[i])
        else:
            lastItem = list[i]
    return list

def methodTwo(list):
    temp = []
    for i in list:
        if not i in temp:
            temp.append(i)

    return temp

def methodThree(dataList):
    return list(set(dataList))


print methodOne(testList), methodTwo(testList), methodThree(testList)