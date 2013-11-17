#!/usr/bin/env python
# coding: utf8

from tornado import httpserver
from tornado import web
from tornado import ioloop
from tornado import options
from uuid import uuid4

class ShopCart(object):
    totalInventory = 10
    callbacks = []
    carts = {}

    def register(self, callback):
        self.callbacks.append(callable)

    def moveItemToCart(self, session):
        if session in self.carts:
            return

        self.carts[session] = True
        self.notifyCallbacks()

    def notifyCallbacks(self):
        for c in self.callbacks:
            self.callbackHelper(c)

    def callbackHelper(self, callback):
        callback(self.getInventoryCount())

    def getInventoryCount(self):
        return self.totalInventory - len(self.carts)

    def removeItemFromCarts(self, session):
        if session not in self.carts:
            return

        del self.carts[session]
        self.notifyCallbacks()

class DetailHandler(web.RequestHandler):
    def get(self):
        session = uuid4()
        count = self.application.shoppingCart.getInventoryCount()
        self.render('index3.html', session=session, count=count)

class CartHandler(web.RequestHandler):
    def post(self):
        action = self.get_argument('action')
        session = self.get_argument('session')

        if not session:
            self.set_status(400)
            return

        if action == 'add':
            self.application.shoppingCart.moveItemToCart(session)
        elif action == 'remove':
            self.application.shoppingCart.removeItemFromCarts(session)
        else:
            self.set_status(400)
            return
class StatusHandler(web.RequestHandler):
    @web.asynchronous
    def get(self):
        self.application.shoppingCart.register(self.async_callback(self.callback))

    def callback(self, count):
        self.write('{"inventory": "%d"}' % count)
        self.finish()

class Application(web.Application):
    def __init__(self):
        self.shoppingCart = ShopCart()
        handlers = [
            ('/', DetailHandler),
            ('/cart', CartHandler),
            (r'/cart/status', StatusHandler)
        ]

        settings = {
            "template_path": 'templates',
            'static_path': 'static'
        }

        web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
    options.parse_command_line()
    app = Application()

    server = httpserver.HTTPServer(app)
    server.listen(8000)
    ioloop.IOLoop.instance().start()