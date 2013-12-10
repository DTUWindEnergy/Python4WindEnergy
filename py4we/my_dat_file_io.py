""" IO classes for YOUR_FILE_TYPE_NAME file types

Copyright (C) 2013 DTU Wind Energy

Author: YOUR_NAME
Email: YOUR_EMAIL
Last revision: DATE

License: Apache v2.0, http://www.apache.org/licenses/LICENSE-2.0
"""


from __future__ import print_function
from we_file_io import WEFileIO, TestWEFileIO
import unittest



### Your class should look like this one ---------------------------------


class MyDatFileIO(WEFileIO):
    """ Description of your MyFileType class should be here.
    You can also describe the different methods.

    methods:
    --------
        write: write a file
        reade: read a file

    """
    def _write(self):
        """ Write a file (overrided)
        """
        # HERE DO SOMETHING TO PREPARE THE DATA TO BE WRITTEN ############
        with open(self.filename, 'w') as f:
            f.write(self.data)


    def _read(self):
        """ Read the file (overrided)
        """
        with open(self.filename, 'r') as f:
            self.data = f.read()
        # HERE DO SOMETHING TO PREPARE THE DATA TO BE READ ############


    def _plot(self, fig):
        ax = fig.add_subplot(1, 1, 1)
        ax.plot([ord(s) for s in self.data])
        ax.set_title(self.data)


## Do Some testing -------------------------------------------------------
class TestMyDatFileIO(TestWEFileIO):
    """ Test class for MyFileType class """

    def test_duplication(self):
        self._test_duplication(MyDatFileIO, './test/dat/test_file.dat')


## Main function ---------------------------------------------------------
if __name__ == '__main__':
    """ This is the main fuction that will run the tests automatically

    $> python my_file_type.py
    .
    ----------------------------------------------------------------------
    Ran X test in XXXs

    OK
    """
    #unittest.main()
    MyDatFileIO("test_file.dat").plot()

