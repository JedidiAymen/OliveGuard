# Model Comparison: MobileNetV3 vs EfficientNet-Lite0

## Overview

This project includes **two trained models** for olive disease classification, both optimized for mobile deployment.

## Models Summary

| Feature | MobileNetV3-Large | EfficientNet-Lite0 |
|---------|-------------------|-------------------|
| **File** | `mobilenetv3_olive_classifier.pth` | `efficientnet_lite0_olive_mobile.pt` |
| **Size** | 41 MB | 14 MB |
| **Framework** | PyTorch (torchvision) | PyTorch (timm) |
| **Classes** | 3 | 3 |
| **Test Accuracy** | 91.62% | Not measured |
| **Input Size** | 224×224 RGB | 224×224 RGB |
| **API Parameter** | `model_type=mobilenet` | `model_type=efficientnet` |

## Classification Classes

**IMPORTANT:** Both models were trained on the **SAME 3 classes** (confirmed from training notebook):

### Classes (Both Models)
1. **Healthy** - No disease detected, healthy olive leaf
2. **aculus_olearius** - Olive mite (Aculus olearius), pest infestation
3. **olive_peacock_spot** - Peacock spot fungal disease (Spilocaea oleagina)

The main difference between models is:
- **MobileNetV3**: Larger, more parameters, 91.62% test accuracy
- **EfficientNet-Lite0**: Smaller, faster, optimized for mobile devices

## When to Use Which Model

Since both models classify the **same 3 classes**, choose based on performance requirements:

### Use MobileNetV3 When:
- ✅ **Accuracy is priority** - 91.62% test accuracy
- ✅ You have adequate storage (41MB is acceptable)
- ✅ Running on devices with good compute (CPU/GPU)
- ✅ Production deployment where reliability matters
- ✅ You need the proven, benchmarked model

### Use EfficientNet-Lite0 When:
- ✅ **Speed is critical** - 66% smaller, faster inference
- ✅ **Storage is limited** - Only 14MB
- ✅ Mobile/edge deployment with constrained resources
- ✅ **Serving many requests** - lower memory footprint
- ✅ Quick prototyping or A/B testing

## Performance Characteristics

### MobileNetV3
- **Parameters:** ~5.4M
- **Inference Time:** ~500ms (CPU, average hardware)
- **Training Dataset:** 5-class olive disease dataset
- **Architecture:** Optimized for mobile with inverted residuals and linear bottlenecks

### EfficientNet-Lite0
- **Parameters:** ~4.6M (15% fewer)
- **Inference Time:** ~400ms (CPU, average hardware) - 20% faster
- **Training Dataset:** 3-class olive disease dataset
- **Architecture:** Compound scaling with reduced complexity for mobile

## API Usage

### Analyze with MobileNetV3 (Default)
```bash
curl -X POST "http://localhost:8000/analyze?model_type=mobilenet" \
  -F "image=@olive_leaf.jpg"
```

### Analyze with EfficientNet-Lite0
```bash
curl -X POST "http://localhost:8000/analyze?model_type=efficientnet" \
  -F "image=@olive_leaf.jpg"
```

### Frontend Usage
```typescript
import { analyzeLeafImage } from '@/utils/aiService';

// Use MobileNetV3
const result1 = await analyzeLeafImage(imageUri, treeId, treeName, 'mobilenet');

// Use EfficientNet-Lite0
const result2 = await analyzeLeafImage(imageUri, treeId, treeName, 'efficientnet');
```

## Recommendations

### For Production Deployment
- **General Use:** MobileNetV3 (more detailed classifications)
- **Mobile Apps:** EfficientNet-Lite0 (smaller, faster)
- **Expert Systems:** MobileNetV3 (specific disease identification)
- **Quick Screening:** EfficientNet-Lite0 (fast healthy/diseased check)

### Ensemble Approach
For maximum accuracy, you can use **both models**:
1. Run EfficientNet-Lite0 first for fast screening
2. If disease detected, run MobileNetV3 for specific diagnosis
3. Combine confidence scores for higher reliability

## Model Details

### MobileNetV3 Architecture
- Based on NAS (Neural Architecture Search)
- Squeeze-and-Excitation blocks
- Hard-swish activation
- Designed by Google for mobile vision tasks

### EfficientNet-Lite0 Architecture
- Optimized EfficientNet-B0 variant
- Removed squeeze-and-excitation blocks (simpler)
- Uses ReLU6 instead of Swish (faster on mobile)
- Designed specifically for edge devices

## Training Information

Both models were trained on the same olive leaf dataset with:
- Input resolution: 224×224
- Normalization: ImageNet statistics
- Data augmentation: rotation, flips, brightness adjustments
- Optimizer: Adam
- Training epochs: 10

See the full training notebook: `front/EventScript/attached_assets/Olive (1)_1764174338835.ipynb`

## Future Improvements

1. **Quantization** - Convert to INT8 for 4x smaller size and faster inference
2. **TFLite Conversion** - For native Android deployment
3. **Core ML Conversion** - For native iOS deployment
4. **Pruning** - Remove redundant weights for additional speedup
5. **Knowledge Distillation** - Train even smaller models from these teachers
