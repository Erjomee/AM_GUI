import pandas as pd

from views.MainWindow.DataCheck.Widget.DriversPlotsWidgets import DriversPlotsWidgets

class DataCheck:
    def __init__(self, main_window):
        self.main_window = main_window
        self.active = False
        self.drivers_plots_widget = DriversPlotsWidgets(self.main_window)

    def update_data(self, csv_data_file_path: str, csv_stamp_file_path: str, csv_fault_file_path: str):
        time_data = pd.read_csv(csv_data_file_path)
        self.drivers_plots_widget.update_plots(time_data)
