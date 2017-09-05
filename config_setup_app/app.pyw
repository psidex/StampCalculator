from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from config_setup_ui import Ui_MainWindow
import json_bridge as j_b
import sys

class config_setup_main_app(Ui_MainWindow):
    def __init__(self, dialog):
        Ui_MainWindow.__init__(self)
        self.setupUi(dialog)
        self.stamp_dict = j_b.get_dict_from_file("stamps.json")
        self.save_changes_btn.clicked.connect(self.save)
        self.add_new_stamp_btn.clicked.connect(self.add_new_stamp)
        self.rmv_selected_btn.clicked.connect(self.remove_item_amount)
        self.load_values()

    def load_values(self):
        self.curr_stamps_list.clear()
        self.amount_stamps_list.clear()
        # Pull stamps from config file and list them
        for item in j_b.get_all_names(self.stamp_dict):
            self.curr_stamps_list.addItem(item)
            amount = str(j_b.get_amount(self.stamp_dict, item))
            self.amount_stamps_list.addItem(amount)

    def add_new_stamp(self):
        item_name = self.new_stamp_name_line_edit.text()

        try:
            item_amount = int(self.new_stamp_amount_line_edit.text())
        except ValueError:
            self.popup("Value Error", "Amount to add must be integer",
                "", QMessageBox.Critical, None, False)
        else:
            item_value = self.new_stamp_value_line_edit.text()
            self.stamp_dict[item_name] = {"value": item_value, "amount": item_amount}
        self.load_values()

    def remove_item_amount(self):
        # There can only ever be 1 selected item
        for item in self.curr_stamps_list.selectedItems():
            item_name = item.text()
            item_amount = j_b.get_amount(self.stamp_dict, item_name)

            try:
                to_remove = int(self.rmv_stamp_amount_line_edit.text())
            except ValueError:
                self.popup("Value Error", "Amount to remove must be integer",
                    "", QMessageBox.Critical, None, False)
            else:
                if to_remove == item_amount:
                    del self.stamp_dict[item_name]
                    self.popup("No more of " + item_name, item_name, "removed",
                               QMessageBox.Warning, None, False)
                elif to_remove > item_amount:
                    self.popup("Value Error", "Amount to remove higher than stamp amount",
                        "", QMessageBox.Critical, None, False)
                else:
                    self.stamp_dict[item_name]["amount"] -= to_remove
        self.load_values()

    def save(self):
        j_b.dump_dict_to_file(self.stamp_dict, "stamps.json")

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
    prog = config_setup_main_app(dialog)
    dialog.show()
    sys.exit(app.exec_())
