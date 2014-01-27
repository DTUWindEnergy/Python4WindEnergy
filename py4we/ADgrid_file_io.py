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
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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



    def _plot(self,fig):
            plt.close()
            fig, ax = plt.subplots(ncols=2, figsize=(18,8))

            # Plot AD grid
            ax[0].plot(self.data[:,0],self.data[:,1])
            ax[0].set_title('Grid')
            ax[0].set_xlabel('x')
            ax[0].set_ylabel('y')

            # Plot the thrust force on the blade.
            # First convert the AD thrust forces to 
            # the thrust force blade distribution.

            # AD force to blade force
            i_r=1
            Fblade=np.zeros((self.dims[0],2))
            Fblade[0,0]=-self.data[0,0]
            for i in range(0,self.dims[0]*self.dims[1]): 
                if i<self.dims[1]*i_r:
                    Fblade[i_r-1,1]=Fblade[i_r-1,1]-self.data[i,3]
                else:
                    Fblade[i_r,0]=-self.data[i,0]
                    i_r=i_r+1
            print("The total thrust force is = ",sum(Fblade[:,1]))
            Fblade[:,1]=Fblade[:,1]/3
              
            # blade force to blade force distrubution
            qblade=Fblade
            dr=np.zeros((self.dims[0],1))
            dr[0,0]=2*Fblade[0,0]*63
            drSum=dr[0,0]
            for i in range(1,self.dims[0]):
                dr[i,0]=(Fblade[i,0]*63-drSum)*2
                drSum=drSum+dr[i,0]
            for i in range(0,self.dims[0]):
                qblade[i,1]=Fblade[i,1]/dr[i,0]

            ax[1].plot(qblade[:,0],qblade[:,1],'r')
            ax[1].set_title('Thrust force')
            ax[1].set_xlabel('r')
            ax[1].set_ylabel('Force')




# Do Some testing -------------------------------------------------------
#class TestADgridFileIO(TestWEFileIO):
#    """ Test class for MyFileType class """
#
#    def test_duplication(self):
#        self._test_duplication(ADgridFileIO, './ADgrid/ADgrid.dat')


#class plotADgrid(object):
#    def(self):
#        plt.

    

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
    #print(MY_OBJ.data) 
    # This is how to plot a file
    MY_OBJ.plot()


