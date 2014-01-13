""" IO classes for .ses Patran file types

Copyright (C) 2013 DTU Wind Energy

Author: Christian Pavese
Email: cpav@dtu.dk
Last revision: 13-01-2014

License: Apache v2.0, http://www.apache.org/licenses/LICENSE-2.0
"""


from __future__ import print_function
from we_file_io import WEFileIO#, TestWEFileIO
#import unittest



### Your class should look like this one ---------------------------------


class PLCtoSES(WEFileIO):
    """ This is a class to generate session input files for Patran. In this
    case, the file generated builds MPCs with RBE3 on selected sections of 
    a blade. Class takes in input the sections ID and coordinate of the MPC.

    methods:
    --------
        build_data_MPC : build the data set for the file
        write: write a file
        reade: read a file

    """
#####################################################################################
### build_data_MPC takes as input 4 lists:                                        ###
###                                                                               ###
### NSec                   : ID of the sections in which the MPCs will be located ###
### xCoord, yCoord, zCoord : Location of the MPCs elements                        ###
#####################################################################################
    
    def build_data_MPC(self, NS, x, y, z):
        data = """STRING fem_create_nodes__nodes_created[VIRTUAL]
        STRING uil_list_create_current_list[VIRTUAL]

        """

        for i in NS:
            MPCnode = 2000000 + i
            SolidList1 = str([1011.2 + i*1e3, 1012.2 + i*1e3, 1013.2 + i*1e3, 
                  1014.2 + i*1e3, 1015.2 + i*1e3, 1016.2 + i*1e3, 
                  1017.2 + i*1e3, 1032.2 + i*1e3, 1033.2 + i*1e3,
                  1034.2 + i*1e3, 1035.2 + i*1e3, 1036.2 + i*1e3, 
                  1037.2 + i*1e3, 1038.2 + i*1e3])
            SolidList1 = SolidList1.replace("[", "") 
            SolidList1 = SolidList1.replace("]", "") 
            SolidList1 = SolidList1.replace(",", "")
            SolidList2 = str([1050.2 + i*1e3, 1051.2 + i*1e3, 1052.2 + i*1e3, 
                  1053.2 + i*1e3, 1054.2 + i*1e3, 1055.2 + i*1e3, 
                  1056.2 + i*1e3, 1057.2 + i*1e3, 1058.2 + i*1e3, 
                  1059.2 + i*1e3])
            SolidList2 = SolidList2.replace("[", "") 
            SolidList2 = SolidList2.replace("]", "") 
            SolidList2 = SolidList2.replace(",", "")
                 
            data += "fem_create_nodes_1( \"Coord 0\", \"Coord 0\", 3, \"%i\", \" @\n" %MPCnode
            data += "[%8.04f, %8.04f, %8.04f] @\n" %(x[i], y[i], z[i])
            data += "\", fem_create_nodes__nodes_created )\n"
            data += "list_create_node_ass_geo( \"Solid %s @\n" %SolidList1
            data += "%s\", \"lista\", uil_list_create_current_list )\n" %SolidList2
            data += "fem_create_mpc_nodal2( %i, \"RBE3\", 0., 2, [TRUE, FALSE]," %i 
            data += "[\"0.\", \"1.0\"], [\"Node %i\", \"`lista`\"], [\"UX,UY,UZ,RX,RY,RZ\", \"UX,UY,UZ\"] )\n" %MPCnode
            data += "uil_list_a.clear(  )\n \n"
    
        self.data = data
    
    def _write(self):
        """ Write a file (overrided)
        """
        # HERE DO SOMETHING TO PREPARE THE DATA TO BE WRITTEN ############
        with open(self.filename, 'w') as f:
            f.write(self.data)


    def _read(self):
        """ Read the file (overrided)
        """
        with open(self.filename, 'r') as f:
            self.data = f.read()
        # HERE DO SOMETHING TO PREPARE THE DATA TO BE READ ############




### Do Some testing -------------------------------------------------------
#class TestMyDatFileIO(TestWEFileIO):
#    """ Test class for MyFileType class """
#
#    def test_duplication(self):
#        self._test_duplication(MyDatFileIO, './test/dat/test_file.dat')
#
#
### Main function ---------------------------------------------------------
#if __name__ == '__main__':
#    """ This is the main fuction that will run the tests automatically
#
#    $> python my_file_type.py
#    .
#    ----------------------------------------------------------------------
#    Ran X test in XXXs
#
#    OK
#    """
#    unittest.main()

filename = PLCtoSES('./test/Patran/MPC_All_Sections.ses')

NSec = [1, 2, 3, 4, 5, 6, 7]
xCoord = [0, 0, 0, 0, 0, 0, 0, 0]
yCoord = [0, 0, 0, 0, 0, 0, 0, 0]
zCoord = [0, 0, 0, 0, 0, 0, 0, 0]

filename.build_data_MPC(NSec, xCoord, yCoord, zCoord)
filename._write()