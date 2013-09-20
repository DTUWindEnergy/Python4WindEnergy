from demonstration import PlotUI
from demonstration.QtGuiLoader import QtMainWindowLoader
from pylab import *
from demonstration.matplotlibwidget import MatplotlibWidget

class Plot(QtMainWindowLoader):
    def __init__(self):
        QtMainWindowLoader.__init__(self, PlotUI)
        self.mpl = MatplotlibWidget()
        self.ui.mplcontainer.addWidget(self.mpl)

    def actionUpdate(self):
        x = arange(-pi, pi, pi / 10)
        y = eval(str(self.ui.lineEdit.text()));
        self.mpl.axes.plot(x, y, '--rx', linewidth=2);
        self.mpl.axes.set_title('Sine Function');
        self.mpl.draw()


Plot().start()
