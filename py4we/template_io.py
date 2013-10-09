""" IO classes for the DTU FileType class

Copyright (C) 2013 DTU Wind Energy

Author: Pierre-Elouan Rethore
Email: pire@dtu.dk
Last revision: 9/10/2013

License: Apache v2.0, http://www.apache.org/licenses/LICENSE-2.0
"""

class FileType(object):
    """Generic IO classe for file types classes."""

    def __init__(self, filename=None):
        """ Initialized the classe using the filename

        Parameters:
        ----------
        filename : string (optional)
                   The file name to read and write
        """
        if filename:
            ### If there is a new filename, replace the object variable
            self.filename = filename
            ### If the filename is provided, read the file 
            self.read()

    def _read(self, filename=None):
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
            with open(self.filename, 'r') as f:
                data = f.read()
                return data
        else:  # If self.filename == None, raise an exception
            raise Exception('No filename has been provided')

    def _write(self, data, filename=None):
        """ Write a file

        Parameters:
        ----------
        data : string
                   The data to be written
        filename : string (optional)
                   The file name to write
        """
        if filename:
            # If there is a new filename, replace the object variable
            self.filename = filename

        if self.filename:
            with open(self.filename, 'w') as f:
                f.write(data) 
        else:
            # If self.filename == None, raise an exception
            raise Exception('No filename has been provided')

    ### Public methods to be implemented in the subclasses --------------------
    def read(self, filename=None):
        """ Read the file 
        Parameters:
        ----------
        filename : string (optional)
                   The file name to read
        """
        ### You are going to replace this code when you inherit from this class
        raise NotImplementedError("This method must be implemented in subclass")

    def write(self, filename=None):
        """ Write a file

        Parameters:
        ----------
        filename : string (optional)
                   The file name to write
        """
        ### You are going to replace this code when you inherit from this class
        raise NotImplementedError("This method must be implemented in subclass")



## Do Some testing -------------------------------------------------------
import unittest

class TestFileType(unittest.TestCase):
    """ Test class for FileType class """

    def _test_duplication(self, klass, filename):
        """ Test if a file is written correctly by comparing with the data 
        of the original file
        """
        original_filename = filename
        new_filename = 'new_' + original_filename

        ### Open a new file
        original_file = klass(original_filename)
        ### write the file to a new filename
        original_file.write(new_filename)

        new_file = klass(new_filename)

        ### Unit test function to check if two things are equal
        self.assertEqual(original_file.data, new_file.data)

