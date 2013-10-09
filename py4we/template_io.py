""" IO classes for YOUR_FILE_TYPE_NAME file types

Copyright (C) 2013 DTU Wind Energy

Author: YOUR_NAME
Email: YOUR_EMAIL
Last revision: DATE

License: Apache v2.0, http://www.apache.org/licenses/LICENSE-2.0
"""


class FileType(object):
    """ general IO classe for YOUR_FILE_TYPE_NAME file types """

    def __init__(self, filename=None):
        """ Initialized the classe using the filename

        Parameters:
        ----------
        filename : string
                   The file name to read and write
        """
        if filename:
            ### If there is a new filename, replace the object variable
            self.filename = filename

    def read(self, filename=None):
        """ Read the file 
        Parameters:
        ----------
        filename : string
                   The file name to read
        """
        if filename:
            ### If there is a new filename, replace the object variable
            self.filename = filename

        if self.filename:
            with open(self.filename, 'r') as f:
                data = f.read()
        else:  # If self.filename == None, raise an exception
            raise Exception('No filename has been provided')

        # HERE DO SOMETHING TO PREPARE THE DATA ##########################
        # Try to put the data into something called self.data ############
        self.data = data  # <- Replace this ##############################

    def write(self, filename=None):
        """ Write a file

        Parameters:
        ----------
        filename : string
                   The file name to write
        """
        if filename:
            # If there is a new filename, replace the object variable
            self.filename = filename

        if self.filename:
            with open(self.filename, 'w') as f:
                # HERE DO SOMETHING TO PREPARE THE DATA TO BE WRITTEN ####
                f.write(self.data)  # <- Replace this ####################
        else:
            # If self.filename == None, raise an exception
            raise Exception('No filename has been provided')



## Do Some testing -------------------------------------------------------
import unittest

class TestFileType(unittest.TestCase):
    """ Test class for FileType class """

    def test_duplication(self):
        """ Test if a file is written correctly by comparing with the data 
        of the original file
        """

        original_file = FileType('test_file.dat')
        original_file.read()
        original_file.write('new_file.dat')

        new_file = FileType('new_file.dat')
        new_file.read()

        ### Unit test function to check if two things are equal
        ##### MODIFY THIS IF NOT APPROPRIATE #############################
        self.assertEqual(original_file.data, new_file.data)

        ### ADD ADDITIONAL TEST TO SEE IF THE FILE HAS BEEN WRITTEN ######
        ### CORRECTLY ####################################################


if __name__ == '__main__':
    """ This is the main fuction that will run the tests automatically

    $> python template_io.py

    .
    ----------------------------------------------------------------------
    Ran X test in XXXs

    OK
    """
    unittest.main()


