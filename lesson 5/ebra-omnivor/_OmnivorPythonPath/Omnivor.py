from __future__ import print_function
from ctypes import *
import numpy as np
from OmnivorTools  import *



# --------------------------------------------------------------------------------
# --- FAKE MATLAB  
# --------------------------------------------------------------------------------
true=True
false=False
end=[]

def disp(var):
    print(var)

def rethrow(var):
    raise(var)

def length(var):
    try: 
        l=var.size
    except Exception,err:
        l=1
    return(l)



def zeros(n1,n2=-1):
    import numpy as np
    if isinstance(n1,tuple):
        return np.zeros(n1)
    else:
        if n2==-1:
            return np.zeros((n1,n1))
        else:
            if n1==1 :
                return np.zeros((n2))
            else:
                return np.zeros((n1,n2))

def isequal(s1,s2):
    return s1==s2

def isa(var,vartype):
    if vartype=='char':
        return isinstance(var,str)
    elif vartype=='double':
        return isinstance(var,float) or isinstance(var,int)
    elif vartype=='logical':
        return isinstance(var,bool)
    else:
        print('TODO omnivor isa')
        return False

def blanks(n):
    return " "*n


from math import cos, sin, tan, acos, asin, atan, atan2, degrees, radians

def cosd(x):
  return cos(radians(x))

def sind(x):
  return sin(radians(x))

def tand(x):
  return tan(radians(x))

def acosd(x):
  return degrees(acos(x))

def asind(x):
  return degrees(asin(x))

def atand(x):
  return degrees(atan(x))

def atan2d(y, x):
  return degrees(atan2(y, x))





# --------------------------------------------------------------------------------
# --- OMNIVOR MAIN CLASS 
# --------------------------------------------------------------------------------
class Omnivor:
    raw=[]
    libname=''
    libdir=''
    libfile=''
    logfile=''
    STATUS=0
    bDEBUG=0
    bTHROW=0
    bLibLoaded=false
    bOmnivorInit=false
    bLibInit=false
    nWings=0

    Fields=[]
    iField=0

    Objects=[]
    iObject=0

    def __init__(self,libname='chipmunk'):
        self.bDEBUG=0;
        self.libname=libname;
        self.STATUS=1; 
        self.load()
    end

    def __del__(self):
        self.close()
    end

    ## function Omnivor.load
    def load(self):
        import os
        import glob
        # Getting environment variable
        self.libdir=os.getenv('OMNIVOR_LIB_DIR', './')
        self.libfile= (glob.glob(self.libdir+'lib'+self.libname+'[.][sd][ol].*'))[0]
#         self.libfile= (glob.glob(self.libdir+'lib'+self.libname+'[.][a]'))[0]
        # Loading library
        self.raw = cdll.LoadLibrary(self.libfile)
        self.bLibLoaded=true;

#         libHandle = ctypes.windll.kernel32.LoadLibraryA('mydll.dll')
#         lib = ctypes.WinDLL(None, handle=libHandle)
#         # Alternative:
#         lib = ctypes.cll(file)
#         libHandle = lib._handle
    end

    ## function Omnivor.check()
    def check(self):
        if self.raw==[]:
            return false
        else:
            if self.STATUS!=0:
                try: 
                    self.STATUS=self.raw.check()
                except Exception, err:
                    if self.bTHROW==1:
                        rethrow(err)
            end
            if self.STATUS==0:
                disp('Omnivor library in Error state!');
                self.close()
                if isequal(self.logfile,''): 
                    disp('Cannot print errors, logfile unknown');
                else:
                    disp('Listing of errors logged by library:');
                    try:
                        f=open(self.logfile)
                        import re
                        for line in f.readlines():
                            if re.match('Error',line) or re.match('Warning',line):
                                print('  >'+line.strip())
                    except Exception, err:
                        if self.bTHROW==1:
                            rethrow(err)

                return false
            else:
                return true
    end
    ## function Omnivor.error_solved()
    def error_solved(self):
        self.STATUS=1;
        self.raw.error_solved();
    end
    ## function Omnivor.term()
    def term(self):
        if self.bOmnivorInit:
            # Terminating Omnivor library
            if not isequal(self.libname, 'chipmunk'):
                self.call_nocheck('io_term');
            end
            self.bOmnivorInit=false;
    end

    ## function omnivor.close()
    def close(self):
        if self.bLibLoaded:
            # First terminating library layers
            self.term_layer()
            self.term()
            # Then attempting to unload the library
            self.bLibLoaded=false;
            del self.raw
            self.raw=[]
    end
    # --------------------------------------------------------------------------------
    # --- Library call
    # --------------------------------------------------------------------------------
    def call(self,func_name,*args):
        if self.check():
            try:
                func_call='self.raw.%s'%func_name
                if self.bDEBUG==1:
                    print(func_call)
#                 print(args)
                return eval(func_call)(*args)
            except Exception,err:
                if self.bTHROW==1:
                    rethrow(err)
            end
        end
    end

    def call_nocheck(self,func_name,*args):
        if self.raw==[]:
            return false
        else:
            try:
                func_call='self.raw.%s'%func_name
                if self.bDEBUG==1:
                    print(func_call)
                return eval(func_call)(*args)
            except Exception,err:
                if self.bTHROW==1:
                    rethrow(err)
            end
        end
    end

    def calladapt(self,func_name,*args):
        if self.check():
            try:
                if isequal(self.libname, 'raccoon'):
                    prefix='ir';
                elif isequal(self.libname, 'mouffette'):
                    prefix='im';
                else:
                    disp('unknown library name')
                    prefix='';
                end
                func_call='self.raw.%s_%s'%(prefix,func_name)
                if self.bDEBUG==1:
                    print(func_call)
                return eval(func_call)(*args)
            except Exception,err:
                self.close()
                if self.bTHROW==1:
                    rethrow(err)
            end
        end
    end

    def calladapt_nocheck(self,func_name,*args):
        if self.raw==[]:
            return false
        else:
            try:
                if isequal(self.libname, 'raccoon'):
                    prefix='ir';
                elif isequal(self.libname, 'mouffette'):
                    prefix='im';
                else:
                    disp('unknown library name')
                    prefix=''
                end
                func_call='self.raw.%s_%s'%(prefix,func_name)
                if self.bDEBUG==1:
                    print(func_call)
                return eval(func_call)(*args)
            except Exception,err:
                if self.bTHROW==1:
                    rethrow(err)
            end
        end
    end

    # --------------------------------------------------------------------------------
    # --- WRAPPED functions 
    # --------------------------------------------------------------------------------
    def init(self,file_or_folder='',bInputFile=false):
        # Initialization of Omnivor link library first
        if not isequal(self.libname, 'chipmunk'):
            if(bInputFile):
                self.STATUS=self.call('io_init_open',file_or_folder);
            else:
                self.STATUS=self.call('io_init',file_or_folder);
            end
            self.check();
        end
        self.bOmnivorInit=true;

        # Trigger init of specific library
#         self.init_lib();
        self.logfile=self.get_common_var('log_file');
    end

    def init_layer(self):
        # Initialization of specific layer
        if not isequal(self.libname, 'chipmunk'):
            self.STATUS=self.calladapt('init');
        end
        self.check();
        self.bLibInit=true;
    end


    ## function Omnivor.term_layer()
    def term_layer(self):
        if self.bLibInit:
            # Terminating Specific library layer
            if not isequal(self.libname, 'chipmunk'):
                self.calladapt_nocheck('term');
            end
            self.bLibInit=false;
        end
    end 



    def apply(self):
        self.STATUS=self.calladapt('apply');
        self.check();
    end



    def dotimeloop(self):
        self.calladapt('dotimeloop');
    end


    def dotimestep(self):
        self.calladapt('dotimestep');
    end

    def loadscalc(self):
        self.calladapt('loadscalc');
    end

    def gridvelocity(self):
        self.calladapt('gridvelocity');
    end


    def finalize1(self):
        self.calladapt('finalize1');
    end

    def finalize2(self):
        self.calladapt('finalize2');
    end

    def loadstate(self,statefile):
        import os
        if os.path.isfile(statefile):
            self.calladapt('loadstate',statefile);
        else:
            disp('ERROR, state file do not exist')
            self.STATUS=0;
        end
    end


    def savestate(self):
        self.calladapt('savestate');
    end

    def export(self,bForce=0):
        self.calladapt('export',to_c_intp(bForce));
    end
    # --------------------------------------------------------------------------------
    # --- Link functions 
    # --------------------------------------------------------------------------------
    def version(self):
        string='12345678';
        self.call('io_get_version',string);
        return(string)
    end

    def set_common_var(self,varname,value):
        if isa(value,'char'):
            # string variable
            self.call('io_set_svar',varname,value);
        elif isa(value,'double') or isa(value,'logical'):
            # number variable
            if value==1:
                value=TRUE
            elif value==0:
                value=FALSE
            else:
                value=to_cp(value)
            end
            self.call('io_set_var',varname,value);
        else:
            disp('type not handled by set_common_var:')
            self.STATUS=0;
        end
    end
    
    def get_common_var(self,varname):
        # string variable
        value=blanks(255);
        n=0;
        n_c=to_c_int(n);
        self.call('io_get_svar',varname,value,byref(n_c));
        n=c_to_py(n_c,n);
        return(value[0:n])
    end


    def set_freewind(self,U0):
        self.call('iw_setfreewind',to_cp(U0));
    end

    def get_freewind(self):
        U0=zeros(1,3);
        U0_c=to_c(U0);
        self.call('iw_getfreewind',U0_c);
        U0=c_to_py(U0_c,U0);
        return U0
    end


    def incrementtime(self):
        b=self.call('it_incrementtime');
        return (b==1)
    end

    def resettime(self):
        self.call('it_resettime');
    end


    # --------------------------------------------------------------------------------
    # --- User velocity field request functions
    # --------------------------------------------------------------------------------
    def set_user_vel_n(self,n):
        self.call('iv_user_vel_init',to_c_intp(n));
        self.iField=0;
    end

    def user_vel_add_from_v1v2v3(self,v1,v2,v3,bComputeGrad,bPolar):
        n1=length(v1);
        n2=length(v2);
        n3=length(v3);
        self.call('iv_user_vel_add_from_v1v2v3',to_cp(v1),to_cp(v2),to_cp(v3),to_c_boolp(bComputeGrad),to_c_boolp(bPolar),to_c_intp(n1),to_c_intp(n2),to_c_intp(n3));
        self.Fields.append({'ncps':n1*n2*n3,'stype':'grid'})
        self.iField=self.iField+1;
    end

    def user_vel_compute(self):
        self.call('iv_user_vel_compute');
    end

    def user_vel_export(self,filebase):
        self.call('iv_user_vel_export',filebase);
    end

    def user_vel_get(self,ifield):
        ncps=self.Fields[ifield-1]['ncps'];
        CPs     = zeros(3,ncps) ; 
        Utot    = zeros(3,ncps) ; 
        U_bound = zeros(3,ncps) ; 
        U0      = zeros(3,ncps) ; 
        Grad    = zeros(9,ncps) ; 
        # intent inout variables
        CPs_c     = to_c(CPs);
        Utot_c    = to_c(Utot);
        U0_c      = to_c(U0);
        U_bound_c = to_c(U_bound);
        Grad_c    = to_c(Grad);
        self.call('iv_user_vel_get',to_c_intp(ifield),to_c_intp(ncps),byref(CPs_c),byref(Utot_c),byref(Grad_c),byref(U0_c),byref(U_bound_c));
        Utot    = c_to_py(Utot_c,Utot);
        U_bound = c_to_py(U_bound_c,U_bound);
        U0      = c_to_py(U0_c,U0);
        Grad    = c_to_py(Grad_c,Grad);
        CPs     = c_to_py(CPs_c,CPs);
        return (Utot,Grad,CPs,U0,U_bound)
    end


    # --------------------------------------------------------------------------------
    # --- Mouffette functions 
    # --------------------------------------------------------------------------------
    def set_algo(self,varname,value):
        if isa(value,'char'):
            # string variable
            disp('type not handled by set_algo: str/char')
            self.STATUS=0;
        elif isa(value,'double') and length(value)==1 :
            # number variable
            self.call('im_set_algo_var',varname,to_cp(value));
        else:
            disp('type not handled by set_algo:')
            self.STATUS=0;
        end
        self.check();
    end

    def prescribe_wing(self,iw,sref,gamma_ref):
        n=length(sref);
        self.call('im_wing_set_gamma',to_c_intp(iw),to_c_intp(n),to_cp(sref),to_cp(gamma_ref))
    end

    def get_panl_loads(self,ncp):
        Cp = zeros(1,ncp);
        Ft = zeros(3,ncp);
        U0 = zeros(3,ncp);
        Ut = zeros(3,ncp);
        CP = zeros(3,ncp);
        It = zeros(1,ncp);
        Cp_c=to_c(Cp);
        Ft_c=to_c(Ft);
        U0_c=to_c(U0);
        Ut_c=to_c(Ut);
        CP_c=to_c(CP);
        It_c=to_c(It);
        self.call('im_get_panl_loads',to_c_intp(ncp),byref(Cp_c),byref(Ft_c),byref(U0_c),byref(Ut_c),byref(CP_c),byref(It_c));
        Cp = c_to_py(Cp_c,Cp);
        Ft = c_to_py(Ft_c,Ft);
        U0 = c_to_py(U0_c,U0);
        Ut = c_to_py(Ut_c,Ut);
        CP = c_to_py(CP_c,CP);
        It = c_to_py(It_c,It);
        return (Cp,Ft,U0,Ut,CP,It)
    end
    # --------------------------------------------------------------------------------
    # --- Raccoon functions 
    # --------------------------------------------------------------------------------
    def set_nbodies(self,nb,nw):
        self.call('ir_set_nbodies',to_c_intp(nb),to_c_intp(nw));
        self.nWings=nw;
    end

    def new_obj(self,objname):
        self.call('ir_new_obj',objname);
    end

    def add_obj(self):
        self.call('ir_add_obj');
    end

    def set_obj(self,varname,value):
        if isa(value,'char'):
            # string variable
            self.call('ir_set_obj_str',varname,value)
        elif isa(value,'double') and length(value)==1 :
            # number variable
            self.call('ir_set_obj_var',varname,to_cp(value))
        else:
            disp('type not handled by set_obj %s:'%type(value))
            self.STATUS=0;
        end
        self.check();
    end

    def set_obj_file(self,filename,filetype,delimiter='',nlines_header=0):
        nlines=nlines_header;
        self.call('ir_set_obj_file',filename,filetype,delimiter,to_c_intp(nlines));
    end

    def set_obj_vel(self,TranslatVel,RotVect,RotCenter,RotVel,RotPhase):
        self.call('ir_set_obj_vel',to_cp(TranslatVel),to_cp(RotVect),to_cp(RotCenter),to_cp(RotVel),to_cp(RotPhase))
    end

    def set_obj_pos(self,ShiftVect,RotMatrix=0):
        if(isinstance(RotMatrix,int)): 
            RotMatrix=np.eye(3);
        to_cp(ShiftVect)
        to_cp(RotMatrix)
        self.call('ir_set_obj_pos',to_cp(ShiftVect),to_cp(RotMatrix))
    end

    # --------------------------------------------------------------------------------
    # --- Chipmunk functions 
    # --------------------------------------------------------------------------------
    def ui_particle(self,CPs,Part,Omegas,SmoothModel,SmoothParam,bComputeGrad):
        nPart=Part.shape[1]
        ncp=CPs.shape[1]
        UI   = zeros(3,ncp)
        Grad = zeros(9,ncp)
        UI_c = to_c(UI)
        G_c  = to_c(Grad)
        self.call('ui_particle',byref(UI_c),byref(G_c),to_cp(CPs),to_cp(Part),to_cp(Omegas),to_c_intp(SmoothModel),to_cp(SmoothParam),to_c_boolp(bComputeGrad),to_c_intp(ncp),to_c_intp(nPart))
        UI   = c_to_py(UI_c,UI)
        Grad = c_to_py(G_c,Grad)

        return (UI,Grad)
    end

    def ui_continuousline(self,CPs,SgmtP,Intensities,SmoothModel,SmoothParam,bComputeGrad):
        nSgmt=SgmtP.shape[1]-1
        ncp=CPs.shape[1]
        UI   = zeros(3,ncp);
        Grad = zeros(9,ncp);
        UI_c = to_c(UI)
        G_c  = to_c(Grad)
        self.call('ui_continuousline',byref(UI_c),byref(G_c),to_cp(CPs),to_cp(SgmtP),to_cp(Intensities),to_c_intp(SmoothModel),to_cp(SmoothParam),to_c_boolp(bComputeGrad),to_c_intp(ncp),to_c_intp(nSgmt))
        UI   = c_to_py(UI_c,UI)
        Grad = c_to_py(G_c,Grad)

        return (UI,Grad)
    end

    def ui_pointsource(self,CPs,SrcP,Omegas,SmoothModel,SmoothParam,bComputeGrad):
        nSrc=SrcP.shape[1]
        ncp=CPs.shape[1]
        UI   = zeros(3,ncp);
        Grad = zeros(9,ncp);
        UI_c = to_c(UI)
        G_c  = to_c(Grad)
        self.call('ui_pointsource',byref(UI_c),byref(G_c),to_cp(CPs),to_cp(SrcP),to_cp(Omegas),to_c_intp(SmoothModel),to_cp(SmoothParam),to_c_boolp(bComputeGrad),to_c_intp(ncp),to_c_intp(nSrc))
        UI   = c_to_py(UI_c,UI)
        Grad = c_to_py(G_c,Grad)

        return (UI,Grad)
    end

    def ui_quaddoubletcst(self,P1,P2,P3,P4,CPs,Gamma,SmoothModel,SmoothParam,bComputeGrad):
        ncp=CPs.shape[1]
        UI   = zeros(3,ncp)
        Grad = zeros(9,ncp)
        UI_c=to_c(UI)
        G_c=to_c(Grad)
        self.call('ui_quaddoubletcst_1n',byref(UI_c),byref(G_c),to_cp(P1),to_cp(P2),to_cp(P3),to_cp(P4),to_cp(CPs),to_cp(Gamma),to_c_intp(SmoothModel),to_cp(SmoothParam),to_c_boolp(bComputeGrad),to_c_intp(ncp))
        UI   = c_to_py(UI_c,UI)
        Grad = c_to_py(G_c,Grad)

        return (UI,Grad)
    end

    def ui_quadsourceplanecst(self,CPs,Sigmas,xi,eta,CentroidRef, TransfoMat,Viscous,bComputeGrad):
        ncp=CPs.shape[1]
        np=xi.shape[1]
        UI   = zeros(3,ncp);
        Grad = zeros(9,ncp);
        UI_c = to_c(UI)
        G_c  = to_c(Grad)
        self.call('ui_quadsourceplanecst',byref(UI_c),byref(G_c),to_cp(CPs),to_cp(Sigmas),to_cp(xi),to_cp(eta),to_cp(CentroidRef),to_cp(TransfoMat),to_cp(Viscous),to_c_boolp(bComputeGrad),to_c_intp(ncp),to_c_intp(np))
        UI   = c_to_py(UI_c,UI)
        Grad = c_to_py(G_c,Grad)

        return (UI,Grad)
    end
    # --------------------------------------------------------------------------------
    # --- Tools
    # --------------------------------------------------------------------------------
    def get_wing_loads(self,nr,svar='',svec=''):
        # TODO
        if svar=='' and svec=='':
            iw=1
            scp    = zeros(1,nr);
            alpha  = zeros(1,nr);
            alpha0 = zeros(1,nr);
            gamma  = zeros(1,nr);

            Vrel  = zeros(3,nr);
            V0    = zeros(3,nr);
            Vbody = zeros(3,nr);

            scp_c    = to_c(scp   );
            alpha_c  = to_c(alpha );
            alpha0_c = to_c(alpha0);
            gamma_c  = to_c(gamma );
            Vrel_c   = to_c(Vrel  );
            V0_c     = to_c(V0    );
            Vbody_c  = to_c(Vbody );

            self.call('im_get_wing_var',byref(scp_c),'scp_ll',to_c_intp(iw),to_c_intp(nr))
            self.call('im_get_wing_var',byref(alpha_c),'alpha_ll',to_c_intp(iw),to_c_intp(nr))
            self.call('im_get_wing_var',byref(alpha0_c),'alpha0_ll',to_c_intp(iw),to_c_intp(nr))
            self.call('im_get_wing_var',byref(gamma_c),'Gamma_ll',to_c_intp(iw),to_c_intp(nr))

            self.call('im_get_wing_vec',byref(Vrel_c),'Vrel_ll',to_c_intp(iw),to_c_intp(nr))
            self.call('im_get_wing_vec',byref(V0_c),'V0_ll',to_c_intp(iw),to_c_intp(nr))
            self.call('im_get_wing_vec',byref(Vbody_c),'Vbody_ll',to_c_intp(iw),to_c_intp(nr))

            scp    = c_to_py(scp_c,scp)
            alpha  = c_to_py(alpha_c,alpha)
            alpha0 = c_to_py(alpha0_c,alpha0)
            gamma  = c_to_py(gamma_c,gamma)
            Vrel  = c_to_py(Vrel_c,Vrel)
            V0    = c_to_py(V0_c,V0)
            Vbody = c_to_py(Vbody_c,Vbody)

            return (scp,alpha,gamma,alpha0,Vrel,V0,Vbody)
        if svar!='':
            iw=1
            if svar=='s':
                nr=nr+1
            var  = zeros(1,nr);
            var_c  = to_c(var)
            self.call('im_get_wing_var',byref(var_c),svar,to_c_intp(iw),to_c_intp(nr))
            var    = c_to_py(var_c,var)
            return(var)
        if svec!='':
            iw=1
            var  = zeros(3,nr);
            var_c  = to_c(var)
            self.call('im_get_wing_vec',byref(var_c),svec,to_c_intp(iw),to_c_intp(nr))
            var    = c_to_py(var_c,var)
            return(var)

    end








# if __name__ == "__main__":
#     import sys
#     print 'called with: ', int(sys.argv[1])
