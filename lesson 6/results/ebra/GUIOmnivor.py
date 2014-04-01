
from __future__ import print_function
import sys
sys.path.append("../py4we") # append py4we package to path to access WEFileIO

from we_file_io import WEFileIO
# from ofield_file_io import OmnivorFieldFile
import numpy as np

import numpy as np
from QtGuiLoader import QtWidgetLoader
import MyUI.OmnivorPlotControlUI



class OmnivorPlotControlWidget(QtWidgetLoader):
    def __init__(self, we_file_io):
        try:self.ui = MyUI.OmnivorPlotControlUI.Ui_Form() # Enables autocompletion (if you are lucky...)
        except: pass
        QtWidgetLoader.__init__(self, ui_module=MyUI.OmnivorPlotControlUI)
        self.we_file_io = we_file_io
                
        #Connect widget signals to actionUpdatePlot
        self.ui.xLineEdit.editingFinished.connect(self.actionUpdatePlot)
        self.ui.yLineEdit.editingFinished.connect(self.actionUpdatePlot)
        self.ui.colorComboBox.currentIndexChanged.connect(self.actionUpdatePlot)
        self.ui.horizontalSlider.valueChanged.connect(self.actionUpdatePlot)
        self.ui.spinBox.valueChanged.connect(self.actionUpdatePlot)
        self.ui.doubleSpinBox.valueChanged.connect(self.actionUpdatePlot)

        
#     x_str = property(lambda self : str(self.ui.xLineEdit.text()))
#     y_str = property(lambda self : str(self.ui.yLineEdit.text()))
    color = property(lambda self : str(self.ui.colorComboBox.currentText()))
    width = property(lambda self : self.ui.horizontalSlider.value())
    ylim = property(lambda self : (self.ui.spinBox.value(), self.ui.doubleSpinBox.value()))
    
    def actionUpdatePlot(self):
        self.we_file_io.plot()

from we_file_io import WEFileIO, TestWEFileIO
import unittest

import numpy as np
import os.path as path

# To read fortran binary files
from fortran_file import FortranFile
import tempfile
import os
import sys



class OmnivorFieldFile(WEFileIO):

    ID_GRID_FIELD =1
    ID_FLAT_FIELD =0


    def __init__(self, mpl_widget):
        WEFileIO.__init__(self, file_type_name = "Exercise2file", file_extension = ".dat")
        self.figure = mpl_widget.figure
        self.ui_control = OmnivorPlotControlWidget(self)
#         self.plot()

    def _write(self):
        """ Write a file (overrided)
        """
        f = FortranFile(self.filename,mode='w')
        # Default omnivor binary header
        f.writeInts   ( self.data['MK']       , 'i' ) 
        f.writeInts   ( self.data['itime']    , 'i' ) 
        f.writeString ( self.data['version']  ) 
        f.writeInts   ( self.data['file_id']  , 'i' ) 
        f.writeString ( self.data['sversion'] ) 
        # Velocity field
        f.writeString ( self.data['stype']   ) 
        f.writeInts   ( self.data['is_grid'] , 'i' ) 
        f.writeInts   ( self.data['nCPs']    , 'i' ) 
        if self.data['MK'] == 8:
            real_char='d'
        else:
            real_char='f'
        if self.data['is_grid']:
            f.writeInts  ( self.data['n1']          , 'i'       ) 
            f.writeInts  ( self.data['n2']          , 'i'       ) 
            f.writeInts  ( self.data['n3']          , 'i'       ) 
            f.writeInts  ( self.data['is_straight'] , 'i'       ) 
            f.writeReals ( self.data['v1']          , real_char ) 
            f.writeReals ( self.data['v2']          , real_char ) 
            f.writeReals ( self.data['v3']          , real_char ) 

        CPs  = self.data['CPs'].flatten(order   = 'F')
        Utot = self.data['Utot'].flatten(order = 'F')
        f.writeReals(CPs,real_char)
        f.writeReals(Utot,real_char)

    def _read(self):
        """ Read the file (overrided)
        """
        with open(self.filename, 'r') as f:
#             self.title = f.read()
            # initializng data dictionary
            print('Opening: %s'%self.filename)
            self.data={}

            f = FortranFile(self.filename)
            # Default omnivor binary header
            self.data['MK']       = f.readInts('i')
            self.data['itime']    = f.readInts('i')
            self.data['version']  = f.readString()
            self.data['file_id']  = f.readInts('i')
            self.data['sversion'] = f.readString()
            # Velocity field
            self.data['stype']   = f.readString()
            self.data['is_grid'] = f.readInts('i')
            nCPs                 = f.readInts('i')
            self.data['nCPs']    = nCPs
            if self.data['MK'] == 8:
                real_char='d'
            else:
                real_char='f'
            if self.data['is_grid']:
                #print('File is a velocity grid file')
                n1                       = f.readInts('i')
                n2                       = f.readInts('i')
                n3                       = f.readInts('i')
                self.data['n1']          = n1
                self.data['n2']          = n2
                self.data['n3']          = n3
                self.data['is_straight'] = f.readInts('i')
                self.data['v1']          = f.readReals(real_char)
                self.data['v2']          = f.readReals(real_char)
                self.data['v3']          = f.readReals(real_char)

            CPs_raw  = f.readReals(real_char)
            Utot_raw = f.readReals(real_char)
            CPs      = np.reshape(CPs_raw,(3,nCPs),order  = 'F')
            Utot     = np.reshape(Utot_raw,(3,nCPs),order = 'F')

            acc=-1
            CPsTab  = np.zeros((3, n1,n2,n3))
            UtotTab = np.zeros((3, n1,n2,n3))
            # Reshaping the nasty way (this is natural order). 
            for i in range(0,n1):
                for j in range(0,n2):
                    for k in range(0,n3):
                        acc=acc+1
                        CPsTab[0:3,i,j,k]  = CPs[0:3,acc]
                        UtotTab[0:3,i,j,k] = Utot[0:3,acc]

            self.data['CPs']  = CPs
            self.data['CPsTab']  = CPsTab
            self.data['Utot'] = Utot
            self.data['UtotTab'] = UtotTab
    
            self.plot()


    def _plot(self,fig):
        from mpl_toolkits.mplot3d import Axes3D
        import matplotlib.pyplot as plt
        from matplotlib import animation

        # Control points and velocity
        CPs=self.data['CPsTab']
        Utot=self.data['UtotTab']

        # dimensions and grid vectors
        nd,nx,ny,nz=np.shape(CPs)
        n={'x':nx ,'y':ny,'z':nz}
        xi=CPs[0,:,0,0]
        yi=CPs[1,0,:,0]
        zi=CPs[2,0,0,:]
        

        #
#         plt.contour(xi, zi, uiy, 15, linewidths = 0.5, colors = 'k')
#         plt.pcolormesh(xi, zi, uiy, cmap = plt.get_cmap('rainbow'))
            ## try an unsteady contour
        # Figure handle and plotting function
#         fig = plt.figure()
        
        axes = fig.axes[0]
#         print(self.ui_control.x_str)
#         print(self.ui_control.y_str)
#         axes.set_ylim(self.ui_control.ylim)
#         axes.set_title(self.title)
#         fig.canvas.draw()
#         fig=plt.figure() 
        ax=fig.gca()
#         ax = fig.axes[0]
        def animate(i,normal,component,ax,fig):
            c2i={'x':0 ,'y':1,'z':2}
            icomp=c2i[component]
            Umean=np.mean(Utot[icomp,:,:,:])
            Ustd=np.std(Utot[icomp,:,:,:])
            if normal=='y':
                x=xi
                y=zi
                ui=Utot[icomp,:,i,:]
                ui=ui.transpose()
            elif normal=='z':
                x=xi
                y=yi
                ui=Utot[icomp,:,:,i]
                ui=ui.transpose()
            else:
                x=yi
                y=zi
                ui=Utot[icomp,i,:,:]
                ui=ui.transpose()

            print(str(i)+' / '+str(n[normal]))
            ax.cla()
#             ax.set_xlabel('Streamwise direction [m]')
#             ax.set_ylabel('Lateral direction [m]')
            ax.set_title('Velocity along %s [m/s]'%component)
            im=ax.contourf(x,y,ui,levels=np.arange(Umean-5*Ustd,Umean+5*Ustd,Ustd/30),cmap=plt.get_cmap('hsv'),linewidth=0.1)
#             plt.axis('equal')
#             if i==1:
#                 plt.colorbar(im) 
#             if i==(n[normal]-1):
#                 plt.close()
            return im
            
        # Component selection and normal for plotting
        component='y'
        normal='y'
        ani = animation.FuncAnimation(fig, animate,frames=n[normal], fargs=(normal,component,ax,fig))
        fig.canvas.draw()
#         plt.show()
#         ani.save('basic_animation.mp4', writer=animation.FFMpegWriter(fps=20,bitrate=10000,codec='libx264'))
#         fig = plt.figure()
#         i=1
#         ax.scatter(CPs[0,i,:,:], CPs[1,i,:,:],CPs[2,i,:,:])
#         ax.scatter(CPs[0,:,i,:], CPs[1,:,i,:],CPs[2,:,i,:])
#         ax = fig.add_subplot(111, projection='3d')
#         ax.set_xlabel('X Label')
#         ax.set_ylabel('Y Label')
#         ax.set_zlabel('Z Label')
# 


    def __getitem__(self, key):
        """ Transform the class instance into a dictionary."""
        return self.data[key]

    def __setitem__(self, key, value):
        """ Transform the class instance into a dictionary."""
        self.data[key] = value


# 
## Do Some testing -------------------------------------------------------

class TestOmnivorField(TestWEFileIO):
    """ Test class for OmnivorField class """

#     test_file = './test/omnivor/ugrid_8584.dat'
#     test_file = './test/omnivor/uservel_8584.dat'
#     InputFile=OmnivorFieldFile(test_file)
#     InputFile.plot()
# #     InputFile.write(test_file+'_new')
# 
    def test_duplication(self):
        import os
        original_file, new_file = self._duplicate(OmnivorFieldFile, self.test_file)
#         self.assertEqual(original_file.data[], new_file.data)
        np.array_equal(original_file.data['CPs'], new_file.data['CPs'])
        np.array_equal(original_file.data['Utot'], new_file.data['Utot'])
        os.remove(new_file.filename)




# --------------------------------------------------------------------------------
# --- 
# --------------------------------------------------------------------------------
# class MyPlotFileIO(WEFileIO):
#     title = "No title"
#     def __init__(self, mpl_widget):
#         WEFileIO.__init__(self, file_type_name = "Exercise2file", file_extension = ".title")
#         self.figure = mpl_widget.figure
#         self.ui_control = MyPlotControlWidget(self)
#         self.plot()
# 
#     def _read(self):
#         with open(self.filename, 'r') as f:
#             self.title = f.read()
#         self.plot()
#     
#     def _plot(self, fig):
#         axes = fig.axes[0]
#         print(self.ui_control.x_str)
#         print(self.ui_control.y_str)
#         x = eval(self.ui_control.x_str)
#         y = eval(self.ui_control.y_str)
#         axes.plot(x,y, self.ui_control.color, linewidth=self.ui_control.width)
#         axes.set_ylim(self.ui_control.ylim)
#         axes.set_title(self.title)
#         fig.canvas.draw()
        



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
        self.fileio = OmnivorFieldFile(mpl)
        self.ui.gridLayoutControl.addWidget(self.fileio.ui_control)
        
    
    def actionOpen(self):
        filename = str(QtGui.QFileDialog.getOpenFileName(self, "Open...", ".", "*%s" % self.fileio.file_extension))
        if filename == "": return #cancel
        self.fileio.read(filename)


MyPlotMainWindow().start()
