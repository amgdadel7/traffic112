#!/bin/bash
# Build script for Render deployment

echo "Starting build process..."

# Upgrade pip and setuptools first
echo "Upgrading pip and setuptools..."
pip install --upgrade pip setuptools wheel

# Install build dependencies
echo "Installing build dependencies..."
pip install --upgrade setuptools wheel

# Install requirements with specific order for Python 3.7.17
echo "Installing core dependencies..."
pip install numpy==1.19.5
pip install Pillow==8.4.0
pip install protobuf==3.20.3

echo "Installing ML libraries..."
pip install opencv-python==4.5.5.64
pip install scikit-learn==1.0.2
pip install scipy==1.7.3
pip install pandas==1.3.5

echo "Installing TensorFlow..."
pip install tensorflow==2.8.4

echo "Installing visualization libraries..."
pip install matplotlib==3.5.3
pip install seaborn==0.11.2
pip install imageio==2.19.5

echo "Installing FastAPI and web dependencies..."
pip install fastapi==0.68.2
pip install uvicorn[standard]==0.15.0
pip install python-multipart==0.0.5
pip install pydantic==1.8.2
pip install aiofiles==0.8.0

echo "Installing additional dependencies..."
pip install gunicorn==20.1.0

echo "Build completed successfully!"