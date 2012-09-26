#!/usr/bin/python
"""
Simple script to find files ending with char '~'
Files ending with char '~' are typically used by Vim :-)
Written by Jean-Etienne Poirrier, 2006 (http://www.poirrier.be)

"""

import os
import time

baseDir = 'D:\\docs'
endFileChar = '~'
count = 0
t0 = time.time()

for rep, srep, fIle in os.walk(baseDir, topdown=True):
    for f in fIle:
        if f.endswith(endFileChar):
            print rep + '\\' + f
            count = count + 1
duration = time.time() - t0
print "%d files ending with ~ found in %f seconds." % (count, duration)
