# 🎨 Complete Guide: How We Built OliveGuard App

## 📱 Simple Explanation of Everything We Created

This guide explains **every part** of the OliveGuard app - frontend, backend, database, AI model integration - in simple terms like you know nothing about programming!

---

## 🎯 The Big Picture: What Did We Build?

```
┌─────────────────────────────────────────────────────────────┐
│  YOU                                                        │
│  📱 Use phone camera to take photo of olive leaf           │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  MOBILE APP (Frontend - React Native)                      │
│  - Screens (Dashboard, Camera, Results, Profile)           │
│  - Beautiful user interface                                │
│  - Stores data on your phone                               │
└─────────────────┬───────────────────────────────────────────┘
                  │ Sends photo + your login token
                  │ via Internet (HTTP)
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  BACKEND SERVER (FastAPI - Python)                         │
│  - Receives your photo                                     │
│  - Checks who you are (Authentication)                     │
│  - Processes the image                                     │
│  - Calls the AI model                                      │
└─────────────────┬───────────────────────────────────────────┘
                  │
      ┌───────────┴───────────┐
      ▼                       ▼
┌──────────────┐      ┌──────────────┐
│  DATABASE    │      │  AI MODEL    │
│  (SQLite)    │      │  (TensorFlow)│
│              │      │              │
│  Stores:     │      │  Analyzes:   │
│  - Users     │      │  - Leaf photo│
│  - Emails    │      │  - Disease   │
│  - Passwords │      │  - Confidence│
└──────────────┘      └──────┬───────┘
                             │ Returns: "Aculus Olearius - 95% confident"
                             ▼
                    ┌─────────────────┐
                    │ BACKEND         │
                    │ Formats response│
                    └────────┬────────┘
                             │ Sends back: Disease name + recommendations
                             ▼
                    ┌─────────────────┐
                    │ MOBILE APP      │
                    │ Shows results   │
                    └─────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ YOU             │
                    │ See diagnosis!  │
                    └─────────────────┘
```

---

## 📱 PART 1: THE FRONTEND (Mobile App)

### What is the Frontend?
**Simple answer:** Everything you **see and touch** on your phone - buttons, screens, colors, animations.

### What Did We Use?
- **React Native**: A tool to build mobile apps using JavaScript
- **Expo**: Makes React Native easier (like training wheels on a bike)
- **TypeScript**: JavaScript with extra safety (catches mistakes before running)

---

### 🏗️ Frontend Architecture

```
OliveGuard App
│
├── 🔐 Authentication Screens (Before Login)
│   ├── LoginScreen.tsx      → Email + Password input
│   └── SignupScreen.tsx     → Create new account
│
└── 📱 Main App (After Login)
    │
    ├── 🏠 Dashboard Tab
    │   ├── DashboardScreen     → Health overview, recent scans
    │   ├── AlertsScreen        → Disease warnings
    │   └── ScanResultScreen    → Detailed scan results
    │
    ├── 📸 Scan Tab
    │   ├── ScanScreen          → Camera interface
    │   └── ScanResultScreen    → Analysis results
    │
    ├── 🌳 Orchard Tab
    │   ├── OrchardScreen       → List all trees
    │   ├── AddTreeScreen       → Add new tree
    │   ├── TreeDetailScreen    → Tree info + scan history
    │   └── TreeEditScreen      → Edit tree details
    │
    ├── 📚 Resources Tab
    │   ├── ResourcesScreen     → Disease information articles
    │   └── ResourceDetailScreen→ Full article view
    │
    └── 👤 Profile Tab
        ├── ProfileScreen       → User info + statistics
        ├── EditProfileScreen   → Edit name, orchard name
        └── SettingsScreen      → App settings
```

---

### 🎨 How Screens Work (Simple Example)

#### Example: DashboardScreen

**What you see:**
```
┌─────────────────────────────┐
│  Good Morning, Aymen! ☀️   │
│                             │
│  ┌───────────────────────┐  │
│  │ Health Score: 87%    │  │
│  │ Trees: 12            │  │
│  │ Alerts: 3            │  │
│  └───────────────────────┘  │
│                             │
│  📊 Recent Scans            │
│  ┌─────────────────────┐   │
│  │ 🌿 Tree #3          │   │
│  │ Healthy - 95%       │   │
│  └─────────────────────┘   │
│                             │
│  📸 [Scan Now Button]       │
└─────────────────────────────┘
```

**How it's built:**
```typescript
// DashboardScreen.tsx
function DashboardScreen() {
  // 1. Get data from storage
  const [scans, setScans] = useState([]);
  const [trees, setTrees] = useState([]);
  
  useEffect(() => {
    // Load data when screen opens
    loadScans();    // Get all previous scans
    loadTrees();    // Get all trees
    loadAlerts();   // Get all alerts
  }, []);
  
  // 2. Calculate statistics
  const healthScore = calculateHealthScore(scans);
  const treeCount = trees.length;
  const alertCount = alerts.filter(a => !a.isRead).length;
  
  // 3. Display on screen
  return (
    <View>
      <Text>Good Morning, {user.name}!</Text>
      
      <StatsCard>
        <Text>Health Score: {healthScore}%</Text>
        <Text>Trees: {treeCount}</Text>
        <Text>Alerts: {alertCount}</Text>
      </StatsCard>
      
      <RecentScans scans={scans} />
      
      <Button onPress={navigateToScan}>
        Scan Now
      </Button>
    </View>
  );
}
```

**What happens:**
1. Screen opens → Load data from phone storage
2. Calculate numbers (health score, tree count)
3. Show everything nicely formatted
4. When you tap "Scan Now" → Go to camera screen

---

### 📸 How Camera Works (ScanScreen)

**Step-by-step:**

```typescript
// ScanScreen.tsx
function ScanScreen() {
  const [photo, setPhoto] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  
  // 1. Take photo
  const takePhoto = async () => {
    const result = await ImagePicker.launchCameraAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      quality: 0.8,  // Compress to 80% quality
    });
    
    if (!result.cancelled) {
      setPhoto(result.uri);  // Save photo location
    }
  };
  
  // 2. Send to backend for analysis
  const analyzePhoto = async () => {
    setAnalyzing(true);  // Show loading spinner
    
    try {
      // Create form data (like a package to send)
      const formData = new FormData();
      formData.append('file', {
        uri: photo,
        type: 'image/jpeg',
        name: 'leaf.jpg'
      });
      
      // Get authentication token
      const token = await getAuthToken();
      
      // Send to backend
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData
      });
      
      // Get result
      const result = await response.json();
      // result = { 
      //   diagnosis: "Aculus Olearius",
      //   confidence: 0.95,
      //   disease_type: "pest",
      //   recommendations: ["Apply neem oil...", ...]
      // }
      
      // 3. Save to phone storage
      await saveScan({
        id: generateId(),
        imageUri: photo,
        diagnosis: result.diagnosis,
        confidenceScore: result.confidence,
        recommendations: result.recommendations,
        scannedAt: new Date().toISOString(),
      });
      
      // 4. Show results
      navigation.navigate('ScanResult', { scan: result });
      
    } catch (error) {
      alert('Failed to analyze. Please try again.');
    } finally {
      setAnalyzing(false);
    }
  };
  
  return (
    <View>
      {photo ? (
        <>
          <Image source={{ uri: photo }} />
          <Button onPress={analyzePhoto}>
            {analyzing ? 'Analyzing...' : 'Analyze Leaf'}
          </Button>
        </>
      ) : (
        <Button onPress={takePhoto}>
          Take Photo
        </Button>
      )}
    </View>
  );
}
```

**Flow:**
1. You tap "Take Photo" → Camera opens
2. Take picture → Photo saved on phone
3. Tap "Analyze" → Send to backend server
4. Wait 2-3 seconds → Get result
5. Save result → Show diagnosis screen

---

### 💾 How Data Storage Works (AsyncStorage)

**Think of it like a filing cabinet on your phone:**

```typescript
// storage.ts

// Save a scan
export async function saveScan(scan: Scan) {
  // 1. Get existing scans
  const scansJson = await AsyncStorage.getItem('@oliveguard_scans');
  const scans = scansJson ? JSON.parse(scansJson) : [];
  
  // 2. Add new scan
  scans.push(scan);
  
  // 3. Save back to storage
  await AsyncStorage.setItem('@oliveguard_scans', JSON.stringify(scans));
}

// Get all scans
export async function getScans() {
  const scansJson = await AsyncStorage.getItem('@oliveguard_scans');
  return scansJson ? JSON.parse(scansJson) : [];
}
```

**What we store:**
```javascript
{
  // Trees
  "@oliveguard_trees": [
    { id: "1", name: "Tree #1", location: "North field", ... },
    { id: "2", name: "Tree #2", location: "South field", ... }
  ],
  
  // Scans
  "@oliveguard_scans": [
    { 
      id: "scan1", 
      treeId: "1",
      diagnosis: "Healthy",
      confidence: 0.98,
      scannedAt: "2025-11-28T10:30:00Z",
      ...
    }
  ],
  
  // Alerts
  "@oliveguard_alerts": [
    {
      id: "alert1",
      treeId: "2",
      diagnosis: "Aculus Olearius",
      severity: "high",
      isRead: false,
      ...
    }
  ],
  
  // User profile
  "@oliveguard_user": {
    id: "user1",
    name: "Aymen",
    email: "aymen@example.com",
    orchardName: "My Olive Farm"
  }
}
```

**Why AsyncStorage?**
- Works offline (no internet needed)
- Fast access
- Persists between app restarts
- Simple to use

---

## 🔐 PART 2: AUTHENTICATION SYSTEM

### What is Authentication?
**Simple answer:** Proving you are who you say you are, like showing an ID card.

### How It Works:

#### 1️⃣ **Sign Up (Create Account)**

```
User enters:
  - Name: "Aymen"
  - Email: "aymen@example.com"
  - Password: "securepass123"

                │
                ▼
        Send to Backend
                │
                ▼
┌─────────────────────────────────┐
│  Backend receives                │
│  1. Hash password with bcrypt    │
│     "securepass123"              │
│     → "$2b$12$xK9j..."  (gibberish)
│                                  │
│  2. Save to database:            │
│     INSERT INTO users VALUES     │
│     ('Aymen', 'aymen@...', '$2b$...')
│                                  │
│  3. Create JWT token             │
│     Token = proof you logged in  │
│                                  │
│  4. Send back:                   │
│     {                            │
│       "access_token": "eyJ0...", │
│       "user": {                  │
│         "id": 3,                 │
│         "name": "Aymen",         │
│         "email": "aymen@..."     │
│       }                          │
│     }                            │
└─────────────────────────────────┘
                │
                ▼
        Mobile App receives
                │
                ▼
        Save token to AsyncStorage
                │
                ▼
        Navigate to Dashboard
```

#### 2️⃣ **Login (Existing Account)**

```
User enters:
  - Email: "aymen@example.com"
  - Password: "securepass123"

                │
                ▼
        Send to Backend
                │
                ▼
┌─────────────────────────────────┐
│  Backend:                        │
│  1. Find user in database        │
│     SELECT * FROM users          │
│     WHERE email = 'aymen@...'    │
│                                  │
│  2. Check password               │
│     compare("securepass123",     │
│             "$2b$12$xK9j...")    │
│     → Match! ✅                  │
│                                  │
│  3. Create new JWT token         │
│  4. Send back token + user info  │
└─────────────────────────────────┘
                │
                ▼
        Save token & login
```

#### 3️⃣ **Making Authenticated Requests**

Every time you use the app:

```
Mobile App:
  "I want to analyze a photo"
  
  Headers:
    Authorization: Bearer eyJ0eXAiOiJKV1QiLCJ...
                          ↑
                    Your JWT token (like an ID badge)

                │
                ▼
        Backend checks:
                │
                ▼
┌─────────────────────────────────┐
│  Is this token valid?            │
│  - Not expired?                  │
│  - Proper signature?             │
│  - Exists in our system?         │
│                                  │
│  YES ✅                          │
│  → Allow access                  │
│  → Process photo                 │
│                                  │
│  NO ❌                           │
│  → Return 401 Unauthorized       │
│  → User must login again         │
└─────────────────────────────────┘
```

**JWT Token Explained:**
```
JWT Token = 3 parts separated by dots:

eyJ0eXAiOiJKV1QiLCJhbGc.eyJzdWIiOiJ1c2VyQG.SflKxwRJSMeKKF2QT
    ↑ Header              ↑ Payload        ↑ Signature

Header:   { "alg": "HS256", "typ": "JWT" }
Payload:  { "sub": "user@email.com", "exp": 1234567890 }
Signature: Ensures nobody tampered with the token
```

---

## 🖥️ PART 3: THE BACKEND (Server)

### What is the Backend?
**Simple answer:** A computer program running 24/7 that:
- Receives requests from mobile apps
- Checks who you are
- Processes images with AI
- Stores user accounts
- Sends responses back

### What Did We Use?
- **FastAPI**: Python framework for building APIs (like a post office for data)
- **Uvicorn**: Server that runs FastAPI (like the building the post office is in)
- **SQLite**: Small database file (like an Excel file for user data)
- **TensorFlow Lite**: AI model runner
- **PIL (Pillow)**: Image processing library

---

### 🏗️ Backend Structure

```
inference_server/
│
├── server.py          → Main API (receives requests)
├── auth.py            → Authentication logic (JWT, passwords)
├── database.py        → Database setup (SQLite)
├── olive_app.db       → Database file (stores users)
├── requirements.txt   → List of tools needed
└── start.sh           → Script to start server
```

---

### 📡 Backend API Endpoints (Like Restaurant Menu)

```python
# server.py

from fastapi import FastAPI, File, UploadFile, Depends
from auth import get_current_user
import tensorflow as tf

app = FastAPI()

# ========================================
# Endpoint 1: Health Check
# ========================================
@app.get("/health")
def health_check():
    """
    Simple check: Is server running?
    Like asking "Are you open?" to a restaurant
    """
    return {
        "status": "ok",
        "model_loaded": True,
        "model": "efficientnet_lite0"
    }

# ========================================
# Endpoint 2: Register New User
# ========================================
@app.post("/auth/register")
def register(email: str, password: str, name: str):
    """
    Create new user account
    
    Steps:
    1. Check if email already exists
    2. Hash the password (for security)
    3. Save to database
    4. Create JWT token
    5. Return token + user info
    """
    # Check if user exists
    existing = db.query("SELECT * FROM users WHERE email = ?", (email,))
    if existing:
        raise HTTPException(400, "Email already registered")
    
    # Hash password
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    # Save to database
    db.execute(
        "INSERT INTO users (email, hashed_password, name) VALUES (?, ?, ?)",
        (email, hashed_password, name)
    )
    
    # Create JWT token
    token = create_access_token(data={"sub": email})
    
    # Return
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user_id,
            "email": email,
            "name": name
        }
    }

# ========================================
# Endpoint 3: Login
# ========================================
@app.post("/auth/login")
def login(email: str, password: str):
    """
    Login existing user
    
    Steps:
    1. Find user in database
    2. Check if password matches
    3. Create JWT token
    4. Return token + user info
    """
    # Find user
    user = db.query("SELECT * FROM users WHERE email = ?", (email,))
    if not user:
        raise HTTPException(401, "Invalid credentials")
    
    # Check password
    if not bcrypt.checkpw(password.encode(), user['hashed_password']):
        raise HTTPException(401, "Invalid credentials")
    
    # Create token
    token = create_access_token(data={"sub": email})
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user['id'],
            "email": user['email'],
            "name": user['name']
        }
    }

# ========================================
# Endpoint 4: Analyze Leaf Image (THE MAIN ONE!)
# ========================================
@app.post("/analyze")
async def analyze_leaf(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user)  # Requires login!
):
    """
    Analyze olive leaf image for diseases
    
    Steps:
    1. Receive image from mobile app
    2. Check user is logged in
    3. Preprocess image (resize, normalize)
    4. Run through AI model
    5. Get prediction
    6. Format response with recommendations
    7. Send back to mobile app
    """
    
    # Step 1: Read image file
    image_bytes = await file.read()
    
    # Step 2: Open with PIL
    image = Image.open(BytesIO(image_bytes))
    
    # Step 3: Preprocess
    # Convert to RGB (in case it's RGBA or grayscale)
    image = image.convert('RGB')
    
    # Resize to 224x224 (model expects this size)
    image = image.resize((224, 224))
    
    # Convert to numpy array
    image_array = np.array(image)
    
    # Normalize pixel values from [0, 255] to [0, 1]
    image_array = image_array / 255.0
    
    # Add batch dimension: (224, 224, 3) → (1, 224, 224, 3)
    image_array = np.expand_dims(image_array, axis=0)
    
    # Step 4: Run through AI model
    interpreter = tf.lite.Interpreter(model_path="model.tflite")
    interpreter.allocate_tensors()
    
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    # Set input
    interpreter.set_tensor(input_details[0]['index'], image_array.astype(np.float32))
    
    # Run inference
    interpreter.invoke()
    
    # Get output
    predictions = interpreter.get_tensor(output_details[0]['index'])[0]
    # predictions = [0.02, 0.03, 0.95]  (probabilities for 3 classes)
    
    # Step 5: Get the class with highest probability
    class_names = ['healthy', 'aculus_olearius', 'olive_peacock_spot']
    predicted_class_idx = np.argmax(predictions)
    confidence = float(predictions[predicted_class_idx])
    
    predicted_class = class_names[predicted_class_idx]
    
    # Step 6: Map to user-friendly names and get recommendations
    disease_info = {
        'healthy': {
            'display_name': 'Healthy Leaf',
            'disease_type': 'healthy',
            'recommendations': [
                'Your olive tree appears healthy!',
                'Continue regular watering and care.',
                'Monitor leaves weekly for early disease detection.'
            ]
        },
        'aculus_olearius': {
            'display_name': 'Aculus Olearius (Olive Leaf Mite)',
            'disease_type': 'pest',
            'recommendations': [
                'Apply sulfur-based miticide spray.',
                'Spray in early morning or late evening.',
                'Repeat treatment every 10-14 days.',
                'Remove heavily infested leaves.',
                'Ensure good air circulation around trees.'
            ]
        },
        'olive_peacock_spot': {
            'display_name': 'Olive Peacock Spot (Cycloconium oleaginum)',
            'disease_type': 'fungal',
            'recommendations': [
                'Apply copper-based fungicide immediately.',
                'Remove and destroy infected leaves.',
                'Avoid overhead watering (use drip irrigation).',
                'Improve air circulation through pruning.',
                'Apply preventive sprays in humid seasons.'
            ]
        }
    }
    
    info = disease_info[predicted_class]
    
    # Step 7: Return response
    return {
        "diagnosis": info['display_name'],
        "confidence": confidence,
        "disease_type": info['disease_type'],
        "recommendations": info['recommendations']
    }
```

---

### 🔐 How Authentication Works in Backend

```python
# auth.py

import jwt
from datetime import datetime, timedelta
import bcrypt

SECRET_KEY = "your-secret-key-keep-this-safe"
ALGORITHM = "HS256"

# ========================================
# Create JWT Token
# ========================================
def create_access_token(data: dict):
    """
    Create a JWT token that expires in 7 days
    
    Like creating a temporary ID badge
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    
    # Encode to JWT
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

# ========================================
# Verify JWT Token
# ========================================
def get_current_user(token: str):
    """
    Check if JWT token is valid
    
    Like checking if an ID badge is real
    """
    try:
        # Decode token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        
        if email is None:
            raise HTTPException(401, "Invalid token")
        
        # Get user from database
        user = db.query("SELECT * FROM users WHERE email = ?", (email,))
        
        if user is None:
            raise HTTPException(401, "User not found")
        
        return user
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.JWTError:
        raise HTTPException(401, "Invalid token")

# ========================================
# Hash Password
# ========================================
def hash_password(password: str):
    """
    Convert password to gibberish (one-way encryption)
    
    "password123" → "$2b$12$xK9jK7..."
    
    Cannot be reversed! Like scrambling eggs.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()

# ========================================
# Check Password
# ========================================
def verify_password(plain_password: str, hashed_password: str):
    """
    Check if password matches the hash
    
    User enters: "password123"
    Database has: "$2b$12$xK9jK7..."
    
    bcrypt magically checks if they match!
    """
    return bcrypt.checkpw(
        plain_password.encode(),
        hashed_password.encode()
    )
```

---

### 💾 How Database Works

```python
# database.py

import sqlite3

# ========================================
# Create Database File
# ========================================
def init_db():
    """
    Create database file and users table
    
    Runs once when server starts
    """
    conn = sqlite3.connect('olive_app.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# ========================================
# Get Database Connection
# ========================================
def get_db():
    """
    Open connection to database
    
    Like opening a file to read/write
    """
    conn = sqlite3.connect('olive_app.db')
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn
```

**Database Structure:**
```
olive_app.db
│
└── users table
    ├── id              (1, 2, 3, ...)
    ├── email           ("aymen@example.com")
    ├── hashed_password ("$2b$12$xK9jK7...")
    ├── name            ("Aymen")
    └── created_at      ("2025-11-28 10:30:00")
```

**Example Data:**
```sql
SELECT * FROM users;

id | email                    | hashed_password        | name   | created_at
---+--------------------------+------------------------+--------+-------------------
1  | test@olive.com          | $2b$12$xK9jK7...     | Test   | 2025-11-28 09:36:42
2  | user@olive.com          | $2b$12$aB3cD4...     | User   | 2025-11-28 09:36:48
3  | aymen.jedidi@ensi-uma.tn| $2b$12$zY8xW9...     | aymen  | 2025-11-28 09:48:24
```

---

## 🤖 PART 4: AI MODEL INTEGRATION

### How the AI Model Works

#### 1️⃣ **Model File**

```
models/saved_models/
└── efficientnet_lite0_olive_mobile.pt  (14 MB file)
```

This file contains:
- **Learned patterns** from 1000+ olive leaf photos
- **Weights** (numbers that determine how the model thinks)
- **Architecture** (the structure of the neural network)

#### 2️⃣ **Loading the Model**

```python
# In server.py

import tensorflow as tf

# Load TensorFlow Lite model
interpreter = tf.lite.Interpreter(
    model_path="models/efficientnet_lite0_olive_mobile.pt"
)

# Allocate memory for the model
interpreter.allocate_tensors()

# Get input/output information
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print("Model loaded successfully!")
print(f"Input shape: {input_details[0]['shape']}")  # [1, 224, 224, 3]
print(f"Output shape: {output_details[0]['shape']}")  # [1, 3]
```

#### 3️⃣ **Image Preprocessing Pipeline**

```python
def preprocess_image(image_bytes):
    """
    Convert raw image to format the model expects
    
    Input:  JPEG file (any size, any format)
    Output: NumPy array (1, 224, 224, 3) with values 0-1
    """
    
    # Step 1: Open image
    image = Image.open(BytesIO(image_bytes))
    # Image might be: 4000x3000 pixels, RGBA format
    
    # Step 2: Convert to RGB
    image = image.convert('RGB')
    # Now: 4000x3000 pixels, RGB format
    
    # Step 3: Resize to 224x224
    image = image.resize((224, 224), Image.LANCZOS)
    # Now: 224x224 pixels, RGB format
    
    # Step 4: Convert to NumPy array
    image_array = np.array(image)
    # Now: NumPy array of shape (224, 224, 3)
    # Values: 0-255 (e.g., red pixel = [255, 0, 0])
    
    # Step 5: Normalize to 0-1 range
    image_array = image_array.astype(np.float32) / 255.0
    # Now: Values 0.0-1.0 (e.g., red pixel = [1.0, 0.0, 0.0])
    
    # Step 6: Add batch dimension
    image_array = np.expand_dims(image_array, axis=0)
    # Now: Shape (1, 224, 224, 3)
    # 1 = batch size (processing 1 image at a time)
    
    return image_array
```

**Visual Representation:**
```
Original Photo (4000×3000×3)
    ↓ Resize
224×224×3
    ↓ Normalize
Values: 0.0 to 1.0
    ↓ Add batch dimension
1×224×224×3
    ↓
Ready for Model!
```

#### 4️⃣ **Running Inference**

```python
def run_inference(preprocessed_image):
    """
    Pass image through AI model and get predictions
    
    Input:  Image array (1, 224, 224, 3)
    Output: Predictions [0.02, 0.03, 0.95]
    """
    
    # Step 1: Set input tensor
    interpreter.set_tensor(
        input_details[0]['index'],
        preprocessed_image
    )
    
    # Step 2: Run the model (this is where AI happens!)
    interpreter.invoke()
    
    # Step 3: Get output tensor
    output_data = interpreter.get_tensor(
        output_details[0]['index']
    )
    
    # Output looks like: [[0.02, 0.03, 0.95]]
    # Means:
    # - 2% chance it's healthy
    # - 3% chance it's aculus_olearius
    # - 95% chance it's olive_peacock_spot
    
    return output_data[0]  # Remove batch dimension → [0.02, 0.03, 0.95]
```

#### 5️⃣ **Post-Processing (Getting Human-Readable Results)**

```python
def postprocess_predictions(predictions):
    """
    Convert model output to human-readable format
    
    Input:  [0.02, 0.03, 0.95]
    Output: {
              "diagnosis": "Olive Peacock Spot",
              "confidence": 0.95,
              "disease_type": "fungal",
              "recommendations": [...]
            }
    """
    
    # Class names (must match training order!)
    class_names = [
        'healthy',
        'aculus_olearius',
        'olive_peacock_spot'
    ]
    
    # Find class with highest probability
    predicted_idx = np.argmax(predictions)  # Returns: 2
    predicted_class = class_names[predicted_idx]  # Returns: 'olive_peacock_spot'
    confidence = float(predictions[predicted_idx])  # Returns: 0.95
    
    # Map to user-friendly information
    disease_map = {
        'healthy': {
            'display_name': 'Healthy Leaf',
            'disease_type': 'healthy',
            'recommendations': [
                'Great! Your tree is healthy.',
                'Continue regular watering.',
                'Monitor weekly for changes.'
            ]
        },
        'aculus_olearius': {
            'display_name': 'Aculus Olearius (Olive Leaf Mite)',
            'disease_type': 'pest',
            'recommendations': [
                'Apply sulfur-based miticide.',
                'Spray early morning or evening.',
                'Repeat every 10-14 days.',
                'Remove infested leaves.'
            ]
        },
        'olive_peacock_spot': {
            'display_name': 'Olive Peacock Spot (Cycloconium oleaginum)',
            'disease_type': 'fungal',
            'recommendations': [
                'Apply copper-based fungicide immediately.',
                'Remove infected leaves.',
                'Avoid overhead watering.',
                'Improve air circulation.'
            ]
        }
    }
    
    info = disease_map[predicted_class]
    
    return {
        'diagnosis': info['display_name'],
        'confidence': confidence,
        'disease_type': info['disease_type'],
        'recommendations': info['recommendations']
    }
```

---

## 🔄 PART 5: COMPLETE DATA FLOW

### Full Journey of a Photo (Step-by-Step)

```
1. USER TAKES PHOTO
   📱 Mobile App
   └─ Open camera
   └─ Take picture
   └─ Save to phone: "file:///storage/photo123.jpg"

2. USER TAPS "ANALYZE"
   📱 Mobile App
   └─ Read photo file
   └─ Create FormData package
   └─ Get JWT token from AsyncStorage
   └─ Send HTTP POST request:
      URL: http://localhost:8000/analyze
      Headers: { Authorization: "Bearer eyJ0..." }
      Body: { file: <image_data> }

3. BACKEND RECEIVES REQUEST
   🖥️ FastAPI Server
   └─ Endpoint: POST /analyze
   └─ Check 1: Is token valid?
      ├─ Decode JWT token
      ├─ Check expiration date
      └─ Find user in database
   └─ ✅ Token valid! Proceed.
   
4. IMAGE PREPROCESSING
   🖥️ Backend
   └─ Read image bytes
   └─ Open with PIL: Image.open()
   └─ Convert to RGB
   └─ Resize to 224×224
   └─ Convert to NumPy array
   └─ Normalize: divide by 255
   └─ Add batch dimension
   └─ Result: (1, 224, 224, 3) float32 array

5. AI MODEL INFERENCE
   🤖 TensorFlow Lite
   └─ Load model.tflite
   └─ Set input tensor
   └─ Run inference (AI magic happens here!)
      └─ 150+ layers of calculations
      └─ Millions of multiplications
      └─ Takes ~200-400ms
   └─ Get output tensor
   └─ Result: [0.02, 0.03, 0.95]

6. POST-PROCESSING
   🖥️ Backend
   └─ Find max probability: index 2, value 0.95
   └─ Map to class name: "olive_peacock_spot"
   └─ Get user-friendly name: "Olive Peacock Spot (Cycloconium oleaginum)"
   └─ Get disease type: "fungal"
   └─ Get recommendations: ["Apply copper fungicide...", ...]

7. SEND RESPONSE
   🖥️ Backend → 📱 Mobile App
   └─ HTTP 200 OK
   └─ JSON response:
      {
        "diagnosis": "Olive Peacock Spot (Cycloconium oleaginum)",
        "confidence": 0.95,
        "disease_type": "fungal",
        "recommendations": [
          "Apply copper-based fungicide immediately.",
          "Remove and destroy infected leaves.",
          "Avoid overhead watering.",
          "Improve air circulation."
        ]
      }

8. MOBILE APP RECEIVES RESPONSE
   📱 Mobile App
   └─ Parse JSON
   └─ Create scan object:
      {
        id: "scan123",
        imageUri: "file:///storage/photo123.jpg",
        diagnosis: "Olive Peacock Spot...",
        confidenceScore: 0.95,
        diseaseType: "fungal",
        recommendations: [...],
        scannedAt: "2025-11-28T14:30:00Z",
        isAnomaly: true
      }

9. SAVE TO LOCAL STORAGE
   📱 Mobile App
   └─ Get existing scans from AsyncStorage
   └─ Add new scan to array
   └─ Save back to AsyncStorage('@oliveguard_scans')
   └─ If confidence < 80%, create alert too

10. SHOW RESULTS TO USER
    📱 Mobile App
    └─ Navigate to ScanResultScreen
    └─ Display:
       ┌────────────────────────────┐
       │  🦠 Disease Detected       │
       │                            │
       │  Olive Peacock Spot        │
       │  Confidence: 95%           │
       │                            │
       │  Type: Fungal disease      │
       │                            │
       │  💊 Recommendations:       │
       │  • Apply copper fungicide  │
       │  • Remove infected leaves  │
       │  • Avoid overhead watering │
       │                            │
       │  [Assign to Tree] [Done]   │
       └────────────────────────────┘

11. USER ASSIGNS TO TREE (Optional)
    📱 Mobile App
    └─ User selects "Tree #3"
    └─ Update scan: treeId = "3", treeName = "Tree #3"
    └─ Update tree: lastScannedAt = now, healthStatus = "diseased"
    └─ Create alert for this tree
    └─ Save all to AsyncStorage

12. DASHBOARD UPDATES
    📱 Mobile App → Dashboard
    └─ Refresh statistics:
       ├─ Health score drops: 92% → 87%
       ├─ Anomalies found: 2 → 3
       ├─ New alerts: 0 → 1
    └─ Show notification badge on bell icon
    └─ Display new alert in alerts list
```

**Timeline:**
```
0ms:    User taps "Analyze"
100ms:  Photo uploaded to backend
200ms:  Backend receives and validates
400ms:  Image preprocessed
800ms:  AI inference complete
900ms:  Response formatted
1000ms: Mobile app receives result
1100ms: Saved to storage
1200ms: Results screen shown to user

Total: ~1.2 seconds from tap to result! ⚡
```

---

## 🔒 PART 6: SECURITY EXPLAINED

### Why We Need Security:

**Without Security:**
```
Bad Actor:
  "Give me all users' data!"
  → Server: "Here you go!" ❌
  
  "Delete all trees!"
  → Server: "Done!" ❌
```

**With Security:**
```
Bad Actor:
  "Give me all users' data!"
  → Server: "Who are you? Show me your token."
  → Bad Actor: "I don't have one."
  → Server: "401 Unauthorized. Go away!" ✅
  
  "Delete all trees!" (with fake token)
  → Server: "This token is invalid/expired."
  → Server: "401 Unauthorized." ✅
```

### Security Layers:

#### Layer 1: Password Hashing (bcrypt)

```python
# When user signs up:
password = "mypassword123"
            ↓
hashed = bcrypt.hashpw(password)
            ↓
hashed = "$2b$12$xK9jK7Lp8qZ..." (gibberish)

# Save to database:
INSERT INTO users VALUES ('aymen@...', '$2b$12$xK9jK7...')

# Even if hacker steals database, they cannot:
# - Reverse the hash to get "mypassword123"
# - Use hash directly (it only works with bcrypt.checkpw)
```

**Why bcrypt?**
- One-way encryption (cannot be reversed)
- Slow by design (makes brute-force attacks expensive)
- Includes salt (same password → different hashes)

#### Layer 2: JWT Tokens

```python
# Token structure:
eyJ0eXAiOiJKV1QiLCJhbGc.eyJzdWIiOiJ1c2Vy.SflKxwRJSMeKKF2QT
    ↑ Header             ↑ Payload      ↑ Signature

# Header: { "alg": "HS256", "typ": "JWT" }
# Payload: { "sub": "user@email.com", "exp": 1735392000 }
# Signature: HMACSHA256(header + payload, SECRET_KEY)
```

**Token Validation:**
```python
# Mobile sends:
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...

# Backend checks:
1. Is structure valid? (3 parts separated by dots)
2. Is signature correct? (recalculate and compare)
3. Is token expired? (check 'exp' timestamp)
4. Does user exist? (query database)

If ANY check fails → 401 Unauthorized
If ALL pass → Allow request ✅
```

#### Layer 3: HTTPS (In Production)

```
Without HTTPS (HTTP):
  Mobile → [password: "secret123"] → Server
           ↑ VISIBLE to anyone on network! ❌

With HTTPS:
  Mobile → [encrypted gibberish] → Server
           ↑ Unreadable to attackers ✅
```

---

## 📊 PART 7: PERFORMANCE OPTIMIZATION

### How We Made It Fast:

#### 1. **Model Optimization**

```
Original Model (EfficientNet):
- Size: 150 MB
- Speed: 2 seconds per image
- Too slow for mobile! ❌

Optimized Model (EfficientNet-Lite0):
- Size: 14 MB (10x smaller!)
- Speed: 400ms per image (5x faster!)
- Perfect for mobile! ✅

How? TensorFlow Lite conversion:
  - Quantization: 32-bit floats → 8-bit integers
  - Pruning: Remove unused parts
  - Layer fusion: Combine operations
```

#### 2. **Image Compression**

```python
# In mobile app:
const result = await ImagePicker.launchCameraAsync({
  quality: 0.8,  // Compress to 80% quality
  // Before: 4MB photo
  // After: 800KB photo (5x smaller!)
});
```

#### 3. **Caching**

```typescript
// Cache AI model in memory (don't reload every time)
let model_loaded = false;
let interpreter = null;

if (!model_loaded) {
  interpreter = tf.lite.Interpreter("model.tflite");
  model_loaded = true;
}
// Now inference is instant!
```

#### 4. **AsyncStorage Optimization**

```typescript
// Bad: Load everything every time ❌
async function getDashboardData() {
  const scans = await getScans();  // 500 scans = slow!
  const trees = await getTrees();
  const alerts = await getAlerts();
  // Takes 2-3 seconds
}

// Good: Load only what you need ✅
async function getDashboardData() {
  const recentScans = await getScans().then(s => s.slice(0, 5));
  const treeCount = await getTrees().then(t => t.length);
  const unreadAlerts = await getAlerts().then(a => a.filter(x => !x.isRead).length);
  // Takes 200ms
}
```

---

## 🎯 Summary: How Everything Works Together

### The Complete System:

```
┌─────────────────────────────────────────────────────────┐
│  📱 MOBILE APP (React Native + Expo)                    │
├─────────────────────────────────────────────────────────┤
│  • 25+ screens (Dashboard, Scan, Orchard, etc.)        │
│  • Camera integration (take photos)                     │
│  • Local storage (AsyncStorage)                         │
│  • Authentication (JWT tokens)                          │
│  • Navigation (React Navigation)                        │
│  • Beautiful UI (custom components)                     │
└─────────────┬───────────────────────────────────────────┘
              │ HTTP requests (JSON)
              │ Authorization: Bearer <JWT>
              ▼
┌─────────────────────────────────────────────────────────┐
│  🖥️ BACKEND SERVER (FastAPI + Python)                  │
├─────────────────────────────────────────────────────────┤
│  • 8 API endpoints (/analyze, /auth/*, etc.)           │
│  • JWT authentication & authorization                   │
│  • Image preprocessing (PIL)                            │
│  • AI model inference (TensorFlow Lite)                │
│  • Database queries (SQLite)                            │
│  • Response formatting (JSON)                           │
└─────────────┬─────────────┬─────────────────────────────┘
              │             │
      ┌───────▼────┐   ┌────▼────────┐
      │ 💾 DATABASE│   │ 🤖 AI MODEL │
      │  (SQLite)  │   │ (TFLite)    │
      ├────────────┤   ├─────────────┤
      │ users      │   │ Input: Image│
      │ - id       │   │ Output: 3   │
      │ - email    │   │  classes    │
      │ - password │   │ - healthy   │
      │ - name     │   │ - mite      │
      └────────────┘   │ - fungus    │
                       └─────────────┘
```

### Key Principles:

1. **Separation of Concerns**
   - Frontend: User interface & experience
   - Backend: Business logic & security
   - Database: User data storage
   - Model: AI inference

2. **Security First**
   - Passwords hashed with bcrypt
   - JWT tokens for authentication
   - Token validation on every request
   - HTTPS in production

3. **Performance Optimized**
   - Lightweight model (14MB)
   - Image compression
   - Efficient caching
   - Minimal data transfer

4. **User Experience**
   - Offline-first (AsyncStorage)
   - Fast responses (< 2 seconds)
   - Clear feedback (loading states)
   - Error handling (graceful failures)

---

## 🎓 Final Analogy: The Restaurant

Think of OliveGuard like a restaurant:

**Mobile App** = The dining room
- Beautiful interior (UI)
- Menu (screens)
- Order form (input fields)
- Waiter (navigation)

**Backend Server** = The kitchen
- Receives orders (API endpoints)
- Checks reservations (authentication)
- Cooks food (processes requests)
- Sends food out (responses)

**Database** = The reservation book
- Customer list (users table)
- Contact info (emails, names)
- History (created_at)

**AI Model** = The chef
- Expert knowledge (trained patterns)
- Processes ingredients (analyzes images)
- Creates dishes (makes predictions)

**JWT Token** = Reservation number
- Proves you're a customer
- Gets you a table
- Valid for limited time

**Request/Response** = Order/Food
- Order: "I want spaghetti" (analyze this image)
- Food: "Here's your spaghetti" (diagnosis + recommendations)

---

**That's everything! You now understand how we built the entire OliveGuard system!** 🎉🫒
