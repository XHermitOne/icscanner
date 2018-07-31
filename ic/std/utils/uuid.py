#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import random
import md5

try:
    from ic.std.log import log
except ImportError:
    from ic.log import log

try:
    import pythoncom
except ImportError:
    log.error(u'Import Error pythoncom')

__version__ = (0, 0, 2, 1)


def get_uuid(*args):
    """
    Generates a universally unique ID.
    Any arguments only create more randomness.
    """
    t = long(time.time() * 1000)
    r = long(random.random()*100000000000000000L)

    a = random.random()*100000000000000000L
    data = str(t)+' '+str(r)+' '+str(a)+' '+str(args)
    data = md5.md5(data).hexdigest()
    return data


def create_guid():
    """
    MS guid.
    """
    return pythoncom.CreateGuid()


def get_uuid_attr(uuid, *attrs):
    """
    """
    for attr in attrs:
        uuid += '_'+str(attr)
        
    return uuid


if __name__ == '__main__':
   
    t1 = time.clock()
    
    for i in range(10):
        print(get_uuid_attr(get_uuid(), *('keyDown', 'a', 5)))

    t2 = time.clock()        
    
    print(u'>>> Time: %s' % (t2-t1))
