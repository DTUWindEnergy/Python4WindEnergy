import MyUI.MyPlotControlUI
from QtGuiLoader import QtMainWindowLoader
import numpy as np
import matplotlib.pyplot as plt

    
class MyPlotControlMainWindow(QtMainWindowLoader):
    def __init__(self):
        try: self.ui = MyUI.MyPlotControlUI.Ui_Form() # Enables autocompletion (maybe...)
        except: pass
        QtMainWindowLoader.__init__(self, ui_module=MyUI.MyPlotControlUI)
                
        #Connect widget signals to actionUpdatePlot
        self.ui.xLineEdit.editingFinished.connect(self.actionUpdatePlot)
        self.ui.yLineEdit.editingFinished.connect(self.actionUpdatePlot)
        self.ui.colorComboBox.currentIndexChanged.connect(self.actionUpdatePlot)
        self.ui.horizontalSlider.valueChanged.connect(self.actionUpdatePlot)
        self.ui.spinBox.valueChanged.connect(self.actionUpdatePlot)
        self.ui.doubleSpinBox.valueChanged.connect(self.actionUpdatePlot)
        
        self.actionUpdatePlot()
        
    x_str = property(lambda self : str(self.ui.xLineEdit.text()))
    y_str = property(lambda self : str(self.ui.yLineEdit.text()))
    color = property(lambda self : str(self.ui.colorComboBox.currentText()))
    width = property(lambda self : str(self.ui.labelWidth.text()))
    ylim = property(lambda self : ("%s, %s") %(self.ui.spinBox.text(),self.ui.doubleSpinBox.text()) )

    def actionUpdatePlot(self):
        print (self.x_str, self.y_str, self.color, self.width, self.ylim)
    
MyPlotControlMainWindow().start()

