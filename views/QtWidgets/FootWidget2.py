import math
import random
import time

import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QLabel, QGraphicsOpacityEffect, QGraphicsScene, \
    QGraphicsPixmapItem, QGraphicsView, QGraphicsEllipseItem, QGraphicsLineItem
from PyQt5.QtCore import Qt, pyqtSlot, QRectF, QTimer

from views.QtWidgets.Object.PressurePoint import PressurePoint


class FootWidget2(QWidget):
    def __init__(self, main_window):
        super(FootWidget2, self).__init__()
        self.animation_start_time = None
        self.main_window = main_window

        self.foot_widget = self.main_window.findChild(QWidget, "foot_widget_1")
        layout = QtWidgets.QHBoxLayout(self.foot_widget)

        # Create the QGraphicsView and QGraphicsScene
        self.graphics_view = QGraphicsView(self.foot_widget)
        self.scene = QGraphicsScene(self)
        self.view_size = self.graphics_view.size()

        self.graphics_view.setScene(self.scene)

        # Add the QGraphicsView to the layout
        layout.addWidget(self.graphics_view)

        # Remove scroll bars
        self.graphics_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphics_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        scene_rect = QRectF(0, 0, self.graphics_view.width(), self.graphics_view.height())
        self.scene.setSceneRect(scene_rect)

        # Store initial size
        self.old_width = self.scene.width()
        self.old_height = self.scene.height()

        ####################### LEFT FOOT ########################

        # Charging left foot image
        self.left_foot_pixmap = QPixmap('assets/left_foot_model.png')  # Ensure the file path is correct

        # Create a QGraphicsPixmapItem with the pixmap
        self.left_foot_pixmap_item = QGraphicsPixmapItem(self.left_foot_pixmap)
        self.left_foot_pixmap_item.setPixmap( self.left_foot_pixmap.scaled(int(self.scene.width() * 0.35), int(self.scene.height() * 0.45)))
        self.left_foot_pixmap_item.setPos(self.scene.width() * 0.05,
                                          self.scene.height() * 0.5 - self.left_foot_pixmap_item.pixmap().height())
        self.scene.addItem(self.left_foot_pixmap_item)

        self.LeftFootPressurePoints = []

        ####################### RIGHT FOOT ########################

        # Charging right foot image
        self.right_foot_pixmap = QPixmap('assets/right_foot_model.png')  # Ensure the file path is correct

        # Create a QGraphicsPixmapItem with the pixmap
        self.right_foot_pixmap_item = QGraphicsPixmapItem(self.right_foot_pixmap)
        self.right_foot_pixmap_item.setPixmap(
            self.right_foot_pixmap.scaled(int(self.scene.width() * 0.35), int(self.scene.height() * 0.45)))
        self.right_foot_pixmap_item.setPos(self.scene.width() * 0.2 + self.left_foot_pixmap_item.pixmap().width(),
                                           self.scene.height() * 0.5 - self.right_foot_pixmap_item.pixmap().height())
        self.scene.addItem(self.right_foot_pixmap_item)

        self.foots_pixmap_item = {"left_foot": self.left_foot_pixmap_item, "right_foot": self.right_foot_pixmap_item}
        self.foot_str_of_pixmap_item = {self.left_foot_pixmap_item: "left_foot",
                                        self.right_foot_pixmap_item: "right_foot"}
        self.foots_center_point = {"left_foot": None, "right_foot": None}

        self.animation_data = None

        self.RightFootPressurePoints = []

        self.x_axis = None
        self.y_axis = None

        ####################### ANIMATION FOOT ########################

        # Adjust items to the view size
        self.graphics_view.resizeEvent = self.resizeEvent

        # Timer for Animation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)

        # Start Animation test
        self.StampBtn = self.main_window.findChild(QtWidgets.QPushButton, "pushButton_3")
        self.StampBtn.clicked.connect(self.on_stamp_btn_clicked)

        self.init_sensor()

        # time.sleep(self.motion_2d(self.left_foot_pixmap_item,self.left_foot_pixmap_item.x(),0,[0,0],10))

    # Click handler for animation test
    def on_stamp_btn_clicked(self):
        self.motion_2d(self.left_foot_pixmap_item,
                       random.randint(0, self.graphics_view.width()),
                       random.randint(0, self.graphics_view.height()),
                       [0, 1]
                       ,5)
    def motion_2d(self, foot_pixmap_item, x_destination, y_destination, vector, time_travel):

        # Finding distance between current pos and destination
        distance = math.sqrt((x_destination - foot_pixmap_item.x()) ** 2 + (y_destination - foot_pixmap_item.y()) ** 2)

        # Frame per seconds
        fps = 100
        total_points_generated = fps * time_travel

        # Distance to travel per every frame
        distance_per_frame = distance / time_travel  # 1sec

        x_values = np.linspace(self.foots_center_point[self.foot_str_of_pixmap_item.get(foot_pixmap_item)][0],
                               x_destination, num=total_points_generated)
        y_values = np.linspace(self.foots_center_point[self.foot_str_of_pixmap_item.get(foot_pixmap_item)][1],
                               y_destination, num=total_points_generated)

        self.animation_data = {
            'foot_pixmap_item': foot_pixmap_item,
            'x_values': x_values,
            'y_values': y_values,
            'current_frame': 0,
            'total_frames': total_points_generated,
            'time_interval': int(1000 / fps)  # milliseconds per frame
        }
        # Start time of the animation
        self.animation_start_time = time.time()

        self.timer.start(self.animation_data['time_interval'])

    def update_position(self):
        self.update_pixmap(self.LeftFootPressurePoints,self.RightFootPressurePoints)
        # self.init_sensor(False)

        data = self.animation_data
        self.set_origin(self.foot_str_of_pixmap_item[data["foot_pixmap_item"]])

        frame = data['current_frame']
        if frame < data['total_frames']:
            new_x = data['x_values'][frame]   # foots_center_point
            new_y = data['y_values'][frame]

            x_gap = (self.foots_center_point[self.foot_str_of_pixmap_item[data["foot_pixmap_item"]]][0]
                     - data['foot_pixmap_item'].x())
            y_gap = (self.foots_center_point[self.foot_str_of_pixmap_item[data["foot_pixmap_item"]]][1]
                     - data['foot_pixmap_item'].y())

            data['foot_pixmap_item'].setPos(new_x - x_gap,new_y - y_gap)
            data['current_frame'] += 1
        else:
            self.timer.stop()
            elapsed_time = time.time() - self.animation_start_time
            print(elapsed_time)


    def init_sensor(self , is_permanent= True):
        point1 = PressurePoint(220, 67, 5, QtGui.QColor(255, 140, 0))
        point2 = PressurePoint(220, -73, 5, QtGui.QColor(255, 140, 0))
        point3right = PressurePoint(-70, 4, 5, QtGui.QColor(255, 140, 0))
        point3left = PressurePoint(-70, -11, 5, QtGui.QColor(255, 140, 0))
        center_point = PressurePoint(0, 0, 3, QtGui.QColor(255, 0, 0), QtGui.QColor(255, 0, 0))

        LeftFootPressurePoints = [point1, point2, point3left, center_point]
        RightFootPressurePoints = [point1, point2, point3right, center_point]

        self.update_pixmap(LeftFootPressurePoints, RightFootPressurePoints, is_permanent)


    def update_pixmap(self, LeftFootPressurePoints=[], RightFootPressurePoints=[], is_permanent=False):

        # Clearing ancient pressure points
        if not is_permanent:
            self.clearItems(QGraphicsEllipseItem)
            self.LeftFootPressurePoints = LeftFootPressurePoints
            self.RightFootPressurePoints = LeftFootPressurePoints

        ListOfFootsCoordsPressure = {"left_foot": LeftFootPressurePoints, "right_foot": RightFootPressurePoints}

        for foot, foot_pixmap_item in self.foots_pixmap_item.items():

            # Verify that the foot is in contact with the ground
            if sum(point.get_pressure for point in ListOfFootsCoordsPressure.get(foot)) != 0 and len(ListOfFootsCoordsPressure) != 0:
                if not is_permanent:
                    foot_pixmap_item.setOpacity(1)
                    # Update foot position
                    # self.moving_2d(foot_pixmap_item)

                # Find the origin point of the foot
                x_foot_pixmap_item_coord = foot_pixmap_item.x()
                y_foot_pixmap_item_coord = foot_pixmap_item.y()
                x_origin_foot_pixmap_item_coord = x_foot_pixmap_item_coord + (80 / 170) * foot_pixmap_item.pixmap().width()
                y_origin_foot_pixmap_item_coord = y_foot_pixmap_item_coord + (235 / 320) * foot_pixmap_item.pixmap().height()
                self.foots_center_point[foot] = [x_origin_foot_pixmap_item_coord, y_origin_foot_pixmap_item_coord]

                # Drawing pressure points
                for point in ListOfFootsCoordsPressure.get(foot):
                    # Calculate coordinates of the point
                    x_pressure_point_coord = x_origin_foot_pixmap_item_coord - ((point.get_circle_center_y / 170) * foot_pixmap_item.pixmap().width()) - point.get_pressure
                    y_pressure_point_coord = y_origin_foot_pixmap_item_coord - ((point.get_circle_center_x / 320) * foot_pixmap_item.pixmap().height()) - point.get_pressure
                    pressure_point_ellipse = QGraphicsEllipseItem(x_pressure_point_coord, y_pressure_point_coord, point.get_pressure * 2, point.get_pressure * 2)

                    # Create a radial gradient for the ellipse
                    radial_gradient = QRadialGradient(x_pressure_point_coord + point.get_pressure, y_pressure_point_coord + point.get_pressure, point.get_pressure)
                    radial_gradient.setColorAt(0, point.get_gradient_center)  # Color at the center
                    radial_gradient.setColorAt(1, point.get_border_color)  # Color at the border

                    # Create a brush with the radial gradient
                    brush = QBrush(radial_gradient)
                    pressure_point_ellipse.setBrush(brush)

                    # Add the ellipse to the scene
                    self.scene.addItem(pressure_point_ellipse)

                # ####################### Calculation of BaryCenter ########################
                # if not is_permanent:
                #     # Get the barycenter point
                #     bary_center_point = self.BarycenterOf(ListOfFootsCoordsPressure.get(foot))
                #     x_bary_center_point_coord = x_origin_foot_pixmap_item_coord - ((bary_center_point.get_circle_center_y / 170) * foot_pixmap_item.pixmap().width()) - bary_center_point.get_pressure
                #     y_bary_center_point_coord = y_origin_foot_pixmap_item_coord - ((bary_center_point.get_circle_center_x / 320) * foot_pixmap_item.pixmap().height()) - bary_center_point.get_pressure
                #     bary_center_point_ellipse = QGraphicsEllipseItem(x_bary_center_point_coord, y_bary_center_point_coord, bary_center_point.get_pressure * 2, bary_center_point.get_pressure * 2)
                #
                #     # Create a radial gradient for the ellipse
                #     radial_gradient = QRadialGradient(x_bary_center_point_coord + bary_center_point.get_pressure, y_bary_center_point_coord + bary_center_point.get_pressure, bary_center_point.get_pressure)
                #     radial_gradient.setColorAt(0, bary_center_point.get_gradient_center)  # Color at the center
                #     radial_gradient.setColorAt(1, bary_center_point.get_border_color)  # Color at the border
                #
                #     # Create a brush with the radial gradient
                #     brush = QBrush(radial_gradient)
                #     bary_center_point_ellipse.setBrush(brush)
                #
                #     # Add the ellipse to the scene
                #     self.scene.addItem(bary_center_point_ellipse)

            else:
                foot_pixmap_item.setOpacity(0.5)

        if not is_permanent:
            self.init_sensor()
            # self.draw_grid()

        # # Créer un timer pour chaque pixmap en mouvement
        # timer = QTimer(self)
        # timer.timeout.connect(lambda: self.move_pixmap(foot_pixmap_item, distance_per_frame, vector, timer, x_destination, y_destination))
        # timer.start(50)  # Appeler la fonction 20 fois par seconde pour une animation fluide

    # def move_pixmap(self, foot_pixmap_item, distance_per_frame, vector, timer , x_destination , y_destination):
    #
    #
    #     # Déplacer le pixmap en fonction de la distance à parcourir
    #     foot_pixmap_item.setPos(foot_pixmap_item.x() - distance_per_frame * vector[0], foot_pixmap_item.y() + -(distance_per_frame * vector[1]))
    #     self.init_sensor()
    #
    #     # Calculer la distance restante à parcourir
    #     remaining_distance = math.sqrt((x_destination - foot_pixmap_item.x())**2 + (y_destination - foot_pixmap_item.y())**2)
    #
    #     # Si le pixmap a atteint sa destination ou presque, arrêter le timer
    #     if remaining_distance < 1:
    #         timer.stop()

    # # Placeholder for your moving_2d implementation
    # if True:
    #     # Comparer les coordonnées y des centres des pieds
    #     if self.left_foot_pixmap_item.y() < self.right_foot_pixmap_item.y():
    #         front_foot = self.left_foot_pixmap_item
    #         back_foot = self.right_foot_pixmap_item
    #         back_foot_str = "right_foot"
    #     else:
    #         front_foot = self.right_foot_pixmap_item
    #         back_foot = self.left_foot_pixmap_item
    #         back_foot_str = "left_foot"
    #
    # self.set_origin(back_foot_str)
    #
    # if front_foot.y() < self.graphics_view.height()*0.05:
    #     front_foot.moveBy(0,speed)
    #     back_foot.moveBy(0,speed)
    #
    # if back_foot.y() + back_foot.pixmap().height() > self.graphics_view.height()*0.98:
    #     back_foot, front_foot = front_foot, back_foot
    #     while front_foot.y() > self.graphics_view.height()*0.05:
    #         front_foot.moveBy(0,-speed)
    #
    # front_foot.moveBy(0,-speed )

    def BarycenterOf(self, ListOfPressurePoints):
        lst_pts_coord = np.array(
            [[Point.get_circle_center_x, Point.get_circle_center_y] for Point in ListOfPressurePoints])
        pressures = np.array([Point.get_pressure for Point in ListOfPressurePoints])

        # Calculate the total weight
        total_weight = np.sum(pressures)

        # Calculate the centroid
        centroid = np.sum(pressures[:, np.newaxis] * lst_pts_coord, axis=0) / total_weight

        return PressurePoint(centroid[0], centroid[1], 5, QtGui.QColor(0, 255, 0), QtGui.QColor(0, 255, 0))

    def clearItems(self, type_Item):

        for item in self.scene.items():
            if isinstance(item, type_Item):
                self.scene.removeItem(item)

    def set_origin(self, foot):
        view_size = self.graphics_view.size()
        step = 20

        # Remove previous grid lines and axes
        self.clearItems(QGraphicsLineItem)

        # Draw axes
        center_x = self.foots_center_point.get(foot)[0]
        center_y = self.foots_center_point.get(foot)[1]

        self.x_axis = self.scene.addLine(0, center_y, view_size.width(), center_y, QPen(Qt.red))
        self.y_axis = self.scene.addLine(center_x, 0, center_x, view_size.height(), QPen(Qt.red))

        self.x_axis.setOpacity(0.5)
        self.y_axis.setOpacity(0.5)

        # Ensure foot pixmaps are in front of grid lines and axes

    def resizeEvent(self, event):
        super().resizeEvent(event)

        old_width = self.scene.sceneRect().width()
        old_height = self.scene.sceneRect().height()

        scene_rect = QRectF(0, 0, self.graphics_view.width(), self.graphics_view.height())
        self.scene.setSceneRect(scene_rect)

        # Taking 35% of the Graphics View for each foot's width
        new_foot_width = self.scene.sceneRect().width() * 0.4

        # # Taking 45% of the Graphics for each foot's height
        new_foot_height = self.scene.sceneRect().height() * 0.8

        x_coeff = self.scene.width() / old_width
        y_coeff = self.scene.height() / old_height

        # # Resizing Left foot
        self.left_foot_pixmap_item.setPixmap(self.left_foot_pixmap.scaled(int(new_foot_width), int(new_foot_height)))
        self.left_foot_pixmap_item.setPos(self.left_foot_pixmap_item.x() * x_coeff,
                                          self.scene.sceneRect().height() * 0.5 - new_foot_height*0.5)
        #
        # # Resizing Right foot
        self.right_foot_pixmap_item.setPixmap(self.right_foot_pixmap.scaled(int(new_foot_width), int(new_foot_height)))
        self.right_foot_pixmap_item.setPos(self.right_foot_pixmap_item.x() * x_coeff,
                                           self.scene.sceneRect().height() * 0.5 - new_foot_height*0.5)

        # # self.update_feets_pos()
        self.update_pixmap(self.LeftFootPressurePoints, self.RightFootPressurePoints)
        #
        # # Call the original resize event
        # # super(QGraphicsView, self.graphics_view).resizeEvent(event)
