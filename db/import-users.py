# import xml into sqlite3 database
# a part of the code is taken from: http://www.cs.berkeley.edu/~bjoern/projects/stackoverflow/
import sqlite3
import xml.parsers.expat
import sys
# a part of the code is taken from: http://www.cs.berkeley.edu/~bjoern/projects/stackoverflow/
# source = the name of a database
source = sys.argv[1]
print "Processing users from " + source
dbfile = '/mnt/nb254_data/db/'+source+'.db'
xmlfile = '/mnt/nb254_data/xml/'+source+'/Users.xml'
conn = sqlite3.connect(dbfile)
f = open(xmlfile,'r')
print("importing %s into %s"%(xmlfile,dbfile))

c = conn.cursor()
c.execute('''create table IF NOT EXISTS users
(Id INTEGER, Reputation INTEGER, CreationDate TEXT, DisplayName TEXT, EmailHash TEXT, LastAccessDate TEXT, WebsiteUrl TEXT, Location TEXT, AGE TEXT, AboutMe TEXT, Views INTEGER, UpVotes INTEGER, DownVotes INTEGER)''')
conn.commit()
columns={"Id":None,
       "Reputation":None, 
       "CreationDate":None, 
       "DisplayName":None, 
       "EmailHash":None,
       "LastAccessDate":None, 
       "WebsiteUrl":None, 
       "Location":None,
       "Age":None, 
       "AboutMe":None, 
       "Views":None, 
       "UpVotes":None, 
       "DownVotes":None}


# 3 handler functions
def start_element(name, attrs):
    if name=='row':
        
        # add default values to attributes if any are missing
        for (k,v) in columns.iteritems():
            if not attrs.has_key(k):
                attrs[k]=v
            
        t = (attrs["Id"], 
                       attrs["Reputation"], 
                       attrs["CreationDate"], 
                       attrs["DisplayName"], 
                       attrs["EmailHash"],
                       attrs["LastAccessDate"], 
                       attrs["WebsiteUrl"], 
                       attrs["Location"],
                       attrs["Age"], 
                       attrs["AboutMe"], 
                       attrs["Views"], 
                       attrs["UpVotes"], 
                       attrs["DownVotes"])
        c.execute("""INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",t)
        
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

