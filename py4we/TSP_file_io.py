""" IO classes for Exhaustive Enumeration of TSP routes, which
define the total distance in km between n different cities. CAREFUL 
NOT TO USE n>10.

Copyright (C) 2014 DTU Wind Energy

Author: Jose Francisco Herbert Acero
Email: jf.herbert.phd.mty@itesm.mx
Last revision: 22/01/2014

License: Apache v2.0, http://www.apache.org/licenses/LICENSE-2.0 """

#Import classes from different sources:
from __future__ import print_function
from we_file_io import WEFileIO, TestWEFileIO

#Import useful libraries:
import os, math, time, unittest
import numpy as np
import matplotlib.pyplot as plt

#Definition of the TSPInputFile class, which inherit from WEFileI class.
class TSPInputFile(WEFileIO):
    """ This class handles TSP input files. The parameters
    to read and/or write are the number of cities (n) and the matrix
    (d) representing distances between cities.

    Methods:
    ------------------------
        _write: writes a TSP type input file
        _read: reads a TSP type input file
        _plot: plots the input file data """

    #Next definitions override the _write and _read definitions
    #of the inhertied WEFileIO class.
    
    #Write the input file method definition:
    def _write(self):

        #Open file to write:
        with open(self.filename, 'w') as f:
            
            #Writes the number of cities (n) in first row and a blank
            #space in second row:
            f.write(str(self.n) + "\n")
            f.write("\n")
            
            #Writes the matrix (d), where d represents the
            #distances in km between the n different cities:
            for i in range(0,self.n):
                aux=str(self.d[i][0])
                for j in range(1,self.n):
                    aux=aux + ' ' + str(self.d[i][j])
                f.write(aux + "\n")
            f.write("\n")
            
            #Writes the names of the n cities:
            for i in range(self.n):
                f.write(self.cities[i] + "\n")
            f.write("\n")
            
            #Writes the matrix of cities coordinates:
            for i in range(0,self.n):
                if i < self.n-1:
                    f.write(str(self.coords[i][0]) + ' ' + str(self.coords[i][1]) + "\n")
                else:
                    f.write(str(self.coords[i][0]) + ' ' + str(self.coords[i][1]))
            f.write("\n")
            
            #Writes if there is an image:
            f.write("\n")            
            f.write("Image:\n")
            f.write(str(self.img))
            
            #Writes the latitude and longitude coordinates if there is an image:
            if self.img:
                f.write("\n")
                f.write("\n")
                f.write(self.imgfilename + "\n")
                f.write(str(self.imglong[0]) + ' ' + str(self.imglong[1]) + "\n")
                f.write(str(self.imglat[0]) + ' ' + str(self.imglat[1]))



    #Read the input file method definition:
    def _read(self):

        #Opens the file TSP:
        with open(self.filename, 'r') as f:
            
            #Reads the number of cities n:
            self.n=int(f.readline())
            
            #Reads the matrix (d) of distances in km beteween the n
            #cities:
            f.readline()    #blank space
            self.d=[]
            for i in range(self.n):
                self.d.append(map(int,f.readline().split(' ')))

            #Reads the names of the n cities:
            f.readline()    #blank space
            self.cities=range(self.n)
            for i in range(self.n):
                self.cities[i]=f.readline().splitlines()[0]
            
            #Reads the latitude and longitude coordinates of the n
            #cities:
            f.readline()    #blank space
            self.coords=[]
            for i in range(self.n):
                self.coords.append(map(float,f.readline().split(' ')))
            
            #Reads if an image (map) is available for plotting:
            f.readline()    #blank space
            f.readline()    #blank space
            self.img = f.readline().splitlines()[0] == 'True'
            
            #Reads the image georeferenced corner coordinates (lat,long):
            if self.img:
                f.readline()    #blank space
                self.imgfilename=f.readline().splitlines()[0]
                self.imglong=(map(float,f.readline().split(' ')))
                self.imglat=(map(float,f.readline().split(' ')))
            
    #Plot the input file data:
    def _plot(self):
                
        #Verify if an image is available:
        if self.img:
            
            #Creates a figure as a function of the image size:
            if abs(abs(self.imglat[0])-abs(self.imglat[1])) > abs(abs(self.imglong[1])- abs(self.imglong[0])):
                fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10*(abs(abs(self.imglong[1])- abs(self.imglong[0]))/abs(abs(self.imglat[0])-abs(self.imglat[1]))),10))
            else:
                fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,10*(abs(abs(self.imglat[0])-abs(self.imglat[1]))/abs(abs(self.imglong[1])- abs(self.imglong[0])))))
            
            #Orders the cities coordinates:
            x=[]
            y=[]
            for i in self.coords:
                x.append(i[1])
                y.append(i[0])
            
            #Creates a figure containing the self.imgfilename as background:
            ax.imshow(plt.imread(self.imgfilename),extent=[self.imglong[0], self.imglong[1], self.imglat[0], self.imglat[1]])
            
            #Plots the cities by coordinates:
            ax.plot(x,y,">",markerfacecolor="red",markeredgecolor="black",label='Cities')
            ax.set_xlim(self.imglong[0], self.imglong[1])
            ax.set_ylim(self.imglat[0], self.imglat[1])
            ax.set_title(self.imgfilename[:-4] + " TSP for " + str(self.n) + " Cities", fontsize=20)
            ax.set_xlabel('Longitude [deg]', fontsize=16)
            ax.set_ylabel('Latitude [deg]', fontsize=16)
            plt.grid()
            ax.legend(fontsize=12, loc="best")
            
            #Saves the figure into self for later use:
            self.fig=fig
            self.ax=ax
            
        #Plotting is performed without background image:
        else:
            #No background image was found. Display a message to user:
            print('No image is available.')
            
            #Creates an empty figure of arbitrary size:
            fig, ax = plt.subplots(nrows=1, ncols=1)
            
            #Orders the cities coordinates:
            x=[]
            y=[]
            for i in self.coords:
                x.append(i[1])
                y.append(i[0])
            
            #Plots the cities by coordinates:
            ax.plot(x,y,">",markerfacecolor="red",markeredgecolor="black",label='Cities')
            ax.set_title("TSP for " + str(self.n) + " Cities", fontsize=20)
            ax.set_xlabel('Longitude [deg]', fontsize=16)
            ax.set_ylabel('Latitude [deg]', fontsize=16)
            plt.grid()
            ax.legend(fontsize=12, loc="best")
            
            #Saves the figure into self for later use:
            self.fig=fig
            self.ax=ax


#Definition of the TSPExEval class, which inherit from WEFileI class.
class TSPExEval(WEFileIO):
    """ This class evaluates TSP routes using the input file parameters.
    The class enumerates all posible route permutations between n different 
    cities and evaluates its total distance. The route(s) with minimum
    distance is reported.

    Methods:
    ------------------------
        _write: writes the obtained results to a file
        all_perms: creates a generator of permutations given an input list.
        _read: reads a TSP type input file
        _plot: plots the results of the TSP evaluation """
        
    #Next definitions override the _write and _read definitions
    #of the inhertied WEFileIO class.
    
    #Write File Definition:
    def _write(self):
        """ The method writes the best found solution and the parameters
        of the problem."""
        
        #Open file in writing mode:
        with open(self.filename, 'w') as f:
            
            #Writes all relevant parameters:
            f.write("TSP for " + str(self.inputs.n) + " Cities.\n")
            f.write("Possible Routes: " + str(self.nRoutes) + "\n")
            f.write("Calculation Completed in: " + str(self.time) + " seconds.\n")
            f.write("\n")
            f.write("Best Route Distance: " + str(self.best) + " km.\n")
            f.write("Best Forward/Backward Route (City ID): " + str(self.BRoute) + "\n")
            
            #Writes the sequence of cities in the best route:
            aux=""
            for i in range(len(self.BRoute)):
                if i == len(self.BRoute)-1:
                    aux=aux+str(self.inputs.cities[self.BRoute[i]-1])
                else:
                    aux=aux + str(self.inputs.cities[self.BRoute[i]-1]) + " - "
            f.write("Best Forward/Backward Route: " + aux + "\n")
            
            #Prints input parameters:
            f.write("\n")
            f.write("Distances Between Cities:\n")
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
        input file parameters. It uses the inputs to generate all possible
        route permutations between the n cities and evaluates all routes
        "tour distance". Finally, it reports the tour with lowest distance."""
        
        #Starts a chronometer:
        tic = time.clock()
        
        #Reads the inputfile:
        self.inputs = TSPInputFile(self.filename)
        
        #Calculates all possible permutations (routes) and determines the
        #number of possible routes:
        Routes = self.all_perms(range(1,self.inputs.n+1))
        self.nRoutes = math.factorial(self.inputs.n)
        
        #Evaluates all routes and saves the best route (min distance):
        self.best = float("inf")
        i=0
        while i < self.nRoutes-1:
            i += 1
            SumT=0
            PR=Routes.next()        #Calculates next permutation.
            for j in range(0,self.inputs.n-1):
                SumT=SumT+self.inputs.d[PR[j]-1][PR[j+1]-1]
            if SumT < self.best:
                self.best = SumT
                self.BRoute = PR
                
            #Display advance to user:
            if (i+1.0)*100/self.nRoutes % 10 == 0:
                os.system('cls')
                print("TSP Calculation for " + str(self.nRoutes) + " Possible Routes.")
                print("Advance: " + str((i+1.0)*100/self.nRoutes) + "% Completed.")
                toc = time.clock()
                print("Elapsed Time: " + str(toc-tic) + " seconds.")
        
        #Saves elapsed time:
        self.time = toc-tic
    
    #Function all_perms. Creates a generator of permutations given an input list.
    def all_perms(self,cities):
        if len(cities) <=1:
            yield cities
        else:
            for perm in TSPExEval.all_perms(self,cities[1:]):
                for i in range(len(cities)):
                    yield perm[:i] + cities[0:1] + perm[i:]


    #Plot the input file data:
    def _plot(self):
                
        #Verify if an image is available:
        if self.inputs.img:
            
            #Creates a figure as a function of the image size:
            if abs(abs(self.inputs.imglat[0])-abs(self.inputs.imglat[1])) > abs(abs(self.inputs.imglong[1])- abs(self.inputs.imglong[0])):
                fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10*(abs(abs(self.inputs.imglong[1])- abs(self.inputs.imglong[0]))/abs(abs(self.inputs.imglat[0])-abs(self.inputs.imglat[1]))),10))
            else:
                fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,10*(abs(abs(self.inputs.imglat[0])-abs(self.inputs.imglat[1]))/abs(abs(self.inputs.imglong[1])- abs(self.inputs.imglong[0])))))
            
            #Orders the cities coordinates:
            x=[]
            y=[]
            for i in self.inputs.coords:
                x.append(i[1])
                y.append(i[0])
                
            #Arrages the coordinates of the best route:
            xb=[]
            yb=[]
            for i in self.BRoute:
                xb.append(self.inputs.coords[i-1][1])
                yb.append(self.inputs.coords[i-1][0])
            
            #Creates a figure containing the self.imgfilename as background:
            ax.imshow(plt.imread(self.inputs.imgfilename),extent=[self.inputs.imglong[0], self.inputs.imglong[1], self.inputs.imglat[0], self.inputs.imglat[1]])
            
            #Plots the cities by coordinates and the best route:
            ax.plot(xb,yb,'w',linewidth=1,label="Best Route")
            ax.plot(x,y,">",markerfacecolor="red",markeredgecolor="black",label='Cities')
            ax.set_xlim(self.inputs.imglong[0], self.inputs.imglong[1])
            ax.set_ylim(self.inputs.imglat[0], self.inputs.imglat[1])
            ax.set_title(self.inputs.imgfilename[:-4] + " TSP for " + str(self.inputs.n) + " Cities", fontsize=20)
            ax.set_xlabel('Longitude [deg]', fontsize=16)
            ax.set_ylabel('Latitude [deg]', fontsize=16)
            plt.grid()
            ax.legend(fontsize=12, loc="best")
            
            #Saves the figure into self for later use:
            self.fig=fig
            self.ax=ax
            
        #Plotting is performed without background image:
        else:
            #No background image was found. Display a message to user:
            print('No image is available.')
            
            #Creates an empty figure of arbitrary size:
            fig, ax = plt.subplots(nrows=1, ncols=1)
            
            #Orders the cities coordinates:
            x=[]
            y=[]
            for i in self.inputs.coords:
                x.append(i[1])
                y.append(i[0])
                
            #Arrages the coordinates of the best route:
            xb=[]
            yb=[]
            for i in self.BRoute:
                xb.append(self.inputs.coords[i-1][1])
                yb.append(self.inputs.coords[i-1][0])
            
            #Plots the cities by coordinates:
            ax.plot(x,y,">",markerfacecolor="red",markeredgecolor="black",label='Cities')
            ax.plot(xb,yb,'black',linewidth=1,label="Best Route")
            ax.set_title("TSP for " + str(self.inputs.n) + " Cities", fontsize=20)
            ax.set_xlabel('Longitude [deg]', fontsize=16)
            ax.set_ylabel('Latitude [deg]', fontsize=16)
            plt.grid()
            ax.legend(fontsize=12, loc="best")
            
            #Saves the figure into self for later use:
            self.fig=fig
            self.ax=ax
            


# Do Some testing -------------------------------------------------------
class TestTSPType(TestWEFileIO):
    """ Test class for TSPInputFile class """
    
    def test_duplication(self):
        self._test_duplication(TSPInputFile, self.test_file)

    def test_TSP_duplication(self):
        """ Test if a file is written correctly by comparing with the data
        of the original file"""
        original_filename = self.test_file
        new_filename = 'new_' +original_filename
        
        #Open the original file by using TSP class:
        original_file = TSPInputFile(original_filename)
        
        #Write the original file into a new file
        original_file.write(new_filename)
        new_file = TSPInputFile(new_filename)
        
        #Verify if two files are equal:
        self.assertTrue(np.linalg.norm(original_file.n-new_file.n)<1.0E-8)
        #self.assertTrue(np.linalg.norm(original_file.d-new_file.d)<1.0E-8)
        #self.assertTrue(np.linalg.norm(original_file.coords-new_file.coords)<1.0E-8)
       

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

