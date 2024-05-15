import sys
import threading
import time

from PyQt5 import QtWidgets, QtGui, uic, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QHBoxLayout
from views.QtWidgets.Object.PressurePoint import PressurePoint

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
        uic.loadUi('views/ui_object/mainwindow.ui', self)
        self.server = Server(SERVER_IP, SERVER_PORT)

        # Charger l'image à partir du fichier
        self.pixmap = QPixmap('assets/foot.jpg')  # Assurez-vous que le chemin d'accès au fichier est correct

        # Récupérer le QLabel par son nom d'objet
        label = self.findChild(QLabel, "label_27")

        # Modifier le QLabel pour afficher l'image
        label.setPixmap(self.pixmap)
        label.setScaledContents(True)  # Si vous souhaitez que l'image soit mise à l'échelle pour s'adapter au QLabel

        self.cpt = 0
        self.test_update_pixmap()

    def run_serv(self):
        # Starting Server
        serverThreadServer = threading.Thread(target=self.server.start_server)
        self.server.newData.connect(self.updateData)
        serverThreadServer.start()

    # Manage close event
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

        # Update the progress bar with data[o]
        self.progressBar.setValue(data[0])
        # self.label_usage_time.setText(f"{self.active_time:.2f}")

        # Update the temperature
        self.label_13.setText(f"{data[0]}% / {data[1]}˚C")
        self.label_16.setText(f"{data[0]}% / {data[2]}˚C")
        self.label_17.setText(f"{data[0]}% / {data[3]}˚C")

        self.timer.start(100)  # Update the usage time label every 100 ms
        # self.update_pixmap()

    def update_usage_time(self):
        elapsed_time = time.time() - self.active_time
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)
        self.label_usage_time.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")

    def update_pixmap(self, LeftFootPressurePoints , RightFootPressurePoints):
        # Instance of QPixmap base on the foot image
        pixmap = QPixmap('assets/foot.jpg')

        # Create a copy of the pixmap
        pixmap_copy = self.pixmap.copy()

        # Painting object on the pixmap
        painter = QtGui.QPainter(pixmap_copy)

        ListOfFoots = [LeftFootPressurePoints,RightFootPressurePoints]

        # Drawing point for each foot
        for foot in ListOfFoots:
            for point in foot:
                # Setting the brush
                print(point.get_circle_center_x)
                radial_gradient = QtGui.QRadialGradient(point.get_circle_center_x, point.get_circle_center_y, point.get_circle_radius)
                radial_gradient.setColorAt(0, QtGui.QColor(255, 255, 255))  # white center
                radial_gradient.setColorAt(1, QtGui.QColor(0, 0, 255))  # blue on border
                brush = QtGui.QBrush(radial_gradient)
                painter.setBrush(brush)

                # Setting the pen
                pen = QtGui.QPen()
                pen.setWidth(5)
                painter.setPen(pen)

                # Gérer le décalage
                # .drawEllipse(x,y,widht,height)
                # x: Coordinates x of superior corner left of rectangle
                # y: Coordinates y of superior corner left of rectangle
                # width: Width of the rectangle
                # height: Height of the rectangle
                painter.drawEllipse(point.get_circle_center_x - point.get_circle_radius, point.get_circle_center_y - point.get_circle_radius, point.get_circle_radius * 2,
                                    point.get_circle_radius * 2)
        painter.end()

        # Modifier le QLabel pour afficher la nouvelle image
        label = self.findChild(QLabel, "label_27")
        label.setPixmap(pixmap_copy)
        label.setScaledContents(True)  # Set scaledContents to True scaledContents to True


    def test_update_pixmap(self):
        point1 = PressurePoint(350,350 , 75 , 10)
        point2 = PressurePoint(200,800 , 50 , 10)

        point3 = PressurePoint(660,300 , 50 , 10)
        point4 = PressurePoint(700,500 , 75 , 10)
        point5 = PressurePoint(690,700 , 40 , 10)

        LeftFootPressurePoints = [point1,point2]
        RightFootPressurePoints = [point3,point4,point5]

        self.update_pixmap(LeftFootPressurePoints ,RightFootPressurePoints)
