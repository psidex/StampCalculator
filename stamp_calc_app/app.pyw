from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from stamp_calc_ui import Ui_MainWindow
import json_bridge as jb
import sys

class stamp_calc_main_app(Ui_MainWindow):
    def __init__(self, dialog):
        try:
            self.stamp_dict = jb.get_dict_from_file("stamps.json")
        except FileNotFoundError:
            # No point doing anything unless stamps.json exists
            self.popup("Fatal Error", "stamps.json", "not found", exit=True)

        Ui_MainWindow.__init__(self)
        self.setupUi(dialog)

        self.weight_lookup = {
            self.sp_1kg: 345,
            self.sp_2kg: 550,
            self.mp_1kg: 575,
            self.mp_2kg: 895,
            self.mp_5kg: 1585,
            self.mp_10kg: 2190,
            self.mp_20kg: 3340
        }

        self.save_changes_btn.clicked.connect(self.save)
        self.add_new_stamp_btn.clicked.connect(self.add_new_stamp)
        self.rmv_selected_btn.clicked.connect(self.remove_selected_stamp)
        self.calc_stamps_button.clicked.connect(self.calculate)

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
            if radio.isChecked():
                self.result_list.clear()
                """
                Work out in multiple different ways and choose the one with
                the least stamps
                """
                mod_used = []
                first_fit_used = []
                aim_price = self.weight_lookup[radio]
                preserved_package_value = aim_price
                list_of_available_stamps = [v["value"] for k,v in self.stamp_dict.items()]

                try:
                    largest_stamp = max(list_of_available_stamps)
                except ValueError:
                    self.popup("Value Error", "No stamps available", "Add some to stock", QMessageBox.Critical)
                    return

                """See if any stamps fit into aim_price"""
                for stamp in list_of_available_stamps:
                    if aim_price % stamp == 0:
                        mod_used.append([stamp for x in range(int(aim_price/stamp))])

                """Decreasing first-fit algorithm"""
                while aim_price > 0:
                    if aim_price - largest_stamp < 0:
                        if abs(aim_price - largest_stamp) < min(list_of_available_stamps):
                            first_fit_used.append(largest_stamp)
                            break
                        list_of_available_stamps.remove(largest_stamp)
                        try:
                            largest_stamp = max(list_of_available_stamps)
                        except ValueError:
                            first_fit_used.append(largest_stamp)
                            break
                        continue
                    first_fit_used.append(largest_stamp)
                    aim_price -= largest_stamp

                # use mod_used as a master list of all calculated lists
                mod_used.append(first_fit_used)

                # find list that contains lowest about of stamps
                shortest = mod_used[0]
                for l in mod_used:
                    if len(shortest) > len(l):
                        shortest = l

                self.output_calculated(shortest, preserved_package_value)

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
            jb.dump_dict_to_file(self.stamp_dict, "stamps.json")
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
    prog = stamp_calc_main_app(dialog)
    dialog.show()
    app.exec_()
    prog.save()  # Save on exit
    sys.exit()
