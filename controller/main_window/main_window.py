import threading
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from controller.main_window.Tabs.data_check import DataCheck
from controller.main_window.Tabs.robot_operation import RobotOperation
from controller.main_window.Tabs.turn_and_debug import TurnAndDebug
from server.dummy_server import Server

SERVER_IP = "localhost"
SERVER_PORT = 1818

class MainWindow(QtWidgets.QTabWidget):
    """
    Main application window with multiple tabs and server integration.

    Signals:
        window_closed: Signal emitted when the window is closed.

    Attributes:
        active (bool): Flag indicating if the window is active.
        server (Server): Instance of the server handling data communication.
        tabs (list): List of tabs (QWidget instances) in the main window.

    Methods:
        __init__(): Initializes the MainWindow instance.
        run_serv(): Starts the server in a separate thread and connects data update signal.
        closeEvent(event): Manages the close event of the window, stops the server and emits window_closed signal.
        updateData(data): Updates data in all tabs using the received data list.
    """

    window_closed = pyqtSignal()

    def __init__(self):
        """
        Initializes the MainWindow instance.

        Loads the UI layout from a .ui file, initializes a server instance,
        and loads all tabs (QWidget instances) of the main window.

        """
        super(MainWindow, self).__init__()
        self.active = False

        # Load Main Window UI
        uic.loadUi('views/ui/mainwindow.ui', self)

        # Launch server listener
        self.server = Server(SERVER_IP, SERVER_PORT)

        # Load all tabs of the Main Window
        self.turn_and_debug = TurnAndDebug(self)
        self.robot_operation = RobotOperation(self)
        self.data_check = DataCheck(self)

        # List of tabs that may need data updates
        self.tabs = [self.robot_operation, self.turn_and_debug]

        # Connect the ForceQuitButton
        self.ForceQuitButton = self.findChild(QtWidgets.QPushButton, "force_quit_button")

    def run_serv(self):
        """
        Starts the server in a separate thread and connects data update signal.

        Uses threading to start the server in the background. Connects the newData
        signal from the server instance to the updateData slot.

        """
        server_thread = threading.Thread(target=self.server.start_server)
        self.server.newData.connect(self.updateData)
        server_thread.start()

    def closeEvent(self, event):
        """
        Manages the close event of the window.

        Stops the server, closes the window, and emits the window_closed signal.

        :param event: Close event object.
        """
        self.active = False  # Window is no longer active
        self.server.stop_server()  # Stop the server
        self.close()  # Close the window
        self.window_closed.emit()  # Emit the signal before closing

    @pyqtSlot(list)
    def updateData(self, data):
        """
        Updates data in all tabs of the main window.

        Receives data from the server and updates each tab with the new data.

        :param data: List containing updated data.
        """
        for tab in self.tabs:
            tab.update(data)

