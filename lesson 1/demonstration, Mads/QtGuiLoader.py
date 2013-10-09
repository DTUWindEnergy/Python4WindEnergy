'''

Classes for loading a QWidget designed in QT Designer as MainWindow, Dialog or Widget
Examples of how to use can be found in UseQtGuiLoader.py

@Created on 13/3/2013
@modified
@version:1.5 (9/7-2013)
@change: 1.5 changed sys.exit(app.exec_()) to app.exec_() to avoid SystemExit exception when running from IPython
             Gridlayout with ui_widget added to QtWidgetLoader
             application argument removed
         1.4 Actions can be connected to methods of same name if they exists by calling 'connect_actions'
             _ui_widget set to last child of action_receiver with name 'QWidget' instead of last child
         1.3 QtWidgetLoader.new() returns MyWidget instead of QWidget
         1.2 QtMainWindowLoader now works on Widget and MainWindow
             Actions are connected to methods of same name if they exists
         1.1 copy attributes from qtGuiLoader to qtGuiLoader.widget
@author: Mads M Pedersen (mmpe@dtu.dk)
'''


from PyQt4 import QtGui, QtCore
import os
import sys
import time


class QtGuiLoader(object):

    def compile_ui(self, ui_module):
        #basename = ui_module.__name__.replace(".", "\\")
        basename = os.path.splitext(os.path.relpath(ui_module.__file__, os.getcwd()))[0]
        ui_file = basename + ".ui"
        py_file = basename + ".py"

        if os.path.exists(ui_file):
            if not os.path.exists(py_file) or \
                os.path.getmtime(ui_file) > os.path.getmtime(py_file) or \
                    os.path.getsize(py_file) == 0:
                os.environ['path'] = os.environ['path'] + ";" + os.path.dirname(sys.executable)
                os.environ['path'] = os.environ['path'] + ";" + os.path.join(os.path.dirname(sys.executable), "scripts")
                os.environ['winpydir'] = os.path.dirname(sys.executable)
                print os.environ['path']
                print ("compile %s > %s" % (ui_file, py_file))
                os.system("pyuic4 %s > %s" % (ui_file, py_file))
        reload(ui_module)

    def connect_actions(self, action_receiver=None):
        if action_receiver is None:
            action_receiver = self
        for name, action in [(n, a) for n, a in vars(self.ui).items() if isinstance(a, QtGui.QAction)]:

            if hasattr(action_receiver, name):
                QtCore.QObject.connect(action, QtCore.SIGNAL("triggered()"), getattr(action_receiver, name))
            elif action.receivers(QtCore.SIGNAL("triggered()")) == 0:
                raise Warning("Action %s not connected. Method with name '%s' not found" % (action.text(), name))

    def setupUI(self, widget):
        self.ui.setupUi(widget)
        root_widgets = [w for w in widget.children() if w.__class__.__name__ == "QWidget"]
        if len(root_widgets) == 0:
            self.ui_widget = self
        else:
            self.ui_widget = [w for w in widget.children() if w.__class__.__name__ == "QWidget"][0]
            if widget.layout() is None:
                g = QtGui.QGridLayout()
                widget.setLayout(g)
                g.addWidget(self.ui_widget)


class QtGuiApplication():

    def __init__(self, ui_module):
        self.ui_module = ui_module
        self.app_filename = os.path.basename(sys.argv[0])
        self.app_name = os.path.splitext(self.app_filename)[0]
        if QtGui.QApplication.startingUp():
            self.app = QtGui.QApplication(sys.argv)

        self.compile_ui(ui_module)

    def save_settings(self):
        settings = QtCore.QSettings("QtGuiApplication", "%s_%s" % (self.app_name, self.__class__.__name__))
        settings.setValue(self.ui_module.__name__ + "/geometry", self.saveGeometry())

    def load_settings(self):
        settings = QtCore.QSettings("QtGuiApplication", "%s_%s" % (self.app_name, self.__class__.__name__))
        self.restoreGeometry(settings.value(self.ui_module.__name__ + "/geometry").toByteArray())

    def save_setting(self, key, value):
        settings = QtCore.QSettings("QtGuiApplication", "%s_%s" % (self.app_name, self.__class__.__name__))
        settings.setValue(self.ui_module.__name__ + "/" + key, value)

    def load_setting(self, key, default_value=None):
        settings = QtCore.QSettings("QtGuiApplication", "%s_%s" % (self.app_name, self.__class__.__name__))
        return settings.value(self.ui_module.__name__ + "/" + key, default_value)


class QtMainWindowLoader(QtGuiLoader, QtGuiApplication, QtGui.QMainWindow):

    def __init__(self, ui_module, parent=None, connect_actions=True):
        QtGuiApplication.__init__(self, ui_module)
        QtGui.QMainWindow.__init__(self, parent)

        if "Ui_Form" in dir(ui_module):
            self.ui = ui_module.Ui_Form()
            centralWidget = QtGui.QWidget(self)
            self.setCentralWidget(centralWidget)
            self.setupUI(centralWidget)
#
        elif "Ui_MainWindow" in dir(ui_module):
            self.ui = ui_module.Ui_MainWindow()
            self.ui.setupUi(self)
        if connect_actions:
            self.connect_actions()

    def start(self):
        self.load_settings()

        self.show()
        if hasattr(self, "app"):
            self.app.exec_()

    def terminate(self):

        QtGui.QApplication.quit()

    def closeEvent(self, *args, **kwargs):
        self.save_settings()
        # Enable paste of clipboard after termination
        clipboard = QtGui.QApplication.clipboard()
        event = QtCore.QEvent(QtCore.QEvent.Clipboard)
        QtGui.QApplication.sendEvent(clipboard, event)

        return QtGui.QMainWindow.closeEvent(self, *args, **kwargs)


class QtDialogLoader(QtGuiLoader, QtGuiApplication, QtGui.QDialog):

    def __init__(self, ui_module, parent, modal=True, connect_actions=True):
        QtGuiApplication.__init__(self, ui_module)
        QtGui.QDialog.__init__(self, parent)
        self.modal = modal
        self.setModal(modal)
        self.ui = ui_module.Ui_Form()
        self.setupUI(self)

        if connect_actions:
            self.connect_actions()

    def start(self):
        self.load_settings()
        self.show()
        self.raise_()
        if hasattr(self, "app"):
            return self.app.exec_()
        elif self.modal:
            return self.exec_()

    def hideEvent(self, *args, **kwargs):
        self.save_settings()
        return QtGui.QDialog.hideEvent(self, *args, **kwargs)


class QtWidgetLoader(QtGuiLoader, QtGui.QWidget):

    def __init__(self, ui_module, action_receiver=None, parent=None, connect_actions=True):
        if "ui_module" not in vars(self):
            QtGui.QWidget.__init__(self, parent)
            self.ui_module = ui_module
            self.compile_ui(ui_module)
            self.ui = ui_module.Ui_Form()

            self.setupUI(self)

            if connect_actions:
                self.connect_actions(action_receiver)
