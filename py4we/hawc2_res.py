# -*- coding: utf-8 -*-
""" IO classes for YOUR_FILE_TYPE_NAME file types

Copyright (C) 2013 DTU Wind Energy

Author: Alexander Stäblein
Email: alsta@dtu.dk
Last revision: 20.01.2014

License: Apache v2.0, http://www.apache.org/licenses/LICENSE-2.0
"""


from __future__ import print_function
from we_file_io import WEFileIO, TestWEFileIO
import unittest
import numpy as np

### Your class should look like this one ---------------------------------


class ResFile(WEFileIO):
    """ Description of your MyFileType class should be here.
You can also describe the different methods.

methods:
--------
write: write a file
reade: read a file

"""
#    def _write(self):
#        """ Write a file (overrided)
#"""
#        # HERE DO SOMETHING TO PREPARE THE DATA TO BE WRITTEN ############
#        with open(self.filename, 'w') as f:
#            f.write(self.data)


    def _read(self):
        """ Read the file (overrided)
"""
        # Read Scalefactor
        with open(self.filename + '.sel') as f:
            data = f.readlines()
        
        N    = int(data[8].split()[0])
        Nch  = int(data[8].split()[1])
        
        scalefactor = ()
        for i in range(9+Nch+5, 9+2*Nch+5):
            scalefactor = scalefactor + (float(data[i]),)
        
        # Get Data 1
        with open(self.filename + '.dat', 'rb') as f:
            self.data = np.fromfile(f, np.int16)
        
        # Scale it
        self.data = np.reshape(self.data, (Nch, N))
        self.data = self.data.T*scalefactor


    def _plot(self, fig):
        # Plot data
        channel = raw_input('Which channel should be plotted? \n')
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(self.data[:,0],self.data[:,channel])


## Do Some testing -------------------------------------------------------
class TestMyDatFileIO(TestWEFileIO):
    """ Test class for MyFileType class """

    def test_duplication(self):
        self._test_duplication(MyDatFileIO, './test/dat/test_file.dat')


# Main function ---------------------------------------------------------
#if __name__ == '__main__':
#    """ This is the main fuction that will run the tests automatically
#$> python my_file_type.py
#.
#----------------------------------------------------------------------
#Ran X test in XXXs
#
#OK
#"""
#    unittest.main()
#
#    file = ResFile('hawc2_res')

if __name__ == "__main__":

    res = ResFile('hawc2_res')
    res.plot()
