#!/usr/bin/python
# -*- coding: cp1252 -*-
# TODO: handling of all exceptions
import socket
import traceback
import urllib2

# get the right input stream (in case it changes everyday)
# change the address to suit your need (yes: user input needed!)
address = "http://old.rtbf.be/rtbf_2000/radios/pure128.m3u"
content = urllib2.urlopen(address)
stream = content.readlines()
stream = stream[0][7:len(stream[0])-1]
inHost = stream[0:stream.index(":")]
inPort = int(stream[stream.index(":")+1:stream.index("/")])
inPath = stream[stream.index("/"):len(stream)]

# set output stream (default is localhost:50008)
outHost = ''
outPort = 50008

# get the in/out sockets
inSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
inSock.connect((inHost, inPort))
outSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
outSock.bind((outHost, outPort))

outSock.listen(1)
outNewSock, outAddress = outSock.accept()

print 'Server at: ', outAddress

# get the info from a *file*, not a simple host URL ...
inSock.send("GET " + inPath + " HTTP/1.0\r\nHost: " + inHost + "\r\n\r\n")

try:
    while 1:
        inData = inSock.recv(2048)
        if not inData:
            print "No data"
        else:
            print "Read ", len(inData), " bytes"
        outNewSock.send(inData)
        print "Sent data to out"
except Exception:
    traceback.print_exc()

# not really needed since program will stop by Ctrl+C or sth like that:
outNewSock.close()
outSock.close()
inSock.close()
