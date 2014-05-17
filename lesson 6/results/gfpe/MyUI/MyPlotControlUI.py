# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MyUI\MyPlotControlUI.ui'
#
# Created: Fri May 16 19:46:16 2014
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(400, 300)
        self.formLayoutWidget = QtGui.QWidget(Form)
        self.formLayoutWidget.setGeometry(QtCore.QRect(110, 90, 191, 171))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.xLabel = QtGui.QLabel(self.formLayoutWidget)
        self.xLabel.setObjectName(_fromUtf8("xLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.xLabel)
        self.xLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.xLineEdit.setObjectName(_fromUtf8("xLineEdit"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.xLineEdit)
        self.yLabel = QtGui.QLabel(self.formLayoutWidget)
        self.yLabel.setObjectName(_fromUtf8("yLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.yLabel)
        self.yLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.yLineEdit.setObjectName(_fromUtf8("yLineEdit"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.yLineEdit)
        self.colorLabel = QtGui.QLabel(self.formLayoutWidget)
        self.colorLabel.setObjectName(_fromUtf8("colorLabel"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.colorLabel)
        self.colorComboBox = QtGui.QComboBox(self.formLayoutWidget)
        self.colorComboBox.setObjectName(_fromUtf8("colorComboBox"))
        self.colorComboBox.addItem(_fromUtf8(""))
        self.colorComboBox.addItem(_fromUtf8(""))
        self.colorComboBox.addItem(_fromUtf8(""))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.colorComboBox)
        self.widthLabel = QtGui.QLabel(self.formLayoutWidget)
        self.widthLabel.setObjectName(_fromUtf8("widthLabel"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.widthLabel)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.horizontalSlider = QtGui.QSlider(self.formLayoutWidget)
        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setMaximum(9)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName(_fromUtf8("horizontalSlider"))
        self.horizontalLayout.addWidget(self.horizontalSlider)
        self.labelWidth = QtGui.QLabel(self.formLayoutWidget)
        self.labelWidth.setMinimumSize(QtCore.QSize(30, 0))
        self.labelWidth.setObjectName(_fromUtf8("labelWidth"))
        self.horizontalLayout.addWidget(self.labelWidth)
        self.formLayout.setLayout(3, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.yLimLabel = QtGui.QLabel(self.formLayoutWidget)
        self.yLimLabel.setObjectName(_fromUtf8("yLimLabel"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.yLimLabel)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.spinBox = QtGui.QSpinBox(self.formLayoutWidget)
        self.spinBox.setMinimum(-10)
        self.spinBox.setMaximum(10)
        self.spinBox.setSingleStep(1)
        self.spinBox.setProperty("value", -5)
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.horizontalLayout_2.addWidget(self.spinBox)
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.doubleSpinBox = QtGui.QDoubleSpinBox(self.formLayoutWidget)
        self.doubleSpinBox.setMinimum(-10.0)
        self.doubleSpinBox.setMaximum(10.0)
        self.doubleSpinBox.setSingleStep(0.1)
        self.doubleSpinBox.setProperty("value", 5.0)
        self.doubleSpinBox.setObjectName(_fromUtf8("doubleSpinBox"))
        self.horizontalLayout_2.addWidget(self.doubleSpinBox)
        self.formLayout.setLayout(4, QtGui.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.actionUpdatePlot = QtGui.QAction(Form)
        self.actionUpdatePlot.setObjectName(_fromUtf8("actionUpdatePlot"))

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.horizontalSlider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.labelWidth.setNum)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.xLabel.setText(_translate("Form", "X:", None))
        self.xLineEdit.setText(_translate("Form", "np.arange(0,10,0.1)", None))
        self.yLabel.setText(_translate("Form", "y:", None))
        self.yLineEdit.setText(_translate("Form", "3*np.sin(x)", None))
        self.colorLabel.setText(_translate("Form", "Color:", None))
        self.colorComboBox.setItemText(0, _translate("Form", "Red", None))
        self.colorComboBox.setItemText(1, _translate("Form", "Green", None))
        self.colorComboBox.setItemText(2, _translate("Form", "blue", None))
        self.widthLabel.setText(_translate("Form", "Width:", None))
        self.labelWidth.setText(_translate("Form", "1", None))
        self.yLimLabel.setText(_translate("Form", "yLim", None))
        self.label.setText(_translate("Form", "to", None))
        self.actionUpdatePlot.setText(_translate("Form", "updatePlot", None))

