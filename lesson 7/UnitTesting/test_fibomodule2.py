import unittest
from fibmodule import fib
from numpy.testing import assert_allclose

class test_fibo(unittest.TestCase):
    def test_first_ten2(self):
        nums = fib(10)
        assert_allclose(fib(10),
                        [0, 1, 1, 2, 3, 5, 8, 13, 21, 34])

    def test_negative(self):
        """Testing that `fib` raises a `ValueError` with a negative number as parameter"""
        with self.assertRaises(ValueError):
            fib(-1)
        
if __name__ == '__main__':
    unittest.main()