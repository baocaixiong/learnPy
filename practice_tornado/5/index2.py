#!/usr/bin/env python
# coding: utf8

from tornado import web
from tornado import httpserver
from tornado import httpclient
from tornado import options
from urllib import urlencode
from tornado import ioloop

import datetime
import json

options.define('port', default=8000, help='run on the given port.', type=int)

class MainHandler(web.RequestHandler):
    # @web.asynchronous
    def get(self):
        self.write({"haha":'hah'}) 
        
    def on_response(self, res):
        body = json.loads(res.body)
        self.write(body)
        self.finish()

if __name__ == '__main__':
    options.parse_command_line()
    settings = {
        'debug': True,
        'handlers': [
            ('/', MainHandler)
        ]
    }

    server = httpserver.HTTPServer(web.Application(**settings))
    server.listen(options.options.port)
    ioloop.IOLoop.instance().start()