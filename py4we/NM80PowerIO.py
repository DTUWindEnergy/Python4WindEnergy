""" IO classes for NM80 Power Curve file types

Copyright (C) 2013 DTU Wind Energy

Author: Iva Hrgovan
Email: ivah@dtu.dk
Last revision: 09-12-2013

License: Apache v2.0, http://www.apache.org/licenses/LICENSE-2.0
"""


from __future__ import print_function
from we_file_io import WEFileIO, TestWEFileIO
import unittest



class NM80PowerIO(WEFileIO):
    """ NM80 Power Curve IO
       reads : wind speed, 
               mechanical power, 
               rotational speed,
               tip speed ratio and
               pitch setting 
        splits data to items by windspeed           
        writes data to a separate file test1.dat without comment header      
               


    """
    def _write(self):
        """ Write a file (overrided)
        """
        
        with open('test1.dat', 'w') as f:
            for line in self.items:
                if line[0] != "%":
                    f.write(line + '\n')


    def _read(self):
        """ Read the file (overrided)
        """
        with open(self.filename, 'r') as f:
            self.data = f.read()
            
        self.items = self.data.split('\n')
        


### Main function ---------------------------------------------------------
if __name__ == '__main__':
    """ This is the main fuction that will run the tests automatically

    $&gt; python my_file_type.py
    .
    ----------------------------------------------------------------------
    Ran X test in XXXs

    OK
    """
#    unittest.main()
    t = NM80PowerIO('PowerExp_NM80_3deg.dat')
    t.write()
