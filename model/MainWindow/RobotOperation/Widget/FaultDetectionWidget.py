import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class FaultDetectionWidget(QWidget):
    """
    Widget for fault detection in a PyQt5 application.
    """

    def __init__(self, main_window):
        """
        Initializes the fault detection widget.

        :param main_window: Reference to the main application window.
        """
        super(FaultDetectionWidget, self).__init__()
        self.main_window = main_window
        self.fault_detection_widget = self.main_window.findChild(QWidget, "fault_detection_widget")
        layout = QVBoxLayout(self.fault_detection_widget)

        # Add margins to the layout
        layout.setContentsMargins(30, 30, 30, 30)  # left, top, right, bottom
        layout.setSpacing(20)  # spacing between widgets

        # Title of the widget
        title = QLabel("Fault Detection")
        title.setStyleSheet("QLabel {"
                            "border: none;"
                            "font: 20pt 'MS Shell Dlg 2';"
                            "}")
        layout.addWidget(title)

        # Configure the scroll area
        self.scrollArea = QtWidgets.QScrollArea(self.fault_detection_widget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)

        # Align items to the top
        self.verticalLayout.setAlignment(Qt.AlignTop)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        layout.addWidget(self.scrollArea)

        # Read the CSV file containing fault IDs and descriptions
        self.df = pd.read_csv("model/MainWindow/RobotOperation/static/fault_id.csv")

        # List of old fault IDs
        self.old_lst_fault_id = []

    def update_fault_list(self, new_lst_fault_id, time):
        """
        Updates the displayed list of faults in the scroll area.

        :param new_lst_fault_id: New list of fault IDs.
        :param time: Current time.
        """
        # Remove unnecessary faults
        fault_id_to_remove = list(set(self.old_lst_fault_id) - set(new_lst_fault_id))
        faults_labels_to_remove = [self.get_label(fault) for fault in fault_id_to_remove]
        self.remove_fault(faults_labels_to_remove)

        # Add new faults
        fault_id_to_add = list(set(new_lst_fault_id) - set(self.old_lst_fault_id))
        faults_labels_to_add = [self.get_label(fault) for fault in fault_id_to_add]
        faults_description = [self.get_description(fault) for fault in fault_id_to_add]
        self.add_fault(faults_labels_to_add, faults_description, time)

        # Update lst_time_fault_detection with current time for new faults
        self.main_window.robot_operation.lst_time_fault_detection.extend([time] * len(fault_id_to_add))

        # Update the new list of current faults
        self.old_lst_fault_id = new_lst_fault_id

    def add_fault(self, lst_fault_label, lst_fault_description, time):
        """
        Adds a list of faults to the scroll area.

        :param lst_fault_label: List of fault labels.
        :param lst_fault_description: List of fault descriptions.
        :param time: Current time.
        """
        for fault_index in range(len(lst_fault_label)):
            # Determine color based on fault description
            match lst_fault_description[fault_index]:
                case "Warning":
                    color = "black"
                case "Error":
                    color = "orange"
                case "Critical":
                    color = "red"
                case _:
                    color = "black"  # Default color if no match

            # Create QLabel for the fault
            fault_Qlabel = QtWidgets.QLabel(
                f"{time} | <span style='color:{color}'>{lst_fault_label[fault_index]}</span>")
            fault_Qlabel.setStyleSheet("QLabel {"
                                       "border: none;"
                                       "font: 11pt 'MS Shell Dlg 2';"
                                       "}")
            self.verticalLayout.addWidget(fault_Qlabel)

    def remove_fault(self, lst_fault):
        """
        Removes a list of faults from the scroll area.

        :param lst_fault: List of fault labels to remove.
        """
        for i in reversed(range(self.verticalLayout.count())):
            widget = self.verticalLayout.itemAt(i).widget()
            if isinstance(widget, QtWidgets.QLabel):
                for fault in lst_fault:
                    if fault in widget.text():
                        self.verticalLayout.removeWidget(widget)
                        widget.deleteLater()

    def get_label(self, id):
        """
        Returns the label associated with a fault ID.

        :param id: Fault ID.
        :return: Fault label.
        """
        # Ensure the fault exists
        if not self.df.loc[self.df['id'] == id].empty:
            fault_label = str(self.df.loc[self.df['id'] == id]["label"].iloc[0])
            return fault_label

    def get_description(self, id):
        """
        Returns the description associated with a fault ID.

        :param id: Fault ID.
        :return: Fault description.
        """
        # Ensure the fault exists
        if not self.df.loc[self.df['id'] == id].empty:
            fault_description = str(self.df.loc[self.df['id'] == id]["description"].iloc[0])
            return fault_description
