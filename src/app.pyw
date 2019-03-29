from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QDialog
import sys
import json
from modules.stampMaths import calcStampAmount
from modules.parcelPriceEditor import parcelPriceEditor
from gui.stampCalculatorUI import Ui_MainWindow

stampDataPath = "stampData.json"


class StampCalculatorApp(Ui_MainWindow):
    def __init__(self, dialog):
        try:
            # Get stampData
            with open(stampDataPath, "r") as jsonIn:
                self.stampData = json.load(jsonIn)
        except FileNotFoundError:
            # No point doing anything unless stampDataPath exists
            self.popup("Fatal Error", f"{stampDataPath} not found", exit=True)

        # Init UI
        Ui_MainWindow.__init__(self)
        self.setupUi(dialog)

        # Do this once now so it can be used later (such as in popup windows)
        self.windowIcon = QtGui.QIcon()
        # :/ is the path for resource files
        self.windowIcon.addPixmap(QtGui.QPixmap(":/Icons/stamp.ico"))

        # For iterating over later
        self.packageRadioButtons = [
            self.smallParcel1kgRadio,
            self.smallParcel2kgRadio,
            self.mediumParcel1kgRadio,
            self.mediumParcel2kgRadio,
            self.mediumParcel5kgRadio,
            self.mediumParcel10kgRadio,
            self.mediumParcel20kgRadio,
        ]

        # Connect UI elements up to class methods
        self.saveChangesBtn.clicked.connect(self.saveStampData)
        self.addNewStampBtn.clicked.connect(self.addNewStamp)
        self.rmveSelectedStampBtn.clicked.connect(self.removeSelectedStamp)
        self.calcStampsToUseBtn.clicked.connect(self.calculateStampsToUse)
        self.editParcelPricesBtn.clicked.connect(self.openParcelPriceEditor)

        # Update UI with current data
        self.updateGuiStampList()

    def openParcelPriceEditor(self):
        # Remove "?" button from the title bar, give default(ish) flags to QDialog
        dialoug = QDialog(
            None,
            QtCore.Qt.WindowSystemMenuHint
            | QtCore.Qt.WindowTitleHint
            | QtCore.Qt.WindowCloseButtonHint,
        )
        priceEditor = parcelPriceEditor(dialoug, self.stampData)
        dialoug.exec_()

        if not priceEditor.cancelled:
            # Update packagePrices with the values from the price editor
            self.stampData["packagePrices"]["smallParcel1kgRadio"] = int(
                priceEditor.smallParcel1kgLineEdit.text()
            )
            self.stampData["packagePrices"]["smallParcel2kgRadio"] = int(
                priceEditor.smallParcel2kgLineEdit.text()
            )
            self.stampData["packagePrices"]["mediumParcel1kgRadio"] = int(
                priceEditor.mediumParcel1kgLineEdit.text()
            )
            self.stampData["packagePrices"]["mediumParcel2kgRadio"] = int(
                priceEditor.mediumParcel2kgLineEdit.text()
            )
            self.stampData["packagePrices"]["mediumParcel5kgRadio"] = int(
                priceEditor.mediumParcel5kgLineEdit.text()
            )
            self.stampData["packagePrices"]["mediumParcel10kgRadio"] = int(
                priceEditor.mediumParcel10kgLineEdit.text()
            )
            self.stampData["packagePrices"]["mediumParcel20kgRadio"] = int(
                priceEditor.mediumParcel20kgLineEdit.text()
            )

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
        Update GUI with calculated Postage and used (and sorted) stamps
        """
        names = self.countStamps(used)
        # https://stackoverflow.com/a/15238187/6396652
        self.postageResultLabel.setText("£{:.2f}".format(packageValue / 100))
        for name in reversed(sorted(names)):
            output = name + " x " + str(names[name])
            self.postageResultStampList.addItem(output)

    def calculateStampsToUse(self):
        """
        Calculate the stamps to use and update GUI
        """
        for radio in self.packageRadioButtons:
            # Only one will return True
            if radio.isChecked():
                self.postageResultStampList.clear()

                aimPrice = self.stampData["packagePrices"][radio.objectName()]
                preservedPackageValue = aimPrice
                availableStamps = [v for k, v in self.stampData["userStamps"].items()]

                try:
                    calculatedStampList = calcStampAmount(aimPrice, availableStamps)
                    self.updateCalculatedStampsGui(
                        calculatedStampList, preservedPackageValue
                    )
                except ValueError:
                    self.popup(
                        "Value Error", "No stamps available", QMessageBox.Critical
                    )

    """
    Configuration Methods
    """

    def addNewStamp(self):
        """
        Add a new stamp to self.stampData["userStamps"] and update the GUI
        """
        newStampName = self.newStampNameLineEdit.text()
        if newStampName.strip() == "":
            self.popup("Value Error", "No stamp name", QMessageBox.Critical)
            return

        try:
            newStampValue = int(self.newStampValueLineEdit.text())
        except ValueError:
            self.popup("Value Error", "Stamp value must be int", QMessageBox.Critical)
            return

        # Add new stamp and update GUI
        self.stampData["userStamps"][newStampName] = newStampValue
        self.newStampNameLineEdit.clear()
        self.newStampValueLineEdit.clear()
        self.updateGuiStampList()

    def removeSelectedStamp(self):
        """
        Remove a stamp from self.stampData["userStamps"] and update the GUI
        """
        for item in self.currentOwnedStampsList.selectedItems():
            removeStampName = item.text()
            del self.stampData["userStamps"][removeStampName]
        self.updateGuiStampList()

    """
    Utility Methods
    """

    def updateGuiStampList(self):
        """
        Update the GUI current owned stamp list (sorted lowest value first)
        """
        self.currentOwnedStampsList.clear()
        for item in sorted([n for n in self.stampData["userStamps"]]):
            self.currentOwnedStampsList.addItem(item)

    def saveStampData(self, *args, successPopup=True):
        """
        Save self.stampData to a JSON file
        *args because button.click events send arguments to the called method
        """
        try:
            with open(stampDataPath, "w") as jsonOut:
                json.dump(self.stampData, jsonOut)
            if successPopup:
                self.popup("Success", f"Save to {stampDataPath} was sucessful")
        except IOError:
            self.popup("Error", f"IOError: Cannot save to {stampDataPath}")

    def popup(self, title, message, icon=QMessageBox.Information, exit=False):
        """
        Create a Qt5 "popup" window
        """
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setWindowIcon(self.windowIcon)
        msg.setWindowTitle("Stamp Calculator")
        msg.setText(title)
        msg.setInformativeText(message)
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
    # Save on exit (don't alert user if successful)
    prog.saveStampData(successPopup=False)
    sys.exit()
