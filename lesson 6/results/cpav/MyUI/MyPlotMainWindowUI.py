# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MyUI\MyPlotMainWindowUI.ui'
#
# Created: Tue Apr 01 11:30:07 2014
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_5 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayoutPlot = QtGui.QGridLayout()
        self.gridLayoutPlot.setObjectName(_fromUtf8("gridLayoutPlot"))
        self.horizontalLayout.addLayout(self.gridLayoutPlot)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.verticalLayout_3.addWidget(self.pushButton)
        self.gridLayoutControl = QtGui.QGridLayout()
        self.gridLayoutControl.setObjectName(_fromUtf8("gridLayoutControl"))
        self.verticalLayout_3.addLayout(self.gridLayoutControl)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.horizontalLayout.setStretch(0, 1)
        self.gridLayout_5.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 18))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.menuFile.addAction(self.actionOpen)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.actionOpen.trigger)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton.setText(_translate("MainWindow", "Open", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.actionOpen.setText(_translate("MainWindow", "Open", None))
        self.actionOpen.setToolTip(_translate("MainWindow", "Open a file", None))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O", None))

