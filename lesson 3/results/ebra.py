# -*- coding: utf-8 -*- <nbformat>3.0</nbformat>

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
# %matplotlib inline

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
ax.set_ylabel(r'$y_{\alpha}$ 12', fontsize=8)

# legend
ax.legend(fontsize=12, loc="best")

# saving the figure in different formats
# fig.savefig('figure-%03i.png' % dpi, dpi=dpi)
# fig.savefig('figure.svg')
# fig.savefig('figure.eps')

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
plt.grid('on')

# <markdowncell>

# * change the location of the legend to different places

# <codecell>

plt.plot(x,x**2, label="label 12")
plt.legend(fontsize=12, loc="upper right")

# <markdowncell>

# * find a way to control the line type and color, marker type and color, control the frequency of the marks (`markevery`). See plot options at: http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.plot 

# <codecell>
stride = max( int(len(x) / 20), 1)
plt.plot(x,x**2, 'ko-',color='forestgreen', markevery=stride,label="label 12") 
plt.legend(fontsize=12, loc="upper center")
# <markdowncell>

# * add different sub-plots

# <codecell>

fig, axes = plt.subplots(nrows=2, ncols=1,sharex=True)
axes[0].plot(x,x**2)
axes[1].plot(x,-x**2)

# <markdowncell>

# * size the figure such that when included on an A4 page the fonts are given in their true size

# <codecell>
# matplotlib.rcParams.update({'font.size': 22})
fig, axes = plt.subplots(nrows=2, ncols=1,sharex=True)
axes[0].plot(x,x**2)
axes[1].plot(x,-x**2)
fig.set_size_inches(8.2,3) # using A4 width in inches?
fig.set_dpi(100)
for ax in axes:
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
                 ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(12)
# ax[0].set('xtick', labelsize=12) # tick labels
# .rc('ytick', labelsize=20) # tick labels
# .rc('axes', labelsize=20)  # axes labels
# fig.savefig('figure.pdf')
# <markdowncell>

# * make a contour plot

# <codecell>
X, Y = np.meshgrid(x,x)
plt.figure()
plt.contourf(X,Y,X*Y,linewidth=0.3,cmap=plt.get_cmap('hsv'))
# im=ax.contourf(x,y,ui,levels=np.arange(Umean-5*Ustd,Umean+5*Ustd,Ustd/30),cmap=plt.get_cmap('hsv'),linewidth=0.1)

# <markdowncell>

# * use twinx() to create a second axis on the right for the second plot

# <codecell>
plt.figure()
ax=plt.gca()
ax.plot(x,x**2)
ax2 = ax.twinx()
ax2.plot(x,x**4, 'r')
# <markdowncell>

# * add horizontal and vertical lines using axvline(), axhline()

# <codecell>

plt.figure()
plt.plot(x,x**2)
plt.axvline(2)
plt.axhline(10)

# <markdowncell>

# * autoformat dates for nice printing on the x-axis using fig.autofmt_xdate()

# <codecell>

import datetime
dates = np.array([datetime.datetime.now() + datetime.timedelta(days=i) for i in xrange(24)])
fig, ax = plt.subplots(nrows=1, ncols=1)
ax.plot(dates,xrange(24))
fig.autofmt_xdate()
# <headingcell level=2>

# Advanced exercises

# <markdowncell>

# We are going to play a bit with regression

# <markdowncell>

# * Create a vector x of equally spaced number between $x \in [0, 5\pi]$ of 1000 points (keyword: linspace)

# <codecell>
n=1000
x=np.linspace(0,5*np.pi,n)

# <markdowncell>

# * create a vector y, so that y=sin(x) with some random noise

# <codecell>
y   = np.sin(x) +np.random.rand(n)-0.5
yth = np.sin(x)

# <markdowncell>

# * plot it like this: ![test](files/plt1.png)

# <codecell>
fig=plt.figure()
ax=plt.gca()
ax.plot(x,y,'b.')
ax.plot(x,yth,'k--',label=r'$y=sin(x)$')

# <markdowncell>

# Try to do a polynomial fit on y(x) with different polynomial degree (Use numpy.polyfit to obtain coefficients)
# 
# Plot it like this (use np.poly1d(coef)(x) to plot polynomials) ![test](files/plt2.png)

# <codecell>
for order in xrange(9):
    coeff=np.polyfit(x,y,order)
    ax.plot(x,np.poly1d(coeff)(x),label='deg %d'%order)

# shrink current axis by 20%
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()
# <codecell>

