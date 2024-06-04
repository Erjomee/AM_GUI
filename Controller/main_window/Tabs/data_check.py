from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer


class DataCheck:
    def __init__(self , main_window):
        self.main_window = main_window
        self.active = False

    def update_data(self, data):
        data_check_label = self.main_window.findChild(QtWidgets.QWidget, "data_check_label")
        data_check_label.setText(data.to_string())

