# importing xml files of Stack Exchange into sqlite3 database,
# a part of the code is taken from: http://www.cs.berkeley.edu/~bjoern/projects/stackoverflow/

import sqlite3
import xml.parsers.expat
import sys

# source = the name of a database
source = sys.argv[1]
print "Processing badges from " + source
dbfile = '/mnt/nb254_data/db/'+source+'.db'
xmlfile = '/mnt/nb254_data/xml/'+source+'/Badges.xml'
conn = sqlite3.connect(dbfile)
f = open(xmlfile,'r')
print("importing %s into %s"%(xmlfile,dbfile))

c = conn.cursor()
c.execute('''create table IF NOT EXISTS badges
(Id INTEGER, UserId INTEGER, Name TEXT, Date text)''')
conn.commit()


# 3 handler functions
def start_element(name, attrs):
    if name=='row':
        t = (attrs["Id"],attrs["UserId"],attrs["Name"],attrs["Date"])
        c.execute("""INSERT INTO badges VALUES (?,?,?,?)""",t)
        if int(attrs['Id'])%1000==0:
            conn.commit()
            print 'Committed at '+ attrs["Id"]
def end_element(name):
    print 'End element:', name
def char_data(data):
    print 'Character data:', repr(data)

p = xml.parsers.expat.ParserCreate()

p.StartElementHandler = start_element
#p.EndElementHandler = end_element
#p.CharacterDataHandler = char_data

p.ParseFile(f)
