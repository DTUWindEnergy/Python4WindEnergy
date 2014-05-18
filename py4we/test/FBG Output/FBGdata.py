""" IO classes for YOUR_FILE_TYPE_NAME file types

Copyright (C) 2013 DTU Wind Energy

Author: YOUR_NAME
Email: YOUR_EMAIL
Last revision: DATE

License: Apache v2.0, http://www.apache.org/licenses/LICENSE-2.0
"""


from __future__ import print_function
from we_file_io import WEFileIO, TestWEFileIO
import unittest

import numpy as np
import os.path as path
import scipy as sp
import sympy
import matplotlib.pyplot as plt

### Your class should look like this one ---------------------------------


class FBGdata(WEFileIO):
    """ FBGdata should read /write the wavelength-shift measurements given by 
    the hardware 
    
    
    
    methods:
    --------
        write: write a file
        reade: read a file

    """
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
            
            
            txtlines=f.readlines()
                      
            """read the info from the file"""
            
            self.head=txtlines[1]
            
            """Read info of sensors"""
            self.sens=txtlines[3]
            
            """ lets count the number of sensors (line 3 number of 
            columes-2(Date time))"""
                        
            self.nsens=np.size(txtlines[3].split('\t'))-2
            names=['date','time']
            formats=['S10', 'S8']
            
            
            """Functions dtype that depend of the number of sensors"""
            for i in range(1,self.nsens+1):
               names.append('s'+ str(i))
               formats.append('f8')
               
               
            dtypes = {'names' : (names),'formats': (formats) }           
            self.data=np.loadtxt(self.filename, dtype=dtypes,skiprows=4)
        #Plot is not used here anymore
    def _plot(self,fig):   
        self.fig=fig
               
        head=self.head.split('\t')
               
        page_width_cm = 13
        dpi = 200
        inch = 2.54 # inch in cm
        # setting global plot configuration using the RC configuration style
        plt.rc('font', family='serif')
        plt.rc('xtick', labelsize=12) # tick labels
        plt.rc('ytick', labelsize=12) # tick labels
        plt.rc('axes', labelsize=12)  # axes labels
               
        
        
        self.fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(10,15))
        self.fig.suptitle('Name: %s \n%s \n Start: %s, End:%s'%(head[0],head[1],head[2],head[3]), fontsize=16)
        
        ax[1].grid()
        ax[0].grid()
        """Plot of Relative values""" 

        ax[0].set_title("Relative Wavelength",fontsize=14)    
                                                       
        for i in range(self.nsens):
            sensor= 's'+str(i+1)
            ax[0].plot(self.data[sensor], linewidth=2.00,label="Sensor "+str(i+1))   
            
        ax[0].legend(fontsize=12, loc="best")
        ax[0].set_xlabel('Time (s)')
        ax[0].set_ylabel(r'$\Delta$\lambda [$\mu m]')
         
        
        """Plot of absolute values"""
        
        ax[1].set_title("Absolute Wavelength",fontsize=14)
        senss=self.sens.split('\t')
        for i in range(self.nsens):
            
            """getting the sensor absolute value"""
            v=senss[i+2]
            sensv=float(v[14:25])
            sensor= 's'+str(i+1)    
            ax[1].plot(sensv+self.data[sensor], linewidth=2.00,label="Sensor "+str(i+1))
            
        ax[1].legend(fontsize=12, loc="best")    
        ax[1].set_xlabel('Time (s)')
        ax[1].set_ylabel('$\lambda [$\mu m]')
          

###------------------------------------------------------------------------





from QtGuiLoader import QtWidgetLoader
import MyUI.MyPlotControlUI
class MyPlotControlWidget(QtWidgetLoader):
    def __init__(self, we_file_io):
        try:self.ui = MyUI.MyPlotControlUI.Ui_Form() # Enables autocompletion (if you are lucky...)
        except: pass
        QtWidgetLoader.__init__(self, ui_module=MyUI.MyPlotControlUI)
        self.we_file_io = we_file_io
                
        #Connect widget signals to actionUpdatePlot
        
        self.ui.horizontalSlider.valueChanged.connect(self.actionUpdatePlot)
        self.ui.spinBox.valueChanged.connect(self.actionUpdatePlot)
        self.ui.doubleSpinBox.valueChanged.connect(self.actionUpdatePlot)
        self.ui.spinBox_2.valueChanged.connect(self.actionUpdatePlot)
        self.ui.doubleSpinBox_2.valueChanged.connect(self.actionUpdatePlot)
        self.ui.radioButton_relative.clicked.connect(self.actionUpdatePlot,)
        self.ui.radioButton_absolute.clicked.connect(self.actionUpdatePlot)
        self.ui.radioButton_relative.clicked.connect(lambda: self.ui.doubleSpinBox.setValue(2))
        self.ui.radioButton_relative.clicked.connect(lambda: self.ui.spinBox.setValue(0))
        self.ui.radioButton_absolute.clicked.connect(lambda: self.ui.doubleSpinBox.setValue(1555))
        self.ui.radioButton_absolute.clicked.connect(lambda: self.ui.spinBox.setValue(1550))

        
    
    width = property(lambda self : self.ui.horizontalSlider.value())
    ylim = property(lambda self : (self.ui.spinBox.value(), self.ui.doubleSpinBox.value()))
    xlim = property(lambda self : (self.ui.spinBox_2.value(), self.ui.doubleSpinBox_2.value()))
    rel= property(lambda self : (self.ui.radioButton_relative.isChecked()))
    leg=property(lambda self : (self.ui.checkBox.isChecked()))
    
    def actionUpdatePlot(self):
        self.we_file_io.plot()



# --------------------------------------------------------------------------------
# --- 
# --------------------------------------------------------------------------------
import sys
sys.path.append("..\py4we") # append py4we package to path to access WEFileIO

from we_file_io import WEFileIO

class MyPlotFileIO(WEFileIO):
    title = "No title"
    def __init__(self, mpl_widget):
        WEFileIO.__init__(self, file_type_name = "FBG", file_extension = ".txt")
        self.figure = mpl_widget.figure
        self.ui_control = MyPlotControlWidget(self)
        self.plot()

    def _read(self):
        with open(self.filename, 'r') as f:
            self.title = f.read()
        self.plot()
      
        
    def _plot(self, fig):
        
        if "my_data" in globals():            
            self.fig=fig
            head=my_data.head.split('\t')            
            axes = fig.axes[0]
            axes.hold(False)
            axes.cla()            
            axes.hold(True)
            
            #Ploting Relative Wavelength
            if self.ui_control.rel == True: 
                axes.set_title("Relative Wavelength",fontsize=14)
                for i in range(my_data.nsens):                
                    sensor= 's'+str(i+1)
                    axes.plot(my_data.data[sensor], linewidth=self.ui_control.width,label="Sensor "+str(i+1))
            
            #Ploting Absolute Wavelength
            else:
                axes.set_title("Absolute Wavelength",fontsize=14)
                senss=my_data.sens.split('\t')
                for i in range(my_data.nsens):
            
     #getting the sensor absolute value
                    v=senss[i+2]
                    sensv=float(v[14:25])
                    sensor= 's'+str(i+1)    
                    axes.plot(sensv+my_data.data[sensor], linewidth=2.00,label="Sensor "+str(i+1))

            axes.set_ylim(self.ui_control.ylim)
            axes.set_xlim(self.ui_control.xlim)
            axes.grid()
            
            if self.ui_control.leg == True:                 
                axes.legend(fontsize=12, loc="best")  
                
            axes.set_xlabel('Time (s)',fontsize=14)
            axes.set_ylabel('$\lambda [\mu m]$',fontsize=14)            
            fig.canvas.draw()

        else:
            fig.canvas.draw()
                           
        
# --------------------------------------------------------------------------------
# ---  
# --------------------------------------------------------------------------------
import MyUI.MyPlotMainWindowUI
from QtGuiLoader import QtMainWindowLoader
from matplotlibwidget import MatplotlibWidget
from PyQt4 import QtGui

class MyPlotMainWindow(QtMainWindowLoader):
    
    def __init__(self):
        module = MyUI.MyPlotMainWindowUI
        try:self.ui = module.Ui_Form() # Enables autocompletion (if you are lucky...)
        except: pass
        QtMainWindowLoader.__init__(self, module)
        mpl = MatplotlibWidget()
        self.ui.gridLayoutPlot.addWidget(mpl)
        self.fileio = MyPlotFileIO(mpl)
        self.ui.gridLayoutControl.addWidget(self.fileio.ui_control)
        
    
    def actionOpen(self):
        filename = str(QtGui.QFileDialog.getOpenFileName(self, "Open...", ".", "*%s" % self.fileio.file_extension))
        if filename == "": return #cancel
        #self.fileio.read(filename)
        global my_data
        my_data = FBGdata(filename)
        my_data.read()             
        return my_data
        




## Do Some testing -------------------------------------------------------
class TestMyDatFileIO(TestWEFileIO):
    """ Test class for MyFileType class """

    def test_duplication(self):
        self._test_duplication(MyDatFileIO, './test/dat/test_file.dat')


## Main function ---------------------------------------------------------
if __name__ == '__main__':
    """ This is the main fuction that will run the tests automatically

    $> python my_file_type.py
    .
    ----------------------------------------------------------------------
    Ran X test in XXXs

    OK
    """
    unittest.main()

