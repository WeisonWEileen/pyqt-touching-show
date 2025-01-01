import serial
import time
import struct
import multiprocessing
from multiprocessing import Queue
import os
import numpy as np
import time
import keyboard
import sys
import queue

import csv
class USB_Connect:     #USB 400Hz 刷新率

    def __init__(self):
        super().__init__()

        print('串口连接成功')

        self.coefficient = 100


    def Message_decode(self,data_flag):
        try:
            # self.com = serial.Serial('COM20', 2000000)
            self.com = serial.Serial('/dev/ttyACM0', 2000000)
        except Exception as e:
            print("---异常---：", e)
            sys.exit(0)

        while True:
            #包头截取
            dd = self.com.read(1)
            if (dd == b'\xbb'):
                if(self.com.read(3) != b'\xbb\xbb\xbb'):
                    continue
            else: continue
            while True:
                data = self.com.read((64+2)*4)

                if(data[0:4] != b'\xaa\xaa\xaa\xaa' or data[-4:] != b'\xbb\xbb\xbb\xbb'): #包头，包尾核对
                    # print('erro')
                    print(data[0:4],'     ',data[-4:])
                    break
                #print('ok')

                data_flag.put(data)

    def sendMessage(self, message):
        self.tcp_client.write(message.encode(encoding='utf-8'))


    def closeClient(self):
        self.com.close()
        print("串口已关闭")


    #清空队列
    def clear_Queue(self,q):
        res = []
        while q.qsize() > 0:
            res.append(q.get())

    def init_data(self,data_flag):
        init_data_buffer = [0 for i in range(0,64)]
        data_buffer = {n: [] for n in range(64)}

        for i in range(20):

            udp_data = data_flag.get(True)
            for i in range(64):
                min_num = 6 + i * 4
                max_num = 8 + i * 4
                data_hend = struct.unpack('>H', udp_data[min_num -2 :max_num - 2])[0]
                data_decode = struct.unpack('>H', udp_data[min_num:max_num])[0] / self.coefficient
                #print(data_decode)

                data_buffer[data_hend].append(data_decode)

        for i in range(64):
            init_data_buffer[i] = int(np.mean(data_buffer[i]))

        return init_data_buffer

    def save_to_csv(self, csv_file, max_value):
        with open(csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([max_value])

    def usb_decode(self,data_flag,data_out,data_z,GUI_order,max_va,max_sensor):
    # def usb_decode(self,data_flag,data_out,data_z,GUI_order):
        data_buffer = {n: [] for n in range(64)}

        z = np.zeros((64, 64))
        Sensor = np.zeros((8, 8))

        send_flag = 0  #装载数据标志位
        strat_time = time.time()  #采样计时

        #初始化，求均值
        init_data = self.init_data(data_flag)


        max_value = 0
        max_array = np.zeros((64,64))
        count = 0


        while True:
            udp_data = data_flag.get(True) #接收数据

            for i in range(64):
                min_num = 6+i*4
                max_num = 8+i*4
                data_hend = struct.unpack('>H', udp_data[min_num-2:max_num-2])[0]
                data_decode = struct.unpack('>H',udp_data[min_num:max_num])[0] / self.coefficient - init_data[data_hend]


                if(len(data_buffer[data_hend]) <100 ):
                    data_buffer[data_hend].append(data_decode)
                    #print(data_hend)
                else:
                    data_buffer[data_hend][:-1] = data_buffer[data_hend][1:]  # shift data in the array one sample left
                    # print(data_hend)
                    # print(data_buffer.shape)

                    data_buffer[data_hend][-1] = data_decode


            #print(data_buffer[1][-1])
            for i in range(8):
                for j in range(8):
                    z[j * 8, i * 8] = data_buffer[i*8 + j][-1]
                    # Sensor[j,i] = data_buffer[i*8 + j][-1]# * self.coefficient

            #z[0,0] = 1000
            #data_out.put(Sensor)
            data_z.put([z,0]) #?

            # print("====",np.max(z))

            if count < 30:
                if max_value < np.max(z):
                    max_value = np.max(z)
                    max_array = z.copy()
                    # np.set_printoptions(threshold=np.inf)
                    # print('max_array',Sensor)
                    #print('max_value',max_value)
                count += 1
            else:
                # max_va.put(max_value)
                max_sensor.put([max_array,0])
                # print(np.max(z))
                max_value = 0
                count = 0
                # max_array = []

            #是否保存数据
            if (GUI_order.empty() == False):   #接收到采样标志后开始采样
                get_flag = GUI_order.get()
                if(get_flag == 'start'): #开始采样装入
                    self.clear_Queue(data_out)  #清空缓存
                    strat_time = time.time()
                    send_flag = 1
                if (get_flag == 'stop'):  # 开始采样装入
                    deta_time = time.time() - strat_time
                    print(deta_time)
                    send_flag = 0

            if(send_flag == 1):
                data_out.put(Sensor)

class USB_DataDecode:

    def __init__(self):
        super().__init__()

        #self.draw_3d = plot3d.PLOT_3D()

        #多进程
        self.data_flag = Queue() #更新状态
        self.data_out = Queue()  #数据解析结果
        self.plot_z = Queue()  # 数据解析结果
        
        self.GUI_order = Queue()  # GUI控制数据解析
        # self.max_value_array = Queue(maxsize=100) # 保存最大值传到上位机
        
        self.max_va = Queue()
        self.max_sensor = Queue()



        #进程1 接收数据
        self.T = USB_Connect()
        self.thread_getMessage = multiprocessing.Process(target=self.T.Message_decode,args=(self.data_flag,))

        #进程2 处理数据
        self.thread_usbdecode = multiprocessing.Process(target=self.T.usb_decode,args=(self.data_flag,self.data_out,self.plot_z,self.GUI_order, self.max_va, self.max_sensor))

        # 进程3 数据解析
        #self.thread_key_monitoring = multiprocessing.Process(target=self.key_monitoring, args=())


        #self.eat_process = multiprocessing.Process(target=self.eat, args=(3, "giao"))
        print("主进程ID:", os.getpid())
        self.thread_getMessage.start(

        )
        self.thread_usbdecode.start()

    def close_usb(self):
        self.thread_getMessage.terminate()
        self.thread_getMessage.join()

        self.thread_usbdecode.terminate()
        self.thread_usbdecode.join()

    def save(self):
        print('zhibin')

    def key_monitoring(self):
        keyboard.add_hotkey('c', self.save())  # 初始化验证
        keyboard.wait()

if __name__ == '__main__':
    usb = USB_DataDecode()

