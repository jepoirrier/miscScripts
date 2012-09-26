#!/usr/bin/python
# test for Gadfly
import os
import gadfly
import time

DBdir = 'cameraDB'
DBname = 'cameraDB'

if os.path.exists(DBdir):
    print 'Database already exists. I will just open it'
    connection = gadfly.gadfly(DBname, DBdir)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM camera")
    for x in cursor.fetchall():
        print x[0] + " " + x[2] + " " + x[1]
    cursor.execute("SELECT COUNT(DISTINCT cmake) FROM camera")
    for x in cursor.fetchall():
        print "Distinct make: " + str(x[0])
    cursor.execute("SELECT COUNT(*) FROM camera")
    for x in cursor.fetchall():
        totalMake = x[0]
    cursor.execute("SELECT COUNT(cmake) FROM camera WHERE cmake = 'Unknown'")
    for x in cursor.fetchall():
        unknownMake = x[0]
    print "Items: + " + str(totalMake) + " including " + str(unknownMake) + " unknown"
else:
    print 'Database not present. I will stop here'

connection.commit()

print 'Done!'
