from gui.parcelPriceEditor import Ui_Dialog

# TODO: Check that the price values aren't blank before saving to dict


class parcelPriceEditor(Ui_Dialog):
    def __init__(self, dialog, stampData):
        super().__init__()
        self.setupUi(dialog)

        self.stampData = stampData
        self.cancelled = False

        self.buttonBox.rejected.connect(self.cancelBtnPressed)

        # Pretty hacky, probably a better way to do this
        dialog.closeEvent = self.closeEvent

        self.populateLineEdits()

    def populateLineEdits(self):
        stampPrices = self.stampData["packagePrices"]
        self.smallParcel1kgLineEdit.setText(str(stampPrices["smallParcel1kgRadio"]))
        self.smallParcel2kgLineEdit.setText(str(stampPrices["smallParcel2kgRadio"]))
        self.mediumParcel1kgLineEdit.setText(str(stampPrices["mediumParcel1kgRadio"]))
        self.mediumParcel2kgLineEdit.setText(str(stampPrices["mediumParcel2kgRadio"]))
        self.mediumParcel5kgLineEdit.setText(str(stampPrices["mediumParcel5kgRadio"]))
        self.mediumParcel10kgLineEdit.setText(str(stampPrices["mediumParcel10kgRadio"]))
        self.mediumParcel20kgLineEdit.setText(str(stampPrices["mediumParcel20kgRadio"]))

    def cancelBtnPressed(self):
        self.cancelled = True

    def closeEvent(self, evnt):
        self.cancelled = True
