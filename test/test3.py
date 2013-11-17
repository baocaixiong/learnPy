#/usr/bin/env python
# coding: utf8

# def thisIsliving(fun):
#   def living(*args, **kw):
#     return fun(*args, **kw) + '活着就是吃嘛。'
#   return living

# @thisIsliving
# def whatIsLiving():
#   "什么是活着"
#   return '对啊，怎样才算活着呢？'

# print whatIsLiving()
# print whatIsLiving.__doc__


# from functools import update_wrapper

# def thisIsliving(fun):
#   def living(*args, **kw):
#     return fun(*args, **kw) + '活着就是吃嘛。'
#   return update_wrapper(living, fun)

# @thisIsliving
# def whatIsLiving():
#   "什么是活着"
#   return '对啊，怎样才算活着呢？'

# print whatIsLiving()
# print whatIsLiving.__doc__


# from functools import wraps

# def thisIsLiving(func):
#   @wraps(func)
#   def wrapper(*args, **kwargs):
#     pass

def deco(arg):
    def _deco(func):
        def __deco():
            print("before %s called [%s]." % (func.__name__, arg))
            func()
            print("  after %s called [%s]." % (func.__name__, arg))
        return __deco
    return _deco
 
@deco("mymodule")
def myfunc():
    print(" myfunc() called.")
 
@deco("module2")
def myfunc2():
    print(" myfunc2() called.")
 
myfunc()
myfunc2()


def warp(method):
    def _(func):
        print 123
        func()
        print 456

        return func

    return _

def bb():
    pass

@warp(bb)
def cc():
    print 789


cc()



