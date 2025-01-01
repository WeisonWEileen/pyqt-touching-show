import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtChart import QChart, QChartView, QBarSet, QBarSeries, QValueAxis
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt

class SinBarChart(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sin Function Bar Chart")
        self.setGeometry(100, 100, 800, 600)

        self.chart = QChart()
        self.chart.setTitle("Real-time Sin Function Bar Chart")

        self.series = QBarSeries()
        self.bar_set = QBarSet("Sin Value")
        self.series.append(self.bar_set)
        self.chart.addSeries(self.series)

        self.axis_x = QValueAxis()
        self.axis_x.setRange(0, 5)
        self.axis_x.setLabelFormat("%d")
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.series.attachAxis(self.axis_x)

        self.axis_y = QValueAxis()
        self.axis_y.setRange(-1, 1)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.series.attachAxis(self.axis_y)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_chart)
        self.timer.start(100)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.chart_view)

        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        self.time = 0
        self.x_data = []

    def update_chart(self):
        self.time += 0.1
        sin_value = np.sin(self.time)
        
        # Update x_data and bar_set
        self.x_data.append(self.time)
        self.bar_set.append(sin_value)
        
        # Keep only the last 10 seconds of data
        if len(self.x_data) > 100:
            self.x_data.pop(0)
            self.bar_set.remove(0)
        
        # Update x axis range
        self.axis_x.setRange(self.x_data[0], self.x_data[-1])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SinBarChart()
    window.show()
    sys.exit(app.exec_())