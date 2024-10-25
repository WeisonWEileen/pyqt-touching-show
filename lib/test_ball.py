import sys
import pyqtgraph as pg
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QGroupBox
from PyQt5.QtGui import QColor, QPalette


class BouncingBall(QGroupBox):
    def __init__(self, parent=None):
        super().__init__()

        self.setGeometry(100, 100, 600, 400)

        self.view = pg.GraphicsLayoutWidget(title="fuckyout")
        # self.view.setBackground(pg.mkColor(255, 0, 0))
        self.view.setTitle("fsdfadfs")
        # 暂时放弃,好像全局设置更加好
        # self.view.setBackground(pg.ImageView ('F:\\fpga\\usb_cap8x8_v1\\asserts\\nk.jpg'))
        self.setCentralWidget(self.view)

        self.plot = self.view.addPlot()
        self.plot.setYRange(0, 10)
        self.plot.setXRange(0, 10)


        self.ball = pg.ScatterPlotItem(size=40, pen=pg.mkPen('w'), brush=pg.mkBrush(pg.mkColor(255, 0, 0)))
        self.plot.addItem(self.ball)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_ball_position)
        self.timer.start(50)

        self.setWindowTitle('高度实时显示')
        self.y_pos = 1
        self.direction = 1  # 1 for up, -1 for down

    def update_ball_position(self):
        self.y_pos += 0.1 * self.direction

        if self.y_pos >= 9 or self.y_pos <= 1:
            self.direction *= -1  # Change direction

        self.ball.setData(x=[5], y=[self.y_pos])  # Keep x constant at 5

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BouncingBall()
    window.show()
    sys.exit(app.exec_())
