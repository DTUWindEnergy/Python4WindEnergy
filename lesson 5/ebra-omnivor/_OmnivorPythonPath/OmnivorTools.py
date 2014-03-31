from ctypes import *

TRUE=byref(c_double(1))
FALSE=byref(c_double(0))

def c_to_py(var_c, var):
    import numpy as np
    if isinstance(var,np.ndarray):
        if var.ndim ==1:
            n=var.shape[0]
            tmp=np.zeros((n))
            tmp[0:n]=var_c[0:n]
            var=tmp
        elif var.ndim==2:
            (n,m)=var.shape
            tmp=np.zeros((n*m,))
            tmp[0:(n*m)]=var_c[0:(n*m)]
            var=tmp.reshape(n,m,order='F')
        else:
            print 'Error numpy aray of dim3'
            var=-1
    elif isinstance(var,int):
        var=int(var_c.value)
    else:
        print 'Error Omnivort tools TODO'+str(type(var))
        pass

    return var

def to_cp(var):
    return byref(to_c(var))
def to_c_intp(var):
    return byref(to_c_int(var))
def to_c_boolp(var):
    return byref(to_c_bool(var))

def to_c(var):
    import numpy as np
    if isinstance(var,np.ndarray):
        if var.ndim ==1:
            n=var.shape[0]
            var_c=(c_double*n)(0)
            var_c[0:n]=var[0:n]
        elif var.ndim==2:
            (n,m)=var.shape
            var_c=(c_double*(n*m))(0)
            var_c[0:(n*m)]=var.flatten(1)[0:(n*m)]
        elif var.ndim==3:
            (n,m,p)=var.shape
            var_c=(c_double*(n*m*p))(0)
            var_c[0:(n*m*p)]=var.flatten(1)[0:(n*m*p)]
        else:
            print 'ERROR numpy of dim4'
            var_c=c_int(2)
    elif isinstance(var,list):
        n=len(var)
        var_c=(c_double*n)(0)
        var_c[0:n]=var[0:n]
    else:
        #print 'type is:',type(var)
        var_c=c_double(var)
    return var_c

def to_c_int(var):
    try:
        n=len(var)
        var_c=(c_int*n)(0)
        var_c[0:n]=var[0:n]
    except TypeError:
        var_c=c_int(var)
    return var_c

def to_c_bool(var):
    if isinstance(var,bool):
        if var:
            var_c=c_int(1)
        else:
            var_c=c_int(0)
    else:
        if var==1:
            var_c=c_int(1)
        else:
            var_c=c_int(0)
    return var_c
