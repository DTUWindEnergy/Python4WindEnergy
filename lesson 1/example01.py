# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 22:32:06 2013

@author: dave
"""

import sympy
import numpy as np
import math
import logging
from matplotlib import pylab as plt
import matplotlib as mpl

mpl.rc('text', usetex=True)

def _solve_A(A, **kwargs):
    r"""
    Centrifugal corrected equivalent moment
    =======================================
    
    Convert beam loading into a single equivalent bending moment. Note that
    this is dependent on the location in the cross section. Due to the 
    way we measure the strain on the blade and how we did the calibration
    of those sensors.
    
    .. math::

        \epsilon = \frac{M_{x_{equiv}}y}{EI_{xx}} = \frac{M_x y}{EI_{xx}} 
        + \frac{M_y x}{EI_{yy}} + \frac{F_z}{EA}
        
        M_{x_{equiv}} = M_x + \frac{I_{xx}}{I_{yy}} M_y \frac{x}{y}  
        + \frac{I_{xx}}{Ay} F_z
    
    Parameters
    ----------
    
    st_arr : np.ndarray(19)
        Only one line of the st_arr is allowed and it should correspond
        to the correct radial position of the strain gauge.
    
    load : list(6)
        list containing the load time series of following components
        .. math:: load = F_x, F_y, F_z, M_x, M_y, M_z
        and where each component is an ndarray(m)
    
    """
    
    d = kwargs.get('d', 40.) 
    L = kwargs.get('L', 150.)
    acc_check = kwargs.get('acc_check', 0.0000001) 
    solve_acc = kwargs.get('solve_acc', 20) 
    
    # set the accuracy target of the solver
    sympy.mpmath.mp.dps = solve_acc
    psi = sympy.Symbol('psi')
    f1 = L - (L*sympy.tan(psi)) + (d/(2.*sympy.cos(psi))) - A
    # initial guess: solve system for delta_x = 0
    psi0 = math.atan(1 - (A/L))
    # solve the equation numerically with sympy
    psi_sol = sympy.nsolve(f1, psi, psi0)
    
    # verify if the solution is valid
    delta_x = d / (2.*math.cos(psi_sol))
    x = L*math.tan(psi_sol)
    Asym = sympy.Symbol('Asym')
    f_check = x - L + Asym - delta_x
    
    # verify that f_check == 0
    if not sympy.solvers.checksol(f_check, Asym, A):
        # in the event that it does not pass the checksol, see how close
        # the are manually. Seems they are rather close
        check_A = L + delta_x - x
        error = abs(A - check_A) / A
        if error > acc_check:
            msg = 'sympy\'s solution does not passes checksol()'
            msg += '\n A_check=%.12f <=> A=%.12f' % (check_A, A)
            raise ValueError, msg
        else:
            msg = 'sympy.solvers.checksol() failed, manual check is ok. '
            msg += 'A=%.2f, rel error=%2.3e' % (A, error)
            logging.warning(msg)
    
    return psi_sol*180./math.pi, psi0*180./math.pi



figpath = '/home/dave/PhD/Projects/PostProcessing/OJF_tests/'
figpath += 'YawLaserCalibration-04/'
pprpath = figpath
fname = 'runs_289_295.yawcal-psiA-stairA'

A_range = range(60,190,5)
A_range[0] = 64
A_range.append(190)

A_psi = np.ndarray((len(A_range),2))
A_psi[:,0] = A_range

n = 0
for A in A_range:
    A_psi[n,1], psi0 = _solve_A(A)
    n += 1

res = np.loadtxt(figpath+fname)

plt.plot(A_psi[:,0], A_psi[:,1])
plt.grid()
plt.title('stuff')
plt.plot(res[:,0], res[:,1], 'rs')
plt.show()


