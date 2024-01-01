import torch
import torchvision
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'


n_epochs = 20
batch_size_train = 64
batch_size_test = 1000
learning_rate = 0.01
momentum = 0.5
log_interval = 10
random_seed = 1
torch.manual_seed(random_seed)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#数据加载，利用torch库中现有的dataloader
train_loader = torch.utils.data.DataLoader(
    torchvision.datasets.MNIST('./data/', train=True, download=True,
                               transform=torchvision.transforms.Compose([
                                   torchvision.transforms.ToTensor(),
                                   torchvision.transforms.Normalize(
                                       (0.14,), (0.3,))
                               ])),
    batch_size=batch_size_train, shuffle=True)
test_loader = torch.utils.data.DataLoader(
    torchvision.datasets.MNIST('./data/', train=False, download=True,
                               transform=torchvision.transforms.Compose([
                                   torchvision.transforms.ToTensor(),
                                   torchvision.transforms.Normalize(
                                       (0.1307,), (0.3081,))
                               ])),
    batch_size=batch_size_test, shuffle=True)


# 定义网络结构
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        # 第一个卷积层，接受1个输入通道，输出10个通道，卷积核大小为5
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        # 第二个卷积层，接受10个输入通道，输出20个通道，卷积核大小为5
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        # Dropout层，随机丢弃一些神经元，防止过拟合
        self.conv2_drop = nn.Dropout2d()
        # 第一个全连接层，将320维的数据映射到50维
        self.fc1 = nn.Linear(320, 50)
        # 第二个全连接层，将50维数据映射到10维（例如，10个类别）
        self.fc2 = nn.Linear(50, 10)

    # 定义网络的前向传播路径
    def forward(self, x):
        # 通过第一个卷积层，然后应用2x2的最大池化和ReLU激活函数
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        # 通过第二个卷积层，应用dropout，然后再次应用2x2的最大池化和ReLU激活函数
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        # 展平多维输入数据
        x = x.view(-1, 320)
        # 通过第一个全连接层，然后应用ReLU激活函数
        x = F.relu(self.fc1(x))
        # 应用dropout
        x = F.dropout(x, training=self.training)
        # 通过第二个全连接层
        x = self.fc2(x)
        # 应用log_softmax，对输出进行对数似然变换
        return F.log_softmax(x, dim=1)


network = Net().to(device)
optimizer = optim.SGD(network.parameters(), lr=learning_rate,
                      momentum=momentum)


# 存储准确率和损失
train_losses = []
train_acc = []
test_losses = []
test_acc = []

def train(epoch):
    network.train()  # 将模型设置为训练模式
    train_loss = 0  # 初始化累计训练损失为0
    correct = 0  # 初始化正确预测的样本数为0
    total = 0  # 初始化总样本数为0

    for batch_idx, (data, target) in enumerate(train_loader):  # 遍历训练数据
        data, target = data.to(device), target.to(device)  # 将数据和标签转移到设备（GPU或CPU）
        optimizer.zero_grad()  # 清除之前的梯度
        output = network(data)  # 得到模型输出
        loss = F.nll_loss(output, target)  # 计算损失
        train_loss += loss.item()  # 累加损失
        loss.backward()  # 反向传播
        optimizer.step()  # 更新模型参数

        pred = output.data.max(1, keepdim=True)[1]  # 获取最大概率的预测结果
        correct += pred.eq(target.data.view_as(pred)).sum().item()  # 计算正确预测的数量
        total += target.size(0)  # 累计样本数量

        if batch_idx % log_interval == 0:  # 每隔一定批次打印训练状态
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.item()))

    train_loss /= len(train_loader)  # 计算平均训练损失
    train_losses.append(train_loss)  # 将平均损失添加到列表中
    accuracy = 100. * correct / total  # 计算训练准确率
    train_acc.append(accuracy)  # 将训练准确率添加到列表中
    print('\nTrain set: Epoch: {}, Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        epoch, train_loss, correct, total, accuracy))  # 打印训练集的平均损失和准确率



def test():
    network.eval()  # 将模型设置为评估模式
    test_loss = 0  # 初始化累计测试损失为0
    correct = 0  # 初始化正确预测的样本数为0
    total = 0  # 初始化总样本数为0
    misclassified_examples = []  # 初始化错分样本列表

    with torch.no_grad():  # 不计算梯度，以节省计算资源
        for data, target in test_loader:  # 遍历测试数据
            data, target = data.to(device), target.to(device)  # 将数据和标签转移到设备
            output = network(data)  # 得到模型输出
            test_loss += F.nll_loss(output, target, reduction='sum').item()  # 累加损失
            pred = output.data.max(1, keepdim=True)[1]  # 获取最大概率的预测结果
            correct += pred.eq(target.data.view_as(pred)).sum().item()  # 计算正确预测的数量
            total += target.size(0)  # 累计样本数量

            # 收集错分的图片
            wrong_idx = (pred != target.view_as(pred)).nonzero()[:, 0]
            for idx in wrong_idx:
                misclassified_examples.append((data[idx], pred[idx], target[idx]))

    test_loss /= len(test_loader.dataset)  # 计算平均测试损失
    test_losses.append(test_loss)  # 将平均损失添加到列表中
    accuracy = 100. * correct / total  # 计算测试准确率
    test_acc.append(accuracy)  # 将测试准确率添加到列表中
    print('\nTest set: Avg. loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, total, accuracy))  # 打印测试集的平均损失和准确率

    return misclassified_examples  # 返回错分样本列表


# 在训练和测试循环中
misclassified_examples = []
for epoch in range(1, n_epochs + 1):
    train(epoch)
    misclassified_examples = test()  # 更新错分图片集

def plot_misclassified_images(misclassified, num_images=10):
    fig = plt.figure(figsize=(15, 10))
    for i, (img, pred, label) in enumerate(misclassified[:num_images]):
        img, pred, label = img.to('cpu'), pred.to('cpu'), label.to('cpu')
        img = img.squeeze().numpy()  # 转换为 NumPy 数组
        ax = fig.add_subplot(2, 5, i+1)
        ax.imshow(img, cmap='gray', interpolation='none')
        ax.set_title(f"Predicted: {pred.item()}, Label: {label.item()}")
        ax.set_xticks([])
        ax.set_yticks([])
    plt.show()

plot_misclassified_images(misclassified_examples, num_images=10)

# 绘制损失曲线
fig1 = plt.figure(figsize=(8, 6))
plt.plot(train_losses, color='blue')
plt.plot(test_losses, color='red')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Training and Testing Loss')
plt.legend(['Train Loss', 'Test Loss'])
plt.show()

# 绘制准确率曲线
fig2 = plt.figure(figsize=(8, 6))
plt.plot(train_acc, color='blue')
plt.plot(test_acc, color='red')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.title('Training and Testing Accuracy')
plt.legend(['Train Accuracy', 'Test Accuracy'])
plt.show()




