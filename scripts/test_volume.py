import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow
from pyqtgraph import PlotWidget
import pyqtgraph as pg
from PyQt5.QtGui import QColor, QBrush
import pyaudio

class VolumeBarGraph(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 创建 PlotWidget 并设置它为窗口的中心 widget
        self.graphWidget = PlotWidget()
        self.setCentralWidget(self.graphWidget)

        # 设置图形样式
        self.graphWidget.setBackground('w')
        self.graphWidget.showGrid(x=True, y=True)

        # 初始化数据
        self.x = np.arange(0, 100, 2)  # x 轴，增加间距
        self.y = np.zeros(50)  # 初始化音量值为0

        color = QColor(250, 249, 222)
        brush = QBrush(color)

        # 创建柱状图项，设置宽度为1.0
        self.bar_item = pg.BarGraphItem(x=self.x, height=self.y, width=5.0, brush=brush)
        self.graphWidget.addItem(self.bar_item)

        # 设置音频流
        self.chunk = 1024  # 数据块大小
        self.rate = 44100  # 采样率
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=self.rate,
                                  input=True,
                                  frames_per_buffer=self.chunk)

        # 启动定时器，用于实时更新音量
        self.timer = pg.QtCore.QTimer()
        self.timer.setInterval(200)  # 每50ms更新一次
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):
        # 读取音频数据并计算音量
        data = np.frombuffer(self.stream.read(self.chunk, exception_on_overflow=False), dtype=np.int16)
        volume = np.abs(data).mean()  # 简单计算音量

        # 更新数据并重新绘制柱状图
        self.y = np.roll(self.y, -1)
        self.y[-1] = volume
        self.bar_item.setOpts(height=self.y)

    def closeEvent(self, event):
        # 关闭音频流
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = VolumeBarGraph()
    main.show()
    sys.exit(app.exec_())