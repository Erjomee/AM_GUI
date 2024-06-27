import sys

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QWidget)
from mpl_toolkits.mplot3d.art3d import Line3D

from utils import get_xyz_of_points, calculate_angle


class Widget3DPlot(QWidget):
    def __init__(self, parent=None):
        super(Widget3DPlot, self).__init__(parent)
        # Initiate all the attributes
        self.fig = None
        self.canvas = None
        self._ax = None
        self.points = {}
        self.lines = {}

        # Initialize components
        self.initUI()
        self.initPlot()
        self.initRobot()

    ############################################################
    #                   Initialize Methods                     #
    ############################################################
    def initUI(self):
        # Initialize the layout
        layout = QVBoxLayout(self)
        self.fig = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.fig)
        self.fig.set_canvas(self.canvas)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.addWidget(self.canvas)

    def initPlot(self):
        # Initial setup of the plot
        self._ax = self.canvas.figure.add_subplot(projection="3d")
        self._ax.view_init(20, 220)
        self._ax.set_xlim(-1, 0.7)
        self._ax.set_ylim(-0.9, 0.9)
        self._ax.set_zlim(0, 1.5)
        self._ax.set_xlabel("X Label")
        self._ax.set_ylabel("Y Label")
        self._ax.set_zlabel("Z Label")

    def initRobot(self):
        # Define points for both sides

        joints = {
            "R_FRONT_FOOT": (-0.4, -0.1265, 0.18694),
            "R_FOOT": (-0.17923, -0.1265, 0.18694),
            "R_SHANK": (-0.2215, -0.23675, 0.57438),
            "R_THIGH": (-0.2125, -0.26175, 1.005),
            "R_HIP": (-0.2125, -0.26, 1.15915),
            "R_BASE": (0, -0.105, 1.2),
            "BASE": (0, 0, 1.2),
            "L_BASE": (0, 0.105, 1.2),
            "L_HIP": (-0.2125, 0.26, 1.15915),
            "L_THIGH": (-0.2125, 0.26175, 1.005),
            "L_SHANK": (-0.2215, 0.23675, 0.57438),
            "L_FOOT": (-0.17923, 0.1265, 0.18694),
            "L_FRONT_FOOT": (-0.4, 0.1265, 0.18694)
        }

        # Defining the points
        for name, coords in joints.items():
            xs, ys, zs = [coords[0]], [coords[1]], [coords[2]]
            self.points[name] = Line3D(xs, ys, zs, c='0.1', marker='.', markersize=4)

        # Defining the lines
        keys = list(self.points.keys())
        for i in range(len(keys) - 1):
            xs, ys, zs = get_xyz_of_points(
                self.points[keys[i]].get_data_3d(),
                self.points[keys[i + 1]].get_data_3d()
            )
            self.lines[f"{keys[i]}-{keys[i+1]}"] = Line3D(xs, ys, zs, c='0.6')

        # Place each line on the plot
        for line in self.lines.values():
            self._ax.add_line(line)
        # Place each point on the plot
        for point in self.points.values():
            self._ax.add_line(point)

    ############################################################
    #                       Utils methods                      #
    ############################################################
    def update_joints(self, motion):
        self.points[side][part].set_data_3d([x], [y], [z])
        # Looking for the line that contains the point updated and update it
        for line, point1, point2 in self.lines:
            if (side, part) == point1 or (side, part) == point2:
                x_data, y_data, z_data = get_xyz_of_points(
                    self.points[point1[0]][point1[1]].get_data_3d(),
                    self.points[point2[0]][point2[1]].get_data_3d()
                )
                line.set_data_3d(x_data, y_data, z_data)

    def move_plan(self, x, y):
        self._ax.set_xlim(x - 500, x + 500)
        self._ax.set_ylim(y - 500, y + 500)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget3DPlot()
    #widget.update_point('right', 'FootCentralPoint', 100, 100, 100)
    widget.show()
    sys.exit(app.exec_())
