# importing comments from xml to sqlite3
# a part of the code is taken from: http://www.cs.berkeley.edu/~bjoern/projects/stackoverflow/
import sqlite3
import xml.parsers.expat
import sys

# source = the name of a database
source = sys.argv[1]
print "Processing comments from " + source
dbfile = '/mnt/nb254_data/db/' + source + '.db'
xmlfile = '/mnt/nb254_data/xml/' + source + '/Comments.xml'
conn = sqlite3.connect(dbfile)
f = open(xmlfile, 'r')
print("importing %s into %s" % (xmlfile, dbfile))

c = conn.cursor()
c.execute('''create table IF NOT EXISTS comments
(Id INTEGER, PostId INTEGER, Text TEXT, CreationDate TEXT, UserId INTEGER)''')
conn.commit()
columns = {"Id": None, "PostId": None, "Text": None, "CreationDate": None, "UserId": None}

# 3 handler functions
def start_element(name, attrs):
    if name == 'row':

        # add default values to attributes if any are missing
        for (k, v) in columns.iteritems():
            if not attrs.has_key(k):
                attrs[k] = v

        t = (attrs["Id"], attrs["PostId"], attrs["Text"], attrs["CreationDate"], attrs["UserId"])
        c.execute("""INSERT INTO comments VALUES (?,?,?,?,?)""", t)

        if int(attrs['Id']) % 1000 == 0:
            conn.commit()
            print attrs['Id']

def end_element(name):
    print 'End element:', name


def char_data(data):
    print 'Character data:', repr(data)


p = xml.parsers.expat.ParserCreate()

p.StartElementHandler = start_element
# p.EndElementHandler = end_element
#p.CharacterDataHandler = char_data

p.ParseFile(f)

