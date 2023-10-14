'''ResNet in PyTorch.

For Pre-activation ResNet, see 'preact_resnet.py'.

Reference:
[1] Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun
    Deep Residual Learning for Image Recognition. arXiv:1512.03385
'''
import torch
import torch.nn as nn
import torch.nn.functional as F


class BasicBlock(nn.Module):
    expansion = 1

    def __init__(self, in_planes, planes, stride=1):
        super(BasicBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_planes, planes, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)

        self.shortcut = nn.Sequential()
        if stride != 1 or in_planes != self.expansion*planes:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_planes, self.expansion*planes, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(self.expansion*planes)
            )

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)
        out = F.relu(out)
        return out


class Bottleneck(nn.Module):
    expansion = 4

    def __init__(self, in_planes, planes, stride=1):
        super(Bottleneck, self).__init__()
        wider_planes=planes*1
        self.conv1 = nn.Conv2d(in_planes, wider_planes, kernel_size=1, bias=False)
        self.bn1 = nn.BatchNorm2d(wider_planes)
        self.conv2 = nn.Conv2d(wider_planes, wider_planes, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(wider_planes)
        self.conv3 = nn.Conv2d(wider_planes, self.expansion*planes, kernel_size=1, bias=False)
        self.bn3 = nn.BatchNorm2d(self.expansion*planes)

        self.shortcut = nn.Sequential()
        if stride != 1 or in_planes != self.expansion*planes:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_planes, self.expansion*planes, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(self.expansion*planes)
            )

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = F.relu(self.bn2(self.conv2(out)))
        out = self.bn3(self.conv3(out))
        out += self.shortcut(x)
        out = F.relu(out)
        return out

class ResNet(nn.Module):
    def __init__(self, block, num_blocks, num_classes):
        super(ResNet, self).__init__()
        self.in_planes = 64
        self.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        
        self.layer1 = self._make_layer(block, 64, num_blocks[0], stride=1)
        self.layer2 = self._make_layer(block, 128, num_blocks[1], stride=2)
        self.layer3 = self._make_layer(block, 256, num_blocks[2], stride=2)
        self.layer4 = self._make_layer(block, 512, num_blocks[3], stride=2)
        self.classifier = nn.Linear(512*block.expansion, num_classes, bias=False)


        self.next_layers={}

        for block_ind in range(len(num_blocks)):
    
            for layer_index in range(num_blocks[block_ind]):


                block_index=block_ind+1

        #         if layer_index ==0 and block_index!=1:
        #             next_layers[("layer"+str(block_ind),layer_index,"conv3")]=[["layer"+str(block_index),layer_index,"shortcut"],["layer"+str(block_index),layer_index,"BatchNorm2d"]]

                self.next_layers[("layer"+str(block_index),layer_index,"conv1")]=[["layer"+str(block_index),layer_index,"conv2"],["layer"+str(block_index),layer_index,"bn1"]]
                self.next_layers[("layer"+str(block_index),layer_index,"conv2")]=[["layer"+str(block_index),layer_index,"conv3"],["layer"+str(block_index),layer_index,"bn2"]]
        #         next_layers[("layer"+str(block_index),layer_index,"conv3")]=[["layer"+str(block_index),layer_index+1,"conv1"],["layer"+str(block_index),layer_index,"bn3"]]

        # next_layers[("layer"+str(block_index),layer_index,"conv0")]=[["layer"+str(0),3,"conv1"],["layer"+str(0),3,"bn1"]]

        self.layer2split = list(self.next_layers.keys())

                
    def _make_layer(self, block, planes, num_blocks, stride):
        
        strides = [stride] + [1]*(num_blocks-1)

        layers = []
        for stride in strides:
        
            layers.append(block(self.in_planes, planes, stride))
            self.in_planes = planes * block.expansion
        return nn.Sequential(*layers)

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.layer1(out)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = F.avg_pool2d(out, 4)
        out = out.view(out.size(0), -1)
        out = self.classifier(out)
        out = F.log_softmax(out, dim=1)
        return out


class ResNetbasic(nn.Module):
    def __init__(self, block, num_blocks, num_classes):
        super(ResNetbasic, self).__init__()
        self.in_planes = 64
        self.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        
        self.layer1 = self._make_layer(block, 64, num_blocks[0], stride=1)
        self.layer2 = self._make_layer(block, 128, num_blocks[1], stride=2)
        self.layer3 = self._make_layer(block, 256, num_blocks[2], stride=2)
        self.layer4 = self._make_layer(block, 512, num_blocks[3], stride=2)
        self.classifier = nn.Linear(512*block.expansion, num_classes, bias=False)


        self.next_layers={}

        for block_ind in range(len(num_blocks)):
    
            for layer_index in range(num_blocks[block_ind]):


                block_index=block_ind+1

        #         if layer_index ==0 and block_index!=1:
        #             next_layers[("layer"+str(block_ind),layer_index,"conv3")]=[["layer"+str(block_index),layer_index,"shortcut"],["layer"+str(block_index),layer_index,"BatchNorm2d"]]

                self.next_layers[("layer"+str(block_index),layer_index,"conv1")]=[["layer"+str(block_index),layer_index,"conv2"],["layer"+str(block_index),layer_index,"bn1"]]
                # self.next_layers[("layer"+str(block_index),layer_index,"conv2")]=[["layer"+str(block_index),layer_index,"conv3"],["layer"+str(block_index),layer_index,"bn2"]]
        #         next_layers[("layer"+str(block_index),layer_index,"conv3")]=[["layer"+str(block_index),layer_index+1,"conv1"],["layer"+str(block_index),layer_index,"bn3"]]

        # next_layers[("layer"+str(block_index),layer_index,"conv0")]=[["layer"+str(0),3,"conv1"],["layer"+str(0),3,"bn1"]]

        self.layer2split = list(self.next_layers.keys())

                
    def _make_layer(self, block, planes, num_blocks, stride):
        
        strides = [stride] + [1]*(num_blocks-1)

        layers = []
        for stride in strides:
        
            layers.append(block(self.in_planes, planes, stride))
            self.in_planes = planes * block.expansion
        return nn.Sequential(*layers)

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.layer1(out)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = F.avg_pool2d(out, 4)
        out = out.view(out.size(0), -1)
        out = self.classifier(out)
        out = F.log_softmax(out, dim=1)
        return out



def ResNet18(c=1000):
    return ResNetbasic(BasicBlock, [2,2,2,2],c)

def ResNet34(c=10):
    return ResNetbasic(BasicBlock, [3,4,6,3],c)

def ResNet50(c=10):
    return ResNet(Bottleneck, [3,4,6,3],c)

def ResNet101(c=10):
    return ResNet(Bottleneck, [3,4,23,3],c)

def ResNet152(c=10):
    return ResNet(Bottleneck, [3,8,36,3],c)


def test():
    net = ResNet18()
    y = net(torch.randn(1,3,32,32))
    print(y.size())

# test()
