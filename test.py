import sys, math
from PyQt5 import QtCore, QtGui, QtWidgets

class MyWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.pen = QtGui.QPen(QtGui.QColor(0,0,0))                      # set lineColor
        self.pen.setWidth(3)                                            # set lineWidth
        self.brush = QtGui.QBrush(QtGui.QColor(255,255,255,255))        # set fillColor
        self.polygon = self.createPoly()                         # polygon with n points, radius, angle of the first point

    def createPoly(self):
        polygon = QtGui.QPolygonF()

        polygon.append(QtCore.QPointF(0, 0))
        polygon.append(QtCore.QPointF(50, 0))
        polygon.append(QtCore.QPointF(50, 50))
        polygon.append(QtCore.QPointF(0, 50))

        return polygon

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        painter.drawPolygon(self.polygon)

app = QtWidgets.QApplication(sys.argv)

widget = MyWidget()
widget.show()

sys.exit(app.exec_())