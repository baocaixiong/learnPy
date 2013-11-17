#!/usr/bin/env python
#coding: utf-8

from functools import update_wrapper
def thisIsliving(fun):
  def living(*args, **kw):
    return fun(*args, **kw) + '活着就是吃嘛。'
  return update_wrapper(living, fun)

@thisIsliving
def whatIsLiving():
  "什么是活着"
  return '对啊，怎样才算活着呢？'

print whatIsLiving()
print whatIsLiving.__doc__


ksy = {'ss': 'xx'}
print id(ksy.copy()), id(ksy)