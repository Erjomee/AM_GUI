from PyQt5 import uic
from PyQt5.QtCore import QTimer


class RobotOperation:
    def __init__(self):
        self.active_time = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_usage_time)

    def initUI(self):
        self.foot_widget = FootWidget(self)
        central_widget = self.findChild(QtWidgets.QWidget, "animation_widget")
        layout = QtWidgets.QVBoxLayout(central_widget)
        # Create the plot widget
        self.plot_widget = Widget3DPlot()
        layout.addWidget(self.plot_widget, 70)
