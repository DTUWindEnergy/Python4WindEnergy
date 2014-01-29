""" IO classes for NM80 Power Curve file types

Copyright (C) 2013 DTU Wind Energy

Author: Iva Hrgovan
Email: ivah@dtu.dk
Last revision: 29-01-2014

License: Apache v2.0, http://www.apache.org/licenses/LICENSE-2.0
"""


from __future__ import print_function
from we_file_io import WEFileIO, TestWEFileIO
import unittest
import matplotlib.pyplot as plt


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
    v = []
    p = []
    
    def _write(self):
        """ Write a file (overrided)
        """
        
        with open('test1.dat', 'w') as f:
            for line in self.items:
                if line[0] != "%": # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    f.write(line + '\n')


    def _read(self):
        """ Read the file (overrided)
        """
        with open(self.filename, 'r') as f:
            self.data = f.read()
            
        self.items = self.data.split('\n')
        
        for i in range(3, len(self.items)):
            self.v.append(float(self.items[i].split()[0]))
            self.p.append(float(self.items[i].split()[1]))
            
        
    def _plot(self,fig):
        axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
        axes.plot(self.v, self.p, 'r')
		
        axes.set_xlabel('V [m/s]')
        axes.set_ylabel('P [kW]')
        axes.set_title('NM80 Power Curve');


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
    t.plot()
