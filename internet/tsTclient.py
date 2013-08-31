#!/usr/bin/env python
#coding: utf-8

from socket import *


HOST = '0.0.0.0'
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)

tcpCliSock.connect(ADDR)

while True:
    data = raw_input('> ')
    if not data:
        break

    tcpCliSock.send(data)

    data = tcpCliSock.recv(BUFSIZ)

    if data:
        break

    print data

tcpCliSock.close()