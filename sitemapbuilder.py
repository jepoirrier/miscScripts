#!/usr/bin/python
"""
Simple script to automatically build a sitemap for web robots
documentation: https://www.google.com/webmasters/sitemaps/docs/en/protocol.html
Written by Jean-Etienne Poirrier, 2006 (http://www.poirrier.be)
TODO: HTML entities encoding, auto export to FTP
More potential features: list of specific files to exclude (e.g. php file to be
     included in another one), ... suggestions welcome at jepoirrier@gmail.com

"""
import os
import time

# variables to suit your needs
baseDir = '/path/to/your/local/website' # on Windows: please use \\ instead of \
baseUrl = 'http://www.yourwebsite.com'
acceptedExtensions = [ 'htm', 'html', 'php' ]
filenamesToStrip = [ 'index' ]
changeFreq = 'monthly' # choices are: always, hourly, daily, weekly, monthly,
                       # yearly and never - see doc for details
priority = 0.5 # any value between 0.0 and 1.0 ; if you choose 0.5, it will be
               # omitted since it's the default value - see doc for details

# variables for the script ; do not edit anything below this line :-)
tmpUrl = ''

TZ = str(int(time.timezone / 3600)) # finds and builds timezone
if len(TZ) == 2:
    TZ = TZ.replace('+', '+0')
    TZ = TZ.replace('-', '-0')
TZ = TZ + ":00" # change to ":30" in India, e.g.

if baseDir.endswith('\\\\') == False:
    baseDir = baseDir + '\\'
if baseUrl.endswith('/') == False:
    baseUrl = baseUrl + '/'

destFile = baseDir + 'sitemap.xml' # where to put the sitemap
df = open(destFile, 'w')
df.write('<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n')
df.write('<urlset xmlns=\"http://www.google.com/schemas/sitemap/0.84\">\n')
cstContent = "\t<changefreq>%s</changefreq>\n" % changeFreq
if priority != 0.5:
    cstContent = cstContent + "\t<priority>%s</priority>\n" % priority
cstContent = cstContent + '</url>\n'

# Some output for cautious users
print "Welcome to this simple sitemap.xml builder"
print "Any comment on this script -> Jean-Etienne <jepoirrier@gmail.com>"
print "---"
print "I will parse the %s directory" % baseDir
print "corresponding to this base URL: %s\n" % baseUrl

# real work starts here
for rep, srep, fIle in os.walk(baseDir, topdown=True):
    for f in fIle:
        for ext in acceptedExtensions:
            if f.endswith('.' + ext):
                for fts in filenamesToStrip:
                    tmpUrl = os.path.join(rep, f)
                    lastModif = os.stat(tmpUrl).st_mtime
                    lastModif = time.strftime("%Y-%m-%dT%H:%M:%S",
                                              time.gmtime(lastModif))
                    lastModif = lastModif + 'T' + TZ
                    if f == (fts + '.' + ext):
                        tmpUrl = rep
        if tmpUrl != '':
            tmpUrl = tmpUrl.replace(baseDir, baseUrl)
            tmpUrl = tmpUrl.replace('\\', '/')
            # Writes content to file
            tmpContent = "<url>\n\t<loc>%s</loc>\n\t<lastmod>%s</lastmod>\n" % (tmpUrl, lastModif)
            df.write(tmpContent)
            df.write(cstContent)
            #print tmpUrl + " " + lastModif
            tmpUrl = ''

# Now finish the file and close it
df.write('</urlset>')
df.close()
