#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Async memcache client for tornado

A level-triggered I/O loop.

We use epoll if it is available, or else we fall back on select(). If
you are implementing a system that needs to handle 1000s of simultaneous
connections, you should use Linux and either compile our epoll module or
use Python 2.6+ to get epoll support.

Example usage for a simple TCP server:

    import errno
    import functools
    import ioloop
    import socket

    def connection_ready(sock, fd, events):
        while True:
            try:
                connection, address = sock.accept()
            except socket.error, e:
                if e[0] not in (errno.EWOULDBLOCK, errno.EAGAIN):
                    raise
                return
            connection.setblocking(0)
            handle_connection(connection, address)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(0)
    sock.bind(("", port))
    sock.listen(128)

    io_loop = ioloop.IOLoop.instance()
    callback = functools.partial(connection_ready, sock)
    io_loop.add_handler(sock.fileno(), callback, io_loop.READ)
    io_loop.start()
"""
import socket
import functools

from tornado.ioloop import IOLoop

class MemcacheClient(object):
    """An non-blocking Memcache client backed with async socket.

    Example usage:

        from tornado import ioloop

        def handle_get(val):
            print val # we want it to return 'world'
            ioloop.IOLoop.instance().stop()

        client = async_memcache.MemcacheClient()
        client.get("hello", handle_get)
        ioloop.IOLoop.instance().start()

    get(): memcache get
    """
    GET = 'get %s\r\n'
    DELETE = 'delete %s\r\n'
    END = 'END\r\n'
    EOL = '\r\n'
    VALUE = 'VALUE'
    STORE = '%s %s %s %s %s\r\n'
    STORED = 'STORED\r\n'
    NOT_STORED = 'NOT_STORED\r\n'
    EXISTS = 'EXISTS\r\n'
    NOT_FOUND = 'NOT_FOUND\r\n'
    DELETED = 'DELETED\r\n'
    
    def __init__(self, host, port):
        self.ioloop = IOLoop.instance()
        self.host = host
        self.port = port
        self.socket = None
        self.fd = None
        self._connect()
        self._send_buffer = []
        self._last_read_callback = None
    
    def get(self, keys, callback):
        new_callback = functools.partial(self._get_callback, callback, keys)
        if isinstance(keys, (list, tuple)):
            keys = ' '.join(keys)
        self._append_to_send(self.GET % keys, new_callback)
    
    def _get_callback(self, callback, keys, data):
        is_get = isinstance(keys, basestring)
        values = {}
        if data.startswith(self.VALUE) and data.endswith(self.END):
            i = 0
            while data[i:i+5] == self.VALUE:
                p = data.find(self.EOL, i)
                _, key, _, size = data[i:p].split()
                size = int(size)
                i = p + 2
                val = data[i:i+size]
                values[key] = val
                i += size + 2
        if is_get:
            vals = values.get(keys, None)
        else:
            vals = [values.get(key, None) for key in keys]
        callback(vals)
    
    def set(self, key, val, callback, exptime=0):
        self._store('set', key, val, callback, exptime=0)
    
    def add(self, key, val, callback, exptime=0):
        self._store('add', key, val, callback, exptime=0)
    
    def replace(self, key, val, callback, exptime=0):
        self._store('replace', key, val, callback, exptime=0)
    
    def append(self, key, val, callback, exptime=0):
        self._store('append', key, val, callback, exptime=0)
        
    def prepend(self, key, val, callback, exptime=0):
        self._store('prepend', key, val, callback, exptime=0)
    
    def _store(self, cmd, key, val, callback, exptime=0):
        # <command name> <key> <flags> <exptime> <bytes> [noreply]\r\n
        datas = [self.STORE % (cmd, key, 1, exptime, len(val))]
        datas.append(val)
        datas.append(self.EOL)
        success_results = [self.STORED]
        if cmd in ('add', 'replace'):
            success_results.append(self.NOT_STORED)
        new_callback = functools.partial(self._store_callback, callback, success_results)
        self._append_to_send(''.join(datas), new_callback)
        
    def _store_callback(self, callback, success_results, data):
        callback(data in success_results)
    
    def delete(self, key, callback):
        new_callback = functools.partial(self._delete_callback, callback)
        self._append_to_send(self.DELETE % key, new_callback)
    
    def _delete_callback(self, callback, data):
        callback(data == self.DELETED)
    
    def _append_to_send(self, data, read_callback):
        if not self._send_buffer:
            self._change_to_write()
        self._send_buffer.append([data, read_callback])
    
    def _ready(self, fd, events):
        if events & IOLoop.READ:
            data = self.socket.recv(10240)
            read_callback = self._last_read_callback
            read_callback(data)
            self._last_read_callback = None
            if self._send_buffer:
                self._change_to_write()
            else:
                self._change_to_none()
        elif events & IOLoop.WRITE:
            data, read_callback = self._send_buffer.pop(0)
            self.socket.send(data)
            self._last_read_callback = read_callback
            self._change_to_read()
    
    def _change_to_write(self):
        self.ioloop.update_handler(self.fd, IOLoop.WRITE)
    
    def _change_to_read(self):
        self.ioloop.update_handler(self.fd, IOLoop.READ)
    
    def _change_to_none(self):
        self.ioloop.update_handler(self.fd, IOLoop.NONE)
        
    def _connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#        if hasattr(s, 'settimeout'): s.settimeout(self._SOCKET_TIMEOUT)
        s.connect((self.host, self.port))
        s.setblocking(0)
#        try:
#            s.connect((self.host, self.port))
#            s.setblocking(0)
#        except socket.timeout, msg:
#            self.mark_dead("connect: %s" % msg)
#            return
#        except socket.error, msg:
#            if isinstance(msg, tuple): msg = msg[1]
#            self.mark_dead("connect: %s" % msg[1])
#            return
        self.socket = s
        self.fd = s.fileno()
        self.ioloop.add_handler(self.fd, self._ready, IOLoop.NONE)
        
    def mark_dead(self, reason):
        print reason
        self._close()
        
    def _close(self):
        if self.socket:
            self.socket.close()
            self.socket = None
            
    def __del__(self):
        self._close()
        
        
if __name__ == '__main__':
    client = MemcacheClient('localhost', 11211)
    def get_callback(val):
        print val
    client.set('hello', 'world', get_callback)
    client.set('hello3', 'world3', get_callback)
    client.get('hello3', get_callback)
    client.get('hello2', get_callback)
    client.get(['hello', 'hello2', 'hello3'], get_callback)
    
    client.set('hello4', 'abc', get_callback)
    client.get('hello4', get_callback)
    client.append('hello4', 'append', get_callback)
    client.get('hello4', get_callback)
    client.prepend('hello4', 'prepend', get_callback)
    client.get('hello4', get_callback)
    client.delete('hello4', get_callback)
    client.get('hello4', get_callback)
    client.delete('hello4', get_callback)
    IOLoop.instance().start()