#!/usr/bin/env  python
#coding: utf-8
#print [x for x in range(2, 21) if x % 2 == 0]

#print [(x, y) for x in range(4) for y in (3, 1, 7, 8)]

def sort (ls): 
    return [] if ls == [] else sort([y for y in ls[1:] if y < ls[0]]) + [ls[0]] + sort([y for y in ls[1:] if y >= ls[0]])
    # 别忘了 python-2.5 的新特性条件分支表达式哦！可惜太长，不得不强制换行。


def mySort(ls):
    if ls == []:
        return ls
    else:
        return mySort([y for y in ls[1:] if y < ls[0]]) + [ls[0]] + mySort([y for y in ls[1:] if y > ls[0]])


print mySort([199,2,34,4,123,12,3,6])