# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'stamp_calc.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(438, 386)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.small_parcel_label = QtWidgets.QLabel(self.centralwidget)
        self.small_parcel_label.setGeometry(QtCore.QRect(20, 10, 61, 31))
        self.small_parcel_label.setObjectName("small_parcel_label")
        self.sp_1kg = QtWidgets.QRadioButton(self.centralwidget)
        self.sp_1kg.setGeometry(QtCore.QRect(50, 50, 82, 17))
        self.sp_1kg.setObjectName("sp_1kg")
        self.sp_2kg = QtWidgets.QRadioButton(self.centralwidget)
        self.sp_2kg.setGeometry(QtCore.QRect(50, 80, 82, 17))
        self.sp_2kg.setObjectName("sp_2kg")
        self.mp_2kg = QtWidgets.QRadioButton(self.centralwidget)
        self.mp_2kg.setGeometry(QtCore.QRect(50, 170, 82, 17))
        self.mp_2kg.setObjectName("mp_2kg")
        self.mp_1kg = QtWidgets.QRadioButton(self.centralwidget)
        self.mp_1kg.setGeometry(QtCore.QRect(50, 140, 82, 17))
        self.mp_1kg.setObjectName("mp_1kg")
        self.meidum_parcel_label = QtWidgets.QLabel(self.centralwidget)
        self.meidum_parcel_label.setGeometry(QtCore.QRect(20, 100, 71, 31))
        self.meidum_parcel_label.setObjectName("meidum_parcel_label")
        self.mp_5kg = QtWidgets.QRadioButton(self.centralwidget)
        self.mp_5kg.setGeometry(QtCore.QRect(50, 200, 82, 17))
        self.mp_5kg.setObjectName("mp_5kg")
        self.mp_20kg = QtWidgets.QRadioButton(self.centralwidget)
        self.mp_20kg.setGeometry(QtCore.QRect(50, 260, 82, 17))
        self.mp_20kg.setObjectName("mp_20kg")
        self.mp_10kg = QtWidgets.QRadioButton(self.centralwidget)
        self.mp_10kg.setGeometry(QtCore.QRect(50, 230, 82, 17))
        self.mp_10kg.setObjectName("mp_10kg")
        self.calc_stamps_button = QtWidgets.QToolButton(self.centralwidget)
        self.calc_stamps_button.setGeometry(QtCore.QRect(20, 290, 111, 41))
        self.calc_stamps_button.setObjectName("calc_stamps_button")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(150, 30, 256, 192))
        self.textBrowser.setObjectName("textBrowser")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 438, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Stamp Calculator"))
        self.small_parcel_label.setText(_translate("MainWindow", "Small Parcel"))
        self.sp_1kg.setText(_translate("MainWindow", "1kg"))
        self.sp_2kg.setText(_translate("MainWindow", "2kg"))
        self.mp_2kg.setText(_translate("MainWindow", "2kg"))
        self.mp_1kg.setText(_translate("MainWindow", "1kg"))
        self.meidum_parcel_label.setText(_translate("MainWindow", "Medium Parcel"))
        self.mp_5kg.setText(_translate("MainWindow", "5kg"))
        self.mp_20kg.setText(_translate("MainWindow", "20kg"))
        self.mp_10kg.setText(_translate("MainWindow", "10kg"))
        self.calc_stamps_button.setText(_translate("MainWindow", "Calculate Stamps"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

