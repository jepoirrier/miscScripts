#!/bin/bash
# Script to automatically remove a rectangle at the bottom of an image
# Requirements: Bash, Sed, Awk, bc and ImageMagick tools
# (c) Jean-Etienne Poirrier, 2005 - GNU GPL

if [ -z "$1" ] ; then
	echo usage: $0 image_to_be_cropped.png
	exit
fi

crop_height=30 # modify this value to adapt to other kind of rectangle
id_check=`identify "$1"`

if echo "$id_check" | grep -i "png" > /dev/null ; then
	# "oi" is for "old image" ; "ni" is for "new image"
	ni_name=`echo "$1" | sed 's/.png$/-crop.png/i'`
	oi_size=`identify "$1" | awk '{print $3}'`
	oi_size_width=`echo "$oi_size" | sed 's/[^0-9]/ /g' | awk '{print $1}'`
	oi_size_height=`echo "$oi_size" | sed 's/[^0-9]/ /g' | awk '{print $2}'`
	ni_size_height=$(echo "$oi_size_height - 30" | bc)
	ni_size=`echo "$oi_size_width"x"$ni_size_height"`
	echo "Cropping $1 ($oi_size) to $ni_name ($ni_size)..."
	convert $1 -crop "$oi_size_width"x"$ni_size_height"+0+0 +repage $ni_name
else
   echo "$1 is not a png file, script aborted"
fi

# end of script
# Script URL: http://www.poirrier.be/~jean-etienne/info/rmpos
