#!/usr/bin/env python
# coding: utf8

from tornado import web
from tornado import httpserver
from tornado import ioloop
from tornado import options
from os import path

import pymongo

options.define('port', default=8000, help='run on the given port.', type=int)

class Application(web.Application):
    def __init__(self):
        handlers = [
        (r'/(\w+)', WordHandler)
        ]

        conn = pymongo.Connection('localhost', 27017)
        self.db = conn.example
        web.Application.__init__(self, handlers, debug=True)

class WordHandler(web.RequestHandler):
    def get(self, word):
        coll = self.application.db.words
        word_doc = coll.find_one({'word': word})

        if word_doc:
            del word_doc['_id']
            self.write(word_doc)
        else:
            self.set_status(404)
            self.write({'error': 'word not found.'})

    def post(self, word):
        coll = self.application.db.words
        definition = self.get_argument("definition")
        word_doc = coll.find_one({'word': word})

        if word_doc:
            word_doc['definition'] = definition
            coll.save(word_doc)
        else:
            word_doc = {'word': word, 'definition': definition}
            coll.insert(word_doc)
        del word_doc["_id"]
        self.write(word_doc)

if __name__ == '__main__':
    options.parse_command_line()
    http_server = httpserver.HTTPServer(Application())
    http_server.listen(options.options.port)
    ioloop.IOLoop.instance().start()