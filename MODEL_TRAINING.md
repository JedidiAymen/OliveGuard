# 🤖 Model Training Guide - OliveGuard

This document explains how the olive disease detection model was trained and how you can retrain or fine-tune it with your own data.

## 📚 Table of Contents

- [Overview](#overview)
- [Dataset Preparation](#dataset-preparation)
- [Training Environment Setup](#training-environment-setup)
- [Model Architecture](#model-architecture)
- [Training Process](#training-process)
- [Model Evaluation](#model-evaluation)
- [Model Export](#model-export)
- [Using the Trained Model](#using-the-trained-model)

## 🎯 Overview

The OliveGuard model is a deep learning classifier trained to detect olive leaf diseases. The current model can classify images into 3 categories:

1. **Healthy** - Normal, disease-free olive leaves
2. **Aculus Olearius** - Olive leaf mite infestation
3. **Olive Peacock Spot** - Fungal disease (Cycloconium oleaginum)

### Model Specifications

- **Architecture**: EfficientNet-Lite0 / MobileNetV3 / Custom CNN
- **Input Size**: 224×224 RGB images
- **Output**: 3-class softmax probabilities
- **Framework**: PyTorch / TensorFlow
- **Training Platform**: Google Colab with GPU
- **Final Format**: TensorFlow Lite (.tflite) for mobile deployment

## 📂 Dataset Preparation

### Dataset Structure

Your dataset should be organized in the following structure:

```
dataset/
├── train/
│   ├── healthy/
│   │   ├── img001.jpg
│   │   ├── img002.jpg
│   │   └── ...
│   ├── aculus_olearius/
│   │   ├── img001.jpg
│   │   ├── img002.jpg
│   │   └── ...
│   └── olive_peacock_spot/
│       ├── img001.jpg
│       ├── img002.jpg
│       └── ...
└── test/
    ├── healthy/
    ├── aculus_olearius/
    └── olive_peacock_spot/
```

### Dataset Requirements

- **Image Format**: JPG or PNG
- **Resolution**: At least 224×224 pixels (higher is better)
- **Quality**: Clear, well-lit photos
- **Quantity**: Minimum 100 images per class, 500+ recommended
- **Split**: 80% training, 20% testing

### Data Collection Tips

1. **Diverse Conditions**: Capture images in different lighting, angles, and backgrounds
2. **Single Leaf**: Focus on one leaf per image
3. **Clear Symptoms**: Ensure disease symptoms are visible
4. **Balanced Classes**: Try to have similar number of images per class
5. **Quality Over Quantity**: Better to have fewer high-quality images than many poor ones

## 🖥 Training Environment Setup

### Option 1: Google Colab (Recommended)

Google Colab provides free GPU access, perfect for training.

1. **Open the Training Notebook**:
   - Upload `models/saved_models/Olive (3).ipynb` to Google Colab
   - Or open directly: [Open in Colab](https://colab.research.google.com/)

2. **Enable GPU**:
   ```
   Runtime → Change runtime type → Hardware accelerator → GPU → Save
   ```

3. **Mount Google Drive**:
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```

4. **Upload Your Dataset**:
   - Zip your dataset folder
   - Upload to Google Drive
   - Unzip in Colab:
   ```python
   !unzip "drive/MyDrive/your_dataset.zip"
   ```

### Option 2: Local Training

If you have a GPU locally:

```bash
# Create conda environment
conda create -n olive-training python=3.8
conda activate olive-training

# Install PyTorch with CUDA
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia

# Install other dependencies
pip install tensorflow keras opencv-python matplotlib numpy pandas scikit-learn tqdm
```

## 🏗 Model Architecture

### Option A: Custom CNN (Baseline)

Simple convolutional neural network for quick training:

```python
class BaselineCNN(nn.Module):
    def __init__(self, num_classes=3):
        super(BaselineCNN, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.BatchNorm2d(32),
            
            nn.Conv2d(32, 64, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.BatchNorm2d(64),
            
            nn.Conv2d(64, 128, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.BatchNorm2d(128)
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 28 * 28, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes)
        )
```

**Pros**: Fast training, small model size, good for small datasets
**Cons**: Lower accuracy on complex cases

### Option B: MobileNetV3 (Recommended)

Efficient architecture optimized for mobile devices:

```python
import torchvision.models as models

model = models.mobilenet_v3_small(pretrained=True)
model.classifier[3] = nn.Linear(model.classifier[3].in_features, num_classes)
```

**Pros**: Good balance of accuracy and speed, mobile-optimized
**Cons**: Medium model size

### Option C: EfficientNet-Lite0 (Best Accuracy)

State-of-the-art efficiency and accuracy:

```python
import tensorflow as tf

base_model = tf.keras.applications.EfficientNetB0(
    include_top=False,
    weights='imagenet',
    input_shape=(224, 224, 3)
)

model = tf.keras.Sequential([
    base_model,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])
```

**Pros**: Highest accuracy, transfer learning from ImageNet
**Cons**: Larger model size, slower inference

## 🎓 Training Process

### Step 1: Data Loading and Augmentation

```python
from torchvision import transforms, datasets
from torch.utils.data import DataLoader

# Define augmentation
train_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(25),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                       std=[0.229, 0.224, 0.225])
])

# Load data
train_data = datasets.ImageFolder(root='dataset/train', transform=train_transforms)
train_loader = DataLoader(train_data, batch_size=32, shuffle=True)
```

### Step 2: Handle Class Imbalance

```python
from sklearn.utils.class_weight import compute_class_weight

labels = [label for _, label in train_data.samples]
class_weights = compute_class_weight(
    class_weight='balanced',
    classes=np.unique(labels),
    y=labels
)
class_weights = torch.tensor(class_weights, dtype=torch.float).to(device)
```

### Step 3: Training Loop

```python
import torch.optim as optim
from tqdm import tqdm

# Setup
criterion = nn.CrossEntropyLoss(weight=class_weights)
optimizer = optim.Adam(model.parameters(), lr=0.001)
EPOCHS = 15

# Training
for epoch in range(EPOCHS):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    for images, labels in tqdm(train_loader, desc=f"Epoch {epoch+1}/{EPOCHS}"):
        images, labels = images.to(device), labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        _, preds = torch.max(outputs, 1)
        correct += (preds == labels).sum().item()
        total += labels.size(0)
    
    epoch_loss = running_loss / len(train_loader)
    epoch_acc = 100 * correct / total
    print(f"Epoch [{epoch+1}/{EPOCHS}] - Loss: {epoch_loss:.4f} | Accuracy: {epoch_acc:.2f}%")
```

### Step 4: Validation

```python
model.eval()
correct = 0
total = 0

with torch.no_grad():
    for images, labels in test_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        _, preds = torch.max(outputs, 1)
        correct += (preds == labels).sum().item()
        total += labels.size(0)

accuracy = 100 * correct / total
print(f"Test Accuracy: {accuracy:.2f}%")
```

## 📊 Model Evaluation

### Confusion Matrix

```python
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns

# Get all predictions
all_preds = []
all_labels = []

model.eval()
with torch.no_grad():
    for images, labels in test_loader:
        images = images.to(device)
        outputs = model(images)
        _, preds = torch.max(outputs, 1)
        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.numpy())

# Plot confusion matrix
cm = confusion_matrix(all_labels, all_preds)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=class_names,
            yticklabels=class_names)
plt.title('Confusion Matrix')
plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.show()

# Print classification report
print(classification_report(all_labels, all_preds, target_names=class_names))
```

### Per-Class Metrics

- **Precision**: How many predicted positives are correct
- **Recall**: How many actual positives are found
- **F1-Score**: Harmonic mean of precision and recall
- **Support**: Number of samples per class

## 💾 Model Export

### Save PyTorch Model

```python
# Save full model
torch.save(model, 'mobilenetv3_olive_classifier.pth')

# Save state dict (recommended)
torch.save(model.state_dict(), 'model_weights.pth')
```

### Convert to TensorFlow Lite

For mobile deployment, convert to TFLite:

```python
import tensorflow as tf

# If using PyTorch, first convert to ONNX, then to TF, then to TFLite
# Or train directly with TensorFlow/Keras

converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()

with open('efficientnet_lite0_olive_mobile.tflite', 'wb') as f:
    f.write(tflite_model)
```

### Test Converted Model

```python
import tensorflow as tf

# Load TFLite model
interpreter = tf.lite.Interpreter(model_path='model.tflite')
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Test inference
test_image = load_and_preprocess_image('test.jpg')
interpreter.set_tensor(input_details[0]['index'], test_image)
interpreter.invoke()
output = interpreter.get_tensor(output_details[0]['index'])
print("Prediction:", output)
```

## 🚀 Using the Trained Model

### In the Backend Server

Place your trained model in `inference_server/` and update `server.py`:

```python
MODEL_PATH = "efficientnet_lite0_olive_mobile.tflite"

# Load model
interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()
```

### Testing Inference

```bash
cd inference_server
python test_server.py
```

## 📈 Hyperparameter Tuning

### Learning Rate

Try different learning rates:
```python
optimizer = optim.Adam(model.parameters(), lr=0.001)  # Start here
# If loss plateaus: reduce to 0.0001
# If loss oscillates: increase to 0.01
```

### Batch Size

- Small (16-32): Better gradients, slower training
- Large (64-128): Faster training, needs more memory

### Data Augmentation

Adjust augmentation strength:
```python
transforms.RandomRotation(25)        # Increase to 45 for more diversity
transforms.ColorJitter(brightness=0.2)  # Increase to 0.3 for more variation
```

### Regularization

Add dropout or weight decay:
```python
nn.Dropout(0.5)  # Increase if overfitting
optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-4)
```

## 🐛 Troubleshooting

### Low Accuracy
- Increase dataset size
- Add more augmentation
- Try transfer learning
- Train for more epochs
- Check data quality

### Overfitting (High train, low test accuracy)
- Add dropout
- Increase data augmentation
- Reduce model complexity
- Add more training data

### Out of Memory
- Reduce batch size
- Use smaller model
- Use mixed precision training
- Clear GPU cache: `torch.cuda.empty_cache()`

### Class Imbalance
- Use class weights
- Oversample minority class
- Undersample majority class
- Use focal loss

## 📚 Resources

- [PyTorch Documentation](https://pytorch.org/docs/)
- [TensorFlow Guide](https://www.tensorflow.org/guide)
- [Transfer Learning Tutorial](https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html)
- [Model Optimization](https://www.tensorflow.org/lite/performance/model_optimization)
- [Data Augmentation Techniques](https://pytorch.org/vision/stable/transforms.html)

## 📧 Support

For questions about model training:
- Open an issue on GitHub
- Email: aymen.jedidi@ensi-uma.tn

---

Happy Training! 🚀🫒
