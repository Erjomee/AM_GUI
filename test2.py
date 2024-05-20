import sys
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsRectItem, QApplication, QGraphicsPixmapItem
from PyQt5.QtGui import QBrush, QPen, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot

class CustomGraphicsView(QGraphicsView):
    def resizeEvent(self, event):
        self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)
        super().resizeEvent(event)


app = QApplication(sys.argv)

# Defining a scene rect of 400x200, with its origin at 0,0.
# If we don't set this on creation, we can set it later with .setSceneRect
scene = QGraphicsScene(0, 0, 500, 700)

# Draw a rectangle item, setting the dimensions.
rect = QGraphicsRectItem(0, 0, 200, 50)

# Set the origin (position) of the rectangle in the scene.
rect.setPos(50, 20)

# Define the brush (fill).
brush = QBrush(Qt.red)
rect.setBrush(brush)

# Define the pen (line)
pen = QPen(Qt.cyan)
pen.setWidth(10)
rect.setPen(pen)

scene.addItem(rect)

# Load the left foot pixmap
left_foot_pixmap = QPixmap('assets/left_foot_model.png')

# Create a QGraphicsPixmapItem with the pixmap
left_foot_pixmap_item = QGraphicsPixmapItem(left_foot_pixmap)

# Optionally, set the position of the pixmap in the scene
left_foot_pixmap_item.setPos(100, 100)

# Add the QGraphicsPixmapItem to the scene
scene.addItem(left_foot_pixmap_item)

# Create the custom view and set the scene
view = CustomGraphicsView(scene)
view.show()
app.exec_()
