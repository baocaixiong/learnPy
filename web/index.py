#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web

urls = ("/(.*)", "hello")
app = web.application(urls, globals())
render = web.template.render('templates/')
db = web.database(dbn='mysql', user='root', pw='123123', db='not_orm')


class hello:
    def GET(self, name):
        if not name:
            name = 'world'

        todos = db.select('author')
        
        return render.index(todos)

if __name__ == "__main__":
    # web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    app.run()