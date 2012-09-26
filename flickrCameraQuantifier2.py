#!/usr/bin/python
"""Quantify camera usage on Flickr.

Simple script to fetch 10 images from Flickr and display their
camera make and model.
"""
import os
import sys
import time
import urllib2

# If for the first time with _my_ Windows installation:
# sys.path.append('C:\\Python24\\my')
# and for _my_ GNU/Linux installation:
# sys.path.append('/home/jepoirrier/python')

# make sure EXIF.py is in the same directory before proceeding to
# the next step. It can be downloaded from:
# http://home.cfl.rr.com/genecash/digital_camera/digital_camera.html
import EXIF

# make sure flickr.py is in the same directory before proceeding to
# the next step. It can be downloaded from:
# http://jamesclarke.info/projects/flickr/
import flickr

# make sure GadFly is installed on your system before proceeding to
# the next step. It can be downloaded from:
# http://gadfly.sourceforge.net/
import gadfly

#TODO: change the DB schema!

#***** ***** Real code begins here ***** *****#

sleepduration = 5 # duration between queries (in seconds) if<=0: only 1 query
niterations = 125 # number of times the query is done (if sleepduration<=0: ->1)
nphotostoget = 1 # number of photos to get for each query
DBdir = 'cameraDB'
DBname = 'cameraDB'

if sleepduration > 0:
    print "I will repeat a query every %s second (%s queries)" % (sleepduration, niterations)
else:
    print "I will only do 1 query"
    sleepduration = 0
    niterations = 0

# Create/Open the database
if os.path.exists(DBdir):
    print 'Database already exists. I will just open it'
    connection = gadfly.gadfly(DBname, DBdir)
    cursor = connection.cursor()
else:
    print 'Database not present. I will create it'
    os.mkdir(DBdir)
    connection = gadfly.gadfly()
    connection.startup(DBname, DBdir)
    cursor = connection.cursor()
    cmd = "CREATE TABLE camera (temps VARCHAR, cmake VARCHAR, cmodel VARCHAR)"
    cursor.execute(cmd)
    
for i in range(niterations):
    # using my modified version of flickr.py (added photos_getrecent(...))
    recentimgs = flickr.photos_getrecent('', str(nphotostoget), '1')

    imgurls = []

    for img in recentimgs:
        try:
            imgurls.append(str(img.getURL(size='Original', urlType='source')))
        except:
            print 'Error while getting an image URL'

    for imgurl in imgurls:
        imgstream = urllib2.urlopen(imgurl)
        # save the image
        f = open('tmp.jpg', 'wb')
        for line in imgstream.readlines():
            f.write(line)
        f.close()
        # get the tags
        f = open('tmp.jpg', 'rb')
        t = str(int(time.time()))
        try:
            tags = EXIF.process_file(f)
            if len(str(tags['Image Make'])) > 0:
                if len(str(tags['Image Model'])) > 0:
                    cmake = str(tags['Image Make'])
                    cmodel = str(tags['Image Model'])
                    print "Image Make: %s - Image Model: %s" % (cmake, cmodel)
                    cmd = "INSERT INTO camera(temps, cmake, cmodel) VALUES ('" + t + "', '" + cmake + "', '" + cmodel + "')"
                    cursor.execute(cmd)
                else:
                    print "Image Make: %s" % (tags['Image Make'])
                    cmd = "INSERT INTO camera(temps, cmake, cmodel) VALUES ('" + t + "', '" + cmake + "', 'Unknown')"
                    cursor.execute(cmd)
            else:
                print "No Image Make nor Model available"
                cmd = "INSERT INTO camera(temps, cmake, cmodel) VALUES ('" + t + "', 'Unknown', 'Unknown')"
                cursor.execute(cmd)
        except:
            print 'Error while getting tags from an image'
            cmd = "INSERT INTO camera(temps, cmake, cmodel) VALUES ('" + t + "', 'Unknown', 'Unknown')"
            cursor.execute(cmd)
        f.close()
        print "Iteration %d/%d done." % (i+1, niterations)

    time.sleep(sleepduration)

connection.commit()

# some clean-up
if os.path.exists('tmp.jpg'):
    try:
        os.remove('tmp.jpg')
    except:
        print 'I could not remove tmp.jpg file'
    
print "Done!"
