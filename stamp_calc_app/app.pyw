from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from stamp_calc_ui import Ui_MainWindow
from decimal import Decimal
import json_bridge as j_b
import sys

class stamp_calc_main_app(Ui_MainWindow):
    def __init__(self, dialog):
        Ui_MainWindow.__init__(self)
        self.setupUi(dialog)
        self.stamp_dict = j_b.get_dict_from_file("stamps.json")
        self.load_values()

        self.weight_lookup = {
            self.sp_1kg: Decimal(3.4),
            self.sp_2kg: Decimal(5.5),
            self.mp_1kg: Decimal(5.7),
            self.mp_2kg: Decimal(8.95),
            self.mp_5kg: Decimal(15.85),
            self.mp_10kg: Decimal(21.9),
            self.mp_20kg: Decimal(33.4)
        }

        self.calc_stamps_button.clicked.connect(self.calculate)

    def get_highest_stamp_below_value(self, package_value):
        biggest = Decimal(0.0)
        for stamp in self.stamp_dict:
            d_val = Decimal(self.stamp_dict[stamp]["value"])
            # Round values to compare them but dont actually change the variables
            if round(d_val, 2) > round(biggest, 2) and round(d_val, 2) < round(package_value, 2):
                biggest = d_val
        return biggest

    def get_lowest_stamp(self):
        val_lis = []
        for stamp in self.stamp_dict:
            val_lis.append(self.stamp_dict[stamp]["value"])
        return Decimal(min(val_lis))

    def count_stamps(self, used):
        names_amounts = {}
        for stamp_value in used:
            nom = j_b.get_name_by_value(self.stamp_dict, stamp_value)
            if nom in names_amounts:
                names_amounts[nom] += 1
            else:
                names_amounts[nom] = 1
        print(names_amounts)
        return names_amounts

    def calculate(self):
        """NEED TO ADD REMOVING STAMPS FROM STAMP DICT WHEN USED IN CALCULATION"""
        self.result_list.clear()
        used = []
        # Only 1 radio can be checked at once
        for radio in self.weight_lookup:
            if radio.isChecked():
                package_value = self.weight_lookup[radio]
                preserved_package_value = package_value
                for stamp in self.stamp_dict:
                    if self.stamp_dict[stamp]["value"] == package_value:
                        """ADD REMOVE HERE"""
                        self.result_list.addItem(str(preserved_package_value))
                        self.result_list.addItem(str(self.stamp_dict[stamp]["value"]))
                        return
                while package_value > 0:
                    highest = self.get_highest_stamp_below_value(package_value)
                    if highest == 0:
                        """ADD REMOVE HERE"""
                        used.append(self.get_lowest_stamp())
                        self.result_list.addItem(str(round(preserved_package_value, 2)))
                        names = self.count_stamps(used)
                        for name in names:
                            output = name + " x " + str(names[name])
                            self.result_list.addItem(output)
                        return
                    package_value -= highest
                    """ADD REMOVE HERE"""
                    used.append(highest)
                self.result_list.addItem(str(round(preserved_package_value, 2)))
                names = self.count_stamps(used)
                for name in names:
                    output = name + " x " + str(names[name])
                    self.result_list.addItem(output)

    def load_values(self):
        self.current_stamps_list.clear()
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
