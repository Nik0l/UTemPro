# import posts from xml into sqlite3 database
import sqlite3
import xml.parsers.expat
import sys
# a part of the code is taken from: http://www.cs.berkeley.edu/~bjoern/projects/stackoverflow/
# source = the name of a database
source = sys.argv[1]
print "Processing posts from " + source
dbfile = '/mnt/nb254_data/db/'+source+'.db'
xmlfile = '/mnt/nb254_data/xml/'+source+'/Posts.xml'
conn = sqlite3.connect(dbfile)
f = open(xmlfile,'r')
print("importing %s into %s"%(xmlfile,dbfile))

c = conn.cursor()
c.execute('''create table IF NOT EXISTS posts
(Id INTEGER, PostTypeId INTEGER, ParentId INTEGER, AcceptedAnswerId INTEGER, CreationDate TEXT, Score INTEGER, ViewCount INTEGER, Body TEXT, OwnerUserId INTEGER, LastEditorUserId INTEGER, LastEditorDisplayName TEXT, LastEditDate TEXT, LastActivityDate TEXT, CommunityOwnedDate TEXT, ClosedDate TEXT, Title TEXT, Tags TEXT, AnswerCount INTEGER, CommentCount INTEGER, FavoriteCount INTEGER)''')
conn.commit()
columns={"Id":None, "PostTypeId":None, "ParentId":None, "AcceptedAnswerId":None, "CreationDate":None, "Score":None, "ViewCount":None, "Body":None, "OwnerUserId":None, "LastEditorUserId":None, "LastEditorDisplayName":None, "LastEditDate":None, "LastActivityDate":None, "CommunityOwnedDate":None, "ClosedDate":None, "Title":None, "Tags":None, "AnswerCount":None, "CommentCount":None, "FavoriteCount":None}


# 3 handler functions
def start_element(name, attrs):
    if name=='row':
        
        # add default values to attributes if any are missing
        for (k,v) in columns.iteritems():
            if not attrs.has_key(k):
                attrs[k]=v
            
        t = (attrs["Id"], attrs["PostTypeId"], attrs["ParentId"], attrs["AcceptedAnswerId"], attrs["CreationDate"], attrs["Score"], attrs["ViewCount"], attrs["Body"], attrs["OwnerUserId"], attrs["LastEditorUserId"], attrs["LastEditorDisplayName"], attrs["LastEditDate"], attrs["LastActivityDate"], attrs["CommunityOwnedDate"], attrs["ClosedDate"], attrs["Title"], attrs["Tags"], attrs["AnswerCount"], attrs["CommentCount"], attrs["FavoriteCount"])
        c.execute("""INSERT INTO posts VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",t)
        
        if int(attrs['Id'])%1000==0:
            conn.commit()
            print attrs['Id'] 

def end_element(name):
    print 'End element:', name
def char_data(data):
    print 'Character data:', repr(data)

p = xml.parsers.expat.ParserCreate()

p.StartElementHandler = start_element
#p.EndElementHandler = end_element
#p.CharacterDataHandler = char_data

p.ParseFile(f)

