#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import tornado.ioloop
import tornado.web
import settings



class MainHandler(tornado.web.RequestHandler):
    def get(self, args):
        self.write(args)
        self.write('hello world!')


application = tornado.web.Application([
    (r'/(.*)', MainHandler)
])


# if __name__ == '__main__':
#     application.listen(8080)
#     tornado.ioloop.IOLoop.instance().start()