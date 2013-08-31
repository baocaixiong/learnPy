#!/usr/bin/env python
#coding: utf-8

from reportlab.lib import colors
from reportlab.graphics.shapes import * 
from reportlab.graphics import renderPDF

import dataProvide

data = dataProvide.data()[:10]

print data

drawing = Drawing(200, 150)

pred = [row[2] - 40 for row in data]
high = [row[3] - 40 for row in data]
low = [row[4] - 40 for row in data]
times = [200*((row[0] + row[1]/12.0) - 2013) - 110 for row in data]



drawing.add(PolyLine(zip(times, pred), strokeColor=colors.blue))
drawing.add(PolyLine(zip(times, high), strokeColor=colors.red))
drawing.add(PolyLine(zip(times, low), strokeColor=colors.green))

drawing.add(String(65, 115, 'Sunspots', fontsize=18, fillColor=colors.red))

renderPDF.drawToFile(drawing, 'report1.pdf', 'Sunspots')