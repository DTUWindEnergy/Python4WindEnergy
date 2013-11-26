""" IO classes for Omnivor input file

Copyright (C) 2013 DTU Wind Energy

Author: Emmanuel Branlard
Email: ebra@dtu.dk
Last revision: ask git

License: None
"""


from __future__ import print_function
from we_file_io import WEFileIO, TestWEFileIO
import unittest

import numpy as np
import os.path as path

# To read fortran namelist
from fortran_namelist_io  import FortranNamelistIO 
import tempfile
import os
import sys


class OmnivorInputFile(FortranNamelistIO):

    def export_lib_command(self, filename_out=None):
        """ Converts input file data into library commands and write it to a file
        """
        # Default comment character and booleans (python style)
        CommentChar='#'
        TrueVal='True'
        FalseVal='False'
        
        # Output to stdout or file
        if filename_out==None:
            f=sys.stdout
        else:
            fileName, fileExtension = os.path.splitext(filename_out)
            f=open(filename_out, 'w')
            # If it's a matlab file, use matlab syntax
            if fileExtension == '.m':
                CommentChar='%'
                TrueVal='true'
                FalseVal='false'

        # map between namelist and library wrapper set function
        Name2Function={
                'commondata':"omnivor.set_common_var",
                'algo':      "omnivor.set_algo_var",
                'coupling':  "%s error"%CommentChar ,
                'wind':  "omnivor.set_wind_var",
                'param':  "%s error"%CommentChar
                }

        # Looping and writting
        for nml in self.data :
                # Sorting dictionary data (in the same order as it was created, thanks to id)
                SortedList = sorted(self.data[nml].items(), key=lambda(k, v): v['id'])

                f.write('%s --------------------------------------------------------------------------------\n' % CommentChar)
                f.write('%s --- %s \n' % (CommentChar,nml))
                f.write('%s --------------------------------------------------------------------------------\n' % CommentChar)
                for param in map(lambda(k,v):k,SortedList):
                    value=','.join(self.data[nml][param]['val'] );
                    if(value=='.true.'):
                        # Dealing with booleans
                        value=TrueVal
                    elif(value=='.false.'):
                        value=FalseVal
                    else:
                        # Dealing with arrays
                        if value.count(',')>0:
                            value='['+value+']'

                    f.write('%s(\'%s\',%s)\n' % ( Name2Function[nml.lower()], param,value))
# 
## Do Some testing -------------------------------------------------------
class TestOmnivorInput(TestWEFileIO):
    """ Test class for MyFileType class """

    test_file = './test/omnivor/freewake_nm80.oin'
    #InputFile=OmnivorInputFile(test_file)
    #print(InputFile['Wind'])
    #InputFile.export_lib_command('./test/omnivor/freewake_nm80.m')

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
    """
    unittest.main()

