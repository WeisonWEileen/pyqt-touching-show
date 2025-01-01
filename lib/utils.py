import numpy as np
import random
import time

def generate_sine_wave_data(self):
    t = 0
    while self.running:
        # 生成正弦波数据
        sine_wave = np.sin(2 * np.pi * t / 100) * np.ones((64, 64))
        self.usbdata.plot_z.put([sine_wave])
        t += 1
        time.sleep(0.1)  # 模拟数据传输间隔