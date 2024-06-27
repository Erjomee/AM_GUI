from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
import pyqtgraph as pg
from PyQt5.QtGui import QPen, QColor, QCursor


class DriversPlotsWidgets:
    def __init__(self, main_window):
        self.driver_widgets = {}
        self.hover_labels = {}  # Dictionnaire pour stocker les labels de survol
        self.infinite_lines = {}  # Dictionnaire pour stocker les lignes infinies
        self.driver = ["LH_Abd", "RH_Abd", "LH_Rot", "RH_Rot", "LH_Flex", "RH_Flex", "LK", "RK", "LA_Lat", "RA_Lat",
                       "LA_Med", "RA_Med"]

        self.temp_plot_styles = {"color": "black", "font-size": "20px"}
        self.amp_plot_styles = {"color": "yellow", "font-size": "20px"}

        self.init_plots(main_window)

    def init_plots(self, main_window):
        for driver in self.driver:
            # Initialize plot widget
            plot_graph = pg.PlotWidget()
            plot_graph.setBackground("w")

            # Left Axis
            left_axis = plot_graph.getAxis("left")
            left_axis.setRange(0, 100)

            # Right Axis
            right_axis = pg.AxisItem("right")
            right_axis.setRange(-100, 100)

            # Set right axis color
            pen_right_axis = QPen(QColor("red"))
            right_axis.setPen(pen_right_axis)

            plot_graph.setAxisItems({'right': right_axis})

            # Bottom Axis
            plot_graph.setLabel("bottom", "Time (s)", **{"color": "blue", "font-size": "20px"})
            plot_graph.addLegend()
            plot_graph.showGrid(x=True, y=True, alpha=0.1)

            plt_driver_widget = main_window.findChild(QWidget, f"{driver}_plot")
            if plt_driver_widget:
                layout = QVBoxLayout(plt_driver_widget)
                layout.addWidget(plot_graph)
            self.driver_widgets[driver] = plot_graph

            # Create label for displaying mouse hover information
            hover_label = QLabel(plt_driver_widget)
            hover_label.setStyleSheet("background-color: white; color: black;")
            layout.addWidget(hover_label)
            self.hover_labels[driver] = hover_label  # Store the label in the dictionary

            # Create an InfiniteLine for vertical cursor
            pen_inf_line = QPen(QColor(0, 0, 255, 128))  # Blue with 50% opacity (255 * 0.5 = 128)
            inf_line = pg.InfiniteLine(angle=90, movable=False, pen=pen_inf_line)
            inf_line.hide()  # Hide the line initially
            plot_graph.addItem(inf_line)
            self.infinite_lines[driver] = inf_line  # Store the InfiniteLine in the dictionary

            # Connect the mouse move event to the custom function
            plot_graph.scene().sigMouseMoved.connect(
                lambda pos, plot=plot_graph, label=hover_label, line=inf_line: self.on_mouse_moved(pos, plot, label,
                                                                                                   line))

    def on_mouse_moved(self, pos, plot_graph, hover_label, inf_line):
        vb = plot_graph.plotItem.vb
        if plot_graph.sceneBoundingRect().contains(pos):
            mouse_point = vb.mapSceneToView(pos)

            # Taking dimensions et mouse pos
            x = mouse_point.x()
            y = mouse_point.y()
            x_range = plot_graph.getViewBox().viewRange()[0]
            x_start, x_end = x_range
            axe_x_length = x_end - x_start

            # Handling Label for position mouse update
            hover_label.setText(f"x={x:.2f}, y={y:.2f}")
            hover_label.move(QCursor.pos())

            # Handling vertical line item for mouse pos
            self.remove_infinite_lines(plot_graph) # Remove ancient infinite_lines pos

            pen_width = axe_x_length * 0.02 # Taking 1% of the x axe width
            pen = QPen(QColor(0, 0, 255, 128))  # Blue with 50% opacity (255 * 0.5 = 128)
            pen.setWidthF(pen_width)

            inf_line.setPen(pen)

            inf_line.setPos(x)
            inf_line.show()
            if inf_line not in plot_graph.items():
                plot_graph.addItem(inf_line)

    def update_plots(self, time_data):
        time_seconds = (time_data['Usage_time'].apply(self.time_to_seconds) -
                        time_data['Usage_time'].apply(self.time_to_seconds).min())

        for driver, plot_graph in self.driver_widgets.items():
            if f"{driver}_Temp" in time_data.columns and f"{driver}_Amp" in time_data.columns:
                plot_graph.clear()

                pen_temp = pg.mkPen(color=(0, 0, 0), width=3)
                self.plot_line(plot_graph, "Temperature °C", time_seconds, time_data[f"{driver}_Temp"], pen_temp,
                               "r", "left")

                pen_amp = pg.mkPen(color=(240, 240, 0), width=3)
                self.plot_line(plot_graph, "Amperage %", time_seconds, time_data[f"{driver}_Amp"], pen_amp, "y",
                               "right")

                plot_graph.setLimits(xMin=0, xMax=time_seconds.max() + time_seconds.max() * 0.01,
                                     yMin=0, yMax=110)


    def plot_line(self, plot_graph, name, time, temperature, pen, brush, axis):
        plot_graph.plot(
            time,
            temperature,
            name=name,
            pen=pen,
            axis=axis
        )

    def remove_infinite_lines(self, plot_graph):
        for driver , line in self.infinite_lines.items():
            plot_graph.removeItem(line)
        plot_graph.update()

    def time_to_seconds(self, time_string):
        parts = time_string.split(':')
        hours = int(parts[0]) * 3600
        minutes = int(parts[1]) * 60
        seconds = int(parts[2])
        milliseconds = int(parts[3]) / 1000
        return hours + minutes + seconds + milliseconds
