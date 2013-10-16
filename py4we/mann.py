""" IO classes for Mann turbulence file types

Copyright (C) 2013 DTU Wind Energy

Author: Pierre-Elouan Rethore
Email: pire@dtu.dk
Last revision: 09/10/2013

License: Apache v2.0, http://www.apache.org/licenses/LICENSE-2.0
"""


from __future__ import print_function
from we_file_io import WEFileIO, TestWEFileIO
import unittest

import numpy as np
import os.path as path


class MannInputFile(WEFileIO):
    """ This is a class for handling the Mann input files

    methods:
    --------
        write: write a file
        reade: read a file

    """
    def _write(self):
        """ Write a file (overrided)
        """
        data = '\n'.join([str(self.data[k]) for k in self.keys])
        with open(self.filename, 'w') as f:
            f.write(data)


    def _read(self):
        """ Read the file (overrided)
        """
        with open(self.filename, 'r') as f:
            data = f.read()

        self.items = data.split('\n')
        self.keys = ['fieldDim', 'NComp', 
                'n1', 'n2', 'n3', 
                'L1', 'L2', 'L3', 
                'type', 'U', 'z', 'z_0', 
                'spectrum', 'seeds', 
                'file_u', 'file_v', 'file_w']

        ## Data is a dictionary containing the variables
        self.data = dict([(k, v) for k, v in zip(self.keys, self.items)])

        # Print out something 
        #print(self.filename, ':', self.data)

    def __getitem__(self, key):
        """ Transform the class instance into a dictionary."""
        return self.data[key]

    def __setitem__(self, key, value):
        """ Transform the class instance into a dictionary."""
        self.data[key] = value


class MannTurbFile(WEFileIO):
    """A mann turbulence file is loaded using the inputfile used to create it.
    The actual path of the turbulence files is included in the mann inputfile.
    The class is loading the three files u,v,w and merge them into a 4D array
    located in self.data.

    methods:
    --------
        write: write a file
        reade: read a file

    """

    def _write(self):
        """ Write a file (overrided)
        First write the input file corresponding to the new file. 
        Then write the 3 corresponding turbulence files. 
        """
        self.inputs.write(self.filename)
        ## The directory name of the input file
        dirname = path.dirname(self.filename)


        n3 = int(self.inputs['n3'])
        n2 = int(self.inputs['n2'])
        n1 = int(self.inputs['n1'])
        self.data = np.zeros([n1,n2,n3,3])

        for i, fname in enumerate(['file_u', 'file_v', 'file_w']):
            ## This command join the path of the dirname with the filename
            new_filename = path.join(dirname, self.inputs[fname])
            ## This command take a slice of the data array, convert it
            ## to float32 format and write it to the new_filename
            self.data[:,:,:,i].astype('float32').tofile(new_filename)


    def _read(self):
        """ Read the file (overrided)
        The method first create a MannInputFile instance, that reads the 
        inputfile used to generate the turbulence file. It then uses the 
        inputs to locate the turbulence file, load it and format it as a 
        4D array.

        Creates:
        -------- 
            self.data: numpy.array([n1, n2, n3, 3])
                The turbulence data (i,j,k,u)
            self.inputs: MannInputFile (behaves as a dict)
                Contains the inputs used to generate the turbulence file
        """
        self.inputs = MannInputFile(self.filename)
        dirname = path.dirname(self.filename)

        n3 = int(self.inputs['n3'])
        n2 = int(self.inputs['n2'])
        n1 = int(self.inputs['n1'])
        self.data = np.zeros([n1,n2,n3,3])

        for i, fname in enumerate(['file_u', 'file_v', 'file_w']):
            with open(path.join(dirname, self.inputs[fname]), 'r') as f:
                data = f.read()

            self.data[:,:,:,i] = np.fromstring(data, np.float32).reshape(n1,n2,n3)


## Do Some testing -------------------------------------------------------
class TestMannType(TestWEFileIO):
    """ Test class for MyFileType class """

    test_file = './test/mann/simABLupwind.inp'

    def test_duplication(self):
        self._test_duplication(MannInputFile, self.test_file)

    def test_Mann_duplication(self):
        """ Test if a file is written correctly by comparing with the data
        of the original file
        """
        original_filename = self.test_file
        new_filename = original_filename + '_new' 

        ### Open a new file
        original_file = MannTurbFile(original_filename)

        for i in ['u', 'v', 'w']:
            original_file.inputs['file_'+i] += '_new' 

        ### write the file to a new filename
        original_file.write(new_filename)

        new_file = MannTurbFile(new_filename)

        ### Unit test function to check if two things are equal
        self.assertTrue(np.linalg.norm(original_file.data-new_file.data)<1.0E-8)


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

