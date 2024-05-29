import math

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QGraphicsScene, \
    QGraphicsPixmapItem, QGraphicsView, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsPolygonItem
from PyQt5.QtCore import Qt, QRectF, QPointF

from views.MainWindow.RobotOperation.Object.PressurePoint import PressurePoint


class FootWidget(QWidget):
    def __init__(self, main_window):
        super(FootWidget, self).__init__()
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
        self.graphics_view.setRenderHint(QPainter.Antialiasing)
        self.graphics_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphics_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        scene_rect = QRectF(0, 0, self.graphics_view.width(), self.graphics_view.height())
        self.scene.setSceneRect(scene_rect)

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
        self.LeftFootSensors = []

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

        self.foots_center_point = {"left_foot": None, "right_foot": None}

        self.RightFootPressurePoints = []
        self.RightFootSensors = []

        self.x_axis = None
        self.y_axis = None

        ####################### ANIMATION FOOT ########################

        # Adjust items to the view size
        self.graphics_view.resizeEvent = self.resizeEvent

    def init_sensor(self , is_permanent = True):
        self.update_pixmap(self.LeftFootSensors, self.RightFootSensors, is_permanent)

    def foot_sensor(self,foot,activate=False):
        point1 = PressurePoint(220, 67, 5, border_color=QtGui.QColor(255, 140, 0))
        point2 = PressurePoint(220, -73, 5, border_color=QtGui.QColor(255, 140, 0))
        point3right = PressurePoint(-70, 4, 5, border_color=QtGui.QColor(255, 140, 0))
        point3left = PressurePoint(-70, -11, 5, border_color=QtGui.QColor(255, 140, 0))
        center_point = PressurePoint(0, 0, 3, border_color=QtGui.QColor(255, 0, 0), gradient_center=QtGui.QColor(255, 0, 0))

        match foot:
            case "left_foot":
                if activate:
                    self.LeftFootSensors = [point1, point2, point3left, center_point]
                else:
                    self.LeftFootSensors = [point.set_inactive() for point in [point1, point2, point3left, center_point]]
            case "right_foot":
                if activate:
                    self.RightFootSensors = [point1, point2, point3right, center_point]
                else:
                    self.RightFootSensors = [point.set_inactive() for point in[point1, point2, point3right, center_point]]


    def update_pixmap(self, LeftFootPressurePoints=[], RightFootPressurePoints=[], is_permanent=False):

        # Clearing ancient pressure points
        if not is_permanent:
            self.clearItems(QGraphicsEllipseItem)
            self.clearItems(QGraphicsLineItem)
            self.clearItems(QGraphicsPolygonItem)
            self.LeftFootPressurePoints = LeftFootPressurePoints
            self.RightFootPressurePoints = LeftFootPressurePoints
            self.init_sensor()

        ListOfFootsCoordsPressure = {"left_foot": LeftFootPressurePoints, "right_foot": RightFootPressurePoints}

        for foot, foot_pixmap_item in self.foots_pixmap_item.items():

            # Verify that the foot is in contact with the ground
            if sum(point.get_pressure for point in ListOfFootsCoordsPressure.get(foot)) != 0 and len(ListOfFootsCoordsPressure) != 0:
                if not is_permanent:
                    foot_pixmap_item.setOpacity(1)
                    self.foot_sensor(foot, activate=True)

                # Find the origin point of the foot
                x_foot_pixmap_item_coord = foot_pixmap_item.x()
                y_foot_pixmap_item_coord = foot_pixmap_item.y()
                x_origin_foot_pixmap_item_coord = x_foot_pixmap_item_coord + (80 / 170) * foot_pixmap_item.pixmap().width()
                y_origin_foot_pixmap_item_coord = y_foot_pixmap_item_coord + (235 / 320) * foot_pixmap_item.pixmap().height()
                self.foots_center_point[foot] = [x_origin_foot_pixmap_item_coord, y_origin_foot_pixmap_item_coord]

                ####################### Drawing the Pressure Points ########################
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

                    ####################### Drawing the Vector Direction ########################

                    if point.get_vector is not None and not is_permanent:
                        self.drawVector(x_pressure_point_coord + point.get_pressure,y_pressure_point_coord + point.get_pressure,point.get_vector,point.get_pressure)
            else:
                foot_pixmap_item.setOpacity(0.4)
                self.foot_sensor(foot, activate=False)

    def drawVector(self, x_start, y_start, vector, value):
            # Calculate the end point of the arrow
            end_x = x_start - vector.get_y
            end_y = y_start - vector.get_x

            # Draw Line of the vector base
            line = QGraphicsLineItem(x_start, y_start, end_x, end_y)
            line.setPen(QPen(QColor("black"), value*0.2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

            # test = QGraphicsEllipseItem(x_start-10/2,y_start-10/2,10,10)

            # Add the arrow to the scene
            self.scene.addItem(line)
            # self.scene.addItem(test)

            self.drawArrowhead(QPointF(x_start, y_start), QPointF(end_x, end_y), QColor("black"), value * 0.2)

    def drawArrowhead(self, start_point, end_point, color, width):
        # Calculate the angle of the line
        angle = math.atan2(start_point.y() - end_point.y(), start_point.x() - end_point.x())

        # Define the size of the arrowhead
        arrow_size = 10

        # Calculate the points for the arrowhead
        arrow_p1 = end_point + QPointF(math.cos(angle + math.pi / 6) * arrow_size,
                                       math.sin(angle + math.pi / 6) * arrow_size)
        arrow_p2 = end_point + QPointF(math.cos(angle - math.pi / 6) * arrow_size,
                                       math.sin(angle - math.pi / 6) * arrow_size)

        # Create a QPolygonF for the arrowhead
        arrow_head = QPolygonF([end_point, arrow_p1, arrow_p2])

        # Create a QGraphicsPolygonItem for the arrowhead
        arrow_item = QGraphicsPolygonItem(arrow_head)

        # Set the pen and brush to define the color and width of the arrowhead
        arrow_pen = QPen(color)
        arrow_pen.setWidthF(width)
        arrow_item.setPen(arrow_pen)
        arrow_item.setBrush(color)

        # Add the arrowhead to the scene
        self.scene.addItem(arrow_item)

    def clearItems(self, type_Item):
        for item in self.scene.items():
            if isinstance(item, type_Item):
                self.scene.removeItem(item)

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

        #  Resizing Right foot
        self.right_foot_pixmap_item.setPixmap(self.right_foot_pixmap.scaled(int(new_foot_width), int(new_foot_height)))
        self.right_foot_pixmap_item.setPos(self.right_foot_pixmap_item.x() * x_coeff,
                                           self.scene.sceneRect().height() * 0.5 - new_foot_height*0.5)

        # # self.update_feets_pos()
        self.update_pixmap(self.LeftFootPressurePoints, self.RightFootPressurePoints)


