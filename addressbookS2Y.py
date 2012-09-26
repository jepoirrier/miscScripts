# addressbookS2Y - SQD Squirrelmail address book to Yahoo address book converter
# SQD = Simple, Quick and Dirty
# (c) Jean-Etienne Poirrier (http://www.poirrier.be/~jean-etienne/), 2007

# REQUIREMENTS:
# - a CSV file with your address book from SquirrelMail named "addressbook1.csv"
#       in the same directory as this script!
# - Python (written with Python 2.5 but it should work with other versions)

# OUTPUT:
# - a CSV file suitable for import in Yahoo! named "addressbook2.csv"

inputfile = "addressbook1.csv"
outputfile = "addressbook2.csv"

nlines = 0

f = open(inputfile, 'r')
g = open(outputfile, 'w')

g.write('"First","Middle","Last","Nickname","Email","Category","Distribution Lists","Yahoo! ID","Home","Work","Pager","Fax","Mobile","Other","Yahoo! Phone","Primary","Alternate Email 1","Alternate Email 2","Personal Website","Business Website","Title","Company","Work Address","Work City","Work County","Work Post Code","Work Country","Home Address","Home Town","Home County","Home Post Code","Home Country","Birthday","Anniversary","Custom 1","Custom 2","Custom 3","Custom 4","Comments","Messenger ID1","Messenger ID2","Messenger ID3","Messenger ID4","Messenger ID5","Messenger ID6","Messenger ID7","Messenger ID8","Messenger ID9","Skype ID","IRC ID","ICQ ID","Google ID","MSN ID","AIM ID","QQ ID"\r\n')

for line in f:
    nlines = nlines + 1
    sp = line.split(',')
    if len(sp) > 1:
        tmp = '"' + sp[2] + '","","' + sp[3] + '","' + sp[0] + '","' + sp[4]
        tmp = tmp + '","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""'
        g.write(tmp + '\r\n')

f.close()
g.close()
