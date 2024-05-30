import numpy as np
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QLabel, QGraphicsOpacityEffect
from views.MainWindow.RobotOperation.Object.PressurePoint import PressurePoint


class FootWidget(QtWidgets.QWidget):
    def __init__(self, main_window):
        super(FootWidget, self).__init__()
        self.main_window = main_window

        self.center_point = PressurePoint(83,235,5)

        ####################### LEFT FOOT ########################

        # Charging left foot image
        self.left_foot_pixmap = QPixmap('assets/left_foot_model.png')  # Assurez-vous que le chemin d'accès au fichier est correct

        # Récupérer le QLabel par son nom d'objet
        label = self.main_window.findChild(QLabel, "left_foot")

        # Adding pixmap to the QLabel
        label.setScaledContents(True)  # Si vous souhaitez que l'image soit mise à l'échelle pour s'adapter au QLabel
        label.setPixmap(self.left_foot_pixmap)

        ####################### RIGHT FOOT ########################

        # Charging right foot image
        self.right_foot_pixmap = QPixmap('assets/right_foot_model.png')  # Assurez-vous que le chemin d'accès au fichier est correct

        # Récupérer le QLabel par son nom d'objet
        label = self.main_window.findChild(QLabel, "right_foot")

        # Adding pixmap to the QLabel
        label.setScaledContents(True)  # Si vous souhaitez que l'image soit mise à l'échelle pour s'adapter au QLabel
        label.setPixmap(self.right_foot_pixmap)

        self.foots_pixmap = {"left_foot": self.left_foot_pixmap, "right_foot": self.right_foot_pixmap}

        self.init_sensor()


    def init_sensor(self):
        point1 = PressurePoint(220, 0, 5, QtGui.QColor(255,140,0))
        point2 = PressurePoint(220, -70, 5, QtGui.QColor(255,140,0))
        point3right = PressurePoint(-70, 7, 5, QtGui.QColor(255,140,0))
        point3left = PressurePoint(-70, -8, 5, QtGui.QColor(255,140,0))
        center_point = PressurePoint(0, 0, 5 , QtGui.QColor(255,0,0) ,QtGui.QColor(255,0,0))

        LeftFootPressurePoints = [point1, point2,point3left,center_point]
        RightFootPressurePoints = [point1, point2,point3right,center_point]

        self.update_pixmap(LeftFootPressurePoints , RightFootPressurePoints , True)

    def update_pixmap(self, LeftFootPressurePoints , RightFootPressurePoints , is_permanent = False):

        ListOfFootsCoordsPressure = {"left_foot": LeftFootPressurePoints, "right_foot": RightFootPressurePoints}

        # For each foot
        for foot , foot_pixmap in self.foots_pixmap.items():

            # Modifier le QLabel pour afficher la nouvelle image
            label = self.main_window.findChild(QLabel, foot)

            if is_permanent:
                # Useing the base pixmap
                pixmap_copy = foot_pixmap
            else:
                # Create a copy of the pixmap
                pixmap_copy = foot_pixmap.copy()

            # Verify that the foot is in contact with the ground
            if sum(point.get_pressure for point in ListOfFootsCoordsPressure.get(foot)) != 0 and len(ListOfFootsCoordsPressure) != 0:
                # Painting object on the pixmap
                painter = QtGui.QPainter(pixmap_copy)

                # Drawing point for each foot
                for point in ListOfFootsCoordsPressure.get(foot):
                    # Setting the brush
                    radial_gradient = QtGui.QRadialGradient(self.center_point.get_circle_center_x - point.get_circle_center_y,
                                                            self.center_point.get_circle_center_y - point.get_circle_center_x,
                                                            point.get_pressure)
                    radial_gradient.setColorAt(0, point.get_gradient_center)  # white center
                    radial_gradient.setColorAt(1, point.get_border_color)  # blue on border
                    brush = QtGui.QBrush(radial_gradient)
                    painter.setBrush(brush)

                    # Setting the pen
                    pen = QtGui.QPen()
                    pen.setWidth(1)
                    painter.setPen(pen)

                    # Gérer le décalage
                    # .drawEllipse(x,y,widht,height)
                    # x: Coordinates x of superior corner left of rectangle
                    # y: Coordinates y of superior corner left of rectangle
                    # width: Width of the rectangle
                    # height: Height of the rectangle
                    painter.drawEllipse(self.center_point.get_circle_center_x - point.get_circle_center_y - point.get_pressure,
                                        self.center_point.get_circle_center_y - point.get_circle_center_x - point.get_pressure,
                                        point.get_pressure * 2,
                                        point.get_pressure * 2)

                ####################### Calculation of BaryCenter ########################
                if not is_permanent:
                    # Drawing the BaryCenter
                    bary_center_point = self.BarycenterOf(ListOfFootsCoordsPressure.get(foot))

                    # Setting the brush
                    radial_gradient = QtGui.QRadialGradient(self.center_point.get_circle_center_x - bary_center_point.get_circle_center_y ,
                                                            self.center_point.get_circle_center_y - bary_center_point.get_circle_center_x,
                                                            bary_center_point.get_pressure)
                    radial_gradient.setColorAt(0, bary_center_point.get_gradient_center)  # white center
                    radial_gradient.setColorAt(1, bary_center_point.get_border_color)  # red on border
                    brush = QtGui.QBrush(radial_gradient)
                    painter.setBrush(brush)

                    # Setting the pen
                    pen = QtGui.QPen()
                    pen.setWidth(3)
                    painter.setPen(pen)

                    # Drawing Circle
                    painter.drawEllipse(int(self.center_point.get_circle_center_x - bary_center_point.get_circle_center_y - bary_center_point.get_pressure),
                                        int(self.center_point.get_circle_center_y - bary_center_point.get_circle_center_x - bary_center_point.get_pressure),
                                        bary_center_point.get_pressure * 2,
                                        bary_center_point.get_pressure * 2)

                painter.end()
                # Create a graphics opacity effect and set the opacity
                opacity_effect = QGraphicsOpacityEffect()
                opacity_effect.setOpacity(1) # set the opacity to 100%

                # Set the graphics opacity effect to the label (image)
                label.setGraphicsEffect(opacity_effect)
                label.setPixmap(pixmap_copy)
                widget_label = self.main_window.findChild(QWidget, "widget_"+foot)

                # Settings up border color with radius
                widget_label.setStyleSheet("border: 2px solid black;border-radius: 10px")
                widget_label.move(0,0)
            else:
                # Create a graphics opacity effect and set the opacity
                opacity_effect = QGraphicsOpacityEffect()
                opacity_effect.setOpacity(0.5) # set the opacity to 50%

                # Set the graphics opacity effect to the label (image)
                label.setGraphicsEffect(opacity_effect)
                label.setPixmap(pixmap_copy)
                widget_label = self.main_window.findChild(QWidget, "widget_"+foot)

                # Removing border
                widget_label.setStyleSheet("border: none")
                widget_label.move(0,0)


            label.setScaledContents(True)  # Set scaledContents to True scaledContents to True


    def BarycenterOf(self, ListOfPressurePoints):
        lst_pts_coord = np.array([[Point.get_circle_center_x, Point.get_circle_center_y] for Point in ListOfPressurePoints])
        pressures = np.array([Point.get_pressure for Point in ListOfPressurePoints])

        # Calculez la somme des poids
        total_weight = np.sum(pressures)

        # Calculez le centroïde
        centroid = np.sum(pressures[:, np.newaxis] * lst_pts_coord, axis=0) / total_weight

        return PressurePoint(centroid[0],centroid[1],5,QtGui.QColor(0,255,0),QtGui.QColor(0,255,0))




