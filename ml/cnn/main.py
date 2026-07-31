import cv2
import torch
from sklearn.model_selection import KFold

from CNNLayer import CNNLayer
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader, SubsetRandomSampler
from PIL import Image,ImageFilter,ImageOps

from opencv_read import predict_multiple_images


def get_test_data():
    transform = transforms.Compose([transforms.ToTensor()])

    # 2. Download the training data
    test_data = datasets.MNIST(root='./data', train=False, download=True, transform=transform)
    test_loader = DataLoader(test_data, batch_size=64, shuffle=True)

    return test_loader
def train():
    transform = transforms.Compose([transforms.ToTensor()])

    # 2. Download the training data
    train_data = datasets.MNIST(root='./data', train=True, download=True, transform=transform)

    epochs = 10
    model = CNNLayer()
    print(model)

    train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
    images, labels = next(iter(train_loader))
    print(f"Batch Shape: {images.shape}")

    model.train()
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    for epoch in range(epochs):
        running_loss = 0.0
        for batch_idx, (images, labels) in enumerate(train_loader):
            # 1. Clear the old gradients (don't want old mistakes affecting new ones)
            optimizer.zero_grad()

            # 2. Forward pass: The model guesses what the digits are
            outputs = model(images)

            # 3. Calculate the loss: How far off were the guesses?
            loss = criterion(outputs, labels)

            # 4. Backward pass: Calculate how to adjust the kernels
            loss.backward()

            # 5. Optimizer step: Actually update the kernels/weights
            optimizer.step()
            running_loss += loss.item()
            # Print status every 100 batches so we can see it learning
            if (batch_idx + 1) % 100 == 0:
                print(f"Batch {batch_idx + 1}/{len(train_loader)} | Loss: {loss.item():.4f}")
        avg_loss = running_loss / len(train_loader)
        print(f"Epoch [{epoch + 1}/{epochs}] complete. Avg Loss: {avg_loss:.4f}")
        # Save the "Brain" to a file
    torch.save(model.state_dict(), "mnist_cnn.pth")
    print("Model weights saved to mnist_cnn.pth")
    print("Training finished! Your CNN has now 'learned' how to read digits.")

def load_model():
    # Create an empty brain
    model = CNNLayer()

    # Load the saved numbers into it
    model.load_state_dict(torch.load("mnist_cnn.pth",weights_only=True))

    return model

def predict(model ):

    # Set to evaluation mode (so it doesn't try to learn anymore)
    model.eval()
    correct = 0
    print("Model loaded and ready for prediction!")
    test_loader = get_test_data()
    print(f"Test Images Shape: {test_loader.dataset}")  # [1000, 1, 28, 28]
    print(f"Number of test images available: {len(test_loader)}")  # Should be 10,000

    with torch.no_grad():
        for images, labels in test_loader:
            outputs = model(images)
            predictions = outputs.argmax(dim=1)
            correct += (predictions == labels).sum().item()

    accuracy = 100 * correct / len(test_loader.dataset)
    print(f"Test Accuracy: {accuracy}%")


def show_errors(model, loader):
    model.eval()
    errors = []

    with torch.no_grad():
        for images, labels in loader:
            outputs = model(images)
            preds = outputs.argmax(dim=1)

            # Find indices where prediction is wrong
            wrong_idx = (preds != labels).nonzero(as_tuple=True)[0]

            for idx in wrong_idx:
                errors.append((images[idx], preds[idx], labels[idx]))
                if len(errors) >= 5: break  # Just get 5 examples
            if len(errors) >= 5: break

    # Plot the mistakes
    fig, axes = plt.subplots(1, 5, figsize=(15, 3))
    for i, (img, pred, actual) in enumerate(errors):
        axes[i].imshow(img.squeeze(), cmap='gray')
        axes[i].set_title(f"AI: {pred} | Actual: {actual}")
        axes[i].axis('off')
    plt.show()


def train_kfold(k_folds=5):
    # 1. Load the full dataset
    transform = transforms.Compose([transforms.ToTensor()])
    dataset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)

    # 2. Define K-Fold
    kfold = KFold(n_splits=k_folds, shuffle=True)
    results = {}

    print(f"Starting {k_folds}-Fold Cross Validation...")

    for fold, (train_ids, test_ids) in enumerate(kfold.split(dataset)):
        print(f"FOLD {fold + 1}")
        print("--------------------------------")

        # Sample the data for this specific fold
        train_subsampler = SubsetRandomSampler(train_ids)
        test_subsampler = SubsetRandomSampler(test_ids)

        # Define Data Loaders
        train_loader = DataLoader(dataset, batch_size=64, sampler=train_subsampler)
        test_loader = DataLoader(dataset, batch_size=64, sampler=test_subsampler)

        # Initialize Model, Loss, and Optimizer
        model = CNNLayer()
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

        # Train for 1 Epoch per fold (you can increase this for better accuracy)
        model.train()
        for batch_idx, (images, labels) in enumerate(train_loader):
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

        # Evaluate this fold
        model.eval()
        correct, total = 0, 0
        with torch.no_grad():
            for images, labels in test_loader:
                outputs = model(images)
                preds = outputs.argmax(dim=1)
                total += labels.size(0)
                correct += (preds == labels).sum().item()

        accuracy = 100.0 * correct / total
        print(f"Accuracy for fold {fold + 1}: {accuracy:.2f}%")
        results[fold] = accuracy

    # Print final results
    print(f"\nK-FOLD CROSS VALIDATION RESULTS FOR {k_folds} FOLDS")
    print("--------------------------------")
    avg = sum(results.values()) / len(results.values())
    for key, value in results.items():
        print(f"Fold {key + 1}: {value:.2f}%")
    print(f"Average: {avg:.2f}%")


# To run it:
# train_kfold(k_folds=5)

# Call it after your prediction loop:

def predict_custom_image(image_path):
    model = CNNLayer()
    model.load_state_dict(torch.load("mnist_cnn.pth",weights_only=True))
    model.eval()
    transform = transforms.Compose([transforms.Grayscale(num_output_channels=1),
                                    transforms.Resize((20, 20)),
                                    transforms.Pad(4),
                                    transforms.ToTensor(),
                                    transforms.Normalize((0.1307,), (0.3081,))])
    img = Image.open(image_path).convert('L')
    # Invert and find bounding box to "tight crop" the digit
    # This removes all the extra empty black space around your 7
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
        img = ImageOps.expand(img, border=20, fill=0)

    img = img.filter(ImageFilter.GaussianBlur(radius=1.5))

    img = img.filter(ImageFilter.MaxFilter(7))
    img = img.point(lambda p: 255 if p > 50 else 0)# blurry pixel to become white
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    img_tensor = transform(img)

    # img_tensor[img_tensor < 0.5] = 0 # make the bg black if grey as model was trained with black bg
    img_tensor = img_tensor.unsqueeze(0)

    # 1. Prepare the image for visualization
    # We remove the normalization to make it viewable and squeeze the batch/channel dims
    viewable_img = img_tensor.squeeze().numpy()

    # 2. Save the image so you can see it
    plt.imsave("model_input.png", viewable_img, cmap='gray')
    print("Saved 'model_input.png'. Open this to see what the AI sees!")

    with torch.no_grad():
        output = model(img_tensor)
        prediction = output.argmax(dim=1).item()
        confidence = torch.nn.functional.softmax(output, dim=1)[0].max().item()
    print(f"I am {confidence * 100:.2f}% sure that this is a: {prediction}")

def regular_method():
    train()
    model = load_model()
    predict(model)
    test_loader = get_test_data()
    show_errors(model, test_loader)
if __name__ == '__main__':
    #regular_method()
    #train_kfold()
    predict_custom_image("images/img1.png")

    predict_multiple_images("images/87.png")
    predict_multiple_images("images/phone_numbers.png")