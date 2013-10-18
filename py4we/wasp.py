""" IO classes for the DTU WAsP file types

Copyright (C) 2013 DTU Wind Energy

Authors: Pierre-Elouan Rethore
Email: pire@dtu.dk
Last revision: 18/10/2013

License: Apache v2.0, http://www.apache.org/licenses/LICENSE-2.0
"""

from we_file_io import WEFileIO, TestWEFileIO
from xml.dom.minidom import parseString
import xml.etree.cElementTree as ET
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement, dump
import unittest

from matplotlib import pylab as plt

import numpy as np

class WTG(WEFileIO):
    """WAsP Turbine File."""

    
    ### Private methods to be implemented in the subclasses --------------------
    def _read(self):
        """ Read the file."""
        xml = ET.parse(self.filename).getroot()
        self.xml = xml
        datapoint = lambda d: [float(d.get(i)) for i in ('WindSpeed', 'PowerOutput', 'ThrustCoEfficient')]

        a = np.array(list(map(datapoint, xml.findall('PerformanceTable/DataTable/DataPoint'))))
        ## Sorting with respect of wind speed
        self.data = a[np.argsort(a[:,0]),:]
        self.density = float(xml.find('PerformanceTable').get('AirDensity'))
        self.rotor_diameter = float(xml.get('RotorDiameter'))
        self.hub_height = xml.findall('SuggestedHeights/Height')[0].text
        self.manufacturer = xml.get('ManufacturerName')

    def _write(self):
        """ Write a file"""
        ### You are going to replace this code when you inherit from this class
        dtable = self.xml.find('PerformanceTable/DataTable')
        #remove the existing datapoints
        dtable.clear()
        for ws, p, ct in self.data:
            SubElement(dtable, 'DataPoint', WindSpeed=str(ws), PowerOutput=str(p), ThrustCoEfficient=str(ct))

        with open(self.filename, 'w' ) as f:
            f.write( '<?xml version="1.0"?>' )
            f.write( ElementTree.tostring( self.xml ) )

class POW(WEFileIO):
    """WAsP POW Turbine File."""

    
    ### Private methods to be implemented in the subclasses --------------------
    def _read(self):
        """ Read the file."""
        with open(self.filename, 'r') as f:
            lines = f.readlines()

        self.name = lines[0].split('\n')[0]
        self.hub_height = float(lines[1].split()[0])
        self.rotor_diameter = float(lines[1].split()[1])
        self.data = np.array([l.split()[:3] for l in lines[3:]], dtype='float32')
        factors = np.array(lines[2].split()[:2], dtype='float32')
        ### Multiplying by the factors to get the right units
        self.data[:,0:2] *= factors
        self.factors = factors

    def _write(self):
        # """ Write a file"""
        # ### You are going to replace this code when you inherit from this class
        with open(self.filename, 'w') as f:
            f.write(self.name + '\n')
            f.write('%f %f\n'%(self.hub_height, self.rotor_diameter))
            f.write('%f %f\n'%(self.factors[0], self.factors[1]))
            for i in range(self.data.shape[0]):
                f.write('%f %f %f\n'%(self.data[i,0] / self.factors[0], 
                                      self.data[i,1] / self.factors[1], 
                                      self.data[i,2]))

class WWF(WEFileIO):
    """WAsP Wind Farm Site."""

    ### Private methods to be implemented in the subclasses --------------------
    def _read(self):
        """ Read the file."""
        xml = ET.parse(self.filename).getroot()
        self.xml = xml
        SiteSummary = lambda d: (d.get('Label'),[float(d.get(i)) for i in ('XLocation', 'YLocation', 'HeightAGL', 'SiteElevation')])
        SectorData = lambda d: [float(d.get(i)) for i in ('CentreAngle', 'Frequency', 'WeibullA', 'Weibullk')]
        SectorWiseData = lambda d: (d.find('SiteSummary').get('Label'), 
                                    np.array(list(map(SectorData, d.findall('PredictedWindClimate/SectorWiseData/SectorData')))))

        self.data = dict(list(map(SiteSummary, xml.findall('TurbineSite/SiteSummary'))))
        self.windroses = dict(list(map(SectorWiseData, xml.findall('TurbineSite'))))
        self.pos = np.array([(d[0], d[1]) for d in self.data.values()])

    def _write(self):
        """ Write a file"""
        ### You are going to replace this code when you inherit from this class
        raise NotImplementedError("This method hasn't been implemented yet")

    def plot(self):
        """ Plot the position of the wind turbines """
        plt.plot(self.pos[:,0], self.pos[:,1] , '.')


        
## Do Some testing -------------------------------------------------------
class TestWAsP(TestWEFileIO):
    """ Test class for MyFileType class """

    test_wtg = 'test/wasp/bonus450.wtg'
    test_pow = 'test/wasp/bonus450.pow'
    test_wwf = 'test/wasp/hornsrev1.wwf'

    def test_WTG_duplication(self):
        self._test_duplication_array(WTG, self.test_wtg)

    def test_POW_duplication(self):
        self._test_duplication_array(POW, self.test_pow)

## Main function ---------------------------------------------------------
if __name__ == '__main__':
    """ This is the main fuction that will run the tests automatically

    $> python my_file_type.py

    ----- SOME_PRINT_STATEMENTS -----
    .
    ----------------------------------------------------------------------
    Ran X test in XXXs

    OK
    """
    unittest.main()