from build_cx_exe import build_exe, PYQT4, MATPLOTLIB, NUMPY
build_exe('my_qt_program.py', "1.0.0", modules=[PYQT4, MATPLOTLIB, NUMPY], icon='test.ico')