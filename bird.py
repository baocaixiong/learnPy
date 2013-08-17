#!/usr/bin/env python
#coding: utf-8

class Bird(object):
    def __init__(self):
        self.hungry = True
    def eat(self):
        if self.hungry:
            print 'Ahaaaa...'
            self.hungry = False
        else:
            print 'No, thanks.'

# bird = Bird()
# bird.eat()
# bird.eat()

class SongBird(Bird):
    def __init__(self):
        # Bird.__init__(self) #old
        super(SongBird, self).__init__() #new object 即使子类继承了多个类，也能使用这样的一句话将所有的父类全部初始化
        self.sound = '唱歌'

    def song(self):
        print self.sound

songBird = SongBird()
songBird.song()
songBird.eat()