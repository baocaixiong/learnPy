#!/usr/bin/env python
#coding: utf-8

import wx
app = wx.App()
win = wx.Frame(None, title = 'Simple Edit')
loadBtn = wx.Button(win, label = 'Open',
    pos = (225, 5), size = (80, 25))
saveBtn = wx.Button(win, label = 'Save', 
    pos = (315, 5), size = (80, 25))

fileName = wx.TextCtrl(win, pos = (5, 5), size = (215, 25))

contents = wx.TextCtrl(win, pos = (5, 35), size = (390, 260),
    style = wx.TE_MULTILINE | wx.HSCROLL)

win.Show()
app.MainLoop()