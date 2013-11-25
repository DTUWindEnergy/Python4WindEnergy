""" IO classes for Omnivor input file

Copyright (C) 2013 DTU Wind Energy

Author: Emmanuel Branlard
Email: ebra@dtu.dk
Last revision: 25/11/2013

Namelist IO: badis functions to read and parse a fortran file into python dictonary and write it back to a file 
The parser was adapted from: fortran-namelist on code.google with the following info:
                __author__ = 'Stephane Chamberland (stephane.chamberland@ec.gc.ca)'
                __version__ = '$Revision: 1.0 $'[11:-2]
                __date__ = '$Date: 2006/09/05 21:16:24 $'
                __copyright__ = 'Copyright (c) 2006 RPN'
                __license__ = 'LGPL'

Recognizes files of the form:
&namelistname
    opt1 = value1
    ...
/
"""

from __future__ import print_function
from we_file_io import WEFileIO, TestWEFileIO
import unittest

import numpy as np
import os.path as path

import sys
import re
import tempfile
import os

__author__ = 'E. Branlard '
class FortranNamelistIO(WEFileIO):
    """
    Fortran Namelist IO class
    Scan a Fortran Namelist file and put Section/Parameters into a dictionary
    Write the file back if needed.
    """
    def _write(self):
        """ Write a file (overrided)
        """
        with open(self.filename, 'w') as f:
            for nml in self.data :
                f.write('&'+nml+'\n')

                # Sorting dictionary data (in the same order as it was created, thanks to id)
                SortedList = sorted(self.data[nml].items(), key=lambda(k, v): v['id'])

#                 for param in self.data[nml]:
                for param in map(lambda(k,v):k,SortedList):
                    f.write(param+'='+','.join(self.data[nml][param]['val']))
                    if len(self.data[nml][param]['com']) >0:
                        f.write(' !'+self.data[nml][param]['com'])
                    f.write('\n')
                f.write('/\n')

    def _read(self):
        """ Read the file (overrided)
        """
        with open(self.filename, 'r') as f:
            data = f.read()

        varname   = r'\b[a-zA-Z][a-zA-Z0-9_]*\b'
        valueInt  = re.compile(r'[+-]?[0-9]+')
        valueReal = re.compile(r'[+-]?([0-9]+\.[0-9]*|[0-9]*\.[0-9]+)')
        valueNumber = re.compile(r'\b(([\+\-]?[0-9]+)?\.)?[0-9]*([eE][-+]?[0-9]+)?')
        valueBool = re.compile(r"(\.(true|false|t|f)\.)",re.I)
        valueTrue = re.compile(r"(\.(true|t)\.)",re.I)
        spaces = r'[\s\t]*'
        quote = re.compile(r"[\s\t]*[\'\"]")

        namelistname = re.compile(r"^[\s\t]*&(" + varname + r")[\s\t]*$")
        paramname = re.compile(r"[\s\t]*(" + varname+r')[\s\t]*=[\s\t]*')
        namlistend = re.compile(r"^" + spaces + r"/" + spaces + r"$")

        #split sections/namelists
        mynmlfile    = {}
        mynmlfileRaw = {}
        mynmlname  = ''
        for item in FortranNamelistIO.clean(data.split("\n"),cleancomma=1):
            if re.match(namelistname,item):
                mynmlname = re.sub(namelistname,r"\1",item)
                mynmlfile[mynmlname] = {}
                mynmlfileRaw[mynmlname] = []
            elif re.match(namlistend,item):
                mynmlname = ''
            else:
                if mynmlname:
                    mynmlfileRaw[mynmlname].append(item)

        #parse param in each section/namelist
        for mynmlname in mynmlfile.keys():
            #split strings
            bb = []
            for item in mynmlfileRaw[mynmlname]:
                if item[0]!='!':
                    # discarding lines that starts with a comment
                    bb.extend(FortranNamelistIO.splitstring(item))
            #split comma and =
            aa = []
            for item in bb:
                if not re.match(quote,item):
                    aa.extend(re.sub(r"[\s\t]*=",r" =\n",re.sub(r",+",r"\n",item)).split("\n"))
#                     aa.extend(re.sub(r"[\s\t]*=",r" =\n",item).split("\n"))
                else:
                    aa.append(item)
            del(bb)
            aa = FortranNamelistIO.clean(aa,cleancomma=1)

            myparname  = ''
            id_cum=0
            for item in aa:
                if re.search(paramname,item):
                    #myparname  = re.sub(paramname,r"\1",item).lower() ! NO MORE LOWER CASE
                    myparname  = re.sub(paramname,r"\1",item)
                    id_cum=id_cum+1
                    mynmlfile[mynmlname][myparname] = {
                    'val' : [],
                    'id' : id_cum,
                    'com' : ''
                    }
                elif paramname:
                    # Storing comments
                    item2=item.split('!')
                    item=item2[0]
                    if len(item) > 1 :
                        mynmlfile[mynmlname][myparname]['com']=''.join(item2[1:])
                    if re.match(valueBool,item):
                        if re.match(valueTrue,item):
                            mynmlfile[mynmlname][myparname]['val'].append('.true.')
                        else:
                            mynmlfile[mynmlname][myparname]['val'].append('.false.')
                    else:
#                         item2=re.sub(r"(^[\'\"]|[\'\"]$)",r"",item.strip())
                        mynmlfile[mynmlname][myparname]['val'].append(item.strip())
                self.data=mynmlfile


    # Accessor and mutator dictionary style
    def __getitem__(self, key):
        """ Transform the class instance into a dictionary."""
        return self.data[key]

    def __setitem__(self, key, value):
        """ Transform the class instance into a dictionary."""
        self.data[key] = value



    #==== Helper functions for Parsing of files
    @staticmethod
    def clean(mystringlist,commentexpr=r"^[\s\t]*\#.*$",spacemerge=0,cleancomma=0):
        """
        Remove leading and trailing blanks, comments/empty lines from a list of strings
        mystringlist = foo.clean(mystringlist,spacemerge=0,commentline=r"^[\s\t]*\#",cleancharlist="")
            commentline: definition of commentline
            spacemerge: if <>0, merge/collapse multi space
            cleancomma: Remove leading and trailing commas
        """
        aa = mystringlist
        if cleancomma:
            aa = [re.sub("(^([\s\t]*\,)+)|((\,[\s\t]*)+$)","",item).strip() for item in aa]
        if commentexpr:
            aa = [re.sub(commentexpr,"",item).strip() for item in aa]
        if spacemerge:
            aa = [re.sub("[\s\t]+"," ",item).strip() for item in aa if len(item.strip()) <> 0]
        else:
            aa = [item.strip() for item in aa if len(item.strip()) <> 0]
        return aa

    @staticmethod
    def splitstring(mystr):
        """
        Split a string in a list of strings at quote boundaries
            Input: String
            Output: list of strings
        """
        dquote=r'(^[^\"\']*)(\"[^"]*\")(.*)$'
        squote=r"(^[^\"\']*)(\'[^']*\')(.*$)"
        mystrarr = re.sub(dquote,r"\1\n\2\n\3",re.sub(squote,r"\1\n\2\n\3",mystr)).split("\n")
        #remove zerolenght items
        mystrarr = [item for item in mystrarr if len(item) <> 0]
        if len(mystrarr) > 1:
            mystrarr2 = []
            for item in mystrarr:
                mystrarr2.extend(FortranNamelistIO.splitstring(item))
            mystrarr = mystrarr2
        return mystrarr

## Do Some testing -------------------------------------------------------
class TestFortranNamelist(TestWEFileIO):
    """ Test class for MyFileType class """

    test_file = './test/fortran/fortran_namelist.nml'

    def test_output_identical(self):
        InputFile=FortranNamelistIO(self.test_file)
        test_fileout=tempfile.mkstemp()[1]
        InputFile.write(test_fileout)

        with open(self.test_file, 'r') as f:
            data_expected = f.read()

        with open(test_fileout, 'r') as f:
            data_read = f.read()
        try:
            self.assertMultiLineEqual(data_read, data_expected)
        finally:
            os.remove(test_fileout)


    def test_duplication(self):
        self._test_duplication(FortranNamelistIO, self.test_file)


## Main function ---------------------------------------------------------
if __name__ == '__main__':
    """ This is the main fuction that will run the tests automatically
    """
    unittest.main()
