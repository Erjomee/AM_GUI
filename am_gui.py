import sys

from Controller.exit_window import ExitWindow
from Controller.start_window import StartWindow
from Controller.main_window.main_window import MainWindow

class AM_GUI:
    """
    A class to represent the main GUI application.

    Attributes:
    ----------
    is_running : bool
        A flag to indicate if the application is running.
    start_window : StartWindow
        An instance of the StartWindow class.
    main_window : MainWindow
        An instance of the MainWindow class.
    exit_window : ExitWindow
        An instance of the ExitWindow class.
    """

    def __init__(self):
        """Initialize the AM_GUI with default values."""
        self.is_running = True
        self.start_window = None
        self.main_window = None
        self.exit_window = None

    def run_app(self):
        """Start the application by showing the start window."""
        self.start_window = StartWindow()
        # Show the Start Window
        self.start_window.show()
        # Connect the StartButton click event to the show_main_window method
        self.start_window.StartButton.clicked.connect(self.show_main_window)

    def show_main_window(self):
        """Show the main window and start the server."""
        self.main_window = MainWindow()

        # Start the server
        self.main_window.run_serv()

        # Show the Main Window
        self.main_window.show()

        # Connect the window_closed signal to the show_exit_window method
        self.main_window.window_closed.connect(self.show_exit_window)
        # Connect the ForceQuitButton click event to the quit_app method
        self.main_window.ForceQuitButton.clicked.connect(self.quit_app)

    def show_exit_window(self):
        """Show the exit window when the main window is closed."""
        self.exit_window = ExitWindow()
        # Show the Exit Window
        self.exit_window.show()
        # Connect the window_closed signal to the run_app method
        self.exit_window.window_closed.connect(self.run_app)

    def quit_app(self):
        """Quit the application by stopping the server and exiting."""
        self.is_running = False
        # Stop the server
        self.main_window.server.stop_server()
        # Exit the application
        sys.exit(0)
