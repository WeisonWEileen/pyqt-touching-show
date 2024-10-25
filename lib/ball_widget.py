import sys
import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QColor, QPalette

class BouncingBall(QtWidgets.QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.view = pg.GraphicsLayoutWidget()
        self.view.setBackground(pg.mkColor(255, 0, 0))

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

        self.plot = self.view.addPlot()
        self.plot.setYRange(0, 10)
        self.plot.setXRange(0, 10)

        self.ball = pg.ScatterPlotItem(size=30, pen=pg.mkPen('w'), brush=pg.mkBrush('b'))
        self.plot.addItem(self.ball)

         # 设置自身的黑色边框
        self.setStyleSheet("""
            QGroupBox {
                border: 2px solid black;  /* 边框颜色和粗细 */
                border-radius: 5px;       /* 边框圆角半径 */
                margin-top: 10px;         /* 标题上方的间距 */
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center; /* 标题位置 */
                padding: 0 3px;                 /* 标题内边距 */
                color: black;                   /* 标题颜色 */
            }
        """)

        self.y_pos = 1
        self.direction = 1  # 1 for up, -1 for down
        # self.view.setTitle("fsdfadfs")

    def update_ball_position(self,max):
        self.y_pos += 0.1 * self.direction

        if self.y_pos >= 9 or self.y_pos <= 1:
            self.direction *= -1  # Change direction

        self.ball.setData(x=[5], y=[max])  # Keep x constant at 5

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = BouncingBall()
    window.show()
    sys.exit(app.exec_())