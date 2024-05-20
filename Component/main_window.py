import threading
import time
import random

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import *

from views.QtWidgets.FootWidget2 import FootWidget2
from views.QtWidgets.Object.PressurePoint import PressurePoint
from views.QtWidgets.FootWidget import FootWidget
from server.dummy_server import Server

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
        uic.loadUi('views/ui_object/mainwindow2.ui', self)
        self.server = Server(SERVER_IP, SERVER_PORT)

        self.foot_widget = FootWidget2(self)
        # self.test_update_pixmap()

        self.ForceQuitButton = self.findChild(QtWidgets.QPushButton, "force_quit_button")
        self.ForceQuitButton.clicked.connect(self.closeEvent)


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
        if not self.active:
            self.active = True
            self.status_label.setText(f"In Progress")
            self.status_label.setStyleSheet("background-color: rgb(0, 170, 0);font-weight: bold;color: 'white';font: "
                                            "12pt 'MS Shell Dlg 2';")
            self.active_time = time.time()

        print("l:", data[0], "w:", data[1], "d:", data[2], "x:", data[3])
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

        self.timer.start(100)

    def update_usage_time(self):
        elapsed_time = time.time() - self.active_time
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)
        self.label_usage_time.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")

    def test_update_pixmap(self):
        point1left = PressurePoint(40, 0, 25)
        point2left = PressurePoint(100, -70, 18)
        point3left = PressurePoint(-15, -70, 30)

        point1right = PressurePoint(40, 0, 15)
        point2right = PressurePoint(120, 70, 10)
        point3right = PressurePoint(200, 20, 20)

        LeftFootPressurePoints = [point1left, point2left, point3left]
        RightFootPressurePoints = [point1right, point2right, point3right]

        self.foot_widget.update_pixmap(LeftFootPressurePoints, RightFootPressurePoints)
