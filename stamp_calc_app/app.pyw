from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from stamp_calc_ui import Ui_MainWindow
import sys

class stamp_calc_main_app(Ui_MainWindow):
    def __init__(self, dialog):
        Ui_MainWindow.__init__(self)
        self.setupUi(dialog)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QMainWindow()
    prog = stamp_calc_main_app(dialog)
    dialog.show()
    sys.exit(app.exec_())
