from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from stamp_calc_ui import Ui_MainWindow
import json_bridge as j_b
import sys

class stamp_calc_main_app(Ui_MainWindow):
    def __init__(self, dialog):
        Ui_MainWindow.__init__(self)
        self.setupUi(dialog)
        self.stamp_dict = j_b.get_dict_from_file("stamps.json")
        self.load_values()

        self.weight_lookup = {
            self.sp_1kg: 3.4,
            self.sp_2kg: 5.5,
            self.mp_1kg: 5.7,
            self.mp_2kg: 8.95,
            self.mp_5kg: 15.85,
            self.mp_10kg: 21.9,
            self.mp_20kg: 33.4
        }

        self.calc_stamps_button.clicked.connect(self.calculate)

    def calculate(self):
        used = []
        # Only 1 radio can be checked at once
        for radio in self.weight_lookup:
            if radio.isChecked():
                package_value = self.weight_lookup[radio]

    def load_values(self):
        # Pull stamps from config file and list them
        for item in j_b.get_all_names(self.stamp_dict):
            amount = str(j_b.get_amount(self.stamp_dict, item))
            self.current_stamps_list.addItem(item + " x " + amount)

    def save(self):
        j_b.dump_dict_to_file(self.stamp_dict, "stamps.json")
        self.popup("Sucess", "Save to stamps.json", "sucessful",
                   QMessageBox.Information, None, False)

    def popup(self, window_title, title, message, icon, action, exit):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setWindowTitle(window_title)
        msg.setText(title)
        msg.setInformativeText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        if action:
            msg.buttonClicked.connect(action)
        if exit:
            sys.exit(msg.exec_())
        else:
            msg.exec_()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QMainWindow()
    prog = stamp_calc_main_app(dialog)
    dialog.show()
    app.exec_()
    prog.save()
    sys.exit()
