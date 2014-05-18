""" IO classes for the DTU FileType class

Copyright (C) 2013 DTU Wind Energy

Authors: Pierre-Elouan Rethore, Mads Moelgaard Pedersen
Email: pire@dtu.dk, mmpe@dtu.dk
Last revision: 9/10/2013

License: Apache v2.0, http://www.apache.org/licenses/LICENSE-2.0
"""

import numpy as np
import matplotlib.pyplot as plt
class WEFileIO(object):
    """Generic IO classe for file types classes."""
    figure = None
    def __init__(self, filename=None, file_type_name = "MyFileTypeName", file_extension="*"):
        """ Initialized the classe using the filename

        Parameters:
        ----------
        filename : string (optional)
                   The file name to read and write
        file_type_name : string (optional)
                   The name of the file type
        file_extension : string (optional)
                   The file name extension of the file type, e.g. "txt"
        """
        self.file_type_name = file_type_name
        self.file_extension = file_extension
        if filename:
            ### If there is a new filename, replace the object variable
            self.filename = filename
            ### If the filename is provided, read the file
            self.read()
         

    def read(self, filename=None):
        """ Read the file
        Parameters:
        ----------
        filename : string (optional)
                   The file name to read

        Returns:
        --------
        data : string
               the data read
        """
        if filename:
            ### If there is a new filename, replace the object variable
            self.filename = filename

        if self.filename:
            self._read()
            #return self.data
        else:  # If self.filename == None, raise an exception
            raise Exception('No filename has been provided')

    def write(self, filename=None):
        """ Write a file

        Parameters:
        ----------
        filename : string (optional)
                   The file name to write
        """

        if filename:
            # If there is a new filename, replace the instance variable
            self.filename = filename

        if self.filename:
            self._write()
        else:
            # If self.filename == None, raise an exception
            raise Exception('No filename has been provided')

    def plot(self, *args, **kwargs):
        if self.figure is None:
            self.figure = plt.figure()
        self._plot(self.figure, *args, **kwargs)
        plt.show()


    ### Private methods to be implemented in the subclasses --------------------
    def _read(self):
        """ Read the file."""
        ### You are going to replace this code when you inherit from this class
        raise NotImplementedError("This method must be implemented in subclass")

    def _write(self):
        """ Write a file"""
        ### You are going to replace this code when you inherit from this class
        raise NotImplementedError("This method must be implemented in subclass")

    def _plot(self, fig):
        """
        Plot your data
        :param matplotlib.figure: figure to plot on
        """
        ### You are going to replace this code when you inherit from this class
        raise NotImplementedError("This method must be implemented in subclass")



## Do Some testing -------------------------------------------------------
import unittest
import os

class TestWEFileIO(unittest.TestCase):
    """ Test class for FileType class """

    def _duplicate(self, class_, filename):
        original_filename = filename
        new_filename = original_filename + '_new'

        ### Open a new file
        original_file = class_(original_filename)
        ### write the file to a new filename
        original_file.write(new_filename)

        new_file = class_(new_filename)

        return original_file, new_file


    def _test_duplication(self, class_, filename):
        """ Test if a file is written correctly by comparing with the data
        of the original file
        """
        original_file, new_file = self._duplicate(class_, filename)
        ### Unit test function to check if two things are equal
        self.assertEqual(original_file.data, new_file.data)
        os.remove(new_file.filename)


    def _test_duplication_array(self, class_, filename):
        """ Test if a file is written correctly by comparing with the data
        of the original file
        """
        original_file, new_file = self._duplicate(class_, filename)

        ### Unit test function to check if two things are equal
        self.assertTrue(np.linalg.norm(original_file.data - new_file.data) < 1.0E-8)
        os.remove(new_file.filename)
