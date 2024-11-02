import sys
import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QColor, QPalette

class BouncingBall(QtWidgets.QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.view = pg.GraphicsLayoutWidget()
        self.view.setBackground(pg.mkColor(155, 187, 255))

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

        self.plot = self.view.addPlot()
        self.plot.setYRange(0, 20)
        self.plot.setXRange(-5, 5)

        self.ball = pg.ScatterPlotItem(size=30, pen=pg.mkPen('w'), brush=pg.mkBrush('b'))
        self.plot.addItem(self.ball)

        self.y_pos = 1
        self.direction = 1  # 1 for up, -1 for down
        # self.view.setTitle("fsdfadfs")

    def update_ball_position(self,max):
        self.y_pos += 0.1 * self.direction

        if self.y_pos >= 9 or self.y_pos <= 1:
            self.direction *= -1  # Change direction

        self.ball.setData(x=[0], y=[max])  # Keep x constant at 5

class plainView(QtWidgets.QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.view = pg.GraphicsLayoutWidget()
        # self.view.setBackground(pg.mkColor(0, 255, 0))

        # layout = QtWidgets.QVBoxLayout()
        # layout.addWidget(self.view)
        # self.setLayout(layout)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = BouncingBall()
    window.show()
    sys.exit(app.exec_())