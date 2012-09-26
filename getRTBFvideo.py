#!/usr/bin/python
# Displays URL of last RTBF1 television news programme
# jepoirrier@gmail.com - last modification & valid on July 18th, 2007

import urllib2

cutStart = 0
cutStop = 0

htmlpage = urllib2.urlopen('http://skynet.rtbf.be/index.html?pq=medium')
for line in htmlpage.readlines():
	cutStart = line.find('src="mms')
	if cutStart > 0:
		cutStart = cutStart + 5
		cutStop = line.find('.wmv"') + 4
		print line[cutStart:cutStop]
		break;
