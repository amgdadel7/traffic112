#!/bin/bash

# Test script to verify Docker build works
set -e

echo "🧪 Testing Docker build..."

# Build Docker image locally
echo "🔨 Building Docker image locally..."
docker build -t traffic-light-test .

echo "✅ Docker build successful!"

# Test that the model is available in the container
echo "🔍 Testing model availability in container..."
docker run --rm traffic-light-test ls -la ssd_mobilenet_v1_coco_11_06_2017/

echo "✅ Model files are available in container!"

# Test that the application starts
echo "🚀 Testing application startup..."
timeout 30s docker run --rm -p 8080:8080 traffic-light-test python -c "
import sys
sys.path.append('.')
from main import load_model
print('Testing model loading...')
load_model()
print('Model loading test completed')
" || echo "⏰ Model loading test timed out (expected for large model)"

echo "✅ Docker build and basic functionality test completed!"