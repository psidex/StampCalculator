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
            # No point doing anything unless stampDataPath exists
            self.popup("Fatal Error", stampDataPath, "not found", exit=True)

        # Init UI
        Ui_MainWindow.__init__(self)
        self.setupUi(dialog)

        self.packageRadioButtons = [
            self.smallParcel1kgRadio, self.smallParcel2kgRadio,
            self.mediumParcel1kgRadio, self.mediumParcel2kgRadio,
            self.mediumParcel5kgRadio, self.mediumParcel10kgRadio,
            self.mediumParcel20kgRadio
        ]

        # Connect UI elements up to class methods
        self.save_changes_btn.clicked.connect(self.saveStampData)
        self.add_new_stamp_btn.clicked.connect(self.addNewStamp)
        self.rmv_selected_btn.clicked.connect(self.removeSelectedStamp)
        self.calc_stamps_btn.clicked.connect(self.calculateStampsToUse)

        # Update UI with current data
        self.updateGuiStampList()

    def countStamps(self, usedList):
        """
        Count the number of times each stamp occurs in a list
        usedList is a list of used stamp values: [340, 340]
        Returns a dict of stamp name + amount used: {"£3.40": 2}
        """
        namedAmounts = {}
        for currentStampValue in usedList:
            # TODO: Optimise this (shouldn't iterate this every time)
            for stampName, stampValue in self.stampData["userStamps"].items():
                if stampValue == currentStampValue:
                    if stampName in namedAmounts:
                        namedAmounts[stampName] += 1
                    else:
                        namedAmounts[stampName] = 1
        return namedAmounts

    def updateCalculatedStampsGui(self, used, packageValue):
        """
        Update GUI with calculated Postage and used stamps
        """
        names = self.countStamps(used)
        # https://stackoverflow.com/a/15238187/6396652
        self.result_label.setText("Postage\n£{:.2f}".format(packageValue/100))
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
                preservedPackageValue = aimPrice
                availableStamps = [v for k,v in self.stampData["userStamps"].items()]

                try:
                    calculatedStampList = calcStampAmount(aimPrice,
                        availableStamps)
                    self.updateCalculatedStampsGui(calculatedStampList,
                        preservedPackageValue)
                except ValueError:
                    self.popup("Value Error", "No stamps available",
                        "Add some to stock", QMessageBox.Critical)

    """
        == CONFIG METHODS ==
    """

    def addNewStamp(self):
        """
        Add a new stamp to self.stampData["userStamps"] and update the GUI
        """
        item_name = self.new_stamp_name_line_edit.text()

        try:
            item_value = int(self.new_stamp_value_line_edit.text())
        except ValueError:
            self.popup("Value Error", "Stamp value", "Value must be int",
                QMessageBox.Critical)
        else:
            self.stampData["userStamps"][item_name] = {"value": item_value}

        self.new_stamp_name_line_edit.clear()
        self.new_stamp_value_line_edit.clear()
        self.updateGuiStampList()

    def removeSelectedStamp(self):
        """
        Remove a stamp from self.stampData["userStamps"] and update the GUI
        """
        for item in self.current_stamps_list.selectedItems():
            item_name = item.text()
            del self.stampData["userStamps"][item_name]
        self.updateGuiStampList()

    """
        == UTILITY METHODS ==
    """

    def updateGuiStampList(self):
        """
        Update the GUI stamp list (sorted lowest value first)
        """
        self.current_stamps_list.clear()
        for item in sorted([n for n in self.stampData["userStamps"]]):
            self.current_stamps_list.addItem(item)

    def saveStampData(self):
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
    prog.saveStampData()
    sys.exit()
