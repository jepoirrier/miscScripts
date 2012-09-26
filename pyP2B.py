#!/usr/bin/python
"""
Retrieve PubMed reference from its PMID given as last argument
Copyright (C) 2006-2007 Jean-Etienne Poirrier

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

USAGE: just put it in a pipe : ./pyP2B.py 16872686 >> myrefs.bib
WARNING: no check for duplicate references (just add the ref)
TODO: all exception handling
INFOS: http://www.poirrier.be/~jean-etienne/software/pyp2b/
E-MAIL: jepoirrier@gmail.com
"""
import codecs
from lxml import etree
import os
import sys
import urllib2

# Small function to strip last dot in string
# (along with leading and trailing spaces) 
def striplastdot(s):
    l = len(s)
    if l > 1: # at least 1 letter (dot!)
        s.strip()
        if s.endswith('.'):
            s = s[0:l-1]
    return s

# Small function to strip electronic reference in Journal title (if exists)
def stripelref(s):
    l = len(s)
    if l > 22: # at least 22 letters
        if s.endswith(" [electronic resource]"):
            s = s[0:l-22]
    return s

correctRef = False
tmpFileName = 'pyP2Btmp.xml'
deftab = 2
#pubmedUID for tests : 16872686 - 16934136
pubmedUID = sys.argv[len(sys.argv)-1]
#pubmedUID = 16549013

queryString = "http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?" +\
              "cmd=text&db=PubMed&uid=" + str(pubmedUID) + "&dopt=XML"

# Getting something from PubMed ...
result = urllib2.urlopen(queryString)

# Processing file (because it was plain HTML, not text)
f = open(tmpFileName, 'w')

for line in result:
    line = line.replace('<pre>', '')
    line = line.replace('</pre>', '')
    line = line.replace('&lt;', '<')
    line = line.replace('&gt;', '>')
    line = line.replace('\n', '')
    line = line.replace('&quot;', '"')
    f.write(line)
f.close()

# Verification if it's a correct reference ...
f = open(tmpFileName, 'r')
for line in f:
    if line.endswith('</PubmedArticle>'):
        correctRef = True
    else:
        print "Reference %d not found. Aborting" % (pubmedUID)
        break
f.close()

# Opening it with lxml and XPath
f = open(tmpFileName, 'r')
tree = etree.parse(f)

# get authors
authors = ""
authl = tree.xpath('/PubmedArticle/MedlineCitation/Article/AuthorList/Author/LastName')
authi = tree.xpath('/PubmedArticle/MedlineCitation/Article/AuthorList/Author/Initials')
for i in range(len(authl)):
    lastname = str((authl[i].text).encode("utf-8"))
    initials = ""
    for j in range(len(authi[i].text)):
        initials = initials + str(authi[i].text)[j]
        initials = initials + "."
    if i > 0:
        authors = "%s and %s, %s" % (authors, lastname, initials)
    else: #i = 0
        authors = "%s, %s" % (lastname, initials)

# get title
title = tree.xpath('/PubmedArticle/MedlineCitation/Article/ArticleTitle')
title = striplastdot(title[0].text)

# get year
year = tree.xpath('/PubmedArticle/MedlineCitation/Article/Journal/JournalIssue/PubDate/Year')
year = year[0].text

# build id (first author's last name + two last year digit)
bibtexId = authl[0].text.lower() + year[len(year)-2:len(year)]

# get journal
journal = tree.xpath('/PubmedArticle/MedlineCitation/Article/Journal/Title')
journal = stripelref(striplastdot(journal[0].text))

# get volume
volume = tree.xpath('/PubmedArticle/MedlineCitation/Article/Journal/JournalIssue/Volume')
volume = volume[0].text

# get issue (if exists)
issue = tree.xpath('/PubmedArticle/MedlineCitation/Article/Journal/JournalIssue/Issue')
if len(issue) > 0:
    issue = issue[0].text
else:
    issue = "0"

# get pages
pages = tree.xpath('/PubmedArticle/MedlineCitation/Article/Pagination/MedlinePgn')
pages = pages[0].text
pages = pages.replace("-", "--")

# get PMID
pmid = tree.xpath('/PubmedArticle/MedlineCitation/PMID')
pmid = pmid[0].text

# get doi (if exists)
idlist = tree.xpath('/PubmedArticle/PubmedData/ArticleIdList/ArticleId')
doi = "0"
if len(idlist) > 0:
    for i in range(len(idlist)):
        if str(idlist[i].attrib['IdType'])== 'doi':
            doi = idlist[i].text

f.close()

# Now write output (to include in a pipe)
print ""
print "@article{%s," % (bibtexId)
print ("\tauthor = {%s}," % (authors)).expandtabs(deftab)
print ("\ttitle = {%s}," % (title)).expandtabs(deftab)
print ("\tyear = %s," % (year)).expandtabs(deftab)
print ("\tjournal = {%s}," % (journal)).expandtabs(deftab)
print ("\tvolume = %s," % (volume)).expandtabs(deftab)
if issue != "0":
    print ("\tnumber = %s," % (issue)).expandtabs(deftab)
print ("\tpages = {%s}," % (pages)).expandtabs(deftab)
print ("\tpmid = %s," % (pmid)).expandtabs(deftab)
if doi != "0":
    print ("\tdoi = {%s}," % (doi)).expandtabs(deftab)
print ("\tkeywords = {}").expandtabs(deftab)
print "}"

# Clean up things ...
os.remove(tmpFileName)
