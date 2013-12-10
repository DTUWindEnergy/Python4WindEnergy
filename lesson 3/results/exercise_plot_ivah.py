# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Plotting with Matplotlib

# <headingcell level=2>

# Prepare for action

# <codecell>

import numpy as np
import scipy as sp
import sympy

# Pylab combines the pyplot functionality (for plotting) with the numpy
# functionality (for mathematics and for working with arrays) in a single namespace
# aims to provide a closer MATLAB feel (the easy way). Note that his approach
# should only be used when doing some interactive quick and dirty data inspection.
# DO NOT USE THIS FOR SCRIPTS
#from pylab import *

# the convienient Matplotib plotting interface pyplot (the tidy/right way)
# use this for building scripts. The examples here will all use pyplot.
import matplotlib.pyplot as plt

# for using the matplotlib API directly (the hard and verbose way)
# use this when building applications, and/or backends
import matplotlib as mpl

# <markdowncell>

# How would you like the IPython notebook show your plots? In order to use the
# matplotlib IPython magic youre IPython notebook should be launched as
# 
#     ipython notebook --matplotlib=inline
# 
# Make plots appear as a pop up window, chose the backend: 'gtk', 'inline', 'osx', 'qt', 'qt4', 'tk', 'wx'
#     
#     %matplotlib qt
#     
# or inline the notebook (no panning, zooming through the plot). Not working in IPython 0.x
#     
#     %matplotib inline
#     

# <codecell>

# activate pop up plots
#%matplotlib qt
# or change to inline plots
%matplotlib inline

# <headingcell level=3>

# Matplotlib documentation

# <markdowncell>

# Finding your own way (aka RTFM). Hint: there is search box available!
# 
# * http://matplotlib.org/contents.html
# 
# The Matplotlib API docs:
# 
# * http://matplotlib.org/api/index.html
# 
# Pyplot, object oriented plotting:
# 
# * http://matplotlib.org/api/pyplot_api.html
# * http://matplotlib.org/api/pyplot_summary.html
# 
# Extensive gallery with examples:
# 
# * http://matplotlib.org/gallery.html

# <headingcell level=3>

# Tutorials for those who want to start playing

# <markdowncell>

# If reading manuals is too much for you, there is a very good tutorial available here:
# 
# * http://nbviewer.ipython.org/github/jrjohansson/scientific-python-lectures/blob/master/Lecture-4-Matplotlib.ipynb
# 
# Note that this tutorial uses
# 
#     from pylab import *
# 
# which is usually not adviced in more advanced script environments. When using
#     
#     import matplotlib.pyplot as plt
# 
# you need to preceed all plotting commands as used in the above tutorial with
#     
#     plt.

# <markdowncell>

# Give me more!
# 
# [EuroScipy 2012 Matlotlib tutorial](http://www.loria.fr/~rougier/teaching/matplotlib/). Note that here the author uses ```from pylab import * ```. When using ```import matplotliblib.pyplot as plt``` the plotting commands need to be proceeded with ```plt.```

# <headingcell level=2>

# Plotting template starting point

# <codecell>

# some sample data
x = np.arange(-10,10,0.1)

# <markdowncell>

# To change the default plot configuration values.

# <codecell>

page_width_cm = 13
dpi = 200
inch = 2.54 # inch in cm
# setting global plot configuration using the RC configuration style
plt.rc('font', family='serif')
plt.rc('xtick', labelsize=12) # tick labels
plt.rc('ytick', labelsize=20) # tick labels
plt.rc('axes', labelsize=20)  # axes labels
# If you don’t need LaTeX, don’t use it. It is slower to plot, and text
# looks just fine without. If you need it, e.g. for symbols, then use it.
#plt.rc('text', usetex=True) #<- P-E: Doesn't work on my Mac

# <codecell>

# create a figure instance, note that figure size is given in inches!
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8,6))
# set the big title (note aligment relative to figure)
fig.suptitle("suptitle 16, figure alignment", fontsize=16)

# actual plotting
ax.plot(x, x**2, label="label 12")


# set axes title (note aligment relative to axes)
ax.set_title("title 14, axes alignment", fontsize=14)

# axes labels
ax.set_xlabel('xlabel 12')
ax.set_ylabel(r'$y_{\alpha}$ 12', fontsize=20)

# legend
ax.legend(fontsize=12, loc="best")

# saving the figure in different formats
fig.savefig('figure-%03i.png' % dpi, dpi=dpi)
fig.savefig('figure.svg')
fig.savefig('figure.eps')

# <codecell>

# following steps are only relevant when using figures as pop up windows (with %matplotlib qt)
# to update a figure with has been modified
fig.canvas.draw()
# show a figure
fig.show()

# <headingcell level=2>

# Exercise

# <markdowncell>

# The current section is about you trying to figure out how to do several plotting features. You should use the previously mentioned resources to find how to do that. In many cases, google is your friend!

# <markdowncell>

# * add a grid to the plot

# <codecell>

plt.plot(x,x**2)
plt.grid(b=None, which='major', axis='both')

# <markdowncell>

# * change the location of the legend to different places

# <codecell>

plt.plot(x,x**2, label="label 12")
plt.legend(fontsize=12, loc=5)

# <markdowncell>

# * find a way to control the line type and color, marker type and color, control the frequency of the marks (`markevery`). See plot options at: http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.plot 

# <codecell>

plt.plot(x,x**2,color='green', linestyle='dashed', marker='H',
     markerfacecolor='red', markersize=3)

# <markdowncell>

# * add different sub-plots

# <codecell>


plt.subplot(211)
plt.plot(x,x**2, 'bo')


plt.subplot(212)
plt.plot(x,x**2, 'r--')



# <markdowncell>

# * size the figure such that when included on an A4 page the fonts are given in their true size

# <codecell>


# <markdowncell>

# * make a contour plot

# <codecell>

X, Y = np.meshgrid(x,np.sin(x))
Z = 4.0 * (X - Y)

plt.figure()
CS = plt.contour(X, Y,Z)
plt.clabel(CS, inline=1, fontsize=15)

# <markdowncell>

# * use twinx() to create a second axis on the right for the second plot

# <codecell>


fig = plt.figure()
ax = fig.add_subplot(111)
plt.plot(x,x**2)

ax2 = ax.twinx()
ax2.plot(x,x**4, 'r', label = 'second')
ax2.set_ylabel(r"Second")


# <markdowncell>

# * add horizontal and vertical lines using axvline(), axhline()

# <codecell>

plt.plot(x,x**2)
plt.axvline(x=-5, ymin=0, ymax=1, hold=None)
plt.axhline(y=60, xmin=0, xmax=1, hold=None)

# <markdowncell>

# * autoformat dates for nice printing on the x-axis using fig.autofmt_xdate()

# <codecell>

import datetime
dates = np.array([datetime.datetime.now() + datetime.timedelta(days=i) for i in xrange(24)])
fig, ax = plt.subplots(nrows=1, ncols=1)

y = range(24)


plt.plot ( dates, y)
fig.autofmt_xdate(bottom = 0.2, rotation=60, ha='right')



# <headingcell level=2>

# Advanced exercises

# <markdowncell>

# We are going to play a bit with regression

# <markdowncell>

# * Create a vector x of equally spaced number between $x \in [0, 5\pi]$ of 1000 points (keyword: linspace)

# <codecell>

x = np.linspace(0, 5*np.pi, 1000)

# <markdowncell>

# * create a vector y, so that y=sin(x) with some random noise

# <codecell>

import random

s = np.random.uniform(-0.5,0.5,1000)
y = np.sin(x)
ys = y+s
#print s

#print y

# <markdowncell>

# * plot it like this: ![test](files/plt1.png)

# <codecell>

plt.plot(x,y,'k--' ,linewidth=2.0, label="y = sin(x)")

plt.plot (x,ys,'cd', markersize = 3)

plt.legend(fontsize=12, loc='upper right')

# <markdowncell>

# Try to do a polynomial fit on y(x) with different polynomial degree (Use numpy.polyfit to obtain coefficients)
# 
# Plot it like this (use np.poly1d(coef)(x) to plot polynomials) ![test](files/plt2.png)

# <codecell>

P0 = np.polyfit(x,ys,0)
P1 = np.polyfit(x,ys,1)
P2 = np.polyfit(x,ys,2)
P3 = np.polyfit(x,ys,3)
P4 = np.polyfit(x,ys,4)
P5 = np.polyfit(x,ys,5)
P6 = np.polyfit(x,ys,6)
P7 = np.polyfit(x,ys,7)
P8 = np.polyfit(x,ys,8)
P9 = np.polyfit(x,ys,9)

# <codecell>

plt.plot(x,y,'k--' ,linewidth=2.0, label="y = sin(x)")

plt.plot (x,ys,'bd', markersize = 3)
plt.plot (x,np.poly1d(P0)(x), label = "deg0")
plt.plot (x,np.poly1d(P1)(x), label = "deg1")
plt.plot (x,np.poly1d(P2)(x), label = "deg2")
plt.plot (x,np.poly1d(P3)(x), label = "deg3")
plt.plot (x,np.poly1d(P4)(x), label = "deg4")
plt.plot (x,np.poly1d(P5)(x), label = "deg5")
plt.plot (x,np.poly1d(P6)(x), label = "deg6")
plt.plot (x,np.poly1d(P7)(x), label = "deg7")
plt.plot (x,np.poly1d(P8)(x), label = "deg8")
plt.plot (x,np.poly1d(P9)(x), label = "deg9")
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))



# <codecell>


