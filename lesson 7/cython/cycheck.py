'''
Created on 29/03/2013

@author: Mads
'''
import cython
import math


def cycheck(p):
    for y in xrange(2, int(math.sqrt(p)) + 1):
        if p % y == 0:
            return False
    return True

@cython.ccall
@cython.locals(y=cython.int, p=cython.ulonglong)
def cycheck_pure(p):
    for y in xrange(2, int(math.sqrt(p)) + 1):
        if p % y == 0:
            return False
    return True


def cycheck_cdef(p):  #cpdef cycheck_cdef(unsigned long long p):
    #cdef int y
    for y in xrange(2, int(math.sqrt(p)) + 1):
        if p % y == 0:
            return False
    return True
