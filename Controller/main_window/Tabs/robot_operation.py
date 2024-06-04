import random
import time
import pandas as pd

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer

from datetime import datetime
import os
import csv

from views.MainWindow.RobotOperation.Widget.FaultDetectionWidget import FaultDetectionWidget
from views.MainWindow.RobotOperation.Widget.FootWidget import FootWidget
from views.MainWindow.RobotOperation.Object.PressurePoint import PressurePoint
from views.MainWindow.RobotOperation.Object.Vector import Vector
from views.MainWindow.RobotOperation.Widget.widget_3dplot import Widget3DPlot


class RobotOperation:
    def __init__(self, main_window):
        self.main_window = main_window
        self.active = False

        self.active_time = 0
        self.current_time = "00:00:00"
        self.latest_time_insertion = ""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_usage_time)

        # 3D Motion Widget
        central_widget = self.main_window.findChild(QtWidgets.QWidget, "animation_widget")
        layout = QtWidgets.QVBoxLayout(central_widget)
        self.plot_widget = Widget3DPlot()
        layout.addWidget(self.plot_widget, 70)

        # 2D Feets CoP Widget
        self.foot_widget = FootWidget(self.main_window)

        # Fault Detection Widget
        self.fault_detection_widget = FaultDetectionWidget(self.main_window)

        # Recording data
        self.on_record = False
        self.RecordingButton = self.main_window.findChild(QtWidgets.QPushButton, "recording_button")
        self.RecordingButton.clicked.connect(self.handle_recording_button)
        self.csv_file_path = None

        # Time Stamp
        self.stamp_cpt = 0
        self.lst_time_stamp = []
        self.StampButton = self.main_window.findChild(QtWidgets.QPushButton, "stamp_button")
        self.StampLCD = self.main_window.findChild(QtWidgets.QLCDNumber, "stamp_cpt")
        self.StampButton.clicked.connect(self.handle_stamp_button)

        # Time fault detection
        self.lst_time_fault_detection = []


    def handle_stamp_button(self):
        self.stamp_cpt += 1
        self.StampLCD.display(self.stamp_cpt)
        self.lst_time_stamp.append(self.latest_time_insertion)

    def handle_recording_button(self):
        if self.on_record:  # End Recording
            self.end_recording()
        else:  # Start Recording
            self.start_recording()

    def start_recording(self):
        date_time = datetime.now().strftime("%Y-%m-%d-%H_%M")

        # Create folder if not exist
        folder_name = "views/MainWindow/RobotOperation/Data/recording"
        os.makedirs(folder_name, exist_ok=True)

        # Path to csv file base on the date and hour
        self.csv_file_path = os.path.join(folder_name, f"{date_time}-{self.current_time.replace(':', '_')[:-4]}.csv")

        # Writing the first row (header)
        with open(self.csv_file_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            csvwriter.writerow(
                ['Usage_time', 'Battery', 'Temp1', 'Temp2', 'Temp3', 'LFoot_x', 'LFoot_y', 'LFoot_z', 'RFoot_x',
                 'RFoot_y', 'RFoot_z',
                 'LFootCOP_x', 'LFootCOP_y', 'RFootCOP_x', 'RFootCOP_y', 'LFootCOP_value', 'LFootCOP_vector_x',
                 'LFootCOP_vector_y', 'RFootCOP_value', 'RFootCOP_vector_x', 'RFootCOP_vector_y', 'LFoot_time_travel',
                 'RFoot_time_travel', 'LH_Abd_Temp', 'LH_Rot_Temp', 'LH_Flex_Temp', 'LK_Temp', 'LA_Lat_Temp',
                 'LA_Med_Temp', 'RH_Abd_Temp', 'RH_Rot_Temp', 'RH_Flex_Temp', 'RK_Temp', 'RA_Lat_Temp', 'RA_Med_Temp',
                 'LH_Abd_Amp', 'LH_Rot_Amp', 'LH_Flex_Amp', 'LK_Amp', 'LA_Lat_Amp', 'LA_Med_Amp', 'RH_Abd_Amp',
                 'RH_Rot_Amp', 'RH_Flex_Amp', 'RK_Amp', 'RA_Lat_Amp', 'RA_Med_Amp', "Stamp"])

        self.on_record = True

        # Updating graphics
        self.main_window.recording_button_container.setStyleSheet(
            ''' QWidget{ background-color: rgb(130, 130, 130);
                    color: black;
                    border: 1px solid black
                }
                QWidget:hover{
                    background-color: rgb(236, 78, 0);
                }''')
        self.RecordingButton.setText("End data storage")

    def end_recording(self):
        self.on_record = False

        # Updating graphics
        self.main_window.recording_button_container.setStyleSheet(
            ''' QWidget{ background-color: blue;
                    color: white;
                    border: 1px solid black
                }
                QWidget:hover{
                    background-color: rgb(0, 85, 255);
                }''')
        self.RecordingButton.setText("Start data storage")

        # Adding time stamp into the csv
        df = pd.read_csv(self.csv_file_path)
        df["Stamp"] = df["Stamp"].astype(str)  # Convert the column to str

        for time_stamp in self.lst_time_stamp:
            df.loc[df["Usage_time"] == time_stamp, "Stamp"] = "True"

        # TODO add fault detection time stamp

        # Passing data to the data checker
        self.main_window.data_check.update_data(df)

        self.lst_time_stamp = []  # Reinitialize the list of time stamp
        df.to_csv(self.csv_file_path, index=False)


    def update_usage_time(self):
        elapsed_time = time.time() - self.active_time
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)
        milliseconds = int((elapsed_time % 1) * 1000)
        self.current_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}:{milliseconds:03d}"
        self.main_window.label_usage_time.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")

    def update(self, data):
        self.timer.start()

        if not self.active:
            self.active = True
            self.main_window.status_label.setText(f"In Progress")
            self.main_window.status_label.setStyleSheet(
                "background-color: rgb(0, 170, 0);font-weight: bold;color: 'white';font: "
                "12pt 'MS Shell Dlg 2';")
            self.active_time = time.time()

        ####################### Battery Update ########################
        self.main_window.progressBar.setValue(data[0])

        if data[0] <= 10:  # 10% battery
            self.main_window.progressBar.setStyleSheet("QProgressBar::chunk { background-color: rgb(255, 0, 0); }")
        elif data[0] <= 50:  # 50% battery
            self.main_window.progressBar.setStyleSheet("QProgressBar::chunk { background-color: rgb(255, 170, 0); }")
        else:
            self.main_window.progressBar.setStyleSheet("QProgressBar::chunk { background-color: rgb(0, 170, 0); }")

        ####################### Temperature Update ########################
        self.main_window.LH_Abd_label.setText(f"{data[34]}% / {data[22]}˚C")
        self.main_window.RH_Abd_label.setText(f"{data[40]}% / {data[28]}˚C")

        self.main_window.LH_Rot_label.setText(f"{data[35]}% / {data[23]}˚C")
        self.main_window.RH_Rot_label.setText(f"{data[41]}% / {data[29]}˚C")

        self.main_window.LH_Flex_label.setText(f"{data[36]}% / {data[24]}˚C")
        self.main_window.RH_Flex_label.setText(f"{data[42]}% / {data[30]}˚C")

        self.main_window.LK_label.setText(f"{data[37]}% / {data[25]}˚C")
        self.main_window.RK_label.setText(f"{data[43]}% / {data[31]}˚C")

        self.main_window.LA_Lat_label.setText(f"{data[38]}% / {data[26]}˚C")
        self.main_window.RA_Lat_label.setText(f"{data[44]}% / {data[32]}˚C")

        self.main_window.LA_Med_label.setText(f"{data[39]}% / {data[27]}˚C")
        self.main_window.RA_Med_label.setText(f"{data[45]}% / {data[33]}˚C")

        ####################### 3D Motion Widget ########################
        # self.plot_widget.update_coords((data[4], -185), (data[7], 185))

        ########################## Foot Widget ###########################

        # Update foot pressure points
        LeftFootPressurePoints = [PressurePoint(data[10], data[11], data[14], vector=Vector(data[15], data[16]))]
        RightFootPressurePoints = [PressurePoint(data[12], data[13], data[17], vector=Vector(data[18], data[19]))]

        self.foot_widget.update_pixmap(LeftFootPressurePoints, RightFootPressurePoints)

        ######################## Fault Detection Widget ########################
        self.fault_detection_widget.update_fault_list([random.randint(1, 16) for _ in range(16)] + [1, 3],
                                                      self.current_time)

        ################## Storing data for Data Check Tab #####################
        if self.on_record:
            # Store new data received in the csv file
            with open(self.csv_file_path, 'a', newline='') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=',')
                tmp = data.copy()
                time_received = self.current_time
                tmp.insert(0, time_received)
                csvwriter.writerow(tmp)
                self.latest_time_insertion = time_received
