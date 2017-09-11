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
        self.rmv_selected_btn.clicked.connect(self.remove_selected_stamp)
        self.load_values()

    def load_values(self):
        self.curr_stamps_list.clear()
        # Pull stamps from config file and list them
        for item in j_b.get_all_names(self.stamp_dict):
            self.curr_stamps_list.addItem(item)

    def add_new_stamp(self):
        item_name = self.new_stamp_name_line_edit.text()

        try:
            item_value = float(self.new_stamp_value_line_edit.text())
        except ValueError:
            self.popup("Value Error", "Stamp value", "Value must be float", QMessageBox.Critical)
        else:
            self.stamp_dict[item_name] = {"value": item_value}

        self.new_stamp_name_line_edit.clear()
        self.new_stamp_value_line_edit.clear()
        self.load_values()

    def remove_selected_stamp(self):
        for item in self.curr_stamps_list.selectedItems():
            item_name = item.text()
            del self.stamp_dict[item_name]
        self.load_values()

    def save(self):
        j_b.dump_dict_to_file(self.stamp_dict, "stamps.json")
        self.popup("Sucess", "Save to stamps.json", "sucessful")

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
    prog = config_setup_main_app(dialog)
    dialog.show()
    app.exec_()
    prog.save()
    sys.exit()
