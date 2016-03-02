import shelve
import sqlite3
# a part of the code is taken from: http://www.cs.berkeley.edu/~bjoern/projects/stackoverflow/
shelvefile = '../../db/querycache.shelve'

def query(cursor,query,parameters=()):
    shlv = shelve.open(shelvefile)
    key = makekey(query,parameters)
    if(shlv.has_key(key)):
        print("found query in cache")
        return shlv[key]
    else:
        # query does not exist - run it and save result in cache
        print("did NOT find query in cache")
        cursor.execute(query,parameters)
        result = cursor.fetchall()
        shlv[key]=result
        return result
        
def clear(query,parameters=()):
    shlv = shelve.open(shelvefile)
    key = makekey(query,parameters)
    if shlv.has_key(key):
        del shlv[key]
        return True
    else:
        return False #nothing to do

def makekey(query,parameters):
    return query+str(parameters)
