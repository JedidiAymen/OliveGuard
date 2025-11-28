#!/usr/bin/env python3
"""
Simple test script to verify the inference server and model.
Run this after starting the server with: uvicorn server:app --reload
"""

import requests
import sys
from pathlib import Path

def test_health():
    """Test the /health endpoint"""
    try:
        response = requests.get('http://localhost:8000/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Health check passed: {data}")
            return True
        else:
            print(f"✗ Health check failed with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server. Is it running on port 8000?")
        return False
    except Exception as e:
        print(f"✗ Health check error: {e}")
        return False


def test_analyze(model_type='mobilenet'):
    """Test the /analyze endpoint with a dummy image"""
    from PIL import Image
    import io
    
    # Create a test image
    img = Image.new('RGB', (224, 224), color='green')
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    buf.seek(0)
    
    try:
        files = {'image': ('test.jpg', buf, 'image/jpeg')}
        response = requests.post(
            f'http://localhost:8000/analyze?model_type={model_type}', 
            files=files, 
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Analysis successful ({model_type}):")
            print(f"  - Diagnosis: {data.get('diagnosis')}")
            print(f"  - Confidence: {data.get('confidenceScore')}%")
            print(f"  - Disease Type: {data.get('diseaseType')}")
            print(f"  - Model Used: {data.get('modelUsed')}")
            return True
        else:
            print(f"✗ Analysis failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Analysis error: {e}")
        return False


def test_models_list():
    """Test the /models endpoint"""
    try:
        response = requests.get('http://localhost:8000/models', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Models list retrieved:")
            for model in data.get('models', []):
                print(f"  - {model['name']}: {model['description']} ({model['size']})")
            return True
        else:
            print(f"✗ Models list failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Models list error: {e}")
        return False


if __name__ == '__main__':
    print("Testing Inference Server - Dual Model Support\n")
    print("=" * 60)
    
    health_ok = test_health()
    print()
    
    models_ok = test_models_list()
    print()
    
    mobilenet_ok = False
    efficientnet_ok = False
    
    if health_ok:
        print("Testing MobileNetV3...")
        mobilenet_ok = test_analyze('mobilenet')
        print()
        
        print("Testing EfficientNet-Lite0...")
        efficientnet_ok = test_analyze('efficientnet')
    else:
        print("Skipping analysis tests due to health check failure")
    
    print()
    print("=" * 60)
    print("Test Summary:")
    print(f"  Health Check:     {'✓' if health_ok else '✗'}")
    print(f"  Models List:      {'✓' if models_ok else '✗'}")
    print(f"  MobileNetV3:      {'✓' if mobilenet_ok else '✗'}")
    print(f"  EfficientNet:     {'✓' if efficientnet_ok else '✗'}")
    print("=" * 60)
    
    if health_ok and models_ok and (mobilenet_ok or efficientnet_ok):
        print("✓ Server is functional!")
        sys.exit(0)
    else:
        print("✗ Some tests failed")
        sys.exit(1)
