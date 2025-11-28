# Integration Architecture

## Overview

This document describes how the MobileNetV3 olive disease classifier model is integrated with the React Native mobile frontend.

## Components

### 1. Model (`models/saved_models/mobilenetv3_olive_classifier.pth`)

- **Framework:** PyTorch
- **Architecture:** MobileNetV3-Large (torchvision.models)
- **Classes:** 5 olive leaf conditions
- **Input:** 224×224 RGB images, normalized with ImageNet stats
- **Output:** Logits for 5 classes, converted to probabilities via softmax

### 2. Inference Server (`inference_server/`)

**Technology:** FastAPI + Uvicorn

**Endpoints:**
- `GET /health` - Returns model load status
- `POST /analyze` - Accepts multipart image upload, returns diagnosis JSON

**Implementation Details:**
- Loads model on first request (lazy loading)
- Handles state_dict prefixes (e.g., `module.` from DataParallel)
- CPU inference by default (can be updated for GPU)
- Graceful fallback to mock data if model fails to load

**Response Format:**
```json
{
  "diagnosis": "Peacock Spot",
  "diseaseType": "fungal",
  "confidenceScore": 87,
  "recommendations": ["..."],
  "isAnomaly": true
}
```

### 3. Frontend Service (`front/EventScript/utils/aiService.ts`)

**Function:** `analyzeLeafImage(imageUri, treeId?, treeName?)`

**Flow:**
1. User selects/captures image → imageUri
2. Fetch image as blob from local URI
3. Create FormData with image file
4. POST to `http://localhost:8000/analyze`
5. Parse JSON response into `Scan` object
6. If server unavailable, fallback to `mockDiagnoses`

**Resilience:**
- Try-catch around API call
- Network timeout handling via fetch
- Automatic fallback to mock data
- Console warning when using mock data

### 4. UI Integration

**Primary Screen:** `screens/ScanScreen.tsx`
- Image picker integration (expo-image-picker)
- Calls `analyzeLeafImage()` after image selection
- Shows loading state during inference
- Navigates to `ScanResultScreen` with results

**Result Display:** `screens/ScanResultScreen.tsx`
- Shows diagnosis with color-coded confidence
- Disease type badge
- Recommendations list
- Saves scan to local storage (AsyncStorage)

## Data Flow

```
User Action (Take Photo)
  ↓
expo-image-picker → imageUri
  ↓
aiService.analyzeLeafImage(imageUri)
  ↓
┌─────────────────────────────┐
│ Try Real Inference          │
│ fetch(imageUri) → blob      │
│ FormData.append('image')    │
│ POST /analyze               │
│ if success → JSON response  │
└─────────────────────────────┘
  ↓ catch error?
┌─────────────────────────────┐
│ Fallback to Mock            │
│ Random from mockDiagnoses   │
│ Simulated delay 2-3s        │
└─────────────────────────────┘
  ↓
Create Scan object
  ↓
ScanResultScreen displays
  ↓
storage.saveScan() → AsyncStorage
```

## Deployment Considerations

### Development
- Frontend: Expo Dev Server (`npm start`)
- Backend: Local uvicorn on `localhost:8000`
- Both run on developer machine

### Production (Future)

**Mobile App:**
- Build with `expo build` or EAS Build
- Deploy to App Store / Play Store

**Inference Server:**
- Deploy to cloud VM (AWS EC2, GCP Compute, etc.)
- Use Docker for reproducible deployment
- Add HTTPS/SSL certificate
- Consider GPU instance for faster inference
- Update `INFERENCE_API` in aiService.ts to production URL

**Scaling:**
- Add load balancer for multiple server instances
- Cache frequent predictions
- Consider on-device ML (TensorFlow Lite) for offline use

## Environment Configuration

### Development
```typescript
// aiService.ts
const INFERENCE_API = 'http://localhost:8000';
```

### Physical Device Testing
```typescript
// aiService.ts
const INFERENCE_API = 'http://192.168.1.100:8000'; // Your computer's local IP
```

### Production
```typescript
// aiService.ts
const INFERENCE_API = process.env.EXPO_PUBLIC_API_URL || 'https://api.example.com';
```

Set in `.env`:
```
EXPO_PUBLIC_API_URL=https://inference.yourapp.com
```

## Model Updates

To update the model:

1. Train new model using the notebook
2. Save as `.pth` file
3. Replace `models/saved_models/mobilenetv3_olive_classifier.pth`
4. Update `LABELS` in `inference_server/server.py` if classes changed
5. Restart inference server
6. No frontend changes needed (API contract unchanged)

## Monitoring & Debugging

**Server Logs:**
```bash
# See uvicorn output for requests
cd inference_server
uvicorn server:app --reload  # Logs to stdout
```

**Frontend Debugging:**
```typescript
// In aiService.ts, check console for:
console.warn('Inference server unavailable, using mock data:', error);
```

**Health Check:**
```bash
curl http://localhost:8000/health
# {"loaded": true}
```

**Test Full Pipeline:**
```bash
cd inference_server
python test_server.py
```

## Performance

- **Inference Time:** ~500ms on CPU (M-series Mac), ~2-3s on older hardware
- **Model Size:** ~20MB (MobileNetV3 is designed for mobile)
- **Memory:** ~200MB RAM for model + FastAPI
- **Network:** ~100-500KB per image upload (JPEG compressed)

## Security Notes

- No authentication implemented (add OAuth/JWT for production)
- No rate limiting (add middleware for production)
- No input validation beyond image format (add max file size check)
- CORS not configured (add for web deployment)
- No HTTPS (required for production)

## Future Enhancements

1. **On-Device Inference** - Convert to TensorFlow Lite/Core ML
2. **Batch Processing** - Analyze multiple images at once
3. **Confidence Thresholding** - Flag uncertain predictions for expert review
4. **Active Learning** - Collect user feedback to improve model
5. **Caching** - Store recent predictions to avoid re-inference
6. **Webhooks** - Notify users when high-severity diseases detected
