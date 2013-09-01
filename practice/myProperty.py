#!/usr/bin/env python
# coding: utf-8
import base64

class female(object):
    @property
    def age(self):
        template = lambda s: '{:s} {:d} 岁'.format(s, self.__age)
        if self.__age < 23:
            return template('芳龄');
        elif self.__age > 22 or self.__age < 28:
            return template('美眉')
        elif self.__age > 27 or self.__age < 38:
            return template('阿姨')
        else:
            return template('大妈')

    @age.setter
    def age(self, value):
        if value < 16:
             raise ValueError('屌丝……请不要糟蹋少女 !')
        elif value >= 60:
            raise ValueError('屌丝……你口味太重啦！')
        else:
            if '_female__age' in dir(self):
                if self.__age > value:
                    raise ValueError('屌丝……时间可以倒流的吗？！')

        self.__age = value

    @age.deleter
    def age(self):
        raise SystemError('屌丝……年轮是可以删除的吗？！')

    @property
    def breif(self):
        STR = b'CC44rqL6V2Y5vip5g2L5GqL5Oip5B+K6fmL53Cq5MCZ5My77/y45Pqb5Li65vip5g2L5Oip5B+K6My77ESa5k2q5wiY5Ly55g2L5T2b5'
        return base64.b64decode(STR[::-1])

if __name__ == '__main__':
    girlfriend = female()   

    try:
        girlfriend.age = 60
    except Exception, e:
        girlfriend.age = 23
        print e.message
    
    print( girlfriend.age )
    try:
        del girlfriend.age
    except Exception, e:
        print e.message
    
    print( girlfriend.breif )

import base64
print base64.b64decode('==QIsu45k2a5vip5Rio5'[::-1])
