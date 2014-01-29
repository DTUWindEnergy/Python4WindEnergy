""" IO classes for the DTU WAsP file types

Copyright (C) 2013 DTU Wind Energy

Authors: Pierre-Elouan Rethore
Email: pire@dtu.dk
Last revision: 31/10/2013

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


#### Semi private classes --------------------------------------------------------------------------
datapoint = lambda d: [float(d.get(i)) for i in ('WindSpeed', 'PowerOutput', 'ThrustCoEfficient')]

def generate_vl(arr_):
    """Iterator for populating a list of VectLines"""
    n1 = 0
    while n1 < len(arr_):
        vl = VectLine(arr_[n1:])
        n1 += vl.n_end
        yield vl

class VectLine(object):
    """Contains a list of points and their respective height"""
    def __init__(self, arr_):
        self.h = arr_[0]
        self.n = int(arr_[1])
        self.n_end = 2+2*self.n
        self.points = arr_[2:self.n_end].reshape([-1,2])
        
    def plot(self, scale=1000.0, colmap=plt.cm.jet, **kwargs):
        """Plot the vectorline"""
        plt.plot(self.points[:,0], self.points[:,1], color=colmap(self.h/scale), **kwargs)
        
    def add_to_wasp(self, wasp_core):
        """Add the vectorline to the wasp core"""
        wasp_core.addorographicline(self.h, self.n, self.points.T)

    def write(self, fid):
        fid.write('%f  %d\n'%(self.h, self.n))
        fid.write(' '.join([str(i) for i in self.points.flatten()]) + '\n')
            

### File I/O Classes ------------------------------------------------------------------------------

class MAP(WEFileIO):
    """WAsP MAP File."""

    ### Private methods to be implemented in the subclasses --------------------
    def _read(self):
        """ Read the map file. Place a list of vector lines in self.data"""
        with open(self.filename, 'r') as f:
            map_str=f.readlines()
        self.header = map_str[:4]
        arr1 = np.array(''.join(map_str[4:]).split(), dtype='float')
        ### Data contains a list of vector lines
        self.data = list(generate_vl(arr1))
        ### Maximum height of all the vector lines
        self.max_height = np.array([v.h for v in self.data]).max()        

    def _write(self):
        """ Write a file, with the same header"""
        with open(self.filename, 'w') as f:
            f.write(''.join(self.header))
            for v in self.data:
                v.write(f)

    def plot(self, **kwargs):
        """Plot all the vector lines. Scale their color with the height. 
        Returns a list of all the plot handles.
        """
        return [vl.plot(scale=self.max_height, **kwargs) for vl in self.data]
            
    def add_to_wasp(self, wasp_core):
        """Add all the vector lines to the wasp core"""
        for v in self.data:
            v.add_to_wasp(wasp_core)


class WTG(WEFileIO):
    """WAsP Turbine File."""

    
    ### Private methods to be implemented in the subclasses --------------------
    def _read(self):
        """ Read the file."""
        xml = ET.parse(self.filename).getroot()
        self.xml = xml

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


from zipfile import ZipFile
class WWH(WEFileIO):
    """WAsP Workspace file .wwh"""

    def _read(self):
        """Unzip and read the file"""
        with ZipFile(self.filename, 'r') as f:
            e = ET.fromstring(f.read('Inventory.xml'))

        ### Simple function to look for a specific Class Descriptor. Return a list.
        xmlf = lambda exml, keyword, address: filter(lambda x: x.get('ClassDescription') == keyword, exml.findall(address))

        ### Find the turbine sites
        turbine_sites = xmlf(e, 'Turbine site group', 
                             'WaspHierarchyMember/ChildMembers/WaspHierarchyMember/ChildMembers/WaspHierarchyMember')

        for ts in turbine_sites:
            ### Get the wind turbine description
            turbine_xml = xmlf(ts, 'Wind turbine generator', 'ChildMembers/WaspHierarchyMember')[0].find('MemberData/WindTurbineGenerator')
            a = np.array(list(map(datapoint, turbine_xml.findall('PerformanceTable/DataTable/DataPoint'))))
            ## Sorting with respect of wind speed
            self.turbine = {}
            self.turbine['data'] = a[np.argsort(a[:,0]),:]
            self.turbine['density'] = float(turbine_xml.find('PerformanceTable').get('AirDensity'))
            self.turbine['rotor_diameter'] = float(turbine_xml.get('RotorDiameter'))
            self.turbine['hub_height'] = turbine_xml.findall('SuggestedHeights/Height')[0].text
            self.turbine['manufacturer'] = turbine_xml.get('ManufacturerName')

            ### Data contains the label name of the turbine as keys, and for each one a list of x,y,h
            ts_xml = xmlf(ts, 'Turbine site', 'ChildMembers/WaspHierarchyMember')

            
            
            SectorData = lambda d: [float(d.get(i)) for i in ('CentreAngleDegrees', 
                                                              'SectorFrequency', 
                                                              'WeibullA', 
                                                              'WeibullK')]

            self.data = {}
            self.windroses = {}
            for i in list(ts_xml):
                label = i.get('Description')
                site_info = i.find('MemberData/SiteInformation')
                location = i.find('MemberData/SiteInformation/Location')
                self.data[label] = [float(location.get('x-Location')),
                                    float(location.get('y-Location')),
                                    float(site_info.get('WorkingHeightAgl'))]
                wind_climates = i.findall('MemberData/CalculationResults/PredictedWindClimate/RveaWeibullWindRose/WeibullWind')
                a = np.array(list(map(SectorData, wind_climates)))
                self.windroses[label] = a[np.argsort(a[:,0]),:]

            ### 2D array of x,y for each turbine
            self.pos = np.array([(d[0], d[1]) for d in self.data.values()])

        
## Do Some testing -------------------------------------------------------
class TestWAsP(TestWEFileIO):
    """ Test class for MyFileType class """

    test_wtg = 'test/wasp/bonus450.wtg'
    test_pow = 'test/wasp/bonus450.pow'
    test_wwf = 'test/wasp/hornsrev1.wwf'
    test_map = 'test/wasp/WaspMap.map'

    def test_WTG_duplication(self):
        self._test_duplication_array(WTG, self.test_wtg)

    def test_POW_duplication(self):
        self._test_duplication_array(POW, self.test_pow)

    def test_MAP_dupplication(self):
        original_file, new_file = self._duplicate(MAP, self.test_map)
        for of, nf in zip(original_file.data, new_file.data):
            self.assertTrue(np.linalg.norm(of.points-nf.points)<1.0E-8)

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