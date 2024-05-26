import sys
from PyQt5 import QtWidgets
from am_gui import *

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AM_GUI()
    window.run_app()
    sys.exit(app.exec_())
