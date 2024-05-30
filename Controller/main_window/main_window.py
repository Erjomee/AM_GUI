import threading

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import *

from Controller.main_window.Tabs.data_check import DataCheck
from Controller.main_window.Tabs.robot_operation import RobotOperation
from Controller.main_window.Tabs.turn_and_debug import TurnAndDebug
from server.dummy_server import Server

SERVER_IP = "localhost"
SERVER_PORT = 1818


class MainWindow(QtWidgets.QTabWidget):
    window_closed = pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.active = False
        _translate = QtCore.QCoreApplication.translate

        # Loading Main Window UI
        uic.loadUi('views/MainWindow/ui/mainwindow.ui', self)
        self.server = Server(SERVER_IP, SERVER_PORT)  # Launching server listener

        # Loading all tabs of the Main Window
        self.robot_operation = RobotOperation(self)
        self.data_check = DataCheck(self)
        self.turn_and_debug = TurnAndDebug(self)
        self.tabs = [self.robot_operation, self.data_check, self.turn_and_debug]

        # Click on quit button
        self.ForceQuitButton = self.findChild(QtWidgets.QPushButton, "force_quit_button")
        self.ForceQuitButton.clicked.connect(self.closeEvent)

    # Starting the server and transmitting data
    def run_serv(self):
        serverThreadServer = threading.Thread(target=self.server.start_server)
        self.server.newData.connect(self.updateData)
        serverThreadServer.start()

    # Quit Event
    def closeEvent(self, event):
        self.active = False
        self.server.stop_server()
        self.close()
        self.window_closed.emit()  # Emit the signal before closing

    # Updating data in all tabs
    @pyqtSlot(list)
    def updateData(self, data):
        for tab in self.tabs:
            tab.update(data)
