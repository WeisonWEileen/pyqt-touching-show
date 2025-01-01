import torch
import numpy as np
from torch.utils.data import Dataset, DataLoader
import os

# 假设数据文件夹路径如下
punch_dir = './punch'
scratch_dir = './scratch'

# 定义一个 Dataset 类
class PunchScratchDataset(Dataset):
    def __init__(self, punch_dir, scratch_dir):
        # 读取目录下所有的 .npy 文件
        self.punch_files = [os.path.join(punch_dir, f) for f in os.listdir(punch_dir) if f.endswith('.npy')]
        self.scratch_files = [os.path.join(scratch_dir, f) for f in os.listdir(scratch_dir) if f.endswith('.npy')]
        
        # 合并两个类别的数据
        self.files = self.punch_files + self.scratch_files
        
        # 标签: 1代表punch, 0代表scratch
        self.labels = [1] * len(self.punch_files) + [0] * len(self.scratch_files)

    def __len__(self):
        # 返回数据集的大小
        return len(self.files)

    def __getitem__(self, idx):
        # 加载数据
        file = self.files[idx]
        label = self.labels[idx]
        
        # 读取 .npy 文件
        data = np.load(file)
        
        # 将数据转为 PyTorch 张量
        data = torch.tensor(data, dtype=torch.float32)
        
        return data, label

if __name__ == '__main__':
    # 创建 Dataset 实例
    dataset = PunchScratchDataset(punch_dir, scratch_dir)

    # 创建 DataLoader 实例
    dataloader = DataLoader(dataset, batch_size=2, shuffle=True)

    # 使用 DataLoader 进行训练
    for batch_data, batch_labels in dataloader:
        print(batch_data.shape)  # 打印每个batch的形状
        print(batch_labels.shape)  # 打印每个batch的标签
