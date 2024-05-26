import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from server.dummy_server import Server
from views.QtWidgets.start_window import StartWindow
from views.QtWidgets.main_window import MainWindow
# from views.QtWidgets.exit_window import ExitWindow


class AM_GUI():
    def __init__(self):
        self.is_running = True
        self.start_window = StartWindow()
        self.main_window = MainWindow()

    def run_app(self):
        # Showing Start Window
        self.start_window.show()
        self.start_window.StartButton.clicked.connect(self.show_main_window)

    def show_main_window(self):
        # Starting server
        self.main_window.run_serv()
        # Showing Main Window
        self.main_window.show()

    def quit_app(self):
        self.is_running = False
        self.server.stop_server()
        sys.exit(0)
            
       
