# Quick Start Guide

## Get the App Running (2 minutes)

### Option 1: With Mock Data (No Model Required)

```bash
cd front/EventScript
npm install
npm start
```

That's it! The app will run with realistic mock predictions. Perfect for UI testing and development.

### Option 2: With Real AI Model (Requires Python Setup)

**Terminal 1 - Start Backend:**
```bash
cd inference_server
./start.sh
# Wait 5-10 minutes for PyTorch to install (first time only)
```

**Terminal 2 - Start Frontend:**
```bash
cd front/EventScript
npm start
```

## What You Get

- 📱 **React Native Expo App** for iOS/Android/Web
- 🤖 **MobileNetV3 AI Model** for olive leaf disease detection
- 🔄 **Smart Fallback** - works offline with mock data if server is unavailable
- 📊 **5 Disease Classes**: Healthy, Peacock Spot, Olive Knot, Scale Insects, Iron Chlorosis

## Testing

1. Launch the app (`npm start`)
2. Press `i` for iOS simulator, `a` for Android, or `w` for web
3. Navigate to "Scan" tab
4. Take/upload a photo of an olive leaf
5. View AI diagnosis and recommendations

## Troubleshooting

**"Cannot connect to server"** → App automatically falls back to mock data. This is normal!

**Want real predictions?** → Make sure the inference server is running on port 8000

**Port 8000 already in use?** → Kill existing process: `lsof -ti:8000 | xargs kill -9`

**Slow model loading?** → First run installs PyTorch (~2GB). Subsequent starts are fast.

## Architecture

```
┌─────────────┐      HTTP POST      ┌──────────────┐
│  React Native│ ──────image──────> │   FastAPI    │
│  Expo App   │ <────diagnosis───── │   Server     │
└─────────────┘                     └──────────────┘
                                           │
                                           ▼
                                    ┌──────────────┐
                                    │  MobileNetV3 │
                                    │  PyTorch     │
                                    └──────────────┘
```

## Next Steps

- Read the full [README.md](./README.md) for detailed documentation
- Check [design_guidelines.md](./front/EventScript/design_guidelines.md) for UI/UX specs
- View training notebook: `front/EventScript/attached_assets/Olive (1)_1764174338835.ipynb`
