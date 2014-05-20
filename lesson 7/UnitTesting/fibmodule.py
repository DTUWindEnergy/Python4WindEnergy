"""
Functions to compute Fibonacci sequences
"""
import numpy as np
from numpy.testing import assert_allclose

def fib(N):
    """
    Compute the first N Fibonacci numbers
    
    Parameters
    ----------
    N : integer
        The number of Fibonacci numbers to compute
    
    Returns
    -------
    x : np.ndarray
        the length-N array containing the first N
        Fibonacci numbers.
        
    Notes
    -----
    This is a pure Python implementation.  For large N,
    consider a Cython implementation
    
    Examples
    --------
    >>> fib(5)
    array([ 0.,  1.,  1.,  2.,  3.])
    """
    x = np.zeros(N, dtype=float)
    for i in range(N):
        if i == 0:
            x[i] = 0
        elif i == 1:
            x[i] = 1
        else:
            x[i] = x[i - 1] + x[i - 2]
    return x

def test_first_ten():
    nums = fib(10)
    assert_allclose(fib(10),
                    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34])