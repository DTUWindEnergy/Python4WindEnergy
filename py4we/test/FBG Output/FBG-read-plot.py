# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 08:23:07 2013

@author: gfpe
"""
from FBGdata import *
from we_file_io import WEFileIO, TestWEFileIO

import numpy as np

my_data = FBGdata('FBG.txt')
my_data.read()

"""files that you can read
my_data.data: Array of the data
can call by the name ex: print my_data.data ['s1']

my_data.head: information of the text, data, sample rate

my_data.sens: information about the sensors (absolute wavelenght)

my_data.nsens: number of sensors
"""

data=my_data.data
head=my_data.head.split('\t')
sens=my_data.sens
nsens=my_data.nsens


"""Ploting"""
import scipy as sp
import sympy
import matplotlib.pyplot as plt

page_width_cm = 13
dpi = 200
inch = 2.54 # inch in cm
# setting global plot configuration using the RC configuration style
plt.rc('font', family='serif')
plt.rc('xtick', labelsize=12) # tick labels
plt.rc('ytick', labelsize=12) # tick labels
plt.rc('axes', labelsize=12)  # axes labels
# If you don’t need LaTeX, don’t use it. It is slower to plot, and text
# looks just fine without. If you need it, e.g. for symbols, then use it.
#plt.rc('text', usetex=True) #<- P-E: Doesn't work on my Mac

fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(10,15))
fig.suptitle('Name: %s \n%s \n Start: %s, End:%s'%(head[0],head[1],head[2],
                                                   head[3]), fontsize=16)
ax[1].grid()
ax[0].grid() 

"""Plot of Relative values""" 

ax[0].set_title("Relative Wavelength",fontsize=14)    
                                               
for i in range(nsens):
    sensor= 's'+str(i+1)
    ax[0].plot(data[sensor], linewidth=2.00,label="Sensor "+str(i+1))   
    
ax[0].legend(fontsize=12, loc="best")
ax[0].set_xlabel('Time (s)')
ax[0].set_ylabel(r'$\Delta$\lambda [$\mu m]')
 

"""Plot of absolute values"""

ax[1].set_title("Absolute Wavelength",fontsize=14)
senss=sens.split('\t')
for i in range(nsens):
    
    """getting the sensor absolute value"""
    v=senss[i+2]
    sensv=float(v[14:25])
    sensor= 's'+str(i+1)    
    ax[1].plot(sensv+data[sensor], linewidth=2.00,label="Sensor "+str(i+1))
    
ax[1].legend(fontsize=12, loc="best")    
ax[1].set_xlabel('Time (s)')
ax[1].set_ylabel('$\lambda [$\mu m]')
    
                                             
