import sys
import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets

class BouncingBall(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Bouncing Ball')
        self.setGeometry(100, 100, 600, 400)

        self.view = pg.GraphicsLayoutWidget()
        self.setCentralWidget(self.view)


        self.plot = self.view.addPlot()
        self.plot.setYRange(0, 10)
        self.plot.setXRange(0, 10)
        self.setStyleSheet("background-color: yellow;")

        self.ball = pg.ScatterPlotItem(size=20, pen=pg.mkPen('w'), brush=pg.mkBrush('b'))
        self.plot.addItem(self.ball)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_ball_position)
        self.timer.start(50)

        self.y_pos = 1
        self.direction = 1  # 1 for up, -1 for down

    def update_ball_position(self):
        self.y_pos += 0.1 * self.direction

        if self.y_pos >= 9 or self.y_pos <= 1:
            self.direction *= -1  # Change direction

        self.ball.setData(x=[5], y=[self.y_pos])  # Keep x constant at 5

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = BouncingBall()
    window.show()
    sys.exit(app.exec_())
