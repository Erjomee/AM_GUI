import sys
import time

import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.tri as mtri
from PyQt5.QtWidgets import (QApplication, QHBoxLayout,
                             QHeaderView, QMainWindow,
                             QTableWidget, QTableWidgetItem, QVBoxLayout,
                             QWidget)

from views.QtWidgets.table_widget import Widget3DTable


class Widget3DPlot(QWidget):
    def __init__(self, parent=None):
        super(Widget3DPlot, self).__init__(parent)

        # Initialize components
        self.initUI()
        self.initPlot()
        self.initRobot()

        # Set first configuration
        self.drawRobot()

    ############################################################
    #                   Initialize Methods                     #
    ############################################################
    def initUI(self):
        # Initialize the layout
        layout = QVBoxLayout(self)
        self.fig = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.fig)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.addWidget(self.canvas)

    def initPlot(self):
        # Initial setup of the plot
        self.fig.set_canvas(self.canvas)
        self._ax = self.canvas.figure.add_subplot(projection="3d")
        self._ax.view_init(30, 30)
        self._ax.set_xlim([-500, 500])
        self._ax.set_ylim([-500, 500])
        self._ax.set_zlim([-500, 500])
        self._ax.set_xlabel("X Label")
        self._ax.set_ylabel("Y Label")
        self._ax.set_zlabel("Z Label")

    def initRobot(self):
        # Array where all the parts of the robot will be
        self.robot = []
        # Coords for the feet
        self.rightFootCop = np.array([0, -185, self._ax.get_zlim3d()[0]])
        self.leftFootCop = np.array([0, 185, self._ax.get_zlim3d()[0]])
        self.robot.append(self.rightFootCop)
        self.robot.append(self.leftFootCop)
        # Coords for the knees
        self.rightKnee = np.array([0, -185, -200])
        self.leftKnee = np.array([0, 185, -200])
        self.robot.append(self.rightKnee)
        self.robot.append(self.leftKnee)
        # Coords for the legs
        self.rightLeg = np.array([0, -185, 200])
        self.leftLeg = np.array([0, 185, 200])
        self.robot.append(self.rightLeg)
        self.robot.append(self.leftLeg)

    ############################################################
    #                        Utils methods                     #
    ############################################################

    def updateCOP(self, data, foot):
        if foot is self.rightFootCop:
            self.rightFootCop = np.array(data)
        else:
            self.leftFootCop = np.array(data)
        #self._ax.clear()
        self.drawRobot()

    def drawRobot(self):
        # The dimension of the feet
        feetDimension = np.array([[235, 85, 0], [235, -85, 0], [0, -85, 0], [-85, 0, 0], [0, 85, 0]])
        # Starting from each COPs we draw the foot
        for member in self.robot:
            if member is self.rightFootCop or member is self.leftFootCop:
                self.X = feetDimension[:, 0] + member[0]
                self.Y = feetDimension[:, 1] + member[1]
                self.Z = feetDimension[:, 2] + member[2]
                self.plotScatterFeet(member)
            elif member is self.rightKnee or member is self.leftKnee:
                self.plotScatterKnees(member)
            elif member is self.rightLeg or member is self.leftLeg:
                self.plotScatterLegs(member)

    def plotScatterFeet(self, foot):
        # Set the data in the table
        # row = 0 if foot is self.rightFootCop else 1
        # self.table_widget.set_table_data(foot, row)
        # Clear the 5 plot to draw the feet
        self._ax.scatter(self.X, self.Y, self.Z, c='0.1', marker='.', s=7)
        # Create a triangulation of the points
        triang = mtri.Triangulation(self.X, self.Y)
        # Plot the surface
        self._ax.plot_trisurf(self.X, self.Y, self.Z, triangles=triang.triangles, color="gainsboro", alpha=0.6,
                              edgecolor='grey')
        self._ax.scatter(foot[0], foot[1], foot[2], c='r', marker='+', s=50)
        self.canvas.draw()

    def plotScatterKnees(self, knee):
        self._ax.scatter(knee[0], knee[1], knee[2], c='0.1', marker='.', s=7)
        foot = self.rightFootCop if knee is self.rightKnee else self.leftFootCop
        self._ax.plot(*zip(knee, foot), c='grey')
        self.canvas.draw()

    def plotScatterLegs(self, leg):
        self._ax.scatter(leg[0], leg[1], leg[2], c='0.1', marker='.', s=7)
        knee = self.rightKnee if leg is self.rightLeg else self.leftKnee
        self._ax.plot(*zip(leg, knee), c='grey')
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget3DPlot()
    widget.show()
    sys.exit(app.exec_())
