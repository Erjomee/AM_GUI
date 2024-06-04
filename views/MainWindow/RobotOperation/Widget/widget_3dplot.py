import sys

import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.tri as mtri
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QWidget)


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
        self._ax.set_zlim([0, 500])
        self._ax.set_xlabel("X Label")
        self._ax.set_ylabel("Y Label")
        self._ax.set_zlabel("Z Label")

    def initRobot(self):
        # The dimension of the feet
        self.feetDimension = np.array([[235, 85, 0], [235, -85, 0], [0, -85, 0], [-85, 0, 0], [0, 85, 0]])
        # Dictionary where all the parts of the robot will be stored
        self.robot = {'left': {}, 'right': {}}
        # Coordinates for the left side
        self.robot['left']['FootCentralPoint'] = np.array([0, 185, self._ax.get_zlim3d()[0]])
        self.robot['left']['Knee'] = np.array([0, 185, 200])
        self.robot['left']['Hip'] = np.array([0, 185, 400])
        # Coordinates for the right side
        self.robot['right']['FootCentralPoint'] = np.array([0, -185, self._ax.get_zlim3d()[0]])
        self.robot['right']['Knee'] = np.array([0, -185, 200])
        self.robot['right']['Hip'] = np.array([0, -185, 400])

    ############################################################
    #                        Utils methods                     #
    ############################################################

    def update_coords(self, new_left_coords, new_right_coords):
        # Condition to know which foot is moving
        if self.robot['left']['FootCentralPoint'][0] != new_left_coords[0] or self.robot['left']['FootCentralPoint'][1] != new_left_coords[1]:
            self.update_foot_positions('left', new_left_coords)
            self.update_knee_positions('left', new_left_coords)
            self.update_hip_positions('left', new_left_coords)
            # Updating the opposite hip and knee to give a realistic movement
            self.update_hip_positions('right', new_right_coords)
            self.update_knee_positions('right', new_right_coords)
        else:
            self.update_foot_positions('right', new_right_coords)
            self.update_knee_positions('right', new_right_coords)
            self.update_hip_positions('right', new_right_coords)
            # Updating the opposite hip and knee to give a realistic movement
            self.update_hip_positions('left', new_left_coords)
            self.update_knee_positions('left', new_left_coords)
        self.redraw_robot()

    def update_foot_positions(self, side, new_coords):
        foot = self.robot[side]['FootCentralPoint']
        self.robot[side]['FootCentralPoint'] = np.array([new_coords[0], new_coords[1], foot[2]])

    def update_knee_positions(self, side, new_coords):
        knee = self.robot[side]['Knee']
        self.robot[side]['Knee'] = np.array([new_coords[0], new_coords[1], knee[2]])

    def update_hip_positions(self, side, new_coords):
        hip = self.robot[side]['Hip']
        foot = self.robot['right' if side == 'left' else 'left']['FootCentralPoint']
        self.robot[side]['Hip'] = np.array([(foot[0] + new_coords[0]) / 2, new_coords[1], hip[2]])

    def redraw_robot(self):
        self.resetPlot()
        self.drawRobot()

    def resetPlot(self):
        for artist in self._ax.collections + self._ax.lines:
            artist.remove()

    def drawRobot(self):
        for side in self.robot.keys():
            for part_name, member in self.robot[side].items():
                if part_name == 'FootCentralPoint':
                    self.plotScatterFeet(member)
                elif part_name == 'Knee':
                    self.plotScatterKnees(member, side)
                elif part_name == 'Hip':
                    self.plotScatterLegs(member, side)
        self.plotScatterHips()

    def plotScatterFeet(self, foot):
        X = self.feetDimension[:, 0] + foot[0]
        Y = self.feetDimension[:, 1] + foot[1]
        Z = self.feetDimension[:, 2] + foot[2]
        # Clear the 5 plot to draw the feet
        self._ax.scatter(X, Y, Z, c='0.1', marker='.', s=7)
        # Create a triangulation of the points
        triang = mtri.Triangulation(X, Y)
        # Plot the surface
        self._ax.plot_trisurf(X, Y, Z, triangles=triang.triangles, color="gainsboro", alpha=0.6, edgecolor='grey')
        self._ax.scatter(*foot, c='r', marker='+', s=50)
        self.canvas.draw()

    def plotScatterKnees(self, knee, side):
        self._ax.scatter(*knee, c='0.1', marker='.', s=7)
        foot = self.robot[side]['FootCentralPoint']
        self._ax.plot(*zip(knee, foot), c='grey')
        self.canvas.draw()

    def plotScatterLegs(self, hip, side):
        self._ax.scatter(*hip, c='0.1', marker='.', s=7)
        knee = self.robot[side]['Knee']
        self._ax.plot(*zip(hip, knee), c='grey')
        self.canvas.draw()

    def plotScatterHips(self):
        # Calculate the midpoint between the two legs to draw the hips
        rightHip = self.robot['right']['Hip']
        leftHip = self.robot['left']['Hip']
        midpoint = (rightHip + leftHip) / 2
        self._ax.scatter(*midpoint, c='blue', marker='|', s=20)
        self.move_plan(midpoint[0], midpoint[1])
        # Get the z limits to draw the vertical line of the center of mass
        z_min, z_max = self._ax.get_zlim()
        self._ax.plot([midpoint[0], midpoint[0]], [midpoint[1], midpoint[1]], [z_min, z_max], c='blue', alpha=0.3)
        # Draw the line that connects the hips
        self._ax.plot(*zip(rightHip, leftHip), c='grey')
        self.canvas.draw()

    def move_plan(self, x, y):
        self._ax.set_xlim(x - 500, x + 500)
        self._ax.set_ylim(y - 500, y + 500)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget3DPlot()
    widget.show()
    sys.exit(app.exec_())
