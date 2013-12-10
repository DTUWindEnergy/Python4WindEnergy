# coding: utf-8

# The iPython notebooks did not work on my computer.
# I therefore did the exercise in plane python.

import numpy as np
import scipy as sp
import sympy

import matplotlib.pyplot as plt
import matplotlib as mpl

x = np.arange(-10,10,0.1)

fig, ax = plt.subplots(nrows=3, ncols=1)

ax[0].plot(x,x**2, 'o-',label='label 12')
ax2 = ax[0].twinx()
ax2.plot(x,x**4, 'r')

ax[0].grid()
ax[0].legend(loc='best')

X, Y = np.meshgrid(x,x)
def f(x,y): return x**2+y**2
ax[1].contour(X, Y, f(X,Y))
ax[1].vlines(3,-10,10)
ax[1].hlines(3,-10,10)

x = np.linspace(0.0,5*np.pi,num=1000)
y = np.sin(x)
z = np.sin(x) + np.random.uniform(-.3, .3, size=1000)

ax[2].plot(x,y)
ax[2].plot(x,z, '.')

for i in range(0, 9):
    coef = np.polyfit(x,z,i)
    lab = 'deg='+ str(i)
    ax[2].plot(x,np.poly1d(coef)(x))

plt.show()
