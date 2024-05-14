import sys
import threading
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from server.dummy_server import Server
SERVER_IP = "localhost"
SERVER_PORT = 1818  

class MainWindow(QtWidgets.QTabWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.active = True
        uic.loadUi('views/ui_object/mainwindow.ui', self)
        self.server = Server(SERVER_IP , SERVER_PORT)



    def run_serv(self):
        # Starting Server
        serverThreadServer = threading.Thread(target=self.server.start_server)
        self.server.newData.connect(self.updateData)
        serverThreadServer.start()


    # Manage close event 
    def closeEvent(self,event): 
        self.active = False
        self.server.stop_server()
        self.close()

    @pyqtSlot(list)
    def updateData(self, data):
        print("l:", data[0], "w:", data[1], "d:", data[2] , "x:" ,data[3])
        self.progressBar.setValue(data[0])  # Mettre à jour la barre de progression avec data[0]
        self.label_13.setText(f"{data[0]}% / {data[1]}˚C")
        self.label_16.setText(f"{data[0]}% / {data[2]}˚C")
        self.label_17.setText(f"{data[0]}% / {data[3]}˚C")


