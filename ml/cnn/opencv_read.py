import torch.nn.functional as F
from CNNLayer import CNNLayer
import cv2
import torch
from torchvision import datasets, transforms
from PIL import Image,ImageFilter,ImageOps

def predict_multiple_images(image_paths):
    model = CNNLayer()
    model.load_state_dict(torch.load("mnist_cnn.pth",weights_only=True))
    model.eval()
    image = cv2.imread(image_paths)
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
    # Find contours (blobs of white pixels)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours from left to right (x-coordinate) so we read the number correctly
    contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0])
    # 3. Define the transform (same as your successful single-digit prediction)
    transform = transforms.Compose([
        transforms.Resize((20, 20)),
        transforms.Pad(4),
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])

    results = []

    for i, ctr in enumerate(contours):
        # Get bounding box for the current digit
        x, y, w, h = cv2.boundingRect(ctr)

        # Ignore tiny specks of noise
        if w < 5 or h < 5:
            continue

        # Extract the digit crop and add a small border so it's not touching edges
        roi = thresh[y:y + h, x:x + w]
        roi = cv2.copyMakeBorder(roi, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=0)

        # Convert OpenCV image (NumPy array) to PIL Image
        roi_pil = Image.fromarray(roi)

        # Apply the "bold" filter you used for the iPad drawings
        roi_pil = roi_pil.filter(ImageFilter.MaxFilter(5))

        # Transform and predict
        img_tensor = transform(roi_pil).unsqueeze(0)

        with torch.no_grad():
            output = model(img_tensor)
            prediction = output.argmax(dim=1).item()
            confidence = F.softmax(output, dim=1)[0].max().item()
            results.append(str(prediction))

            # Optional: Save each detected crop to check OpenCV's work
            # roi_pil.save(f"digit_{i}.png")

    final_number = "".join(results)
    print(f"Detected Digits: {final_number}")
    return final_number