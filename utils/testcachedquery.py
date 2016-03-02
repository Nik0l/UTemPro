import matplotlib.pyplot as plt
import sqlite3
import time
import sys
sys.path.append("../utils/")
import cachedquery as cq

conn = sqlite3.connect('../../db/stackoverflow.db')
c = conn.cursor()
        
t0 = time.time()
result = cq.query(c,'''SELECT Tags from posts LIMIT 100''',)
t1 = time.time()
print "QUERY: %f seconds" % (t1-t0)

for r in result:
    print r
