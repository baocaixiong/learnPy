#!/usr/bin/env python
# coding: utf-8

from daemon_my import Daemon
import time


class MainDaemon(Daemon):
    def run(self):
        while 1:
            print 12313
            time.sleep(1)


if __name__ == '__main__':
    d = MainDaemon('/tmp/dpid', stdout='/tmp/tmpout')
    d.start()