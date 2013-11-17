#!/usr/bin/env python 
# coding: utf8

from tornado import ioloop, httpclient
import functools

class MyTask2(object):
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def callback(self, reponse):
        try:
            self.gen.send(reponse)
        except StopIteration:
            pass

    def run(self, gen):
        self.gen = gen
        partial_func = functools.partial(self.func, *self.args, **self.kwargs)
        partial_func(callback=self.callback)

def generator(func):
    def _(*args, **kwargs):
        task_generator = func(*args, **kwargs)
        task = task_generator.next()
        task.run(task_generator)

    return _

@generator
def download(url):
    http_client = httpclient.AsyncHTTPClient()
    response = yield MyTask2(http_client.fetch, url) # 创建Task对象，然后直接yield抛出
    print 'response.length =', len(response.body)
    ioloop.IOLoop.instance().stop()

download("http://www.baidu.com/")

ioloop.IOLoop.instance().start()