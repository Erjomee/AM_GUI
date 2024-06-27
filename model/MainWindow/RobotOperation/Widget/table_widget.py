import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QTableWidget, QTableWidgetItem, QWidget, QHeaderView


class Widget3DTable(QWidget):
    def __init__(self, parent=None):
        super(Widget3DTable, self).__init__(parent)
        self.column_names = ["X Label", "Y Label", "Z Label"]
        self.initUI()
        self.initTableConfiguration()

    def initUI(self):
        # Initialize the layout and table
        self.table = QTableWidget()
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        layout = QVBoxLayout(self)
        layout.addWidget(self.table)

    def initTableConfiguration(self):
        # Configure the table with rows, columns, and headers
        self.table.setRowCount(2)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(self.column_names)
        # Set the background color of the table
        self.table.setStyleSheet("QTableWidget { background-color: lightgray; color: blue; }"
                                 "QHeaderView::section { background-color: gray; color: white; }"
                                 "QTableCornerButton::section { background-color: gray; }")
        self.table.resizeColumnsToContents()

    def set_table_data(self, data, row):
        # Set data in the table for the given row
        for i in range(3):
            self.table.setItem(row, i, QTableWidgetItem(f"{data[i]:.2f}"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget3DTable()
    widget.show()
    sys.exit(app.exec_())
