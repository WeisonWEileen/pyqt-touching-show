import numpy as np

# 读取 npz 文件
data = np.load('data/sensor.npz')
print(type(data))
# 打印文件中的所有数组
for key, value in data.items():
    print(f"{key}: {value}")
    exit()