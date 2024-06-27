from PyQt5 import QtGui


class PressurePoint:
    def __init__(self, circle_center_x, circle_center_y, pressure,vector = None, border_color = QtGui.QColor(0, 0, 255),
                 gradient_center= QtGui.QColor(255, 255, 255) , active=True):
        self._circle_center_x = circle_center_x
        self._circle_center_y = circle_center_y
        self._pressure = pressure
        self._vector = vector
        self._border_color = border_color
        self._gradient_center = gradient_center

    # Getter for circle_center_x
    @property
    def get_circle_center_x(self):
        return self._circle_center_x

    # Getter for circle_center_y
    @property
    def get_circle_center_y(self):
        return self._circle_center_y

    @property
    def get_pressure(self):
        return self._pressure

    @property
    def get_vector(self):
        return self._vector

    # Getter for border_color
    @property
    def get_border_color(self):
        return self._border_color

    # Getter for gradient_center
    @property
    def get_gradient_center(self):
        return self._gradient_center

    def set_inactive(self):
        self._border_color = QtGui.QColor(255, 255, 255)
        self._gradient_center = QtGui.QColor(255, 255, 255)
        return self
