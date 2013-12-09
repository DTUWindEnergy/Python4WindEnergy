""" IO classes for Exhaustive Enumeration of TSP routes, which
define the total distance in km between n different cities. CAREFUL 
NOT TO USE n>10.

Copyright (C) 2013 DTU Wind Energy

Author: Jose Francisco Herbert Acero
Email: jf.herbert.phd.mty@itesm.mx
Last revision: 08/12/2013

License: Apache v2.0, http://www.apache.org/licenses/LICENSE-2.0 """

#Import classes from different sources:
from __future__ import print_function
from we_file_io import WEFileIO, TestWEFileIO

#Import useful libraries:
import unittest
import numpy as np
import os.path as path
import itertools

#Definition of the TSPInputFile class, which inherit from WEFileI class.
class TSPInputFile(WEFileIO):
    """ This class handles TSP input files. The parameters
    to read and/or write are the number of cities (n) and the matrix
    (d) representing distances between cities.

    Methods:
    ------------------------
        write: write a file
        read: read a file"""

    #Next definitions override the _write and _read definitions
    #of the inhertied WEFileIO class.
    
    #Write File Definition:
    def _write(self):

        #Open file to write:
        with open(self.filename, 'w') as f:
            
            #Writes the number of cities n in first row:
            f.write(str(self.n) + "\n")
            
            #Writes the matrix d into a file, where d represents the
            #distances in km between the n different cities:
            for i in range(0,self.n):
                aux=str(self.d[i][0])
                for j in range(1,self.n):
                    aux=aux + ' ' + str(self.d[i][j])
                if i==self.n-1 & j==self.n-1:
                    f.write(aux)
                else:
                    f.write(aux + "\n")            

    #Read File Definition:
    def _read(self):

        #Opens the file TSP:
        with open(self.filename, 'r') as f:
            
            #Reads the number of cities n:
            self.n=int(f.readline())
            
            #Reads the matrix (d) of distances in km beteween the n
            #cities:
            self.d = [ map(int,line.split(' ')) for line in f ]


#Definition of the TSPExEval class, which inherit from WEFileI class.
class TSPExEval(WEFileIO):
    """ This class evaluates TSP routes using the inputfile parameters.
    The class enumerates all posible permutations of n different cities
   (routes) and evaluate its total distance. The route(s) with minimum
   distance is reported.

    Methods:
    ------------------------
        write: write a file
        read: read a file"""

    #Next definitions override the _write and _read definitions
    #of the inhertied WEFileIO class.
    
    #Write File Definition:
    def _write(self):
        """ The method writes the best found solution and the parameters
        of the problem."""
        
        #Open file to write:
        with open(self.filename, 'w') as f:
            
            #Writes the number of cities n in first row:
            f.write("TSP for " + str(self.inputs.n) + " Cities.\n")
            f.write("Possible Routes: " + str(self.nRoutes) + "\n")
            f.write("\n")
            f.write("Best Route Distance: " + str(self.best) + " km.\n")
            f.write("Best Forward/Backward Route: " + str(self.BRoute) + "\n")
            f.write("\n")
            f.write("Distances between Cities:\n")
            f.write("\n")
            
            #Writes the matrix d into a file, where d represents the
            #distances in km between the n different cities:
            for i in range(0,self.inputs.n):
                aux=str(self.inputs.d[i][0])
                for j in range(1,self.inputs.n):
                    aux=aux + ' ' + str(self.inputs.d[i][j])
                if i==self.inputs.n-1 & j==self.inputs.n-1:
                    f.write(aux)
                else:
                    f.write(aux + "\n")  


    #Read File Definition:
    def _read(self):
        """ The method creates a TSPInputFile instance, that reads the
        inputfile parameters. It uses the inputs to generate all possible
        permutations of the n considered cities and evaluates all routes
        "tour distance". Finally, it reports the tour with lowest distance."""
        
        #Reads the inputfile:
        self.inputs = TSPInputFile(self.filename)
        
        #Calculates all possible permutations (routes) and determines the
        Routes = list(itertools.permutations(range(1,self.inputs.n+1)))
        self.nRoutes = len(Routes)
        
        #Evaluates all routes and saves the best route (min distance):
        self.best = float("inf")
        for i in range(0,self.nRoutes):
            SumT=0
            for j in range(0,self.inputs.n-1):
                SumT=SumT+self.inputs.d[Routes[i][j]-1][Routes[i][j+1]-1]
            if SumT < self.best:
                self.best = SumT
                self.BRoute = Routes[i]


# Do Some testing -------------------------------------------------------
class TestTSPType(TestWEFileIO):
    """ Test class for TSPInputFile class """
    
    test_file = './test/TSP/TSP_Mex_Medium.txt'
    
    def test_duplication(self):
        self._test_duplication(TSPInputFile, self.test_file)

    def test_TSP_duplication(self):
        """ Test if a file is written correctly by comparing with the data
        of the original file"""
        original_filename = self.test_file
        new_filename = original_filename + '_new'
        
        #Open the original file by using TSP class
        original_file = TSPInputFile(original_filename)
        
        #Write the original file into a new file
        original_file.write(new_filename)
        new_file = TSPInputFile(new_filename)
        
        #Verify if two files are equal:
        self.assertTrue(np.linalg.norm(original_file.d-new_file.d)<1.0E-8)
       

# Main function ---------------------------------------------------------
#if __name__ == '__main__':
    """ This is the main fuction that will run the tests automatically

    $> python my_file_type.py
    .
    ----------------------------------------------------------------------
    Ran X test in XXXs

    OK
    """
#    unittest.main()

