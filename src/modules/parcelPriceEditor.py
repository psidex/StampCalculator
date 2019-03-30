from gui.parcelPriceEditor import Ui_Dialog


class parcelPriceEditor(Ui_Dialog):
    def __init__(self, dialog, stampData):
        super().__init__()
        self.setupUi(dialog)

        self.stampData = stampData
        self.accepted = False
        self.error = False
        self.errMsg = ""

        # All the line edits, in order
        self.lineEdits = [
            self.smallParcel1kgLineEdit,
            self.smallParcel2kgLineEdit,
            self.mediumParcel1kgLineEdit,
            self.mediumParcel2kgLineEdit,
            self.mediumParcel5kgLineEdit,
            self.mediumParcel10kgLineEdit,
            self.mediumParcel20kgLineEdit,
        ]
        # All of the dictionary keys for the parcel prices, same order as above
        self.parcelPriceKeys = [
            "smallParcel1kg",
            "smallParcel2kg",
            "mediumParcel1kg",
            "mediumParcel2kg",
            "mediumParcel5kg",
            "mediumParcel10kg",
            "mediumParcel20kg",
        ]

        self.buttonBox.accepted.connect(self.acceptBtnPressed)

        self.populateLineEdits()

    def populateLineEdits(self):
        """
        For each line edit, set it's value to the corresponding value in the parcel
        price dictionary
        """
        stampPrices = self.stampData["parcelPrices"]

        for index, lineEdit in enumerate(self.lineEdits):
            lineEdit.setText(str(stampPrices[self.parcelPriceKeys[index]]))

    def acceptBtnPressed(self):
        if self.checkValues():
            self.accepted = True
        else:
            self.error = True

    def checkValues(self):
        for lineEdit in self.lineEdits:
            lineText = lineEdit.text()
            if lineText.strip() == "":
                self.errMsg = "Parcel price value cannot be empty"
                return False
            try:
                int(lineText)
            except ValueError:
                self.errMsg = f"{lineText} is an invalid value for parcel price"
                return False
        return True
