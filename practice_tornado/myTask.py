#!/usr/bin/env python
# coding: utf8


from tornado import ioloop, httpclient
import functools

class MyTask(object):

    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def callback(self, response):
        try:
            self.gen.send(response)
        except StopIteration:
            pass

    def run(self, gen):
        self.gen = gen
        partail_func = functools.partial(self.func, *self.args, **self.kwargs)
        partail_func(callback = self.callback)

def myengine(func):
    def _(*args, **kwargs):
        task_generator = func(*args, **kwargs) # 调用download方法
        print dir(task_generator)
        task = task_generator.next() # 获得download方法由yield抛出的Task对象
        task.run(task_generator) # 运行对象
    return _

@myengine
def download(url):
    http_client = httpclient.AsyncHTTPClient()
    response = yield MyTask(http_client.fetch, url) # 创建Task对象，然后直接yield抛出
    print 'response.length =', len(response.body)
    ioloop.IOLoop.instance().stop()


download("http://www.baidu.com/")

ioloop.IOLoop.instance().start()
