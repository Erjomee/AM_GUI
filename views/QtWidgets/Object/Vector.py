from PyQt5 import QtGui

class Vector:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    # Getter for x
    @property
    def get_x(self):
        return self._x

    # Getter for y
    @property
    def get_y(self):
        return self._y


