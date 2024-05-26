import threading
import time
import random

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import *

from views.QtWidgets.FootWidget2 import FootWidget2
from views.QtWidgets.Object.PressurePoint import PressurePoint
from views.QtWidgets.FootWidget import FootWidget
from server.dummy_server import Server
from views.QtWidgets.widget_3dplot import Widget3DPlot

SERVER_IP = "localhost"
SERVER_PORT = 1818

class MainWindow(QtWidgets.QTabWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.active = False
        _translate = QtCore.QCoreApplication.translate

        self.active_time = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_usage_time)
        uic.loadUi('views/ui_object/mainwindow.ui', self)
        self.server = Server(SERVER_IP, SERVER_PORT)

        self.initUI()

        self.ForceQuitButton = self.findChild(QtWidgets.QPushButton, "force_quit_button")
        self.ForceQuitButton.clicked.connect(self.closeEvent)


    def initUI(self):
        self.foot_widget = FootWidget2(self)
        central_widget = self.findChild(QtWidgets.QWidget, "animation_widget")
        layout = QtWidgets.QVBoxLayout(central_widget)
        # Create the plot widget
        self.plot_widget = Widget3DPlot()
        layout.addWidget(self.plot_widget, 70)


    def run_serv(self):
        serverThreadServer = threading.Thread(target=self.server.start_server)
        self.server.newData.connect(self.updateData)
        serverThreadServer.start()

    def closeEvent(self, event):
        self.active = False
        self.server.stop_server()
        self.close()

    @pyqtSlot(list)
    def updateData(self, data):
        print(data)
        if not self.active:
            self.active = True
            self.status_label.setText(f"In Progress")
            self.status_label.setStyleSheet("background-color: rgb(0, 170, 0);font-weight: bold;color: 'white';font: "
                                            "12pt 'MS Shell Dlg 2';")
            self.active_time = time.time()

        self.progressBar.setValue(data[0])

        self.label_13.setText(f"{data[0]}% / {data[1]}˚C")
        self.label_16.setText(f"{data[0]}% / {data[2]}˚C")

        # Update foot pressure points
        LeftFootPressurePoints = []
        RightFootPressurePoints = []
        point1 = PressurePoint(data[3],data[4],data[5])
        point2 = PressurePoint(data[6],data[7],data[8])
        cond1 , cond2 = random.randint(0, 1),random.randint(0, 1)

        # Conditions
        conditions = [cond1, cond2]
        # Points de pression
        points = [point1, point2]
        # Boucle sur les conditions et les points
        for condition, point in zip(conditions, points):
            if condition == 0:
                LeftFootPressurePoints.append(point)
            else:
                RightFootPressurePoints.append(point)

        self.foot_widget.update_pixmap(LeftFootPressurePoints,RightFootPressurePoints)

        self.timer.start()

    def update_usage_time(self):
        elapsed_time = time.time() - self.active_time
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)
        self.label_usage_time.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
