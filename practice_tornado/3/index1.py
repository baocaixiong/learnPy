#!/usr/bin/env python
# coding: utf8

from tornado import web
from tornado import httpserver
from tornado import ioloop
from tornado import options
from os import path

options.define('port', default=8000, help='run on the given port.', type=int)

class MainHandler(web.RequestHandler):
    def get(self):
        self.render('index1.html', header_text=u'这是里头部',
            footer_text=u'这里是尾部')

class HelloModule(web.UIModule):
    def render(self, word):
        return self.render_string('/modules/test_module.html', word=word)


if __name__ == '__main__':
    options.parse_command_line()

    settings = {
        'template_path': path.join(path.dirname(__file__), 'templates'),
        'static_path': path.join(path.dirname(__file__), 'static'),
        'debug': True
    }

    app = web.Application(
        [
            ('/', MainHandler)
        ],
        **settings
    )

    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.options.port)
    ioloop.IOLoop.instance().start()