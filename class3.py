#!/usr/bin/env python
#coding: utf-8

class Test(object):

    def InstanceFun(self):
        print("InstanceFun");
        print(self);

    @classmethod
    def ClassFun(cls):
        print("ClassFun");
        print(cls);

    @staticmethod
    def StaticFun():
        print("StaticFun");

    #这个函数算鸟东西？
    def Ballshurt():
        print("Ballshurt");


# t = Test();
# t.InstanceFun();
# Test.ClassFun();
# #t.Ballshurt(); #access error
# #Test.Ballshurt();
# Test.StaticFun();
# t.StaticFun();
# t.ClassFun();
# Test.InstanceFun(t);
# Test.InstanceFun(Test);




class Color(object):
    _color = (0, 0, 0);

    @classmethod
    def value(cls):
        if cls.__name__== 'Red':
            cls._color  = (255, 0, 0)

        elif cls.__name__ == 'Green':
            cls._color = (0, 255, 0)

        return cls._color

class Red(Color):
    pass

class Green(Color):
    pass

class UnknownColor(Color):
    pass

red = Red()
green = Green()
xcolor = UnknownColor()

print 'red = ', red.value()
print 'green = ', green.value()
print 'xcolor =', xcolor.value()

