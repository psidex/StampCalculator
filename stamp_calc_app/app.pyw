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
        package_value = round(package_value, 2)
        biggest = round(Decimal(0.00), 2)
        for stamp in self.stamp_dict:
            d_val = round(Decimal(self.stamp_dict[stamp]["value"]), 2)
            if d_val > biggest and d_val <= package_value:
                biggest = d_val
        return biggest

    def get_lowest_stamp(self):
        val_lis = []
        for stamp in self.stamp_dict:
            val_lis.append(self.stamp_dict[stamp]["value"])
        return round(Decimal(min(val_lis)), 2)

    def count_stamps(self, used):
        names_amounts = {}
        for stamp_value in used:
            nom = j_b.get_name_by_value(self.stamp_dict, stamp_value)
            if nom in names_amounts:
                names_amounts[nom] += 1
            else:
                names_amounts[nom] = 1
        return names_amounts

    def calculate(self):
        self.result_list.clear()
        used = []
        # Only 1 radio can be checked at once
        for radio in self.weight_lookup:
            if radio.isChecked():
                package_value = self.weight_lookup[radio]
                preserved_package_value = package_value
                for stamp in self.stamp_dict:
                    """
                    If package has same price as value of one of the stamps
                    """
                    if self.stamp_dict[stamp]["value"] == package_value:
                        self.result_label.setText("Postage = £" + str(round(preserved_package_value, 2)))
                        self.result_list.addItem(str(self.stamp_dict[stamp]["value"]))
                        return
                while package_value > 0:
                    package_value = round(package_value, 2)  # Not sure why but it gets turned to a horrible float somewhere
                    highest = self.get_highest_stamp_below_value(package_value)
                    if highest == 0:
                        """
                        If there is no stamp that first inbetween postage &
                        current worked out value, get the lowest value stamp and use that
                        """
                        lowest_stamp = self.get_lowest_stamp()
                        used.append(lowest_stamp)
                        names = self.count_stamps(used)
                        self.result_label.setText("Postage = £" + str(round(preserved_package_value, 2)))
                        for name in names:
                            output = name + " x " + str(names[name])
                            self.result_list.addItem(output)
                        return
                    package_value -= highest
                    used.append(highest)
                """
                Package value has been worked out exactly with current stamps
                (for example £0.25 * 2 stamps for a £0.50 package)
                """
                names = self.count_stamps(used)
                self.result_label.setText("Postage = £" + str(round(preserved_package_value, 2)))
                for name in names:
                    output = name + " x " + str(names[name])
                    self.result_list.addItem(output)

    def load_values(self):
        self.current_stamps_list.clear()
        # Pull stamps from config file and list them (sorted lowest value first)
        for item in sorted(j_b.get_all_names(self.stamp_dict)):
            self.current_stamps_list.addItem(item)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QMainWindow()
    prog = stamp_calc_main_app(dialog)
    dialog.show()
    app.exec_()
    sys.exit()
