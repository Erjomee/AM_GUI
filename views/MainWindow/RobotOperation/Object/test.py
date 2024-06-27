import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import QTimer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.timer = QTimer()
        self.timer.timeout.connect(self.process_iteration)

        self.iterations = 0
        self.max_iterations = 10  # Nombre total d'itérations
        self.interval = 1000  # Intervalle en millisecondes (1 seconde)

    def initUI(self):
        self.setWindowTitle("PyQt5 Timer Loop Example")

        self.start_button = QPushButton("Start Loop", self)
        self.start_button.clicked.connect(self.start_loop)

        self.stop_button = QPushButton("Stop Loop", self)
        self.stop_button.clicked.connect(self.stop_loop)

        self.status_label = QLabel("Press 'Start Loop' to begin", self)

        layout = QVBoxLayout()
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_loop(self):
        self.iterations = 0
        self.status_label.setText(f"Iteration: {self.iterations}")
        self.timer.start(self.interval)

    def stop_loop(self):
        self.timer.stop()
        self.status_label.setText("Loop stopped")

    def process_iteration(self):
        self.iterations += 1
        self.status_label.setText(f"Iteration: {self.iterations}")

        # Effectuer le traitement de chaque itération ici
        print(f"Processing iteration {self.iterations}")

        if self.iterations >= self.max_iterations:
            self.timer.stop()
            self.status_label.setText("Loop finished")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
