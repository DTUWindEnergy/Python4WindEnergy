# write function maxima above to file 'maxima.py'
# compile, import and run

import inspect
import os
import sys
import cython
from PrintTime import print_time

def test_func(funcs,args):
    func_name = funcs[0].func_name
    with open('cy_%s.py'%func_name,'w') as f:
        f.write("import numpy as np\n#cimport numpy as np\nimport cython\n")
        for func in funcs:
            f.write(inspect.getsource(func))
    for ext in ['pyd','so']:
        filename = 'cy_%s.%s' % (func_name, ext)
        if os.path.isfile(filename):
           try: 
               os.remove(filename)
           except:
               print "Restart kernel in order to replace library"

    from cython_import import cython_import
    cython_import('cy_%s' % func_name)
    
    print "cy_%s"%func_name
    
    @print_time
    def python_func(*args,**kwargs):
        funcs[0](*args,**kwargs)

    @print_time
    def cython_func(*args, **kwargs):
        module = __import__("cy_%s"%func_name)
        f = getattr(module, func_name)
        f(*args,**kwargs)
    
    
    python_func(*args)
    cython_func(*args)