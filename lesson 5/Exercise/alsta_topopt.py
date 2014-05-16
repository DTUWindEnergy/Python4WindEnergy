# coding: utf-8
#
# This is an adaptation of the 200 line topology optimization code provided
# by the TopOpt research group at DTU.
# The original is available on: http://www.topopt.dtu.dk/?q=node/881
#
# While the original implementation uses MMA as a solver and is considerably
# faster in finding the minimum, the openMDAO native solvers have been used here.
# SLSQP gives generally the best results. Without derivatives it provides
# the lowest minimum of the objective, however, it is considerably faster
# when derivatives are provided (9000 vs 100 iterations).
#
# Alexander Stäblein, DTU Wind Energy
# alsta@dtu.dk

from __future__ import division
from openmdao.main.api import Assembly
from openmdao.main.api import Component
from openmdao.lib.drivers.api import COBYLAdriver
from openmdao.lib.drivers.api import CONMINdriver
from openmdao.lib.drivers.api import NEWSUMTdriver
from openmdao.lib.drivers.api import SLSQPdriver
from openmdao.lib.datatypes.api import Array, Float

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve
from matplotlib import colors
import matplotlib.pyplot as plt

import pdb # pdb.set_trace() for debugging

class openMDAO_TopOpt(Assembly):

    def configure(self):
        #self.add('driver', COBYLAdriver())
        #self.add('driver', CONMINdriver())
        #self.add('driver', NEWSUMTdriver())
        self.add('driver', SLSQPdriver())
        
        self.add('topopt', TopOpt())
        self.driver.workflow.add('topopt')
        self.driver.iprint = 0 # optimizers verbosity
        self.driver.add_constraint('topopt.vol <= 0.5')

        self.driver.add_objective('topopt.c')
        self.driver.add_parameter('topopt.var', low=0.0, high=1.0)

class TopOpt(Component):

    # use derivatives
    deriv = 1

    # set design parameters
    nelx=30
    nely=10
    volfrac=0.5
    rmin=1.5
    penal=3.0
    ft=1 # ft==0 -> sens, ft==1 -> dens

    # set up interface of the framework
    var = Array(volfrac*np.ones(nely*nelx), dtype=float, iotype='in', desc='Design Parameter')
    c = Float(iotype='out', desc='Objective Function')
    vol = Float(volfrac, iotype='out', desc='Constraint')

    # Max and min stiffness
    Emin=1e-9
    Emax=1.0

    # dofs:
    ndof = 2*(nelx+1)*(nely+1)

    # Allocate design variables (as array), initialize and allocate sens.
    x     = volfrac * np.ones(nely*nelx,dtype=float)
    xold  = x.copy()
    xPhys = x.copy()

    g=0 # must be initialized to use the NGuyen/Paulino OC approach
    dc=np.zeros((nely,nelx), dtype=float)

    #element stiffness matrix
    def lk():
        E=1
        nu=0.3
        k=np.array([1/2-nu/6,1/8+nu/8,-1/4-nu/12,-1/8+3*nu/8,-1/4+nu/12,-1/8-nu/8,nu/6,1/8-3*nu/8])
        KE = E/(1-nu**2)*np.array([ [k[0], k[1], k[2], k[3], k[4], k[5], k[6], k[7]],
        [k[1], k[0], k[7], k[6], k[5], k[4], k[3], k[2]],
        [k[2], k[7], k[0], k[5], k[6], k[3], k[4], k[1]],
        [k[3], k[6], k[5], k[0], k[7], k[2], k[1], k[4]],
        [k[4], k[5], k[6], k[7], k[0], k[1], k[2], k[3]],
        [k[5], k[4], k[3], k[2], k[1], k[0], k[7], k[6]],
        [k[6], k[3], k[4], k[1], k[2], k[7], k[0], k[5]],
        [k[7], k[2], k[1], k[4], k[3], k[6], k[5], k[0]] ]);
        return (KE)

    def deleterowcol(self, A, delrow, delcol):
        # Assumes that matrix is in symmetric csc form !
        m = A.shape[0]
        keep = np.delete (np.arange(0, m), delrow)
        A = A[keep, :]
        keep = np.delete (np.arange(0, m), delcol)
        A = A[:, keep]
        return A

    # FE: Build the index vectors for the for coo matrix format.
    KE=lk()
    edofMat=np.zeros((nelx*nely,8),dtype=int)
    for elx in range(nelx):
            for ely in range(nely):
                    el = ely+elx*nely
                    n1=(nely+1)*elx+ely
                    n2=(nely+1)*(elx+1)+ely
                    edofMat[el,:]=np.array([2*n1+2, 2*n1+3, 2*n2+2, 2*n2+3,2*n2, 2*n2+1, 2*n1, 2*n1+1])
    # Construct the index pointers for the coo format
    iK = np.kron(edofMat,np.ones((8,1))).flatten()
    jK = np.kron(edofMat,np.ones((1,8))).flatten()

    # Filter: Build (and assemble) the index+data vectors for the coo matrix format
    nfilter=nelx*nely*((2*(np.ceil(rmin)-1)+1)**2)
    iH = np.zeros(nfilter)
    jH = np.zeros(nfilter)
    sH = np.zeros(nfilter)
    cc=0
    for i in range(nelx):
            for j in range(nely):
                    row=i*nely+j
                    kk1=int(np.maximum(i-(np.ceil(rmin)-1),0))
                    kk2=int(np.minimum(i+np.ceil(rmin),nelx))
                    ll1=int(np.maximum(j-(np.ceil(rmin)-1),0))
                    ll2=int(np.minimum(j+np.ceil(rmin),nely))
                    for k in range(kk1,kk2):
                            for l in range(ll1,ll2):
                                    col=k*nely+l
                                    fac=rmin-np.sqrt(((i-k)*(i-k)+(j-l)*(j-l)))
                                    iH[cc]=row
                                    jH[cc]=col
                                    sH[cc]=np.maximum(0.0,fac)
                                    cc=cc+1
    # Finalize assembly and convert to csc format
    H=coo_matrix((sH,(iH,jH)),shape=(nelx*nely,nelx*nely)).tocsc()
    Hs=H.sum(1)

    # BC's and support
    dofs=np.arange(2*(nelx+1)*(nely+1))
    fixed=np.union1d(dofs[0:2*(nely+1):2],np.array([2*(nelx+1)*(nely+1)-1]))
    free=np.setdiff1d(dofs,fixed)

    # Solution and RHS vectors
    f=np.zeros((ndof,1))
    u=np.zeros((ndof,1))

    # Set load
    f[1,0]=-1

    # Initialize plot and plot the initial design
    plt.ion() # Ensure that redrawing is possible
    fig,ax = plt.subplots()
    im = ax.imshow(-xPhys.reshape((nelx,nely)).T, cmap='gray',\
    interpolation='none',norm=colors.Normalize(vmin=-1,vmax=0))
    fig.show()

    loop=0
    change=1
    ce = np.ones(nely*nelx)
    dc = np.ones(nely*nelx)
    dv = np.ones(nely*nelx)

    def fea(self):

        # Filter design variables
        if self.ft==0:   self.xPhys[:]=self.var
        elif self.ft==1: self.xPhys[:]=np.asarray(self.H*self.var[np.newaxis].T/self.Hs)[:,0]

        # Setup and solve FE problem
        self.sK=((self.KE.flatten()[np.newaxis]).T*(self.Emin+(self.xPhys)**self.penal \
                *(self.Emax-self.Emin))).flatten(order='F')
        self.K = coo_matrix((self.sK,(self.iK,self.jK)),shape=(self.ndof,self.ndof)).tocsc()

        # Remove constrained dofs from matrix
        self.K = self.deleterowcol(self.K,self.fixed,self.fixed)
        # Solve system 
        self.u[self.free,0]=spsolve(self.K,self.f[self.free,0]) 
        # Objective 
        self.ce[:] = (np.dot(self.u[self.edofMat].reshape(self.nelx*self.nely,8),self.KE) \
                *self.u[self.edofMat].reshape(self.nelx*self.nely,8) ).sum(1)

    def execute(self):

        self.loop=self.loop+1

        self.fea()
        self.c=( (self.Emin+self.xPhys**self.penal*(self.Emax-self.Emin))*self.ce ).sum()

        # Compute the change by the inf. norm
        self.change=np.linalg.norm(self.var.reshape(self.nelx*self.nely,1) \
                -self.xold.reshape(self.nelx*self.nely,1),np.inf)
        self.xold[:]=self.var
        # Update volume constraint
        self.vol = sum(self.var)/(self.nelx*self.nely)
        # Plot to screen
        self.im.set_array(-self.xPhys.reshape((self.nelx,self.nely)).T)
        self.fig.canvas.draw()

        # Write iteration history to screen (req. Python 2.6 or newer)
        print("it.: {0} , obj.: {1:.3f} Vol.: {2:.3f}, ch.: {3:.3f}".format(\
        self.loop,self.c,self.vol,self.change))

    if deriv:

        def list_deriv_vars(self):
            return ('var',), ('c','vol')
            
        def provideJ(self):
            """Calculate the Jacobian"""
            self.fea()
    
            # Sensitivity
            self.dc[:] = (-self.penal*self.xPhys**(self.penal-1)*(self.Emax-self.Emin))*self.ce
            self.dv[:] = np.ones(self.nely*self.nelx)
            # Sensitivity filtering:
            if self.ft==0:
                    self.dc[:] = np.asarray((self.H*(self.var*self.dc))[np.newaxis].T/self.Hs)[:,0] / np.maximum(0.001,self.var)
            elif self.ft==1:
                    self.dc[:] = np.asarray(self.H*(self.dc[np.newaxis].T/self.Hs))[:,0]
                    self.dv[:] = np.asarray(self.H*(self.dv[np.newaxis].T/self.Hs))[:,0]
            self.J = np.vstack((self.dc,self.dv))
            return self.J

if __name__ == "__main__":
    opt_problem = openMDAO_TopOpt()

    import time
    tt = time.time()

    opt_problem.run()

    print "\n"
    print "Minimum found with c = %f" % opt_problem.topopt.c
    print "Elapsed time: ", time.time()-tt, "seconds"
    plt.show()
    raw_input("Press any key...")


