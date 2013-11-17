#!/usr/bin/env python
# coding: utf8

from tornado import web
from tornado import httpserver
from tornado import ioloop
from tornado import options
from os import path


options.define('port', default=8000, help='run on the given port.', type=int)

class HelloHandler(web.RequestHandler):
    def get(self, word):
        self.render('hello.html', word=word)

class HelloModule(web.UIModule):
    def render(self, word):
        return '<h1>Hello, '+word+'</h1>'

    def embedded_javascript(self):
        return "document.write(\"hi!\")"

    def css_files(self):
        return "/static/css/newreleases.css"

if __name__ == '__main__':
    options.options.parse_command_line()
    app = web.Application(
        handlers=[
            (r'/(.+)', HelloHandler)
        ],
        template_path=path.join(path.dirname(__file__), 'templates'),
        ui_modules={'Hello': HelloModule},
        debug=True
    ) 
    server = httpserver.HTTPServer(app)
    server.listen(options.options.port)
    ioloop.IOLoop.instance().start()


