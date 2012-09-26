#!/usr/bin/python
# Opens a PNG image and prints timestamp on it
# (c) Jean-Etienne Poirrier, 2008 ; GNU GPL
# See http://www.epot.org/blog/?p=290

from PIL import Image, ImageDraw, ImageFont
import _imagingft # to load TrueTypeFont
import time
import os

# *** parameters -- Modify according to your needs! ***
mydir = "/home/jepoirrier/Documents/hauppauge/081123a/"
fontFile = "/home/jepoirrier/Documents/hauppauge/FreeSans.ttf"
fontSize = 15
topLeftWidthDivider = 5 # increase to make the textbox shorter in width
topLeftHeightDivider = 23 # increase to make the textbox shorter in height
textPadding = 2 # 

# *** real work ***
fileList = os.listdir(mydir)
for fileName in fileList:
    if fileName.endswith(".png"):
        fileName2 = fileName.split('.')
        fileInfo = os.stat(mydir + fileName)
        timeInfo = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(fileInfo.st_mtime))
        print(fileName + ": " + timeInfo)
        
        im = Image.open(mydir + fileName)
        myfont = ImageFont.truetype(fontFile, fontSize)
        topLeftWidth = int(im.size[0] - (im.size[0] / topLeftWidthDivider))
        topLeftHeight = int(im.size[1] - (im.size[1] / topLeftHeightDivider))
        draw = ImageDraw.Draw(im)
        draw.rectangle([topLeftWidth, topLeftHeight, im.size[0], im.size[1]], fill="black")
        draw.text([topLeftWidth + textPadding, topLeftHeight + textPadding], timeInfo, fill="lime", font=myfont)
        del draw
        
        #write image
        im.save(mydir + fileName2[0] + ".jpg", 'JPEG')
print("Done.")
