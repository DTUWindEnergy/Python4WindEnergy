""" IO classes for Omnivor input file

Copyright (C) 2013 DTU Wind Energy

Author: Emmanuel Branlard
Email: ebra@dtu.dk
Last revision: 25/11/2013

License: None
"""


from __future__ import print_function
from we_file_io import WEFileIO, TestWEFileIO
import unittest

import numpy as np
import os.path as path

# To read fortran namelist
from fortran_namelist_io  import FortranNamelistIO , TestFortranNamelist
import tempfile
import os


class OmnivorInputFile(FortranNamelistIO):
    pass

## Do Some testing -------------------------------------------------------
class TestOmnivorInput(TestWEFileIO):
    """ Test class for MyFileType class """

    test_file = './test/omnivor/freewake_nm80.oin'
    #InputFile=OmnivorInputFile(test_file)
    #print(InputFile['Wind'])
    

    def test_output_identical(self):
        InputFile=OmnivorInputFile(self.test_file)
        test_fileout=tempfile.mkstemp()[1]
        InputFile.write(test_fileout)

        with open(self.test_file, 'r') as f:
            data_expected = f.read()

        with open(test_fileout, 'r') as f:
            data_read = f.read()
        try:
            self.assertMultiLineEqual(data_read, data_expected)
        finally:
            os.remove(test_fileout)


    def test_duplication(self):
        self._test_duplication(OmnivorInputFile, self.test_file)


## Main function ---------------------------------------------------------
if __name__ == '__main__':
    """ This is the main fuction that will run the tests automatically

    $> python my_file_type.py

    ----- SOME_PRINT_STATEMENTS -----
    .
    ----------------------------------------------------------------------
    Ran X test in XXXs

    OK
    """
    unittest.main()

