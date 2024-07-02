import pandas as pd
from model.MainWindow.DataCheck.Widget.DriversPlotsWidgets import DriversPlotsWidgets

class DataCheck:
    def __init__(self, main_window):
        """
        Initializes the DataCheck tab class of the main window.
        :param main_window: Reference to the main application window.
        """
        self.main_window = main_window
        self.active = False  # Indicator of the active or inactive state of the object
        self.drivers_plots_widget = DriversPlotsWidgets(self.main_window)  # Initializes the widget for drivers plots

    def update_data(self, csv_data_file_path: str, csv_stamp_file_path: str, csv_fault_file_path: str):
        """
        Updates the data by reading the CSV files and refreshing the plots.
        :param csv_data_file_path: Path to the CSV file containing time data.
        :param csv_stamp_file_path: Path to the CSV file containing timestamp data (currently unused).
        :param csv_fault_file_path: Path to the CSV file containing fault data (currently unused).
        """
        # Read time data from the CSV file
        time_data = pd.read_csv(csv_data_file_path)

        # Update the plots with the new time data
        self.drivers_plots_widget.update_plots(time_data)
