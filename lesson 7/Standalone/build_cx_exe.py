'''
Created on 21/01/2013

@author: Mads
'''
from __future__ import division, absolute_import, unicode_literals
try: range = xrange; xrange = None
except NameError: pass
try: str = unicode; unicode = None
except NameError: pass
import numpy as np
import glob
import os
import shutil
import sys
import time
import zipfile
#from functions.io import make_dirs, make_packages
NUMPY = 'numpy'
MATPLOTLIB = 'matplotlib'
GUIDATA = 'guidata'
PYQT4 = 'PyQt4'
PYSIDE = 'PySide'
SCIPY = 'scipy'
CTYPES = '_ctypes'
MULTIPROCESSING = '_multiprocessing'
DOCX = "docx"
OPENGL = "_opengl"
PIL = "PIL"
HDF5 = "h5py"
PANDAS = 'pandas'

def build_exe(filename, version="1.0.0", description="", author="", modules=[NUMPY], includes=[], packages="[]", include_files=[], icon=None):
    basename = filename.replace('.py', '')
    folder = '%s_dist/' % basename
    prepare(modules)
    write_setup(basename, version, description, author, modules, includes, packages, include_files, icon)

    if os.path.isdir(folder):
        shutil.rmtree(folder)
    os.system('%s setup.py build' % sys.executable)
    shutil.move('./build/', folder)
    os.remove('setup.py')
    clean(modules)

    print ("distribution created (%s/)" % folder)

def build_msi(filename, version, description="", author=""):
    basename = filename.replace('.py', '')
    folder = '%s_dist/' % basename
    if os.path.exists(folder):
        shutil.rmtree(folder)
    write_setup(basename, version, description, author)
    os.system('python setup.py bdist_msi')

    shutil.move('./dist/', '%s/' % folder)

    os.remove('setup.py')
    shutil.rmtree('build')
    shutil.rmtree('dist')

    print ("Installer created (%s/)" % (folder))


def write_setup(name, version, description="", author="", modules=[NUMPY], includes=[], packages="[]", include_files=[], icon=None):
    """['appfuncs','gui_test']"""
    """["graphics/", "imageformats/", ]"""
    """"includes":["sip"],"""
    imports = []
    base = ""
    excludes = ['PyQt4.uic.port_v3', 'Tkconstants', 'tcl', 'tk', 'doctest', '_gtkagg', '_tkagg', 'bsddb',
                'curses', 'email', 'pywin.debugger', 'pywin.debugger.dbgcon', 'pywin.dialogs', 'Tkinter',
                'tables', 'zmq', 'win32', 'Pythonwin', 'Cython', 'statmodels', 'cvxopt', '_sqlite3', '_ssl', '_testcapi',
                'markupsafe', 'numexpr', '_elementtree', '_hashlib', '_testcapi', 'bz2', 'simplejson', 'pyexpat', "lxml",
                MATPLOTLIB, GUIDATA, PYQT4, PYSIDE, SCIPY, NUMPY, MULTIPROCESSING, CTYPES, DOCX, OPENGL, PIL, HDF5]
    #'pandas', '_socket', 'sip',
    if MATPLOTLIB in modules:
        include_files.append("""(matplotlib.get_data_path(),"mpl-data")""")
        imports.append("import matplotlib")
        excludes.remove('email')  #py3_64
        excludes.remove(CTYPES)

    if GUIDATA in modules:
        include_files.append("guidata/images/")
    if PYQT4 in modules:
        include_files.append("imageformats/")
        includes.append("sip")
        base = "base='Win32GUI', "
    if SCIPY in modules:
        imports.append("import scipy.sparse.csgraph")
        includes.extend(["scipy.sparse.csgraph._validation", "scipy.sparse.linalg.dsolve.umfpack",
        "scipy.integrate.vode", "scipy.integrate._ode", "scipy.integrate.lsoda"])
        includes.append("scipy.special._ufuncs_cxx")  #py3_64
        from scipy.sparse.sparsetools import csr, csc, coo, dia, bsr, csgraph

        for f in [csr._csr.__file__,
                  csc._csc.__file__,
                  coo._coo.__file__,
                  dia._dia.__file__,
                  bsr._bsr.__file__,
                  csgraph._csgraph.__file__]:
            shutil.copy(f, os.path.basename(f))
            include_files.append("%s" % os.path.basename(f))

    if DOCX in modules:
        include_files.append("functions/docx_document/docx-template_clean/")
        include_files.append("functions/docx_document/inkscape/")
        includes.append("lxml._elementpath")
        excludes.remove("lxml")
        excludes.remove(PIL)

    if OPENGL in modules:
        includes.append("OpenGL")
        includes.append("OpenGL.platform.win32")
        includes.append("OpenGL.arrays.numpymodule")
        includes.append("OpenGL.arrays.arraydatatype")
        includes.append("OpenGL.converters")
        includes.append("OpenGL.arrays.numbers")
        includes.append("OpenGL.arrays.strings")


    if HDF5 in modules:
        #from h5py import _conv, _errors, _objects, _proxy, defs, h5, h5a, h5d, h5ds, h5f, h5fd, h5g, h5i, h5l, h5o, h5p, h5r, h5s, h5t, h5z, utils
        #for f in [_conv, _errors, _objects, _proxy, defs, h5, h5a, h5d, h5ds, h5f, h5fd, h5g, h5i, h5l, h5o, h5p, h5r, h5s, h5t, h5z, utils]:
        #    f = f.__file__
        #    shutil.copy(f, "h5py." + os.path.basename(f))
        #    include_files.append("'h5py.%s'" % os.path.basename(f))
        #import h5py
        #for f in [f for f in os.listdir(os.path.dirname(h5py.__file__)) if f.endswith(".pyd")]:
        #    shutil.copy2(os.path.join(os.listdir(os.path.dirname(h5py.__file__)), "h5py.%s"%f)
        #shutil.rmtree("h5py", ignore_errors=True)
        #shutil.copytree(os.path.dirname(h5py.__file__), "h5py")
        #include_files.append("'h5py/'")

        #includes.extend(["'h5py.defs'", "'h5py.utils'", "'h5py._proxy'"])
        pass


    for m in modules:
        try:
            excludes.remove(m)
        except ValueError:
            pass




    imports = "\n".join(imports)
    if include_files:
        include_files = "['" + "','".join(include_files) + "']"
        include_files = include_files.replace("""'(matplotlib.get_data_path(),"mpl-data")'""", """(matplotlib.get_data_path(), "mpl-data")""")
    if includes:
        includes = "['" + "','".join(includes) + "']"

    if icon is not None:
        icon = "icon='%s', " % icon
    else:
        icon = ""

    with open('setup.py', 'w') as fid:
        fid.writelines("""from cx_Freeze import setup, Executable
%s

build_exe_options = {
"includes": %s,
"packages": %s,
'excludes' : %s,

"include_files": %s}

setup(
name = "%s",
version="%s",
description="%s",
author = "%s",
options = { "build_exe": build_exe_options},
executables = [Executable("%s.py", %s%sshortcutName="%s", shortcutDir="DesktopFolder")])
    """ % (imports, includes, packages, excludes, include_files, name, version, description, author, name, base, icon, name))


def prepare(modules):
    clean(modules)
    if GUIDATA in modules:
        if not os.path.isdir("guidata"):
            os.mkdir("guidata/")
        if not os.path.isdir("guidata/images/"):
            shutil.copytree(r"%s/Lib/site-packages/guidata/images/" % os.path.dirname(sys.executable), "guidata/images/")
    if PYQT4 in modules:
        copy_imageformats()
    if DOCX in modules:
        from functions.docx_document import docx_document
        source_path = os.path.dirname(docx_document.__file__)
        dest_path = "functions/docx_document/"
        make_dirs(dest_path)
        for folder in ['docx-template_clean', 'inkscape']:
            shutil.copytree(os.path.join(source_path, folder), os.path.join(dest_path, folder))



def clean(modules):
    if modules and GUIDATA in modules:
        if os.path.isdir("guidata"):
            shutil.rmtree("guidata/")
    if modules and PYQT4 in modules:
        if os.path.isdir('imageformats'):
            shutil.rmtree('imageformats/')
    if modules and DOCX in modules:
        if os.path.isdir('functions'):
            shutil.rmtree('functions')
    if modules and SCIPY in modules:
        from scipy.sparse.sparsetools import csr, csc, coo, dia, bsr, csgraph
        for f in [csr._csr.__file__,
                  csc._csc.__file__,
                  coo._coo.__file__,
                  dia._dia.__file__,
                  bsr._bsr.__file__,
                  csgraph._csgraph.__file__]:
            if os.path.isfile(os.path.basename(f)):
                os.remove(os.path.basename(f))
    if modules and HDF5 in modules:
        #from h5py import _conv, _errors, _objects, _proxy, defs, h5, h5a, h5d, h5ds, h5f, h5fd, h5g, h5i, h5l, h5o, h5p, h5r, h5s, h5t, h5z, utils
        #for f in [_conv, _errors, _objects, _proxy, defs, h5, h5a, h5d, h5ds, h5f, h5fd, h5g, h5i, h5l, h5o, h5p, h5r, h5s, h5t, h5z, utils]:
        #    f = f.__file__
        #    shutil.copy(f, "h5py." + os.path.basename(f))
        #    include_files.append("'h5py.%s'" % os.path.basename(f))
        shutil.rmtree("h5py/", ignore_errors=True)



def copy_imageformats():
    """
    Run this function if icons are not loaded
    """
    from PyQt4 import QtCore
    import sys
    app = QtCore.QCoreApplication(sys.argv)
    qt_library_path = QtCore.QCoreApplication.libraryPaths()


    imageformats_path = None
    for path in qt_library_path:
        if os.path.exists(os.path.join(str(path), 'imageformats')):
            imageformats_path = os.path.join(str(path), 'imageformats')
            local_imageformats_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'imageformats')
            local_imageformats_path = os.path.join(os.getcwd(), 'imageformats')
            if not os.path.exists(local_imageformats_path):
                os.mkdir(local_imageformats_path)
            for file in glob.glob(os.path.join(imageformats_path, '*')):
                shutil.copy(file, os.path.join(local_imageformats_path, os.path.basename(file)))

