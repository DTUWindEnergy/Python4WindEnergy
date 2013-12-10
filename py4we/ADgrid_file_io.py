""" IO classes for YOUR_FILE_TYPE_NAME file types

Copyright (C) 2013 DTU Wind Energy

Author: Paul van der Laan
Email: plaa@dtu.dk
Last revision: 10-12-2013

License: Apache v2.0, http://www.apache.org/licenses/LICENSE-2.0
"""


from __future__ import print_function
from we_file_io import WEFileIO, TestWEFileIO
import unittest
import numpy as np


### Your class should look like this one ---------------------------------


class ADgridFileIO(WEFileIO):
    """ Read and write the grid of an Actuator disk that is used in the CFD code EllipSys3D.

    methods:
    --------
        write: write a file
        reade: read a file

    """
    def _write(self):
        """ Write a file (overrided)
        """
        with open(self.filename, 'w') as f:
            # Write dimensions
            f.write('%i %i %i\n'%(self.dims[0],self.dims[1],self.dims[2]))
            # Write grid  
            for i in range(0,self.dims[0]*self.dims[1]):
                f.write("%8.4f %8.4f %8.4f %12.8f %12.8f %12.8f\n"%(self.data[i,0],self.data[i,1],self.data[i,2],self.data[i,3],self.data[i,4],self.data[i,5]))

           


    def _read(self):
        """ Read the file (overrided)
        """
        with open(self.filename, 'r') as f:
            # Read dimensions on first line
            self.data=f.readline()
            self.dims=map(int, self.data.split(' '))
            #print(self.dims[0]*self.dims[1])
            # Read the grid into an array
            self.data=np.loadtxt(self.filename, usecols=range(self.dims[0]*self.dims[1],self.dims[2]),skiprows=1)
            #print(self.data)
            #print(self.dims[0])





# Do Some testing -------------------------------------------------------
#class TestADgridFileIO(TestWEFileIO):
#    """ Test class for MyFileType class """
#
#    def test_duplication(self):
#        self._test_duplication(ADgridFileIO, './ADgrid/ADgrid.dat')


## Main function ---------------------------------------------------------
if __name__ == '__main__':
    """ This is the main fuction that will run the tests automatically

    $> python my_file_type.py
    .
    ----------------------------------------------------------------------
    Ran X test in XXXs

    OK
    """
    #main.unittest()
    # If the file exists, it reads the file:
    MY_OBJ = ADgridFileIO('test/ADgrid/ADgrid.dat')
    # This is how to write a file:
    MY_OBJ.write('test/ADgrid/ADgrid2.dat')


