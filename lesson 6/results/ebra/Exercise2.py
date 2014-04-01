import numpy as np
from numpy import *
from QtGuiLoader import QtWidgetLoader
import MyUI.MyPlotControlUI
class MyPlotControlWidget(QtWidgetLoader):
    def __init__(self, we_file_io):
        try:self.ui = MyUI.MyPlotControlUI.Ui_Form() # Enables autocompletion (if you are lucky...)
        except: pass
        QtWidgetLoader.__init__(self, ui_module=MyUI.MyPlotControlUI)
        self.we_file_io = we_file_io
                
        #Connect widget signals to actionUpdatePlot
        self.ui.xLineEdit.editingFinished.connect(self.actionUpdatePlot)
        self.ui.yLineEdit.editingFinished.connect(self.actionUpdatePlot)
        self.ui.colorComboBox.currentIndexChanged.connect(self.actionUpdatePlot)
        self.ui.horizontalSlider.valueChanged.connect(self.actionUpdatePlot)
        self.ui.spinBox.valueChanged.connect(self.actionUpdatePlot)
        self.ui.doubleSpinBox.valueChanged.connect(self.actionUpdatePlot)

        
    x_str = property(lambda self : str(self.ui.xLineEdit.text()))
    y_str = property(lambda self : str(self.ui.yLineEdit.text()))
    color = property(lambda self : str(self.ui.colorComboBox.currentText()))
    width = property(lambda self : self.ui.horizontalSlider.value())
    ylim = property(lambda self : (self.ui.spinBox.value(), self.ui.doubleSpinBox.value()))
    
    def actionUpdatePlot(self):
        self.we_file_io.plot()



# --------------------------------------------------------------------------------
# --- 
# --------------------------------------------------------------------------------
import sys
sys.path.append("../py4we") # append py4we package to path to access WEFileIO

from we_file_io import WEFileIO
import numpy as np
class MyPlotFileIO(WEFileIO):
    title = "No title"
    def __init__(self, mpl_widget):
        WEFileIO.__init__(self, file_type_name = "Exercise2file", file_extension = ".title")
        self.figure = mpl_widget.figure
        self.ui_control = MyPlotControlWidget(self)
        self.plot()

    def _read(self):
        with open(self.filename, 'r') as f:
            self.title = f.read()
        self.plot()
    
    def _plot(self, fig):
        axes = fig.axes[0]
        print(self.ui_control.x_str)
        print(self.ui_control.y_str)
        x = eval(self.ui_control.x_str)
        y = eval(self.ui_control.y_str)
        axes.plot(x,y, self.ui_control.color, linewidth=self.ui_control.width)
        axes.set_ylim(self.ui_control.ylim)
        axes.set_title(self.title)
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
        self.fileio.read(filename)


MyPlotMainWindow().start()
