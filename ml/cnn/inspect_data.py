import torch
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader
# 1. Define how to transform the raw data into tensors
transform = transforms.Compose([transforms.ToTensor()])

# 2. Download the training data
train_data = datasets.MNIST(root='./data', train=True, download=True, transform=transform)


# 3. Pull one sample to see its shape
image, label = train_data[0]
print(f"Image shape: {image.shape}") # Should be [1, 28, 28]
print(f"Label: {label}")

# 4. Plot the first 5 images
fig, axes = plt.subplots(1, 5, figsize=(10, 3))
for i in range(5):
    img, lbl = train_data[i]
    axes[i].imshow(img.squeeze(), cmap='gray')
    axes[i].set_title(f"Label: {lbl}")
    axes[i].axis('off')

plt.show()

train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
images, labels = next(iter(train_loader))
print(f"Batch Shape: {images.shape}")
