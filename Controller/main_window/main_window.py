import threading
import time

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import *

from views.MainWindow.RobotOperation.FootWidget import FootWidget
from views.MainWindow.RobotOperation.Object.PressurePoint import PressurePoint
from server.dummy_server import Server
from views.MainWindow.RobotOperation.widget_3dplot import Widget3DPlot

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
        uic.loadUi('views/MainWindow/ui/mainwindow.ui', self)
        self.server = Server(SERVER_IP, SERVER_PORT)

        self.initUI()

        self.ForceQuitButton = self.findChild(QtWidgets.QPushButton, "force_quit_button")
        self.ForceQuitButton.clicked.connect(self.closeEvent)

    def initUI(self):
        #self.foot_widget = FootWidget(self)
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
        # print(data)
        if not self.active:
            self.active = True
            self.status_label.setText(f"In Progress")
            self.status_label.setStyleSheet("background-color: rgb(0, 170, 0);font-weight: bold;color: 'white';font: "
                                            "12pt 'MS Shell Dlg 2';")
            self.active_time = time.time()

        self.progressBar.setValue(data[0])

        self.label_13.setText(f"{data[0]}% / {data[1]}˚C")
        self.label_16.setText(f"{data[0]}% / {data[2]}˚C")
        self.label_17.setText(f"{data[0]}% / {data[3]}˚C")

        # Update foot pressure points
        LeftFootPressurePoints = [PressurePoint(data[10], data[11], data[14])]
        RightFootPressurePoints = [PressurePoint(data[12], data[13], data[17])]

        #self.foot_widget.update_pixmap(LeftFootPressurePoints, RightFootPressurePoints)

        # Update the 3D plot
        self.plot_widget.update_coords((data[4], data[5]), (data[7], data[8]))

        self.timer.start()

    def update_usage_time(self):
        elapsed_time = time.time() - self.active_time
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)
        self.label_usage_time.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
