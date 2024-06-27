import sys
import threading
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from server.dummy_server import Server


class StartWindow(QtWidgets.QDialog):
    def __init__(self):
        super(StartWindow, self).__init__()

        self.active = True
        self.is_showed = False

        uic.loadUi('views/StartWindow/ui/startwindow.ui', self)
        self.setFixedSize(450, 300)  # Set fixed size

        # Listenner on startBTN
        self.StartButton = self.findChild(QtWidgets.QPushButton, "StartButton")
        self.StartButton.clicked.connect(self.closeEvent)

        # Listenner on quitBTN
        self.QuitButton = self.findChild(QtWidgets.QPushButton, "QuitButton")
        self.QuitButton.clicked.connect(self.closeEvent)

    def startAPP(self):
        self.run_serv()
        self.active = False

    # Manage close event 
    def closeEvent(self, event):
        self.active = False
        self.close()
