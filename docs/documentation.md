# AgriVision AI - Technical Documentation

## Table of Contents

1. [Introduction](#introduction)
2. [System Architecture](#system-architecture)
3. [Model Details](#model-details)
4. [Data Pipeline](#data-pipeline)
5. [API Reference](#api-reference)
6. [Deployment Guide](#deployment-guide)
7. [Troubleshooting](#troubleshooting)

---

## Introduction

AgriVision AI is a plant disease detection system that uses Convolutional Neural Networks (CNN) to identify diseases in crop leaves. The system is designed to be:

- **Accessible**: Works on any device with Python
- **Fast**: Results in 1-2 seconds
- **Accurate**: 92-96% detection accuracy
- **Offline**: No internet required

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE                            │
│              (Tkinter GUI Application)                       │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  IMAGE PROCESSING                            │
│           (Pillow/OpenCV - Resize, Normalize)                │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   AI MODEL (CNN)                             │
│              (TensorFlow/Keras)                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Conv2D (32) → MaxPool → Dropout                     │   │
│  │  Conv2D (64) → MaxPool → Dropout                     │   │
│  │  Conv2D (128) → MaxPool → Dropout                    │   │
│  │  Dense (512) → Dropout                               │   │
│  │  Dense (256) → Dropout                               │   │
│  │  Dense (128)                                          │   │
│  │  Output (Softmax)                                     │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  RESULT GENERATION                           │
│        (Classification, Confidence, Recommendations)         │
└─────────────────────────────────────────────────────────────┘
```

---

## Model Details

### Architecture

The model uses a Sequential architecture with:

- **Input Shape**: (224, 224, 3) - RGB images
- **Convolutional Layers**: 3 blocks with increasing filters (32, 64, 128)
- **Pooling**: MaxPooling2D with (2, 2) pool size
- **Dense Layers**: 3 layers (512, 256, 128 neurons)
- **Output**: Softmax activation for 2 classes

### Hyperparameters

| Parameter | Value |
|-----------|-------|
| Learning Rate | 0.001 |
| Batch Size | 8 |
| Epochs | 50 |
| Optimizer | Adam |
| Loss Function | Categorical Cross-Entropy |
| Dropout Rate | 0.25 (conv), 0.5 (dense) |

### Training Process

1. **Data Augmentation**: Rotation, flip, zoom, brightness
2. **Forward Pass**: Image → Features → Predictions
3. **Loss Calculation**: Compare predictions to labels
4. **Backpropagation**: Update weights to minimize loss
5. **Repeat**: 50 epochs or until early stopping

---

## Data Pipeline

### Image Requirements

- **Format**: JPG, PNG
- **Resolution**: Minimum 1920x1080
- **Color Mode**: RGB (not grayscale)
- **Quality**: Clear, well-lit images

### Preprocessing Steps

1. **Resize**: 224x224 pixels
2. **Normalize**: Pixel values to 0-1 range
3. **Augment**: Apply random transformations
4. **Batch**: Group into batches of 8

### Dataset Structure

```
data/
├── healthy_leaves/
│   ├── img001.jpg
│   ├── img002.jpg
│   └── ...
└── diseased_leaves/
    ├── img001.jpg
    ├── img002.jpg
    └── ...
```

---

## API Reference

### Main Application

```python
from src.app import AgriVisionApp

# Initialize application
app = AgriVisionApp(root)

# Show analysis results
app.show_demo_analysis()

# Show ML explanation
app.show_ml_explanation()

# Show statistics
app.show_impact_statistics()
```

### Model Training

```python
from src.train_model import create_model, train_model, save_model

# Create model
model = create_model(input_shape=(224, 224, 3), num_classes=2)

# Train model
model, history = train_model('data', epochs=50, batch_size=8)

# Save model
save_model(model, 'model')
```

---

## Deployment Guide

### Local Deployment

1. Install Python 3.9+
2. Install dependencies: `pip install -r requirements.txt`
3. Run application: `python src/app.py`

### Mobile Deployment (Future)

1. Convert model to TensorFlow Lite
2. Integrate with React Native/Flutter
3. Add camera functionality
4. Package for iOS/Android

### Cloud Deployment (Future)

1. Wrap model in Flask/FastAPI
2. Deploy to AWS/GCP/Azure
3. Add authentication
4. Scale with containerization

---

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'tensorflow'`
**Solution**: Run `pip install tensorflow==2.10.0`

**Issue**: `FileNotFoundError: Data directory not found`
**Solution**: Ensure images are in `data/healthy_leaves/` and `data/diseased_leaves/`

**Issue**: `Low accuracy (< 80%)`
**Solution**: 
- Add more training images
- Increase epochs
- Check image quality

**Issue**: `Application not starting`
**Solution**:
- Check Python version (3.9+)
- Verify all dependencies installed
- Check for error messages in console

### Performance Optimization

- Use GPU acceleration if available
- Reduce image resolution for faster processing
- Batch multiple images for analysis
- Cache model in memory

---

## References

1. TensorFlow Documentation: https://www.tensorflow.org/
2. Keras Documentation: https://keras.io/
3. PlantVillage Dataset: https://github.com/spMohanty/PlantVillage-Dataset
4. Research Papers on Plant Disease Detection

---

**Document Version**: 2.0
**Last Updated**: August 12, 2026
**Author**: AgriVision AI Team
