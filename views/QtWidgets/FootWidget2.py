import time

import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QLabel, QGraphicsOpacityEffect, QGraphicsScene, \
    QGraphicsPixmapItem, QGraphicsView, QGraphicsEllipseItem, QGraphicsLineItem
from PyQt5.QtCore import Qt, pyqtSlot

from views.QtWidgets.Object.PressurePoint import PressurePoint

class FootWidget2(QWidget):
    def __init__(self, main_window):
        super(FootWidget2, self).__init__()
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

        # Store initial size
        self.old_width = self.graphics_view.width()
        self.old_height = self.graphics_view.height()

        ####################### LEFT FOOT ########################

        # Charging left foot image
        self.left_foot_pixmap = QPixmap('assets/left_foot_model.png')  # Ensure the file path is correct

        # Create a QGraphicsPixmapItem with the pixmap
        self.left_foot_pixmap_item = QGraphicsPixmapItem(self.left_foot_pixmap)
        self.scene.addItem(self.left_foot_pixmap_item)
        # self.left_foot_pixmap_item.setPixmap(self.left_foot_pixmap.scaled(int(self.view_size.width() * 0.35), int(self.view_size.height() * 0.45)))
        # self.left_foot_pixmap_item.setPos(self.view_size.width() * 0.1,0 + self.view_size.height()*0.5 - (self.left_foot_pixmap_item.pixmap().height()) / 2)

        self.LeftFootPressurePoints = []

        ####################### RIGHT FOOT ########################

        # Charging right foot image
        self.right_foot_pixmap = QPixmap('assets/right_foot_model.png')  # Ensure the file path is correct

        # Create a QGraphicsPixmapItem with the pixmap
        self.right_foot_pixmap_item = QGraphicsPixmapItem(self.right_foot_pixmap)
        self.scene.addItem(self.right_foot_pixmap_item)

        self.foots_pixmap_item = {"left_foot": self.left_foot_pixmap_item, "right_foot": self.right_foot_pixmap_item}
        self.foots_center_point = {"left_foot": None, "right_foot": None}

        self.RightFootPressurePoints = []

        self.x_axis = None
        self.y_axis = None


        # Adjust items to the view size
        self.graphics_view.resizeEvent = self.on_view_resize

        self.cpt = 0

        self.init_sensor()
    #
    def update_feets_pos(self, x_coeff , y_coeff):

        pass
        # # print(self.left_foot_pixmap_item.x())
        # print(x_coeff)
        # print(self.left_foot_pixmap_item.x())
        # self.left_foot_pixmap_item.setPos(self.left_foot_pixmap_item.x()*x_coeff,self.left_foot_pixmap_item.y()*y_coeff)
        # # self.scene.setSceneRect(0, 0, self.graphics_view.width(), self.graphics_view.height())

    def init_sensor(self):
        point1 = PressurePoint(220, 67, 5, QtGui.QColor(255, 140, 0))
        point2 = PressurePoint(220, -73, 5, QtGui.QColor(255, 140, 0))
        point3right = PressurePoint(-70, 4, 5, QtGui.QColor(255, 140, 0))
        point3left = PressurePoint(-70, -11, 5, QtGui.QColor(255, 140, 0))
        center_point = PressurePoint(0, 0, 3, QtGui.QColor(255, 0, 0), QtGui.QColor(255, 0, 0))

        LeftFootPressurePoints = [point1, point2, point3left, center_point]
        RightFootPressurePoints = [point1, point2, point3right, center_point]

        self.update_pixmap(LeftFootPressurePoints, RightFootPressurePoints, True)

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
                    self.moving_2d(foot_pixmap_item)

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

                ####################### Calculation of BaryCenter ########################
                if not is_permanent:
                    # Get the barycenter point
                    bary_center_point = self.BarycenterOf(ListOfFootsCoordsPressure.get(foot))
                    x_bary_center_point_coord = x_origin_foot_pixmap_item_coord - ((bary_center_point.get_circle_center_y / 170) * foot_pixmap_item.pixmap().width()) - bary_center_point.get_pressure
                    y_bary_center_point_coord = y_origin_foot_pixmap_item_coord - ((bary_center_point.get_circle_center_x / 320) * foot_pixmap_item.pixmap().height()) - bary_center_point.get_pressure
                    bary_center_point_ellipse = QGraphicsEllipseItem(x_bary_center_point_coord, y_bary_center_point_coord, bary_center_point.get_pressure * 2, bary_center_point.get_pressure * 2)

                    # Create a radial gradient for the ellipse
                    radial_gradient = QRadialGradient(x_bary_center_point_coord + bary_center_point.get_pressure, y_bary_center_point_coord + bary_center_point.get_pressure, bary_center_point.get_pressure)
                    radial_gradient.setColorAt(0, bary_center_point.get_gradient_center)  # Color at the center
                    radial_gradient.setColorAt(1, bary_center_point.get_border_color)  # Color at the border

                    # Create a brush with the radial gradient
                    brush = QBrush(radial_gradient)
                    bary_center_point_ellipse.setBrush(brush)

                    # Add the ellipse to the scene
                    self.scene.addItem(bary_center_point_ellipse)

            else:
                foot_pixmap_item.setOpacity(0.5)

        if not is_permanent:
            self.init_sensor()
            # self.draw_grid()

    def moving_2d(self, foot_pixmap_item, speed=0.3):
        # Placeholder for your moving_2d implementation
        if True:
            # Comparer les coordonnées y des centres des pieds
            if self.left_foot_pixmap_item.y() < self.right_foot_pixmap_item.y():
                front_foot = self.left_foot_pixmap_item
                back_foot = self.right_foot_pixmap_item
                back_foot_str = "right_foot"
            else:
                front_foot = self.right_foot_pixmap_item
                back_foot = self.left_foot_pixmap_item
                back_foot_str = "left_foot"

        self.set_origin(back_foot_str)

        if front_foot.y() < self.graphics_view.height()*0.02:
            front_foot.moveBy(0,speed)
            back_foot.moveBy(0,speed)

        if back_foot.y() + back_foot.pixmap().height() > self.graphics_view.height()*0.98:
            back_foot, front_foot = front_foot, back_foot
            while front_foot.y() > self.graphics_view.height()*0.02:
                front_foot.moveBy(0,-speed)

        front_foot.moveBy(0,-speed )

    def BarycenterOf(self, ListOfPressurePoints):
        lst_pts_coord = np.array([[Point.get_circle_center_x, Point.get_circle_center_y] for Point in ListOfPressurePoints])
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


    def set_origin(self,foot):
        view_size = self.graphics_view.size()
        step = 20

        # Remove previous grid lines and axes
        self.clearItems(QGraphicsLineItem)

        # Draw axes
        center_x = self.foots_center_point.get(foot)[0]
        center_y =  self.foots_center_point.get(foot)[1]

        self.x_axis = self.scene.addLine(0, center_y, view_size.width(), center_y, QPen(Qt.red))
        self.y_axis = self.scene.addLine(center_x, 0, center_x, view_size.height(), QPen(Qt.red))

        self.x_axis.setOpacity(0.5)
        self.y_axis.setOpacity(0.5)

        # Ensure foot pixmaps are in front of grid lines and axes

    def on_view_resize(self, event):
        view_size = self.graphics_view.size()
        self.scene.setSceneRect(0, 0, view_size.width(), view_size.height())

        # Taking 35% of the Graphics View for each foot's width
        new_width = view_size.width() * 0.35

        # Taking 45% of the Graphics for each foot's height
        new_height = view_size.height() * 0.45

        # Resizing Left foot
        self.left_foot_pixmap_item.setPixmap(self.left_foot_pixmap.scaled(int(new_width), int(new_height)))
        self.left_foot_pixmap_item.setPos(view_size.width() * 0.1, view_size.height() * 0.5 - (self.left_foot_pixmap_item.pixmap().height()) / 2)

        # Resizing Right foot
        self.right_foot_pixmap_item.setPixmap(self.right_foot_pixmap.scaled(int(new_width), int(new_height)))
        self.right_foot_pixmap_item.setPos(view_size.width() * 0.2 + self.left_foot_pixmap_item.pixmap().width(),
                                           view_size.height() * 0.5 - (self.left_foot_pixmap_item.pixmap().height()) / 2)

        # self.update_feets_pos()
        self.update_pixmap(self.LeftFootPressurePoints , self.RightFootPressurePoints)
        # Call the original resize event
        super(QGraphicsView, self.graphics_view).resizeEvent(event)
