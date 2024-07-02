from PyQt5 import QtGui

class PressurePoint:
    """
    Represents a pressure point with attributes used for graphical representation.

    Attributes:
        _circle_center_x (int): X-coordinate of the circle center.
        _circle_center_y (int): Y-coordinate of the circle center.
        _pressure (int): Magnitude of the pressure at the point.
        _vector (optional, object): Vector associated with the pressure point.
        _border_color (QtGui.QColor): Border color of the pressure point.
        _gradient_center (QtGui.QColor): Center color of the gradient fill around the pressure point.
    """

    def __init__(self, circle_center_x, circle_center_y, pressure, vector=None,
                 border_color=QtGui.QColor(0, 0, 255), gradient_center=QtGui.QColor(255, 255, 255), active=True):
        """
        Initializes a PressurePoint object with the given parameters.

        Args:
            circle_center_x (int): X-coordinate of the circle center.
            circle_center_y (int): Y-coordinate of the circle center.
            pressure (int): Magnitude of the pressure at the point.
            vector (optional, object): Vector associated with the pressure point.
            border_color (QtGui.QColor, optional): Border color of the pressure point.
                Default is QtGui.QColor(0, 0, 255) (blue).
            gradient_center (QtGui.QColor, optional): Center color of the gradient fill around the pressure point.
                Default is QtGui.QColor(255, 255, 255) (white).
            active (bool, optional): Flag indicating if the pressure point is active.
                Default is True.
        """
        self._circle_center_x = circle_center_x
        self._circle_center_y = circle_center_y
        self._pressure = pressure
        self._vector = vector
        self._border_color = border_color
        self._gradient_center = gradient_center

    @property
    def get_circle_center_x(self):
        """
        Getter for the X-coordinate of the circle center.

        Returns:
            int: X-coordinate of the circle center.
        """
        return self._circle_center_x

    @property
    def get_circle_center_y(self):
        """
        Getter for the Y-coordinate of the circle center.

        Returns:
            int: Y-coordinate of the circle center.
        """
        return self._circle_center_y

    @property
    def get_pressure(self):
        """
        Getter for the pressure magnitude.

        Returns:
            int: Magnitude of the pressure at the point.
        """
        return self._pressure

    @property
    def get_vector(self):
        """
        Getter for the vector associated with the pressure point.

        Returns:
            object: Vector associated with the pressure point.
        """
        return self._vector

    @property
    def get_border_color(self):
        """
        Getter for the border color of the pressure point.

        Returns:
            QtGui.QColor: Border color of the pressure point.
        """
        return self._border_color

    @property
    def get_gradient_center(self):
        """
        Getter for the center color of the gradient fill around the pressure point.

        Returns:
            QtGui.QColor: Center color of the gradient fill around the pressure point.
        """
        return self._gradient_center

    def set_inactive(self):
        """
        Sets the pressure point as inactive by changing the border color and gradient center color to white.

        Returns:
            PressurePoint: The PressurePoint instance itself (allows method chaining).
        """
        self._border_color = QtGui.QColor(255, 255, 255)  # White color
        self._gradient_center = QtGui.QColor(255, 255, 255)  # White color
        return self
