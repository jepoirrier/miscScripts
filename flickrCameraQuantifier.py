#!/usr/bin/python
#see details on http://www.epot.org/blog/
import urllib2

import EXIF
import flickr

recentimgs = flickr.photos_getrecent('', '10', '1')

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
    try:
        tags = EXIF.process_file(f)
        if len(str(tags['Image Make'])) > 0:
            if len(str(tags['Image Model'])) > 0:
                print "Image Make: %s - Image Model: %s" % (tags['Image Make'], tags['Image Model'])
            else:
                print "Image Make: %s" % (tags['Image Make'])
        else:
            print "No Image Make nor Model available"
    except:
        print 'Error while getting tags from an image'
    f.close()

print "Done!"

