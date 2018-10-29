from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from ui.StampCalculatorUI import Ui_MainWindow
from modules.stampMaths import calcStampAmount
import sys
import json

stampDataPath = "stampData.json"

class StampCalculatorApp(Ui_MainWindow):
    def __init__(self, dialog):
        try:
            # Setup stampData
            with open(stampDataPath, "r") as jsonIn:
                self.stampData = json.load(jsonIn)
        except FileNotFoundError:
            # No point doing anything unless stamps.json exists
            self.popup("Fatal Error", "stampData.json", "not found", exit=True)

        # TODO: Remove this quick fix
        self.stamp_dict = self.stampData["userStamps"]

        # Init UI
        Ui_MainWindow.__init__(self)
        self.setupUi(dialog)

        self.packageRadioButtons = [
            self.sp_1kg, self.sp_2kg, self.mp_1kg, self.mp_2kg, self.mp_5kg,
            self.mp_10kg, self.mp_20kg
        ]

        # Connect UI elements up to class methods
        self.save_changes_btn.clicked.connect(self.save)
        self.add_new_stamp_btn.clicked.connect(self.add_new_stamp)
        self.rmv_selected_btn.clicked.connect(self.remove_selected_stamp)
        self.calc_stamps_button.clicked.connect(self.calculateStampsToUse)

        # Update UI with current data
        self.load_values()

    def count_stamps(self, usedList):
        """
        Count the number of times each stamp occurs in a list
        usedList is a list of used stamp values: [340, 340]
        Returns a dict of stamp name + amount used: {"£3.40": 2}
        """
        namedAmounts = {}
        for currentStampValue in usedList:
            # TODO: Optimise this (shouldn't iterate this every time)
            for stampName, stampValue in self.stamp_dict.items():
                if stampValue == currentStampValue:
                    if stampName in namedAmounts:
                        namedAmounts[stampName] += 1
                    else:
                        namedAmounts[stampName] = 1
        return namedAmounts

    def output_calculated(self, used, package_val):
        """
        Update GUI with calculated Postage and used stamps
        """
        names = self.count_stamps(used)
        # https://stackoverflow.com/a/15238187/6396652
        self.result_label.setText("Postage = £{:.2f}".format(package_val/100))
        for name in reversed(sorted(names)):
            output = name + " x " + str(names[name])
            self.result_list.addItem(output)

    def calculateStampsToUse(self):
        """
        Calculate the stamps to use and update GUI
        """
        for radio in self.packageRadioButtons:
            # Only one will return True
            if radio.isChecked():
                self.result_list.clear()

                aimPrice = self.stampData["packagePrices"][radio.objectName()]
                preserved_package_value = aimPrice
                availableStamps = [v for k,v in self.stamp_dict.items()]

                try:
                    calculatedStampList = calcStampAmount(aimPrice,
                        availableStamps)
                    self.output_calculated(calculatedStampList,
                        preserved_package_value)
                except ValueError:
                    self.popup("Value Error", "No stamps available",
                        "Add some to stock", QMessageBox.Critical)

    """
        == CONFIG METHODS ==
    """

    def add_new_stamp(self):
        """
        Add a new stamp to self.stamp_dict and update the GUI
        """
        item_name = self.new_stamp_name_line_edit.text()

        try:
            item_value = int(self.new_stamp_value_line_edit.text())
        except ValueError:
            self.popup("Value Error", "Stamp value", "Value must be int",
                QMessageBox.Critical)
        else:
            self.stamp_dict[item_name] = {"value": item_value}

        self.new_stamp_name_line_edit.clear()
        self.new_stamp_value_line_edit.clear()
        self.load_values()

    def remove_selected_stamp(self):
        """
        Remove a stamp from self.stamp_dict and update the GUI
        """
        for item in self.current_stamps_list.selectedItems():
            item_name = item.text()
            del self.stamp_dict[item_name]
        self.load_values()

    """
        == UTILITY METHODS ==
    """

    def load_values(self):
        """
        Update the GUI stamp list (sorted lowest value first)
        """
        self.current_stamps_list.clear()
        for item in sorted([n for n in self.stamp_dict]):
            self.current_stamps_list.addItem(item)

    def save(self):
        """
        Save self.stampData to a JSON file
        """
        try:
            with open(stampDataPath, "w") as jsonOut:
                json.dump(self.stampData, jsonOut)
            self.popup("Success", "Save to stamps.json", "Sucessful")
        except IOError:
            self.popup("Error", "IOError", "Cannot save to stamps.json")

    def popup(self, windowTitle, title, message, icon=QMessageBox.Information, exit=False):
        """
        Create a Qt5 "popup" window
        """
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setWindowTitle(windowTitle)
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
    # Save on exit
    prog.save()
    sys.exit()
