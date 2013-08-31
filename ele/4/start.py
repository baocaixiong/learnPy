#!/usr/bin/env python
#coding: utf-8

import time
from nntplib import NNTP

day = 24 * 60 * 60
yesterday = time.localtime(time.time() - day)

date = time.strftime('%y%m%d', yesterday)
hour = time.strftime('%H%M%S', yesterday)

serverName = 'news2.neva.ru'
group = 'alt.sex.telephone'

server = NNTP(serverName)
ids = server.newnews(group, date, hour)[1]

for id in ids:
    head = server.head(id)[3]
    for line in head:
        if line.lower().startswith('subject:'):
            subject = line[9:]
            break

    body = server.body(id)[3]
    
    print subject
    print '-' * len(subject)
    print '\n'.join(body)
