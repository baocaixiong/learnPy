#!/usr/bin/env python
#coding: utf-8

import MySQLdb
conn = MySQLdb.connect(host='localhost', user='root',passwd='123123')

conn.select_db('not_orm')

cursor = conn.cursor()

cursor.execute('set names utf8')  


count = cursor.execute('select * from author')

#print count

x, y = cursor.fetchone()

print x , y