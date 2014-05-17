# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 08:23:07 2013

@author: gfpe
"""
from FBGdata import *
from we_file_io import WEFileIO, TestWEFileIO

import numpy as np

#Conventional Plot
"""

my_data = FBGdata('FBG.txt')
my_data.read()

files that you can read
my_data.data: Array of the data
can call by the name ex: print my_data.data ['s1']

my_data.head: information of the text, data, sample rate

my_data.sens: information about the sensors (absolute wavelenght)

my_data.nsens: number of sensors


data=my_data.data
head=my_data.head.split('\t')
sens=my_data.sens
nsens=my_data.nsens

my_data.plot()


"""


#plot with UI
MyPlotMainWindow().start()