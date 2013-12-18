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

import numpy as np
import os.path as path


### Your class should look like this one ---------------------------------


class FBGdata(WEFileIO):
    """ FBGdata should read /write the wavelength-shift measurements given by 
    the hardware 
    
    
    
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
            txtlines=f.readlines() 
            
            """read the info from the file"""
            
            self.head=txtlines[1]
            
            """Read info of sensors"""
            self.sens=txtlines[3]
            
            """ lets count the number of sensors (line 3 number of 
            columes-2(Date time))"""
                        
            self.nsens=np.size(txtlines[3].split('\t'))-2
            names=['date','time']
            formats=['S10', 'S8']
            
            
            """Functions dtype that depend of the number of sensors"""
            for i in range(1,self.nsens+1):
               names.append('s'+ str(i))
               formats.append('f8')
               
               
            dtypes = {'names' : (names),'formats': (formats) }           
            self.data=np.loadtxt(self.filename, dtype=dtypes,skiprows=4)
        
  




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
    unittest.main()

