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
import scipy as sp
import sympy
import matplotlib.pyplot as plt

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
        
    def _plot(self,fig):   
        self.fig=fig
        
        
        head=self.head.split('\t')
        
                
        page_width_cm = 13
        dpi = 200
        inch = 2.54 # inch in cm
        # setting global plot configuration using the RC configuration style
        plt.rc('font', family='serif')
        plt.rc('xtick', labelsize=12) # tick labels
        plt.rc('ytick', labelsize=12) # tick labels
        plt.rc('axes', labelsize=12)  # axes labels
                    
        
        
        self.fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(10,15))
        self.fig.suptitle('Name: %s \n%s \n Start: %s, End:%s'%(head[0],head[1],head[2],head[3]), fontsize=16)
        
        ax[1].grid()
        ax[0].grid()
        """Plot of Relative values""" 

        ax[0].set_title("Relative Wavelength",fontsize=14)    
                                                       
        for i in range(self.nsens):
            sensor= 's'+str(i+1)
            ax[0].plot(self.data[sensor], linewidth=2.00,label="Sensor "+str(i+1))   
            
        ax[0].legend(fontsize=12, loc="best")
        ax[0].set_xlabel('Time (s)')
        ax[0].set_ylabel(r'$\Delta$\lambda [$\mu m]')
         
        
        """Plot of absolute values"""
        
        ax[1].set_title("Absolute Wavelength",fontsize=14)
        senss=self.sens.split('\t')
        for i in range(self.nsens):
            
            """getting the sensor absolute value"""
            v=senss[i+2]
            sensv=float(v[14:25])
            sensor= 's'+str(i+1)    
            ax[1].plot(sensv+self.data[sensor], linewidth=2.00,label="Sensor "+str(i+1))
            
        ax[1].legend(fontsize=12, loc="best")    
        ax[1].set_xlabel('Time (s)')
        ax[1].set_ylabel('$\lambda [$\mu m]')
          



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

