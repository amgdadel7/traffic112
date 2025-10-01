#!/bin/bash

echo "🚀 Building and testing Traffic Light Detection API Docker container..."

# Build the Docker image
echo "📦 Building Docker image..."
docker build -t traffic-light-detection .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
else
    echo "❌ Docker build failed!"
    exit 1
fi

# Run the container
echo "🐳 Starting Docker container..."
docker run -d \
  --name traffic-light-test \
  -p 8080:8080 \
  -v "$(pwd)/test_images:/app/test_images:ro" \
  -v "$(pwd)/output_images:/app/output_images" \
  traffic-light-detection

if [ $? -eq 0 ]; then
    echo "✅ Docker container started successfully!"
else
    echo "❌ Failed to start Docker container!"
    exit 1
fi

# Wait for the container to start
echo "⏳ Waiting for container to start..."
sleep 10

# Check container logs
echo "📋 Container logs:"
docker logs traffic-light-test

# Test the API
echo "🧪 Testing API..."
sleep 30  # Give more time for model loading

# Test health endpoint
echo "Testing health endpoint..."
curl -f http://localhost:8080/health || echo "Health check failed"

# Test model status
echo "Testing model status..."
curl -f http://localhost:8080/model-status || echo "Model status check failed"

# Test detection with a sample image
echo "Testing detection endpoint..."
if [ -f "test_images/img_1.jpg" ]; then
    curl -X POST \
      -F "file=@test_images/img_1.jpg" \
      http://localhost:8080/detect || echo "Detection test failed"
else
    echo "No test image found, skipping detection test"
fi

# Show container status
echo "📊 Container status:"
docker ps | grep traffic-light-test

echo "🎉 Testing completed!"
echo "To stop the container: docker stop traffic-light-test"
echo "To remove the container: docker rm traffic-light-test"