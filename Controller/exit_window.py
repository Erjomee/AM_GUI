from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import pyqtSignal


class ExitWindow(QtWidgets.QDialog):
    window_closed = pyqtSignal()

    def __init__(self):

        super(ExitWindow, self).__init__()

        self.active = True
        self.is_showed = False

        uic.loadUi('views/ExitWindow/ui/exitwindow.ui', self)
        self.setFixedSize(450, 300)  # Set fixed size
        #
        # Start a QTimer to close the window after 2 seconds
        self.timer = QtCore.QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.activate_close_event)
        self.timer.start(2000)  # 2000 milliseconds = 2 seconds


    def startAPP(self):
        self.run_serv()
        self.active = False

    def activate_close_event(self):
        self.active = False
        self.close()
        self.window_closed.emit()  # Emit the signal before closing

    # Manage close event
    def closeEvent(self, event):
        if self.active:
            event.ignore()  # Ignore the close event if active
        else:
            super(ExitWindow, self).closeEvent(event)  # Call the base class method to close the window

