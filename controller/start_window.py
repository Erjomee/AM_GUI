from PyQt5 import QtWidgets, uic

class StartWindow(QtWidgets.QDialog):
    """
    Dialog window for the start screen of the application.

    Attributes:
        active (bool): Indicates if the start window is active.
        is_showed (bool): Indicates if the start window has been displayed.

    Methods:
        __init__(self):
            Initializes the StartWindow dialog.
        startAPP(self):
            Starts the application after running necessary setup tasks.
        closeEvent(self, event):
            Handles the close event of the dialog window.

    Example Usage:
        # Example of creating and using StartWindow in a PyQt5 application
        start_window = StartWindow()
        start_window.show()
        start_window.startAPP()
    """

    def __init__(self):
        """
        Initializes the StartWindow dialog by loading its UI from 'views/ui/startwindow.ui'.
        Sets up the fixed size of the dialog and connects button click signals.

        Returns:
            None
        """
        super(StartWindow, self).__init__()

        self.active = True  # Start window is initially active
        self.is_showed = False  # Start window is initially not shown

        uic.loadUi('views/ui/startwindow.ui', self)  # Load UI file into the dialog
        self.setFixedSize(450, 300)  # Set fixed size for the dialog

        # Connect signals to slots
        self.StartButton = self.findChild(QtWidgets.QPushButton, "StartButton")
        self.StartButton.clicked.connect(self.closeEvent)  # Connect start button to closeEvent method

        self.QuitButton = self.findChild(QtWidgets.QPushButton, "QuitButton")
        self.QuitButton.clicked.connect(self.closeEvent)  # Connect quit button to closeEvent method

    def startAPP(self):
        """
        Starts the application after performing necessary setup tasks.

        Returns:
            None
        """
        self.run_serv()  # Perform setup tasks
        self.active = False  # Mark start window as inactive

    def closeEvent(self, event):
        """
        Handles the close event of the dialog window.

        Args:
            event (QCloseEvent): Close event object

        Returns:
            None
        """
        self.active = False  # Mark start window as inactive
        self.close()  # Close the dialog window
