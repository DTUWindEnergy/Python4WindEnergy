import cython

def primes(n): #cpdef int primes(int n):
    #cdef int count, i, j
    count = 0
    for i in xrange(2,n):
        for j in xrange(2,i):
            if i%j==0: 
                break
        else:
            count+=1
    return count

