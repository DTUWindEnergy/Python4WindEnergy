'''
Created on 28/02/2013

@author: mmpe
'''
import inspect
import os
import shutil
import subprocess
import sys

"""
Functions for compiling and importing a Python module
syntax:

from cython_import import cython_import

cython_import("cycheck")
from cycheck import * #import after compilation
cycheck(xxx)


Types of variables can be declared in the module via 'pure' http://docs.cython.org/src/tutorial/pure.html
import cython

@cython.ccall
@cython.locals(n=cython.int)
@cython.returns(cython.int)
def foo(n):
    return n

or 
'#cdef int x'    '#' allows normal python execution and is automatically removed by script


A function that takes a numpy array as input and output can be declared using:

#cimport numpy as np
def foo(inp): #cpdef np.ndarray[int,ndim=1] foo(np.ndarray[int,ndim=1] inp):
  
"""

            

def cython_import(module,compiler=None):
    exec("import %s"%module)
    pyd_module = module
    if not is_compiled(eval(pyd_module)):
        
        #Generate pyx file
        file_path = module.replace(".", "/") + ".py"
        fid = open(file_path)
        pylines = fid.readlines()
        fid.close
        
        fid = open(file_path.replace('.py','.pyx'),'w')
        pyxlines = py2pyx(pylines)
        fid.writelines(pyxlines)
        fid.close()
        
        #Generate setup.py script
        fid=open('setup.py','w')
        setup_str = """from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy

ext_modules = [Extension("%s", ["%s"], include_dirs = [numpy.get_include()])]

setup(
  name = 'name',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)"""%(module,file_path.replace('.py','.pyx'))
        fid.write(setup_str)
        fid.close()
        
        #compile
        if compiler is not None:
            compiler_str = "--compiler=%s"%compiler
        else:
#            if "mingw" in os.environ['path'].lower():
#                compiler_str = "--compiler=mingw32"
#            else:
#                compiler_str = ""
            
            
            if os.name == 'nt' and "mingw" in os.environ['path'].lower():
                    compiler_str = "--compiler=mingw32"
            else:
                compiler_str = ""
            
        bin_python = os.path.basename(sys.executable)
        cmd = "%s setup.py build_ext --inplace %s" % (bin_python, compiler_str)
        print "compiling %s: %s"%(module, cmd)
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                                stderr=subprocess.STDOUT, shell=True)
        (out, err) = proc.communicate()        
#        os.system(cmd)
        
        #Reload and check that module is compiled
        reload(eval(module))
        if not is_compiled(eval(pyd_module)):
            line = '\n'+'='*79+'\n'
            sys.stderr.write("%s was not compiled correctly. It may result in slower execution" % pyd_module)
            sys.stderr.write('%sstdout:%s%s' % (line, line, out))
            sys.stderr.write('%sstderr:%s%s' % (line, line, err))
            
        else:
            print "Compiling succeeded"
        
        
        #Clean up. Remove temporary files and folders
        if os.path.isdir("build"):
            shutil.rmtree("build")
        for f in ['setup.py',file_path.replace(".py",'.c'),file_path.replace(".py",'.pyx')]:
            if os.path.isfile(f):
                os.remove(f)
                pass

def py2pyx(pylines):
    pyxlines = []
    for i in xrange(len(pylines)):
        
        l = pylines[i]
        if "#c " in l:
            indent = l[:len(l) - len(l.lstrip())]
            cdef = l[l.index("#c ")+3:]
            l = indent + cdef

        if "#c" in l:
            indent = l[:len(l) - len(l.lstrip())]
            cdef = l[l.index("#c")+1:]
            l = indent + cdef
        pyxlines.append(l)
    return pyxlines   


def is_compiled(module):
    return module.__file__.lower()[-4:]==".pyd" or module.__file__.lower()[-3:]==".so" 
