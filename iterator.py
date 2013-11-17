#!/usr/bin/env python
#coding: utf-8

__metaclass__ = type


class Fibs:

    def __init__(self):
        self.a = 0
        self.b = 1

    def next(self):
        """
        :return: :raise:
        """
        print(self.a, self.b)
        self.a, self.b = self.b, self.a + self.b
        if self.b > 2000:
            raise StopIteration
        return self.a

    def __iter__(self):
        """
        :rtype : object
        :return:
        """
        return self

fibs = Fibs()
print(list(fibs))
for f in fibs:
    if f > 1000:
        print(f)
        break