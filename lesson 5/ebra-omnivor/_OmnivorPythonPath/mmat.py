"""
mmat - a function to format arrays of arbitrary dimension for easy copy
and paste to an interactive matlab session

"""

from numpy import ndarray, unravel_index, prod

def mmat(x, format='%.12e'):
    """Display the ndarray 'x' in a format suitable for pasting to MATLAB"""

    def print_row(row, format):
        for i in row:
            print format % i,

    if x.ndim == 1:
        # 1d input
        print "[",
        print_row(x, format)
        print "]"
        print ""

    if x.ndim == 2:
        print "[",
        print_row(x[0], format)
        if x.shape[0] > 1:
            print ';',
        for row in x[1:-1]:
            print " ",
            print_row(row, format)
            print ";",
        if x.shape[0] > 1:
            print " ",
            print_row(x[-1], format)
        print "]",

    if x.ndim > 2:
        d_to_loop = x.shape[2:]
        sls = [slice(None,None)]*2
        print "reshape([ ",
        # loop over flat index
        for i in range(prod(d_to_loop)):
            # reverse order for matlab
            # tricky double reversal to get first index to vary fastest
            ind_tuple = unravel_index(i,d_to_loop[::-1])[::-1]
            ind = sls + list(ind_tuple)
            mmat(x[ind],format)          

        print '],[',
        for i in x.shape:
            print '%d' % i,
        print '])'
