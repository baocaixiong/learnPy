#!/usr/bin/env python
# coding:utf-8

def upper_attr(future_class_name, future_class_parents, future_class_attr):
    '''返回一个类对象，将属性都转为大写形式'''
    attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith('__'))
    # 将它们转为大写形式
    uppercase_attr = dict((name.upper(), value) for name, value in attrs)

    return type(future_class_name, future_class_parents, uppercase_attr)

# __metaclass__ = upper_attr

class Foo(object):
    __metaclass__ = upper_attr
    bar = 'bip'

print hasattr(Foo, 'bar')

print hasattr(Foo, 'BAR')