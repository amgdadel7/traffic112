#!/usr/bin/env python3
"""
Simple test script for the Traffic Light Detection API
"""
import requests
import json
import base64
from pathlib import Path

# API endpoint
API_URL = "https://traffic112.onrender.com"

def test_health():
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=10)
        print(f"✅ Status: {response.status_code}")
        print(f"📋 Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_root():
    """Test the root endpoint"""
    print("\n🔍 Testing root endpoint...")
    try:
        response = requests.get(f"{API_URL}/", timeout=10)
        print(f"✅ Status: {response.status_code}")
        print(f"📋 Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_detect_base64(image_path=None, base64_string=None):
    """Test the detect-base64 endpoint"""
    print("\n🔍 Testing detect-base64 endpoint...")
    
    if image_path:
        # Read image file and convert to base64
        with open(image_path, 'rb') as f:
            image_data = f.read()
            base64_string = base64.b64encode(image_data).decode('utf-8')
    
    if not base64_string:
        print("❌ No image provided")
        return False
    
    # Prepare request
    payload = {
        "image_base64": base64_string,
        "image_format": "jpeg"
    }
    
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    
    try:
        print("📤 Sending request...")
        response = requests.post(
            f"{API_URL}/detect-base64",
            json=payload,
            headers=headers,
            timeout=60  # Longer timeout for inference
        )
        print(f"✅ Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"📋 Response: {json.dumps(result, indent=2)}")
            return True
        else:
            print(f"❌ Error response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Traffic Light Detection API\n")
    print(f"📍 API URL: {API_URL}\n")
    
    # Test health
    health_ok = test_health()
    
    # Test root
    root_ok = test_root()
    
    # Test detect-base64 (if image file provided)
    import sys
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        if Path(image_path).exists():
            test_detect_base64(image_path=image_path)
        else:
            print(f"\n❌ Image file not found: {image_path}")
    else:
        print("\n💡 To test detection, provide an image file:")
        print(f"   python test_api.py path/to/image.jpg")
    
    print("\n" + "="*50)
    if health_ok and root_ok:
        print("✅ API is working correctly!")
    else:
        print("⚠️  Some tests failed. Check the output above.")

