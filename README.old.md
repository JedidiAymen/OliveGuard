# Olive Tree Health Monitor

A mobile application for olive tree health monitoring with AI-powered leaf disease detection using a MobileNetV3 model.

## Project Structure

```
olives/
├── front/EventScript/          # React Native (Expo) mobile app
│   ├── screens/                # UI screens (Scan, Dashboard, etc.)
│   ├── utils/aiService.ts      # AI inference integration
│   └── package.json
├── inference_server/           # FastAPI inference backend
│   ├── server.py               # API endpoints for model inference
│   └── requirements.txt
└── models/saved_models/
    └── mobilenetv3_olive_classifier.pth  # Trained PyTorch model
```

## Setup & Running

### 1. Start the Inference Server (Optional)

The inference server runs the MobileNetV3 model and exposes an HTTP API. **The mobile app works without it** using mock data, but for real AI predictions you need to start the server.

```bash
cd inference_server

# Quick start (Linux/Mac)
./start.sh

# Or manual setup:
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (takes 5-10 minutes due to PyTorch)
pip install -r requirements.txt

# Run the server on port 8000
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

The server will be available at `http://localhost:8000`. Check health at `http://localhost:8000/health`.

**Test the server:**
```bash
python test_server.py
```

### 2. Run the Mobile App

The React Native app is built with Expo.

```bash
cd front/EventScript

# Install dependencies (first time only)
npm install

# Start the Expo development server
npm start

# Or run on specific platform:
npm run ios      # iOS simulator
npm run android  # Android emulator
npm run web      # Web browser
```

**Important:** For the mobile app to reach the inference server:
- **iOS Simulator / Android Emulator:** Use `http://localhost:8000`
- **Physical Device:** Update `INFERENCE_API` in `utils/aiService.ts` to your computer's local IP (e.g., `http://192.168.1.100:8000`)

### 3. Using the App

1. Navigate to the **Scan** tab
2. Tap "Take Photo" or "Choose from Library"
3. Select an olive leaf image
4. The app will send the image to the inference server
5. View diagnosis, confidence score, and recommendations

If the inference server is unavailable, the app falls back to mock data.

## Model Information

This project includes **two trained models** for olive disease classification. Both models classify the **same 3 conditions**:

**Classes (Both Models):**
1. **Healthy** - No disease detected
2. **aculus_olearius** - Olive mite (pest)
3. **olive_peacock_spot** - Fungal disease

### 1. MobileNetV3-Large (Recommended)
- **Size:** 41 MB
- **Accuracy:** 91.62% (tested)
- **Location:** `models/saved_models/mobilenetv3_olive_classifier.pth`
- **Best for:** Production use, highest accuracy

### 2. EfficientNet-Lite0 (Mobile-Optimized)
- **Size:** 14 MB (66% smaller)
- **Accuracy:** Not benchmarked
- **Location:** `models/saved_models/efficientnet_lite0_olive_mobile.pt`
- **Best for:** Faster inference, constrained devices

**Input:** Both models use 224×224 RGB images with ImageNet normalization.

**Training:** Models were trained using the notebook in `front/EventScript/attached_assets/Olive (1)_1764174338835.ipynb`.

**Comparison:** See [MODELS.md](./MODELS.md) for detailed comparison and usage recommendations.

## Development

### Linting & Formatting

```bash
cd front/EventScript
npm run lint
npm run format
```

### Environment Variables

For production, set the inference API URL via environment variable:

```bash
export INFERENCE_API_URL=https://your-inference-server.com
```

## Troubleshooting

**Issue:** App can't connect to inference server
- Verify server is running: `curl http://localhost:8000/health`
- Check firewall settings
- On physical device, use local IP instead of localhost

**Issue:** Model fails to load
- Ensure `mobilenetv3_olive_classifier.pth` exists in `models/saved_models/`
- Check PyTorch version compatibility
- Review server logs for detailed errors

**Issue:** TypeScript errors in aiService.ts
- These are compile-time warnings related to tsconfig target. The code runs correctly at runtime.

## License

Private
