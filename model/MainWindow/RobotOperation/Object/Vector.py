from PyQt5 import QtGui


class Vector:
    """
    Simple vector class representing a 2D vector with x and y components.
    """

    def __init__(self, x, y):
        """
        Initializes a 2D vector with given x and y components.

        :param x: X component of the vector.
        :param y: Y component of the vector.
        """
        self._x = x
        self._y = y

    @property
    def get_x(self):
        """
        Getter method for retrieving the x component of the vector.

        :return: X component of the vector.
        """
        return self._x

    @property
    def get_y(self):
        """
        Getter method for retrieving the y component of the vector.

        :return: Y component of the vector.
        """
        return self._y
