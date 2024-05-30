import random
import time

from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QTimer

from views.MainWindow.RobotOperation.FaultDetectionWidget import FaultDetectionWidget
from views.MainWindow.RobotOperation.FootWidget import FootWidget
from views.MainWindow.RobotOperation.Object.PressurePoint import PressurePoint
from views.MainWindow.RobotOperation.Object.Vector import Vector
from views.MainWindow.RobotOperation.widget_3dplot import Widget3DPlot

class RobotOperation:
    def __init__(self , main_window):
        self.main_window = main_window
        self.active = False

        self.active_time = 0
        self.current_time = "00:00:00"
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

    def update_usage_time(self):
        elapsed_time = time.time() - self.active_time
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)
        self.current_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.main_window.label_usage_time.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")

    def update(self, data):
        self.timer.start()

        if not self.active:
            self.active = True
            self.main_window.status_label.setText(f"In Progress")
            self.main_window.status_label.setStyleSheet("background-color: rgb(0, 170, 0);font-weight: bold;color: 'white';font: "
                                            "12pt 'MS Shell Dlg 2';")
            self.active_time = time.time()

        self.main_window.progressBar.setValue(data[0])

        self.main_window.label_13.setText(f"{data[0]}% / {data[1]}˚C")
        self.main_window.label_16.setText(f"{data[0]}% / {data[2]}˚C")
        self.main_window.label_17.setText(f"{data[0]}% / {data[3]}˚C")


        ####################### 3D Motion Widget ########################
        self.plot_widget.update_coords((data[4],data[5]), (data[7],data[8]))


        ####################### Foot Widget ########################

        # Update foot pressure points
        LeftFootPressurePoints = [PressurePoint(data[10],data[11],data[14],vector=Vector(data[15], data[16]))]
        RightFootPressurePoints = [PressurePoint(data[12],data[13],data[17],vector=Vector(data[18], data[19]))]

        self.foot_widget.update_pixmap(LeftFootPressurePoints,RightFootPressurePoints)


        ####################### Fault Detection Widget ########################
        self.fault_detection_widget.update_fault_list([random.randint(1,16) for _ in range(16)] + [1,3] ,self.current_time)
