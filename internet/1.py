#!/usr/bin/env python
#coding: utf-8

import socket

s = socket.socket()

host = socket.gethostname()
port = 1234
s.bind((host, port))

s.listen(5)
while True:
    c, addr = s.accept()
    print('Got connection form %s.' % addr)
    c.send('Thank you for connection.')
    c.close