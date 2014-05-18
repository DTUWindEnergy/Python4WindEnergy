# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MyUI\MyPlotControlUI.ui'
#
# Created: Sat May 17 20:11:22 2014
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
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 221, 271))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.widthLabel = QtGui.QLabel(self.formLayoutWidget)
        self.widthLabel.setObjectName(_fromUtf8("widthLabel"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.widthLabel)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.horizontalSlider = QtGui.QSlider(self.formLayoutWidget)
        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setMaximum(10)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName(_fromUtf8("horizontalSlider"))
        self.horizontalLayout.addWidget(self.horizontalSlider)
        self.labelWidth = QtGui.QLabel(self.formLayoutWidget)
        self.labelWidth.setMinimumSize(QtCore.QSize(30, 0))
        self.labelWidth.setObjectName(_fromUtf8("labelWidth"))
        self.horizontalLayout.addWidget(self.labelWidth)
        self.formLayout.setLayout(2, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.spinBox_2 = QtGui.QSpinBox(self.formLayoutWidget)
        self.spinBox_2.setMinimum(-20000)
        self.spinBox_2.setMaximum(20000)
        self.spinBox_2.setSingleStep(100)
        self.spinBox_2.setProperty("value", 0)
        self.spinBox_2.setObjectName(_fromUtf8("spinBox_2"))
        self.horizontalLayout_3.addWidget(self.spinBox_2)
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_3.addWidget(self.label_3)
        self.doubleSpinBox_2 = QtGui.QDoubleSpinBox(self.formLayoutWidget)
        self.doubleSpinBox_2.setDecimals(0)
        self.doubleSpinBox_2.setMinimum(-20000.0)
        self.doubleSpinBox_2.setMaximum(20000.0)
        self.doubleSpinBox_2.setSingleStep(100.0)
        self.doubleSpinBox_2.setProperty("value", 15000.0)
        self.doubleSpinBox_2.setObjectName(_fromUtf8("doubleSpinBox_2"))
        self.horizontalLayout_3.addWidget(self.doubleSpinBox_2)
        self.formLayout.setLayout(4, QtGui.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.ylimLabel = QtGui.QLabel(self.formLayoutWidget)
        self.ylimLabel.setObjectName(_fromUtf8("ylimLabel"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.ylimLabel)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.spinBox = QtGui.QSpinBox(self.formLayoutWidget)
        self.spinBox.setMinimum(-10)
        self.spinBox.setMaximum(2000)
        self.spinBox.setSingleStep(50)
        self.spinBox.setProperty("value", 0)
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.horizontalLayout_2.addWidget(self.spinBox)
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.doubleSpinBox = QtGui.QDoubleSpinBox(self.formLayoutWidget)
        self.doubleSpinBox.setDecimals(0)
        self.doubleSpinBox.setMinimum(0.0)
        self.doubleSpinBox.setMaximum(2000.0)
        self.doubleSpinBox.setSingleStep(50.0)
        self.doubleSpinBox.setProperty("value", 2.0)
        self.doubleSpinBox.setObjectName(_fromUtf8("doubleSpinBox"))
        self.horizontalLayout_2.addWidget(self.doubleSpinBox)
        self.formLayout.setLayout(5, QtGui.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.radioButton_relative = QtGui.QRadioButton(self.formLayoutWidget)
        self.radioButton_relative.setChecked(True)
        self.radioButton_relative.setObjectName(_fromUtf8("radioButton_relative"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.radioButton_relative)
        self.radioButton_absolute = QtGui.QRadioButton(self.formLayoutWidget)
        self.radioButton_absolute.setObjectName(_fromUtf8("radioButton_absolute"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.FieldRole, self.radioButton_absolute)
        self.pushButton = QtGui.QPushButton(self.formLayoutWidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.SpanningRole, self.pushButton)
        self.checkBox = QtGui.QCheckBox(self.formLayoutWidget)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.FieldRole, self.checkBox)
        self.actionUpdatePlot = QtGui.QAction(Form)
        self.actionUpdatePlot.setObjectName(_fromUtf8("actionUpdatePlot"))

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.horizontalSlider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.labelWidth.setNum)
        QtCore.QObject.connect(self.radioButton_relative, QtCore.SIGNAL(_fromUtf8("clicked()")), self.radioButton_relative.toggle)
        QtCore.QObject.connect(self.radioButton_absolute, QtCore.SIGNAL(_fromUtf8("clicked()")), self.radioButton_absolute.toggle)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.actionUpdatePlot.trigger)
        QtCore.QObject.connect(self.checkBox, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")), self.actionUpdatePlot.trigger)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.widthLabel.setText(_translate("Form", "width", None))
        self.labelWidth.setText(_translate("Form", "1", None))
        self.label_2.setText(_translate("Form", "xlim", None))
        self.label_3.setText(_translate("Form", "to", None))
        self.ylimLabel.setText(_translate("Form", "ylim", None))
        self.label.setText(_translate("Form", "to", None))
        self.radioButton_relative.setText(_translate("Form", "Relative Wavelength", None))
        self.radioButton_absolute.setText(_translate("Form", "Absolute Wavelength", None))
        self.pushButton.setText(_translate("Form", "Plot/Update", None))
        self.checkBox.setText(_translate("Form", "Legend", None))
        self.actionUpdatePlot.setText(_translate("Form", "updatePlot", None))

