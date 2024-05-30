import sys
from Controller.start_window import StartWindow
from Controller.main_window import MainWindow
# from views.QtWidgets.exit_window import ExitWindow

class AM_GUI():
    def __init__(self):
        self.is_running = True
        self.start_window = StartWindow()
        self.main_window = None

    def run_app(self):
        # Showing Start Window
        self.start_window.show()
        self.start_window.StartButton.clicked.connect(self.show_main_window)

    def show_main_window(self):
        self.main_window = MainWindow()
        
        # Starting server
        self.main_window.run_serv()
        # Showing Main Window
        self.main_window.show()

    def quit_app(self):
        self.is_running = False
        self.server.stop_server()
        sys.exit(0)
            
       
