import sys

from Controller.exit_window import ExitWindow
from Controller.start_window import StartWindow
from Controller.main_window.main_window import MainWindow


class AM_GUI:
    def __init__(self):
        self.is_running = True
        self.start_window = None
        self.main_window = None
        self.exit_window = None

    def run_app(self):
        self.start_window = StartWindow()
        # Showing Start Window
        self.start_window.show()
        self.start_window.StartButton.clicked.connect(self.show_main_window)

    def show_main_window(self):
        self.main_window = MainWindow()

        # Starting server
        self.main_window.run_serv()

        # Showing Main Window
        self.main_window.show()

        # Connect the close signal to show_exit_window
        self.main_window.window_closed.connect(self.show_exit_window)
        self.main_window.ForceQuitButton.clicked.connect(self.quit_app)

    def show_exit_window(self):
        self.exit_window = ExitWindow()
        # Showing Exit Window
        self.exit_window.show()
        # Connect the close signal to show_exit_window
        self.exit_window.window_closed.connect(self.run_app)


    def quit_app(self):
        self.is_running = False
        self.main_window.server.stop_server()
        sys.exit(0)


