from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from stamp_calc_ui import Ui_MainWindow
import json_bridge as j_b
import sys

class stamp_calc_main_app(Ui_MainWindow):
    def __init__(self, dialog):
        Ui_MainWindow.__init__(self)
        self.setupUi(dialog)

        self.weight_lookup = {
            self.sp_1kg: 340,
            self.sp_2kg: 550,
            self.mp_1kg: 570,
            self.mp_2kg: 895,
            self.mp_5kg: 1585,
            self.mp_10kg: 2190,
            self.mp_20kg: 3340
        }

        self.save_changes_btn.clicked.connect(self.save)
        self.add_new_stamp_btn.clicked.connect(self.add_new_stamp)
        self.rmv_selected_btn.clicked.connect(self.remove_selected_stamp)
        self.calc_stamps_button.clicked.connect(self.calculate)

        self.stamp_dict = j_b.get_dict_from_file("stamps.json")
        self.load_values()

    def flatten_used(self, used):
        """ == WIP ==
        For example:
        used = ["£0.2":2, "£0.4":3]
        into
        used = ["£0.4":4]
        """
        print(used)
        return used

    def get_highest_stamp_below_value(self, package_value):
        package_value = package_value
        biggest = 0
        for stamp in self.stamp_dict:
            d_val = self.stamp_dict[stamp]["value"]
            if d_val > biggest and d_val <= package_value:
                biggest = d_val
        return biggest

    def get_lowest_stamp(self):
        val_lis = []
        for stamp in self.stamp_dict:
            val_lis.append(self.stamp_dict[stamp]["value"])
        return min(val_lis)

    def count_stamps(self, used):
        names_amounts = {}
        for stamp_value in used:
            nom = j_b.get_name_by_value(self.stamp_dict, stamp_value)
            if nom in names_amounts:
                names_amounts[nom] += 1
            else:
                names_amounts[nom] = 1
        return names_amounts

    def output_calculated(self, used_param, preserved_package_value):
        #
        used = self.flatten_used(used_param)
        #
        names = self.count_stamps(used)
        self.result_label.setText("Postage = £" + str(preserved_package_value/100))
        for name in reversed(sorted(names)):
            output = name + " x " + str(names[name])
            self.result_list.addItem(output)

    def calculate(self):
        self.result_list.clear()
        used = []
        for radio in self.weight_lookup:
            if radio.isChecked():
                package_value = self.weight_lookup[radio]
                preserved_package_value = package_value
                for stamp in self.stamp_dict:
                    """
                    If package has same price as value of one of the stamps
                    """
                    if self.stamp_dict[stamp]["value"] == package_value:
                        self.result_label.setText("Postage = £" + str(preserved_package_value/100))
                        self.result_list.addItem(str(stamp) + " x 1")
                        return  # Exit method
                while package_value > 0:
                    highest = self.get_highest_stamp_below_value(package_value)
                    if highest == 0:
                        """
                        If there is no stamp that first inbetween postage &
                        current worked out value, get the lowest value stamp and use that
                        """
                        lowest_stamp = self.get_lowest_stamp()
                        used.append(lowest_stamp)
                        self.output_calculated(used, preserved_package_value)
                        return  # Exit method
                    package_value -= highest
                    used.append(highest)
                """
                Package value has been worked out exactly with current stamps
                (for example £0.25 * 2 stamps for a £0.50 package)
                """
                self.output_calculated(used, preserved_package_value)

    def load_values(self):
        self.current_stamps_list.clear()
        # Pull stamps from config file and list them (sorted lowest value first)
        for item in sorted(j_b.get_all_names(self.stamp_dict)):
            self.current_stamps_list.addItem(item)

    """ == CONFIG METHODS [BELOW] == """

    def add_new_stamp(self):
        item_name = self.new_stamp_name_line_edit.text()

        try:
            item_value = int(self.new_stamp_value_line_edit.text())
        except ValueError:
            self.popup("Value Error", "Stamp value", "Value must be int", QMessageBox.Critical)
        else:
            self.stamp_dict[item_name] = {"value": item_value}

        self.new_stamp_name_line_edit.clear()
        self.new_stamp_value_line_edit.clear()
        self.load_values()

    def remove_selected_stamp(self):
        for item in self.current_stamps_list.selectedItems():
            item_name = item.text()
            del self.stamp_dict[item_name]
        self.load_values()

    def save(self):
        j_b.dump_dict_to_file(self.stamp_dict, "stamps.json")
        self.popup("Success", "Save to stamps.json", "Sucessful")

    def popup(self, window_title, title, message, icon=QMessageBox.Information):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setWindowTitle(window_title)
        msg.setText(title)
        msg.setInformativeText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QMainWindow()
    prog = stamp_calc_main_app(dialog)
    dialog.show()
    app.exec_()
    prog.save()  # Save on exit
    sys.exit()
