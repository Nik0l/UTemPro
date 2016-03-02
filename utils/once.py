
"""
The once module provides caching of function results across program executions
for crash-and-rerun programming. It implements Greg Little's once() from the
TurKit UIST 2010 paper: on first execution, function are called and results
are written in order into a database. On subsequent executions, calls to once
check whether a result is already in the database. If so, and if the function
is still the 'same', the cached result is returned immediately.
'Same' is operationalized as: same function bytecode, same arguments.

From Greg:  if you think of once as caching a result given a
key, then that key is the number of onces encountered so far while
executing the program (e.g. if a program consists of a call to once in
a for-loop, then the first time around the key will be 0, and the
second time around the key will be 1).
bjoern@eecs.berkeley.edu
"""
    
import shelve
import time
access_counter = 0
shelvefile = 'once.shelve'

def onceinit(dbname):
    """initialize and use database dbname.shelve (call with onceinit(__file__))"""
    global shelvefile
    shelvefile = dbname.split(".")[0]+".shelve"
    
def once(fn, *args, **kwargs):
    """
    Execute function fn(*args, **kwargs) once and cache result.
    return cached result on subsequent calls.
    Invalidates rest of cache when a function call changes.
    """
    global access_counter

    print("once %d: opening shelve file" % access_counter)
    shlv = shelve.open(shelvefile)

    #print("once %d: computing hash" % access_counter)
    #fn_str=str(hash(fn.func_code.co_code+str(args)+str(kwargs))) - fails too often
    #problem: class objects have memory addresses in their str function, e.g.:
    #<sqlite3.Cursor object at 0x1089efea0> - these do not stay constant between executions
    #solution for now: programmer has to be careful.
    fn_str = fn.func_name+"("+str(args)+","+str(kwargs)+")"
    key = str(access_counter)
    invoke = False
    result = None
    if(shlv.has_key(key)):
        if(fn_str == shlv[key]['func']):    
            print("once %d: found saved result, function %s and args match." % (access_counter,fn.func_name))
            result = shlv[key]['result']
        else:
            print("once %d: found result, but function %s or args changed. invalidating" % (access_counter,fn.func_name))
            length = len(shlv)
            for i in range(access_counter,length):
                print("   -- removing %d"% i)
                del shlv[str(i)]
            invoke=True
    else:
        invoke=True
    if(invoke):
        print("once %d: invoking %s..." % (access_counter,fn_str))
        t0=time.time()
        result = fn(*args, **kwargs)
        t1=time.time()
        print("once %d: fn() took %f sec" % (access_counter, (t1-t0)))
        shlv[key]={'func':fn_str,'func_name':fn.func_name,'result':result}

    shlv.close()
    access_counter = access_counter+1
    return result
    
def onceunsafe(fn):
    """Like once() but does not invalidate when a new function is passed in"""
    global access_counter
    shlv = shelve.open(shelvefile)
    fn_str=fn.func_code.co_code
    #key = str(access_counter)+":"+fn_str
    key = str(access_counter)
    result = None
    if(shlv.has_key(key)):
        print("once %d: found saved result" % access_counter)
        result = shlv[key]
    else:
        print("once %d: not executed before. executing..." % access_counter)
        t0=time.time()
        result = fn()
        t1=time.time()
        print("once %d: eval() took %f sec" % (access_counter, (t1-t0)))
        shlv[key]=result
    shlv.close()
    access_counter = access_counter+1
    return result

def onceprintdb():
    """print info about once database"""
    print("once database")
    shlv = shelve.open(shelvefile)
    sorted_items = sorted(shlv.iteritems())
    for i in sorted_items:
        print("%s: func: %s  result class: %s (len: %d)"% (int(i[0]),i[1]['func_name'],i[1]['result'].__class__,len(i[1]['result'])))
        
def oncecleardb(start=0):
    """Clear the once() database from entry start onwards.
    (Default: clear all)"""
    shlv = shelve.open(shelvefile)
    if(start==0):
        shlv.clear()
    else:
        length = len(shlv)
        for i in range(start,length):
            print("   -- removing %d"% i)
            del shlv[str(i)]
    shlv.close()

####### END ONCE IMPLEMENTATION############
if __name__ == "__main__":
    print(__doc__)
    help(once)
    help(onceprintdb)
    help(oncecleardb)
