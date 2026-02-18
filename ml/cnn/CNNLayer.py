import torch.nn as nn
import torch.nn.functional as F

class CNNLayer(nn.Module):
    def __init__(self):
        super(CNNLayer,self).__init__()

        self.conv1 = nn.Conv2d(in_channels=1,out_channels= 8 , kernel_size= 3,padding= 1)

        # Layer 2: 16 input channels -> 32 kernels
        self.conv2 = nn.Conv2d(8, 16, kernel_size=3, padding=1)

        self.pool = nn.MaxPool2d(kernel_size =2,stride = 2)
        self.dropout = nn.Dropout(0.25)
        self.fc1 = nn.Linear(784,10) # 16 kernel * 7 * 7  7-> after pooling 2 times, reduced dimension from 28 to 14 to 7

    def forward(self,x):
        x = F.relu(self.conv1(x))
        x = self.pool(x)

        x = F.relu(self.conv2(x))
        x = self.pool(x)

        x = x.view(-1,784)
        x = self.dropout(x)
        x = self.fc1(x)

        return x
