#!/usr/bin/python
# Displays URL of last FRANCE2 television news programme
# jepoirrier@gmail.com - last modification & valid on July 18th, 2007

import urllib2
import time

def to2digits(n):
	m = str(n)
	if len(m) == 1:
		m = '0' + m
	else:
		m = m[0:2]
	return m

cutStart = 0
cutStop = 0

ct = time.localtime()
timestamp = str(ct[0]) + to2digits(ct[1])
if ct[3] < 21: # too early to download today video if < 9.00pm
	# dDisplaying yesterday URL
	timestamp = timestamp + to2digits(ct[2]-1)
else:
	# displaying today URL
	timestamp = timestamp + to2digits(ct[2])

URL = 'http://jt.france2.fr/20h/rubrix/asx.php?JT=20h/HD_20h_'
URL = URL + timestamp + '&start=0&WMCache=0'

htmlpage = urllib2.urlopen(URL)
for line in htmlpage.readlines():
	cutStart = line.find('href="mms')
	if cutStart > 0:
		cutStart = cutStart + 6
		cutStop = line.find('" />')
		print line[cutStart:cutStop]
		break;
