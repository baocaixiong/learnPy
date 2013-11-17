#!/usr/bin/env python
# coding: utf8

import textwrap

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options

from tornado.options import define, options

define('port', default=8000, help='run on the given port.', type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ', friendly user!')
    def write_error(self, status_code, **kwargs):
        self.write("Gosh darnit, user! You caused a %d error." % status_code)

class ReverseHandler(tornado.web.RequestHandler):
    def get(self, input):
        self.set_status(400)
        self.set_header('Content-Type', 'application/json')
        self.write(input[::-1])


class WrapHandler(tornado.web.RequestHandler):
    def post(self):
        text = self.get_argument('text')
        width = self.get_argument('width', 40)

        self.write(textwrap.fill(text, int(width)))


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=(
            (r'/', IndexHandler),
            (r'/reverse/(\w+)', ReverseHandler),
            (r'/wrap', WrapHandler)
        ),
        debug=True
    )

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()