# import os
# import sys
# sys.path.insert(0, os.getcwd())
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Queue
import lib.usb_get as usb_get
from lib.ui_ball import Ui_Form
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
import sys
import time
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
        self.w.setCameraPosition(distance=32)

        # xy平面坐标显示绘图部件
        self.xy = gl.GLViewWidget()
        self.xy.show()
        # self.w.setWindowTitle('pyqtgraph example: GLSurfacePlot')
        self.xy.setCameraPosition(distance=20, elevation=-90, azimuth=0)

        self.g = gl.GLGridItem()
        self.g.scale(2, 2.05, 1)
        self.g.setColor((221, 221, 221))
        self.g.setDepthValue(-1)  # draw grid after surfaces since they may be translucent
        self.g.setSpacing(1, 1, 1)  # 调整网格线之间的间距
        self.xy.addItem(self.g)

        ## Manually specified colors
        self.z = pg.gaussianFilter(np.random.normal(size=(64, 64)), (1, 1))
        self.x = np.linspace(-12, 12, 64)
        self.y = np.linspace(-12, 12, 64)
        self.radius = 12 
        for i in range(64):
            for j in range(64):
                    # self.z[i][j] = np.sqrt(self.radius**2 - self.x[i]**2 - self.y[j]**2)
                    self.z[i][j] = np.sqrt(self.radius**2 - self.x[i]**2 )
        # self.z = np.array()
        print("=====",type(self.z))
        print("=====",self.z.shape)
        print("=====",self.z)

        self.cmap = plt.get_cmap('rainbow')
        self.minZ=np.min(self.z)
        self.maxZ=np.max(self.z)
        self.rgba_img = self.cmap((self.z-self.minZ)/(self.maxZ -self.minZ))


        # self.p3 = gl.GLSurfacePlotItem(z=self.z,colors=self.rgba_img)
        self.p3 = gl.GLSurfacePlotItem(z=self.z,colors=self.rgba_img)
        self.p3.scale(16. / 49., 16. / 49., 1.0)
        self.p3.translate(-10, -10, 0)
        self.w.addItem(self.p3)

        # 新建窗口绘图部件
        self.p3_s = gl.GLSurfacePlotItem(z=self.z,colors=self.rgba_img)
        self.p3_s.scale(16. / 49., 16. / 49., 1.0)
        self.p3_s.translate(-10, -10, 0)
        self.update_flag = 0

        # xy平面坐标显示绘图部件
        self.p3_xy = gl.GLSurfacePlotItem(z=self.z,colors=self.rgba_img)
        self.p3_xy.scale(16. / 49., 16. / 49., 1.0)
        self.p3_xy.translate(-10, -10, 0)
        self.xy.addItem(self.p3_xy)

        # 状态指示灯绘图部件
        Ui_Form.setStatusColor(self,color='green')

        #小球碰撞窗口
        self.p3_b1 = gl.GLSurfacePlotItem(z=self.z,colors=self.rgba_img)
        self.p3_b1.scale(16. / 49., 16. / 49., 1.0)
        self.p3_b1.translate(-10, -10, 0)




        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(1)

        self.timer_save = QtCore.QTimer()
        self.timer_save.timeout.connect(self.save_timer)



        self.usbdata = usb_get.USB_DataDecode()
        self.sensor = []

        self.verticalLayout_graph.addWidget(self.w)  # 添加绘图部件到网格布局层
        self.verticalLayout_graph_4.addWidget(self.xy) # 添加绘图部件到网格布局层
       

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
        
        #柔性展示
        self.skin_button.clicked.connect(self.skin_display)

        #小球展示
        self.ball_button.clicked.connect(self.ball_detect_start)
        self.ball_flag = 0
        self.ball_detect_array = []
        self.ball_max_value = []
        self.ball_button_stop.clicked.connect(self.ball_detect_stop)

        self.timer_save = QtCore.QTimer()
        self.timer_save.timeout.connect(self.save_timer)
        self.savedata_button.setText("Start Save")


    def ball_detect_start(self):
        self.ball_detect_array = []
        self.ball_max_value = []
        self.ball_showflag = 0
    
    def ball_detect_stop(self):
        temp1 = self.ball_detect_array
        temp2 = np.array(self.ball_max_value)
        sorted_indices = np.argsort(temp2)
        self.b1 = gl.GLViewWidget()
        self.b1.show()
        self.b1.setWindowTitle('Ball Detect')
        self.b1.setCameraPosition(distance=32)
        self.b1.addItem(self.p3_b1 )
        print("小球碰撞结果演示")

        if (self.ball_showflag == 0):
            self.ball_showflag = 1

        self.b1.addItem(self.p3_b1)
        self.max_balls = 10
        if (self.ball_showflag < self.max_balls):
            z = temp1[sorted_indices[-self.ball_showflag]]
            self.ball_showflag += 1
        elif (self.ball_showflag == self.max_balls):
            z = temp1[sorted_indices[-self.max_balls]]
            # self.ball_showflag = 0
        else:
            pass
        rgba_img = self.cmap(z)
        self.p3_b1.setData(z=z,colors=rgba_img)

        print(len(self.ball_detect_array))

    def skin_display(self):
        # 新窗口画传感器柔性展示
        self.s = gl.GLViewWidget()
        self.s.show()
        self.s.setWindowTitle('e-skin')
        self.s.setCameraPosition(distance=32)
        print("电子皮肤柔性展示")
        self.update_flag = 1
        self.s.addItem(self.p3_s)


    def port_open(self):
        print("开始")
        self.clear_Queue(self.usbdata.data_out) #清空队列
        # self.usbdata.GUI_order.put('start')     #发送开始
        # self.textBrowser_3.append("开始检测")  # 在指定的区域显示提示信息
        self.timer_save.start(1)
        self.timer.start(1)

    def start_measure(self):
        print("清空")
        self.sensor = []

    def port_close(self):
        # self.usbdata.GUI_order.put('stop')  # 发送结束
        self.timer.stop()
    
    def save_data_button(self):
        button_state = self.savedata_button.text()
        if button_state == 'Start Save':
            self.savedata_button.setText("Collecting...")
            self.clear_Queue(self.usbdata.data_out)  # 清空队列
            self.usbdata.GUI_order.put('start')  # 发送开始
            # self.textBrowser_3.append("开始检测")  # 在指定的区域显示提示信息
            self.timer_save.start(10)
            self.frames_collected = 0  # 初始化帧计数器
            self.collected_data = []  # 初始化数据列表
        else:
            self.usbdata.GUI_order.put('stop')  # 发送结束
            self.timer_save.stop()  # 停止
            # self.textBrowser_2.append("保存成功")  # 在指定的区域显示提示信息
            # self.textBrowser_3.append("保存结束")  # 在指定的区域显示提示信息
            self.savedata_button.setText("Start Save")

    def save_timer(self):
        while self.usbdata.data_out.qsize() > 0:
            z = self.usbdata.plot_z.get(True)[0]
            self.collected_data.append(z)
            self.frames_collected += 1
            print(f"{self.frames_collected} {np.max(z)}")

            if self.frames_collected >= 5000:
                self.usbdata.GUI_order.put('stop')  # 发送结束
                self.timer_save.stop()  # 停止
                self.save_collected_data()  # 保存数据
                # self.textBrowser_2.append("保存成功")  # 在指定的区域显示提示信息
                # self.textBrowser_3.append("保存结束")  # 在指定的区域显示提示信息
                self.savedata_button.setText("Start Save")
                break

    def save_collected_data(self):
        # int_time = time.strftime("%Y年%m月%d日 %H时%M分%S秒", time.localtime())
        int_time = time.strftime("_%Y_%m_%d_%H_%M_%S_", time.localtime())
        file_name = './data_punch' + int_time + '.npy'
        collected_data_np = np.array(self.collected_data)
        np.save(file_name, collected_data_np)
        self.collected_data = []  # 清空数据列表
        self.frames_collected = 0  # 重置帧计数器


    # def save_data(self):
    #     int_time = time.strftime("%Y年%m月%d日 %H时%M分%S秒", time.localtime())
    #     excel_npz = './lib/data_save/' + int_time + '_sensor.npz'
        # np.savez_compressed(excel_path, np.array(self.sensor[-5001:-1])) #保存5000个数据点
    #     np.savez_compressed(excel_npz, np.array(self.sensor))  # 保存全部数据

    #     # excel 保存
    #     self.sensor = np.array(self.sensor)
    #     print(self.sensor.shape)
    #     self.sensor = self.sensor.reshape(np.size(self.sensor, 0), 20)  # (//X,64)
    #     excel_data = pd.DataFrame(self.sensor)
    #     excel_path = './lib/data_save/' + int_time + '_sensor.xlsx'
    #     writer = pd.ExcelWriter(excel_path)
    #     excel_data.to_excel(writer, 'sheet_1', float_format='%.2f')
    #     writer.save()
    #     writer.close()

    #     self.sensor = []
    #     print("保存成功")

    # def save_data_button(self):
    #     button_state = self.savedata_button.text()
    #     int_time = time.strftime("%Y年%m月%d日 %H时%M分%S秒", time.localtime())
    #     self.savepath =  './lib/data_save/' + int_time + '_sensor.csv'
    #     self.res = []

    #     if (button_state == 'Start Save'):
    #         self.savedata_button.setText("Complete save")
    #         self.clear_Queue(self.usbdata.data_out)  # 清空队列
    #         self.usbdata.GUI_order.put('start')  # 发送开始
    #         self.textBrowser_3.append("开始检测")  # 在指定的区域显示提示信息
    #         self.timer_save.start(10)     #定时保存时间 ms
    #         #初始化保存
    #         self.save_data_init(self.savepath)

    #     else:
    #         self.usbdata.GUI_order.put('stop')  # 发送结束
    #         self.timer_save.stop()  # 停止
    #         #self.save_data()  # 保存内容
    #         self.textBrowser_2.append("保存成功")  # 在指定的区域显示提示信息
    #         self.textBrowser_3.append("保存结束")  # 在指定的区域显示提示信息
    #         self.savedata_button.setText("Start Save")


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


    # def save_timer(self):
    #     #计时显示
    #     int_time = time.strftime("%Y-%m-%d- %H:%M:%S", time.localtime())

    #     # self.textBrowser_2.append(int_time )  # 在指定的区域显示提示信息

    #     while self.usbdata.data_out.qsize() > 0:
    #         self.res.append(self.usbdata.data_out.get())

    #     if len(self.res) > 0:
    #         self.res.reverse()
    #         self.sensor = self.res[-1]
    #         self.sensor = self.sensor.reshape(64)
    #         savedata = [int_time] + list(self.sensor)
    #         self.write_data(savedata)

    def clear_Queue(self,q):
        res = []
        while q.qsize() > 0:
            res.append(q.get())

    #绘图
    def update_plot(self):

        z = self.usbdata.plot_z.get(True)[0]
        self.clear_Queue(self.usbdata.plot_z) # 清空队列

        z = pg.gaussianFilter(z,(4,4))   #高斯平滑
        rgba_img = self.cmap(z)
        self.p3.setData(z=z,colors=rgba_img)
        #显示第一个数值
        self.textBrowser.append(str(round(z[0][0],5)))  # 在指定的区域显示提示信息
        
        #显示到新窗口中
        if (self.update_flag == 1):
            rgba_img = self.cmap(z)
            z = self.z + z
            self.p3_s.setData(z=z,colors=rgba_img)


        #显示到xy平面窗口中以及小球
        try:
            z = self.usbdata.max_sensor.get(False)[0]
            self.clear_Queue(self.usbdata.max_sensor) # 清空队列
            # print(self.ball_detect_array.shape[1])

            max_value = np.max(z)/10
            # print("================")
            # print("plot", "{:.2f}".format(max_value))
            # print("================")

            if(max_value>=20):
                Ui_Form.setStatusColor(self,color='red')
            elif(max_value>=10):
                Ui_Form.setStatusColor(self,color='yellow')
            elif(max_value>=0):
                Ui_Form.setStatusColor(self,color='green')
            self.verticalGroupBox_2.update_ball_position(max_value)

            if (self.ball_flag == 0):
                z = pg.gaussianFilter(z,(4,4))   #高斯平滑
                xy_img = self.cmap(z)
                self.p3_xy.setData(z=z,colors=xy_img) # xy平面
            elif (self.ball_flag == 1):
                z = pg.gaussianFilter(z,(4,4))   #高斯平滑
                xy_img = self.cmap(z)
                self.p3_b1.setData(z=z,colors=xy_img) # xy平面

            #小球弹跳多个数据采集窗口
            if (self.ball_showflag == 0):
                if(len(self.ball_detect_array)<300):
                    self.ball_detect_array.append(z)
                    self.ball_max_value.append(max_value)
                else:
                    print('Ball detectio time out')
                    self.ball_detect_array = []
                    self.ball_max_value = []
                    self.ball_detect_array.append(z)
                    self.ball_max_value.append(max_value)
                if(self.ball_detect_array.shape[1]>=2):
                    self.ball_detect_array = np.array([])
            else:
                pass

        except Exception as e:
            pass
            # print("plot", "{:.2f}".format(max_value))
            # self.verticalGroupBox_2.update_ball_position(0)



def closehand():
    print('close')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = PLOT_3D()
    window.show()
    sys.exit(app.exec_())



