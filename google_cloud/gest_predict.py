import torch
import pandas as pd
import numpy as np
import csv
import torch.nn as nn

class CNNClassifier(nn.Module):
    def __init__(self):
        super(CNNClassifier, self).__init__()
        self.conv1 = nn.Conv1d(1, 16, kernel_size=5)
        self.fc1 = nn.Linear(16 * 446, 64)
        self.fc2 = nn.Linear(64, 8)  # 输出层设置为8，因为有8个类别

    def forward(self, x):
        x = x.view(x.size(0), 1, -1)
        x = self.conv1(x)
        x = torch.relu(x)
        x = x.view(x.size(0), -1)
        x = self.fc1(x)
        x = torch.relu(x)
        x = self.fc2(x)
        return x

class GestPredict(object):
    def __init__(self):
        # 加载已保存的模型
        self.model = CNNClassifier()  # 使用与保存模型相同的模型类初始化

        # 加载保存的模型权重
        self.model.load_state_dict(torch.load('your_model.pth'))
        self.model.eval()  # 设置模型为评估模式

        self.mapping = {
            0: "C",
            1: "O",
            2: "L",
            3: "U",
            4: "M",
            5: "B",
            6: "I",
            7: "A",
        }

    def read_data(self, path):
        with open(path, 'r') as file:
            reader = csv.reader(file)
            first_row = next(reader)

        # 将第一行数据转换为PyTorch张量（浮点数）
        self.sample_data = torch.tensor([float(value) for value in first_row])

        # 确保测试数据的形状为 1x450
        self.sample_data = self.sample_data.view(1, 1, -1)  # 1 表示批处理大小，1 表示通道数，-1 自动调整以匹配剩余的维度
        return

    def predict(self):
        # 步骤 3: 使用加载的模型进行测试
        with torch.no_grad():
            output = self.model(self.sample_data)

        # 步骤 4: 处理模型的输出以获取结果
        predicted_class = torch.argmax(output).item()
        print(f'Predicted Result: {self.mapping[predicted_class]}')
        return self.mapping[predicted_class]
