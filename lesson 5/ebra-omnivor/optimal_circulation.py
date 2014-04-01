#!/usr/bin/env python
import os, sys, inspect
# pythonpath=os.path.realpath(os.path.abspath(os.path.join(os.getenv('OMNIVOR_MKF_DIR', './'),'_PythonPath')))
pythonpath=os.path.realpath(os.path.abspath(os.path.join('./','_OmnivorPythonPath')))
sys.path.insert(0, pythonpath)
#
from matplotlib.pylab import *
from numpy import *
from pylab import *
from Omnivor import *
from OmnivorTools import *
from time import sleep


# --------------------------------------------------------------------------------
# --- OPENMDAO 
# --------------------------------------------------------------------------------
from openmdao.main.api import Component, Assembly, Slot, Case
from openmdao.main.datatypes.api import Float, Int
from openmdao.util.testutil import assert_rel_error, assert_raises


from openmdao.lib.casehandlers.api import DBCaseRecorder, ListCaseRecorder, ListCaseIterator
from openmdao.lib.drivers.api import CaseIteratorDriver
from openmdao.main.api import Driver
from openmdao.lib.casehandlers.dbcase import list_db_vars, case_db_to_dict

from openmdao.lib.drivers.api import COBYLAdriver, CONMINdriver, NEWSUMTdriver, SLSQPdriver, Genetic
    
import os.path as path
import pandas as pd
import sys



nr   = 25;
U0=10.05 

def simulation(s_prescr,g_prescr,case,bPlot=0):
    # Main Parameters
    nw   = 3;
    RPM  = 22.; # gives lambda =7 with 10.05mps
    dt   = 0.1 ;
    tmax = 3   ;
    Smooth_Model = 3 ;
    Smooth_t0    = 0.1  ;
    Smooth_delta = 200;
    Smooth_method = 2;
    pSmooth_Model = 3;
    pSmooth_t0    = 0.96  ; # used to be 0.76
    pSmooth_delta = 200;    # used to be 100
    SpanMesh = 'cos';
    SpanCPMesh = 'fullcosineapprox';
#     SpanCPMesh = 'fullcosineapprox';
#     SpanMesh = 'linear';
#     SpanCPMesh = 'middle';
    RelSizeNW = 0.25;
    nExport=0


    
    
    # --------------------------------------------------------------------------------
    # --- Initialization of Omnivor library and layer 
    # --------------------------------------------------------------------------------
    omnivor=Omnivor('raccoon')
    # Parameters that should be specified before init of layer
    omnivor.set_common_var('bSILENT',1);   
    omnivor.set_common_var('bSILENT_WARN',1);   
    omnivor.set_common_var('bDEBUG',0);
    omnivor.set_common_var('bDEBUGMIN',0);
    omnivor.set_common_var('bLOG_FILE',0);  
    omnivor.set_common_var('bOUT_FILE',0); 
    omnivor.set_common_var('bGEOM_FILE',0);
    omnivor.set_common_var('bSTOP_ALLOWED',1);
#     omnivor.init('sim_opticirc-'+case)
    omnivor.init()
    omnivor.init_layer()
    # Retrieving version
    current_version=omnivor.version()[1:8]

    #--------------------------------------------------------------------------------
    #--- Common Data 
    #--------------------------------------------------------------------------------
    omnivor.set_common_var('tmax',tmax);
    omnivor.set_common_var('dt',dt);
    omnivor.set_common_var('bExportStates',0);
    omnivor.set_common_var('nExportStates',2);
    omnivor.set_freewind([0,U0,0]);
    #--------------------------------------------------------------------------------
    #--- Raccoon Part
    #--------------------------------------------------------------------------------
    omnivor.set_nbodies(nw,nw);
    # Wind turbine
    omnivor.new_obj('from_file');

    # Files
    omnivor.set_obj('nFiles',1);
#     omnivor.set_obj_file('blade_stations_cos20.txt','delim-S-C-B-DR-t100',' ',1);
    omnivor.set_obj_file('data/Tjaereborg_BladeGeometry.dat','delim-S-C-B-t100',' ',1);


    # Geometry
    omnivor.set_obj('Pitch' , 0.0);
    omnivor.set_obj('rHub',0.0);
    omnivor.set_obj('nB',nw);

    # Panelling
    omnivor.set_obj('nMainDirection',nr);
    omnivor.set_obj('nSecondaryDirection',1);
    omnivor.set_obj('sSpanMeshFunction',SpanMesh);
    # omnivor.set_obj('sSpanCPMeshFunction','fullcosineapprox');
    omnivor.set_obj('sSpanCPMeshFunction',SpanCPMesh);

    # Algo
    omnivor.set_obj('pIntCompMeth',3);#0:nothing, 1:Solve, 2:Profiles, 3:Prescribed

    omnivor.set_obj('bStartAtLE',0); # TODO manu emit a warning if prescribed and not start at LE
    omnivor.set_obj('bEndAtTE',1);


    # Motion
    TranslatVel=[0.,0.,0.];
    RotVect=[0.,1,0.];
    RotCenter=[0.,0.,0.];
    RotVel=RPM*2.*pi/60.;
    RotPhase=0;
    omnivor.set_obj_vel(TranslatVel,RotVect,RotCenter,RotVel,RotPhase);

    # Adding object at the end
    omnivor.add_obj();



    #--------------------------------------------------------------------------------
    #--- Mouffette Part
    #--------------------------------------------------------------------------------
    omnivor.set_algo('bProfiles2PiAlpha',1);
    omnivor.set_algo('bPlaceConcentratedShedVorticity',1);


    omnivor.set_algo('bConvertToPart',0);
    omnivor.set_algo('tConvertToPart',40);
    omnivor.set_algo('bNoRollUp',1); # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#     omnivor.set_algo('tRollUpStart',0);
    omnivor.set_algo('bDistortPart',0);

    omnivor.set_algo('RelSizeNWPanel',RelSizeNW);

    # Smooth
    omnivor.set_algo('SgmtSmooth%Model',Smooth_Model);
    omnivor.set_algo('SgmtSmooth%Param1',Smooth_delta);
    omnivor.set_algo('SgmtSmooth%Param2',Smooth_t0);
    omnivor.set_algo('SgmtSmooth%ParamMethod',Smooth_method);
    omnivor.set_algo('PanlSmooth%Model',pSmooth_Model);
    omnivor.set_algo('PanlSmooth%Param1',pSmooth_delta);
    omnivor.set_algo('PanlSmooth%Param2',pSmooth_t0);


    # Exportation
    omnivor.set_algo('pExportPlotFormat',0);
    omnivor.set_algo('pExportVelocityFormat',1);
    omnivor.set_algo('nExportPlot',nExport);
    omnivor.set_algo('nExportLoads',nExport);

    omnivor.set_algo('ProfileSolving_relax',0.003);
    omnivor.set_algo('ProfileSolving_MaxIter',20);
    # 
    #--------------------------------------------------------------------------------
    #--- Simulation
    #--------------------------------------------------------------------------------
    omnivor.set_common_var('bDEBUG',0);
    omnivor.apply();


    for iw in range(1,nw+1):
        omnivor.prescribe_wing(iw,s_prescr,g_prescr)

    omnivor.dotimeloop();
    (scp_ll,alpha_ll,Gamma_ll,alpha0_ll,Vrel,V0,Vbody)=omnivor.get_wing_loads(nr);

#     cpt=0;
#     while omnivor.incrementtime():
#         omnivor.dotimestep();
#         omnivor.loadscalc();
# 
#         (scp_ll,alpha_ll,Gamma_ll,alpha0_ll,Vrel,V0,Vbody)=omnivor.get_wing_loads(nr);
#         iw=1;
#         cpt=cpt+1;
# #         if bPlot==1:
# #             if cpt % 50 ==1:
# #                 plot(scp_ll,Vrel[1,:]-V0[1,:])
# # #                 ylim([-4,0])
# #                 draw()
# #                 sleep(0.05)
#     #     ax.cla()
# 
# #         omnivor.gridvelocity();
#         omnivor.finalize1();
# #         omnivor.export();
# #         omnivor.savestate();
#         omnivor.finalize2();
    omnivor.close()


    # --------------------------------------------------------------------------------
    # ---  Variables to compute turbine data
    # --------------------------------------------------------------------------------
    yaw=0
    nb=nw
    R=30.55
    omega=RotVel;
    vt=arange(0,tmax,dt);
    vpsi_hawc=omega*tmax*180/pi; # [deg!]
    vpsi=fmod(vpsi_hawc+180,360);
    # Using my convention (yaw articles)
    vpsi_manu=fmod(vpsi_hawc-90,360);

    # --------------------------------------------------------------------------------
    # ---  Normal/tangential velocities and induced velocities 
    # --------------------------------------------------------------------------------
    Un     = zeros((1,nr))
    Ut     = zeros(1,nr)
    Uin    = zeros(1,nr)
    Uit    = zeros(1,nr)
    Ut_rel = zeros(1,nr)

    # Normal component, i.e. y component
    Un     =Vrel[1,:];
    Uin    =Un-U0;

    # Tangential component (Using psi manu, because that's what I used for a scheme on paper, might as well use psi_racc (but different formula)
    Ut_rel[:] = -Vrel[0,:]*sind(vpsi_manu)-Vrel[2,:]*cosd(vpsi_manu) ; # Should be negative!!!!!!
    Ut[:]     = Ut_rel[:]-(-omega*scp_ll[:])                               ; # The induction due to wind and induction
    Uit[:]    = Ut[:]- (-U0*sind(yaw)*sind(vpsi_manu))                  ; 


    Gamma=interp(scp_ll,s_prescr,g_prescr)
#     figure()
#     plot(scp_ll,Gamma*Un*scp_ll)
#     plot(scp_ll,Gamma*Ut_rel)
    CP=float(nb)/(0.5*pi*R**2*U0**3)*trapz(Gamma*Un*scp_ll,scp_ll)
    CT=-float(nb)/(0.5*pi*R**2*U0**2)*trapz(Gamma*Ut_rel,scp_ll)
    print(CP,CT)
    return (CT,CP,scp_ll,Gamma_ll,Vrel,Un,Uin,Ut,Uit,Ut_rel)
# --------------------------------------------------------------------------------
# ---  
# --------------------------------------------------------------------------------
def standalone_run():
    # Loading Goldstein circulation
    filename='data/Goldstein-Gamma-CT0.60-lambda7.0-n1000.dat';
    FH = np.loadtxt(filename,comments='#',delimiter='\t',skiprows=1)
    s_ref=FH[:,0]
    g_ref=FH[:,1]
    bPlot=1

    # 
    s_prescr=s_ref;
    g_prescr=g_ref;
    print(max(g_ref))
#     hold(True)
#     box(True)
#     grid(True)
#     plot(s_prescr,g_prescr)
    case='test'
    (CT,CP,scp_ll,Gamma_ll,Vrel,Un,Uin,Ut,Uit,Ut_rel)=simulation(s_prescr,g_prescr,case,bPlot)


def call_func(self, outputs=None, **kwargs):
    """
    Conveniently call the assemblies/component in a functional way.
        output1, output2, ... = assembly(['output1', 'output2', ...], input1=val1, input2=val2...)
    or:
        output1 = assembly('output1', input1=val1, input2=val2...)
    or:
        assembly = assembly(input1=val1, input2=val2...)

    The function will do:
        self.input1 = val1
        self.input2 = val2
        ....
        self.execute()
        return [self.output1, self.output2,...]
    """
    for k, v in kwargs.iteritems():
        if hasattr(self, k):
            setattr(self, k, v)
            #print k + '=' + str(v)
    self.run()
    # Prepare outputs
    if not outputs:
        # Return the object executed that can then be used directly
        return self
    if isinstance(outputs, str):
        outputs_val = getattr(self, outputs)
    elif isinstance(outputs, list):
        outputs_val = []
        for o in outputs:
            outputs_val.append(getattr(self, o))
    return outputs_val

Component.__call__ = call_func
Assembly.__call__ = call_func

## Transform an openmdao recorder into a pandas dataframe
rec2df = lambda rec: pd.DataFrame([[c[k] for k in rec.cases[0].keys()] for c in rec.cases], columns=rec.cases[0].keys())

class OmnivorRun(Component):

    x   = Float(iotype='in')
    CP  = Float(iotype='out')
    CT  = Float(iotype='out')

    def execute(self):
        """ Performs a run with prescribed circulation """

        # Loading Goldstein circulation
        filename='data/Goldstein-Gamma-CT0.60-lambda7.0-n1000.dat';
        FH = np.loadtxt(filename,comments='#',delimiter='\t',skiprows=1)
        s_ref=FH[:,0]
        g_ref=FH[:,1]
        bPlot=1

        s_prescr=s_ref;
        case='test'

        # Using self parameters to adjust prescribed circulation
        x = self.x
        g_prescr=g_ref*x;
# params=fminsearchbnd(@fFitGammaNew,[xmax 0.25 0.5 0.25],[0.1 -Inf 0 0.2],[0.9 1 Inf 1],options,r,Gamma);
# [sse fit R2]=fFitGammaNew(params,r,Gamma);
# 
#         x0=params(1);
#         x2=params(2);
#         y3=params(3);
#         t0=params(4);
#         x3=1;
#         y4=0;
#         % t0=0.25;
#         [ a b c d e f g ] = facbdef( t0 );
#         y2=1/(d*b/a-e)*(d/a+y3*(f-d*c/a));
#         y1=1/a-(b/a*y2+c/a*y3);
#         x1=x0/a-(b/a*x2+c/a+g/a);



        print(max(g_ref))
        print(max(g_prescr))
        (CT,CP,scp_ll,Gamma_ll,Vrel,Un,Uin,Ut,Uit,Ut_rel)=simulation(s_prescr,g_prescr,case,bPlot)
        self.CP=-CP
        self.CT=CT


class OptiCirc(Assembly):
    def configure(self):
        """ Configure driver and its workflow. """
        super(Assembly, self).configure()
        ## Add some components
        self.add('omnivorRun', OmnivorRun())
        ## Add an optimizer: COBYLAdriver, CONMINdriver, NEWSUMTdriver, SLSQPdriver, Genetic
        self.add('driver', COBYLAdriver())         

        self.driver.workflow.add('omnivorRun')
        
        ## The parameters of the optimization
        self.driver.add_parameter('omnivorRun.x', low=0, high=5, start=0.1)
        self.driver.add_objective('omnivorRun.CP')
        self.driver.add_constraint('abs(omnivorRun.CT-0.6) <= 0.001')
        
        ## This recorder will create a list of cases
        self.driver.recorders = [ListCaseRecorder()]
        ## These variables will be recorded
        self.driver.printvars = ['omnivorRun.x','omnivorRun.CT','omnivorRun.CP']

        ## Some optimizer options
        self.driver.itmax = 100
        self.driver.fdch = 0.00001
        self.driver.fdchm = 0.000001
        self.driver.ctlmin = 0.001
        self.driver.delfun = 0.0001

if __name__ == "__main__":
    opti = OptiCirc()
    # optional here, replace optimizer: COBYLAdriver, CONMINdriver, NEWSUMTdriver, SLSQPdriver, Genetic
#     opti.replace('driver', COBYLAdriver())
#     opti.replace('driver', Genetic())
    opti.run()

    ## Transform the openmdao recorder into a pandas dataframe
    df = rec2df(opti.driver.recorders[0])
    figure()
    df.plot(x='omnivorRun.x',y='omnivorRun.CP', marker='x', color='k')
    df.plot(x='omnivorRun.x',y='omnivorRun.CT', marker='+', color='k')
    df[df['omnivorRun.CP']==df['omnivorRun.CP'].iget(-1)].plot(x='omnivorRun.x', y='omnivorRun.CP', marker='o', color='r')
    df[df['omnivorRun.CP']==df['omnivorRun.CP'].iget(-1)].plot(x='omnivorRun.x', y='omnivorRun.CT', marker='o', color='r')
    xlabel('x1'); ylabel('CP, CT')

    print('Max CP for constant CT constrained optimization:')
    print((df['omnivorRun.x'].iget(-1),df['omnivorRun.CP'].iget(-1), df['omnivorRun.CT'].iget(-1)))
    show()
#     savefig('rosenbrock_optimization.pdf')


