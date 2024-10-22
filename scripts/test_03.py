# import os
# import sys
# sys.path.insert(0, os.getcwd())
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np
import random 
import matplotlib.pyplot as plt
import multiprocessing
from multiprocessing import Queue
import lib.usb_get as usb_get
from lib.ui_ball import Ui_Form
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
import sys
import time
import threading
import serial
import pandas as pd
import csv


class PLOT_3D(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.setWindowIcon(QIcon('asserts/image.png'))
        self.init() #界面按钮初始化

        # 绘图部件
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        ## Create a GL View widget to display data
        #self.app = pg.mkQApp("GLSurfacePlot Example")
        self.w = gl.GLViewWidget()
        self.w.show()
        self.w.setWindowTitle('pyqtgraph example: GLSurfacePlot')
        self.w.setCameraPosition(distance=64)

        ## Add a grid to the view
        self.g = gl.GLGridItem()
        self.g.scale(2, 2, 1)
        self.g.setDepthValue(10)  # draw grid after surfaces since they may be translucent
        self.w.addItem(self.g)


        ## Manually specified colors
        self.z = pg.gaussianFilter(np.random.normal(size=(64, 64)), (1, 1))
        self.x = np.linspace(-12, 12, 64)
        self.y = np.linspace(-12, 12, 64)

        self.cmap = plt.get_cmap('rainbow')
        self.minZ=np.min(self.z)
        self.maxZ=np.max(self.z)
        self.rgba_img = self.cmap((self.z-self.minZ)/(self.maxZ -self.minZ))

        self.p3 = gl.GLSurfacePlotItem(z=self.z,colors=self.rgba_img)
        self.p3.scale(16. / 49., 16. / 49., 1.0)
        self.p3.translate(-10, -10, 0)
        self.w.addItem(self.p3)


        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(1)

        self.timer_save = QtCore.QTimer()
        self.timer_save.timeout.connect(self.save_timer)



        self.usbdata = usb_get.USB_DataDecode()
        self.sensor = []

        self.verticalLayout_graph.addWidget(self.w)  # 添加绘图部件到网格布局层

    """定义信号与槽"""

    def init(self):
        # 打开按钮
        self.open_button.clicked.connect(self.port_open)
        # 关闭按钮
        self.close_button.clicked.connect(self.port_close)

        # 清空
        self.start_measure_button.clicked.connect(self.start_measure)

        # 保存数据
        self.savedata_button.clicked.connect(self.save_data_button)

        # 退出应用
        self.quit_Button.clicked.connect(self.quit)

        self.timer_save = QtCore.QTimer()
        self.timer_save.timeout.connect(self.save_timer)
        self.savedata_button.setText("Start Save")


    def port_open(self):
        print("开始")
        self.clear_Queue(self.usbdata.data_out) #清空队列
        self.usbdata.GUI_order.put('start')     #发送开始
        self.textBrowser_3.append("开始检测")  # 在指定的区域显示提示信息
        self.timer_save.start(1)

    def start_measure(self):
        print("清空")
        self.sensor = []

    def port_close(self):
        self.usbdata.GUI_order.put('stop')  # 发送结束
        self.timer_save.stop()  # 停止
        self.sensor = []
        self.textBrowser_3.append("已停止")  # 在指定的区域显示提示信息
        print("已停止")

    def save_data(self):
        int_time = time.strftime("%Y年%m月%d日 %H时%M分%S秒", time.localtime())
        excel_npz = './lib/data_save/' + int_time + '_sensor.npz'
        # np.savez_compressed(excel_path, np.array(self.sensor[-5001:-1])) #保存5000个数据点
        np.savez_compressed(excel_npz, np.array(self.sensor))  # 保存全部数据

        # excel 保存
        self.sensor = np.array(self.sensor)
        print(self.sensor.shape)
        self.sensor = self.sensor.reshape(np.size(self.sensor, 0), 20)  # (//X,64)
        excel_data = pd.DataFrame(self.sensor)
        excel_path = './lib/data_save/' + int_time + '_sensor.xlsx'
        writer = pd.ExcelWriter(excel_path)
        excel_data.to_excel(writer, 'sheet_1', float_format='%.2f')
        writer.save()
        writer.close()

        self.sensor = []
        print("保存成功")

    def save_data_button(self):
        button_state = self.savedata_button.text()
        int_time = time.strftime("%Y年%m月%d日 %H时%M分%S秒", time.localtime())
        self.savepath =  './lib/data_save/' + int_time + '_sensor.csv'
        self.res = []

        if (button_state == 'Start Save'):
            self.savedata_button.setText("Complete save")
            self.clear_Queue(self.usbdata.data_out)  # 清空队列
            self.usbdata.GUI_order.put('start')  # 发送开始
            self.textBrowser_3.append("开始检测")  # 在指定的区域显示提示信息
            self.timer_save.start(10)     #定时保存时间 ms
            #初始化保存
            self.save_data_init(self.savepath)

        else:
            self.usbdata.GUI_order.put('stop')  # 发送结束
            self.timer_save.stop()  # 停止
            #self.save_data()  # 保存内容
            self.textBrowser_2.append("保存成功")  # 在指定的区域显示提示信息
            self.textBrowser_3.append("保存结束")  # 在指定的区域显示提示信息
            self.savedata_button.setText("Start Save")


    def quit(self):
        try:
            self.usbdata.close_usb()
        except:
            pass
        app.quit()
        print("成功退出")

    def save_data_init(self, filenname):
        time_head = ['times']
        data_head = ['sensor' + str(i) for i in range(1, 65)]
        headers = time_head + data_head
        with open(filenname, 'w',newline='') as form:
            writer = csv.writer(form)
            writer.writerow(headers)

    def write_data(self, data):
        filenname = self.savepath
        with open(filenname, 'a',newline='') as form:
            writer = csv.writer(form)
            writer.writerow(data)


    def save_timer(self):
        #计时显示
        int_time = time.strftime("%Y-%m-%d- %H:%M:%S", time.localtime())

        self.textBrowser_2.append(int_time )  # 在指定的区域显示提示信息

        while self.usbdata.data_out.qsize() > 0:
            self.res.append(self.usbdata.data_out.get())

        if len(self.res) > 0:
            self.res.reverse()
            self.sensor = self.res[-1]
            self.sensor = self.sensor.reshape(64)
            savedata = [int_time] + list(self.sensor)
            self.write_data(savedata)

    def clear_Queue(self,q):
        res = []
        while q.qsize() > 0:
            res.append(q.get())

    #绘图
    def update_plot(self):

        z = self.usbdata.plot_z.get(True)[0]
        self.clear_Queue(self.usbdata.plot_z) # 清空队列

        #3D绘图可视化

        z = pg.gaussianFilter(z,(4,4))   #高斯平滑


        # max = np.max(z)
        max_value_list = []
        while not self.usbdata.max_value_array.empty():
            max_value_list.append(self.usbdata.max_value_array.get())

        # max_value_list = max(list(self.usbdata.max_value_array))
        
        print("====length=====",len(max_value_list))
        max_value = max(max_value_list)
        # self.clear_Queue(self.usbdata.max_value_array)
        # print("master", max_value)


        rgba_img = self.cmap(z)
        self.p3.setData(z=z,colors=rgba_img)
        #显示第一个数值
        self.textBrowser.append(str(z[0][0]))  #在指定的区域显示提示信息

        # print(max)
        self.verticalGroupBox_2.update_ball_position(max_value)

def closehand():
    print('close')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = PLOT_3D()
    window.show()
    sys.exit(app.exec_())



