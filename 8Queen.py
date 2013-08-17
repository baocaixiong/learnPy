#!/usr/bin/env python
#coding: utf-8

def conflict(state, nextX):
    nextY = len(state)
    for i in range(nextY):
        #print state[i], nextX, nextY, i, '-----', state[i] - nextX, nextY - i, abs(state[i] - nextX) in (0, nextY - i)
        if abs(state[i] - nextX) in (0, nextY - i):
            return True
    return False

def queens(num = 8, state = ()):
    for pos in range(num):
        if not conflict(state, pos):
            if len(state) == num - 1:
                yield (pos,)
            else:
                for result in queens(num, state + (pos,)):
                    yield (pos,) + result

def prettyPrint(solution):
    """

    :param solution:
    :return:
    """

    def line(pos, length = len(solution)):
        return ". " * pos + 'X ' + '. ' * (length - pos - 1)
    for pos in solution:
        print(line(pos))


import random

prettyPrint(random.choice(list(queens())))
#print list(queens(4, (1, 3, 0)))