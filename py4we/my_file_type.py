""" IO classes for YOUR_FILE_TYPE_NAME file types

Copyright (C) 2013 DTU Wind Energy

Author: YOUR_NAME
Email: YOUR_EMAIL
Last revision: DATE

License: Apache v2.0, http://www.apache.org/licenses/LICENSE-2.0
"""


from __future__ import print_function
from template_io import FileType, TestFileType
import unittest


### Your class should look like this one ---------------------------------


class MyFileType(FileType):
    """ Description of your MyFileType class should be here. 
    You can also describe the different methods.

    methods:
    --------
        write: write a file
        reade: read a file

    """
    def write(self, filename=None):
        """ Write a file (overrided)

        Parameters:
        ----------
        filename : string (optional)
                   The file name to write
        """
        # HERE DO SOMETHING TO PREPARE THE DATA TO BE WRITTEN ############
        data = self.data
        self._write(data, filename)

    def read(self, filename=None):
        """ Read the file (overrided)

        Parameters:
        ----------
        filename : string (optional)
                   The file name to read
        """
        data = self._read(filename)  
        # HERE DO SOMETHING TO PREPARE THE DATA ##########################
        # Try to put the data into something called self.data ############
        self.data = data

        # Print out something 
        print(self.filename, ':', self.data)



## Do Some testing -------------------------------------------------------
class TestMyFileType(TestFileType):
    """ Test class for MyFileType class """

    def test_duplication(self):
        self._test_duplication(MyFileType, 'test_file.dat')


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

