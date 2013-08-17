#!/usr/bin/env python
#coding: utf-8

mySum = 0

for i in range(1000):
    if i % 3 == 0 or i % 5 == 0:
        mySum += i

print mySum


print sum([i for i in range(1000) if i % 3 == 0 or i % 5 == 0])


#fib=lambda n,x=0,y=1:x if not n else fib(n-1,y,x+y)

def fib(n):
    x, y = 0, 1
    while(n):
        x, y, n = y, x+y, n-1
    return x

print fib(4000000)