from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):
    """
    Matplotlib canvas embedded in a PyQt5 application for plotting.

    Attributes:
        axes (matplotlib.axes.Axes): Axes for plotting within the figure.

    Methods:
        __init__(self, parent=None, width=5, height=4, dpi=0):
            Initializes a Matplotlib canvas with specified dimensions and DPI.

    Example Usage:
        # Example of creating and using MplCanvas in a PyQt5 application
        canvas = MplCanvas(parent=self, width=6, height=4, dpi=100)
        canvas.axes.plot(x_data, y_data, label='Data')
        canvas.axes.legend()
    """

    def __init__(self, parent=None, width=5, height=4, dpi=0):
        """
        Initializes a Matplotlib canvas within a PyQt5 application.

        Args:
            parent (QWidget, optional): Parent widget to which the canvas belongs. Default is None.
            width (int, optional): Width of the figure in inches. Default is 5.
            height (int, optional): Height of the figure in inches. Default is 4.
            dpi (int, optional): Dots per inch (resolution) of the figure. Default is 0, which uses the system DPI.

        Returns:
            None
        """
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)  # Create a single subplot within the figure
        super(MplCanvas, self).__init__(fig)
