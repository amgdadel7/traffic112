#!/usr/bin/env python3
"""
Test script specifically for base64 functionality
"""
import requests
import base64
from PIL import Image
import io

def create_test_image_base64():
    """Create a simple test image and convert to base64"""
    # Create a red image (should trigger Stop command)
    img = Image.new('RGB', (100, 100), color='red')
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    base64_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return base64_data

def test_base64_detection(base_url="http://localhost:8080"):
    """Test base64 detection endpoint"""
    
    print(f"Testing base64 detection at {base_url}")
    
    # Create test image
    base64_data = create_test_image_base64()
    print(f"Created test image (base64 length: {len(base64_data)})")
    
    # Test 1: Basic base64 detection
    try:
        data = {
            "image_base64": base64_data,
            "image_format": "jpeg"
        }
        response = requests.post(f"{base_url}/detect-base64", json=data)
        print(f"✓ Basic base64 detection: {response.status_code}")
        print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"✗ Basic base64 detection failed: {e}")
    
    # Test 2: Data URL format
    try:
        data_url = f"data:image/jpeg;base64,{base64_data}"
        data = {
            "image_base64": data_url,
            "image_format": "jpeg"
        }
        response = requests.post(f"{base_url}/detect-base64", json=data)
        print(f"✓ Data URL base64 detection: {response.status_code}")
        print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"✗ Data URL base64 detection failed: {e}")
    
    # Test 3: PNG format
    try:
        # Create PNG image
        img = Image.new('RGB', (50, 50), color='yellow')
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        png_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        data = {
            "image_base64": png_base64,
            "image_format": "png"
        }
        response = requests.post(f"{base_url}/detect-base64", json=data)
        print(f"✓ PNG base64 detection: {response.status_code}")
        print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"✗ PNG base64 detection failed: {e}")

if __name__ == "__main__":
    test_base64_detection()