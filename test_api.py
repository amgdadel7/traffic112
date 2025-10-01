#!/usr/bin/env python3
"""
Simple test script for the Traffic Light Detection API
"""
import requests
import json
import os
import base64
from PIL import Image
import numpy as np

def test_api_endpoints(base_url="http://localhost:8080"):
    """Test the API endpoints"""
    
    print(f"Testing API at {base_url}")
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/")
        print(f"✓ Root endpoint: {response.status_code}")
        print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"✗ Root endpoint failed: {e}")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✓ Health endpoint: {response.status_code}")
        print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"✗ Health endpoint failed: {e}")
    
    # Test with a sample image (if available)
    test_image_path = "test_images/img_1.jpg"
    if os.path.exists(test_image_path):
        try:
            with open(test_image_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(f"{base_url}/detect", files=files)
                print(f"✓ Image detection: {response.status_code}")
                print(f"  Response: {response.json()}")
        except Exception as e:
            print(f"✗ Image detection failed: {e}")
    else:
        print("⚠ No test image found, skipping image detection test")
    
    # Test URL detection
    try:
        test_url = "https://via.placeholder.com/300x200/ff0000/ffffff?text=Test+Image"
        data = {"image_url": test_url}
        response = requests.post(f"{base_url}/detect-url", json=data)
        print(f"✓ URL detection: {response.status_code}")
        print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"✗ URL detection failed: {e}")
    
    # Test base64 detection
    try:
        # Create a simple test image
        test_image = Image.new('RGB', (100, 100), color='red')
        buffer = io.BytesIO()
        test_image.save(buffer, format='JPEG')
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        data = {
            "image_base64": image_base64,
            "image_format": "jpeg"
        }
        response = requests.post(f"{base_url}/detect-base64", json=data)
        print(f"✓ Base64 detection: {response.status_code}")
        print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"✗ Base64 detection failed: {e}")

if __name__ == "__main__":
    # Test local API
    test_api_endpoints("http://localhost:8080")
    
    print("\n" + "="*50)
    print("To test with a deployed API, run:")
    print("python test_api.py https://your-app-name.onrender.com")