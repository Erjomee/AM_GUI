class PressurePoint:
    def __init__(self, circle_center_x, circle_center_y, circle_radius, pressure):
        self._circle_center_x = circle_center_x
        self._circle_center_y = circle_center_y
        self._circle_radius = circle_radius
        self._pressure = pressure

    # Getter for circle_center_x
    @property
    def get_circle_center_x(self):
        return self._circle_center_x

    # Getter for circle_center_y
    @property
    def get_circle_center_y(self):
        return self._circle_center_y

    # Getter for circle_radius
    @property
    def get_circle_radius(self):
        return self._circle_radius

    # Getter for pressure
    @property
    def get_pressure(self):
        return self._pressure
