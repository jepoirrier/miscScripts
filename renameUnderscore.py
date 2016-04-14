#!/usr/bin/python
# rename all pictures beginning with '_' with 'I' -> PHOTOS
import os
counter = 0
flist = os.listdir('.')
flist = filter(os.path.isfile, flist)
for f in flist:
    if f.endswith('.JPG') and f[0] == '_':
        f2 = f.replace('_', 'I', 1)
        os.rename(f, f2)
        counter = counter + 1
print 'Replaced ' + str(counter) + ' files'
