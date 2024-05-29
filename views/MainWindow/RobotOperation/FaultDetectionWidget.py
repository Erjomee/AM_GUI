import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget , QVBoxLayout, QLabel

class FaultDetectionWidget(QWidget):
    def __init__(self, main_window):
        super(FaultDetectionWidget, self).__init__()
        self.main_window = main_window
        self.fault_detection_widget = self.main_window.findChild(QWidget, "fault_detection_widget")
        layout = QVBoxLayout(self.fault_detection_widget)

        title = QLabel("Fault Detection")
        title.setStyleSheet("QLabel {"
                                "border: none;"
                                "font: 16pt 'MS Shell Dlg 2';"
                            "}")
        layout.addWidget(title)

        self.scrollArea = QtWidgets.QScrollArea(self.fault_detection_widget)
        self.scrollArea.setWidgetResizable(True)

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        layout.addWidget(self.scrollArea)

        self.df = pd.read_csv("views/MainWindow/RobotOperation/Data/fault_id.csv")

        self.old_lst_fault_id = []

    # Function to add a fault in the scroll area base on the ID
    def update_fault_list(self , new_lst_fault_id , time):
        # Removing unneeded faults
        fault_id_to_remove = list(set(self.old_lst_fault_id) - set(new_lst_fault_id))
        faults_labels_to_remove = [self.get_label(fault) for fault in fault_id_to_remove]
        self.remove_fault(faults_labels_to_remove)

        # Adding faults
        fault_id_to_add = list(set(new_lst_fault_id) - set(self.old_lst_fault_id))
        faults_labels_to_add = [self.get_label(fault) for fault in fault_id_to_add]
        self.add_fault(faults_labels_to_add , time)

        # Updating the new list of current fault
        self.old_lst_fault_id = new_lst_fault_id

    # Function ton add a list of fault
    def add_fault(self,lst_fault,time):
        for fault in lst_fault:
            fault_Qlabel = QtWidgets.QLabel(f"{time}  {fault}")
            fault_Qlabel.setStyleSheet("QLabel {"
                                       "border: none;"
                                       "font: 10pt 'MS Shell Dlg 2';"
                                       "}")
            self.verticalLayout.addWidget(fault_Qlabel)

    # Function ton remove a list of fault
    def remove_fault(self, lst_fault):
        for i in reversed(range(self.verticalLayout.count())):
            widget = self.verticalLayout.itemAt(i).widget()
            if isinstance(widget, QtWidgets.QLabel):
                for fault in lst_fault:
                    if fault in widget.text():
                        self.verticalLayout.removeWidget(widget)
                        widget.deleteLater()

    # Get the label fault of the associate ID
    def get_label(self, id):
        # Ensure that the fault exist
        if not self.df.loc[self.df['id'] == id].empty:
            fault_label = str(self.df.loc[self.df ['id'] == id]["label"].iloc[0] )
            return fault_label