import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QColor, QPalette

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple QMainWindow")
        self.setGeometry(100, 100, 800, 600)

        # 设置背景颜色为红色
        palette = self.palette()
        palette.setColor(QPalette.Background, QColor(255, 0, 0))
        self.setPalette(palette)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
