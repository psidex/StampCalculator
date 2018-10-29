from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from ui.StampCalculatorUI import Ui_MainWindow
from modules.stampMaths import calcStampAmount
import sys
import json

stampDataPath = "stampData.json"

class StampCalculatorApp(Ui_MainWindow):
    def __init__(self, dialog):
        # Setup stampData
        try:
            with open(stampDataPath, "r") as jsonIn:
                self.stampData = json.load(jsonIn)
        except FileNotFoundError:
            # No point doing anything unless stamps.json exists
            self.popup("Fatal Error", "stampData.json", "not found", exit=True)

        # Init UI
        Ui_MainWindow.__init__(self)
        self.setupUi(dialog)

        # Maps radio buttons to package prices
        self.weight_lookup = {
            self.sp_1kg: 345,
            self.sp_2kg: 550,
            self.mp_1kg: 575,
            self.mp_2kg: 895,
            self.mp_5kg: 1585,
            self.mp_10kg: 2190,
            self.mp_20kg: 3340
        }

        # Connect UI elements up to class methods
        self.save_changes_btn.clicked.connect(self.save)
        self.add_new_stamp_btn.clicked.connect(self.add_new_stamp)
        self.rmv_selected_btn.clicked.connect(self.remove_selected_stamp)
        self.calc_stamps_button.clicked.connect(self.calculate)

        # Update UI with current data
        self.load_values()

    """ == CALCULATION METHODS [BELOW] == """

    def count_stamps(self, used):
        names_amounts = {}
        for stamp_value in used:
            nom = jb.get_name_by_value(self.stamp_dict, stamp_value)
            if nom in names_amounts:
                names_amounts[nom] += 1
            else:
                names_amounts[nom] = 1
        return names_amounts

    def output_calculated(self, used, package_val):
        names = self.count_stamps(used)
        # https://stackoverflow.com/a/15238187/6396652
        self.result_label.setText("Postage = £" + "{:.2f}".format(package_val/100))
        for name in reversed(sorted(names)):
            output = name + " x " + str(names[name])
            self.result_list.addItem(output)

    def calculate(self):
        for radio in self.weight_lookup:
            # Only one return True
            if radio.isChecked():
                self.result_list.clear()
                """
                Work out in multiple different ways and choose the one with
                the least stamps
                """
                aimPrice = self.weight_lookup[radio]
                preserved_package_value = aim_price
                availableStamps = [v["value"] for k,v in self.stamp_dict.items()]

                try:
                    calculatedStampList = calcStampAmount(aimPrice, availableStamps)
                    self.output_calculated(calculatedStampList, preserved_package_value)
                except ValueError:
                    self.popup("Value Error", "No stamps available", "Add some to stock", QMessageBox.Critical)

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

    """ == UTILITY METHODS [BELOW] == """

    def load_values(self):
        self.current_stamps_list.clear()
        # Pull stamps from stamp array and list them (sorted lowest value first)
        for item in sorted([n for n in self.stamp_dict]):
            self.current_stamps_list.addItem(item)

    def save(self):
        try:
            with open(stampDataPath, "w") as jsonOut:
                json.dump(self.stampData, jsonOut)
            self.popup("Success", "Save to stamps.json", "Sucessful")
        except IOError:
            self.popup("Error", "IOError", "Cannot save to stamps.json")

    def popup(self, window_title, title, message, icon=QMessageBox.Information, exit=False):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setWindowTitle(window_title)
        msg.setText(title)
        msg.setInformativeText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        if exit:
            sys.exit(msg.exec_())
        else:
            msg.exec_()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QMainWindow()
    prog = StampCalculatorApp(dialog)
    dialog.show()
    app.exec_()
    prog.save()  # Save on exit
    sys.exit()
