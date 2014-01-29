""" IO classes for YOUR_FILE_TYPE_NAME file types

Copyright (C) 2013 DTU Wind Energy

Author: Juan Pablo Murcia
Email: jumu@dtu.dk
Last revision: 28.01.2014

License: Apache v2.0, http://www.apache.org/licenses/LICENSE-2.0
"""


from __future__ import print_function
from we_file_io import WEFileIO, TestWEFileIO
import unittest


class DakotaTabFileIO(WEFileIO):
    """ Dakota tabular self.data (.dat) file class
    
    A Multilevel Parallel Object-Oriented Framework for:

    Design Optimization
    Parameter Estimation
    Uncertainty Quantification
    Sensitivity Analysis

    methods:
    --------
        write: write a file
        read:  read a file

    """
    def _write(self):
        """ Write a file (overrided)
        """
        n_col = len(self.data)
        n_row = len(self.data[self.keys[0]])
        data = list()
        for i_row in range(n_row):
            data.append('')
            for i_col in range(n_col):
                if i_col == 0:
                    data[-1] = data[-1] + format(self.data[self.keys[i_col]][i_row], '8.0f')
                else:
                    data[-1] = data[-1] + '   ' + format(self.data[self.keys[i_col]][i_row], ' 1.10e')

        header = ''
        for i_col in range(n_col):
            if i_col == 0:
                header = header + format(self.keys[i_col], '<5')
            else:
                header = header + format(self.keys[i_col], '>16')

        data.insert(0, header)
        data[0] = "%" + data[0]

        out = '\n'.join( data )
        with open(self.filename, 'w') as f:
            f.write(out)


    def _read(self):
        """ Read the file (overrided)
        """

        with open(self.filename, 'r') as myfile:
            rawData = myfile.readlines()

            header = rawData[0]
            self.keys   = header.split()
            self.keys[0] = self.keys[0][1:]
            n_col = len(self.keys)

            rawData = rawData[1:]
            n_row = len(rawData)

            # Initialize data dictionary
            self.data = {}
            for i_col in range(n_col):          
                self.data[self.keys[i_col]] = list()
            # Loop over lines and extract variables of interest    
            for i_row in range(n_row):
                line = rawData[i_row]
                columns = line.split()
                for i_col in range(n_col):          
                    self.data[self.keys[i_col]].append(float(columns[i_col]))

        # Print out something 
        # print (self.keys) 
        # print (self.data[ self.keys[0] ])

    def _plot(self,fig):

        n_row = len(self.keys)
        for i_row in range(n_row):
            if  i_row != 0:
                ax = fig.add_subplot(1, n_row-1, i_row)
                ax.plot(self.data[self.keys[0]],self.data[self.keys[i_row]])
                ax.set_xlabel(self.keys[0])
                ax.set_ylabel(self.keys[i_row])

    def __getitem__(self, key):
        """ Transform the class instance into a dictionary."""
        return self.data[key]

## Do Some testing -------------------------------------------------------
class TestDakotaTabFileIO(TestWEFileIO):
    """ Test class for MyFileType class """

    test_file = './test/mann/simABLupwind.inp'

    def test_duplication(self):
        self._test_duplication(DakotaTabFileIO, './test/dakota/rosen_grad_opt.dat')


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
    
    ''' Example uses of DakotaTabFileIO class: 
    '''
    # a = DakotaTabFileIO("rosen_grad_opt.dat")    
    # print (type(a))
    # print (a.keys)
    # print (a.data)
    # print (a['x1'])
    # a.plot()
    
    

