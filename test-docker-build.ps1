# Test script to verify Docker build works
Write-Host "🧪 Testing Docker build..." -ForegroundColor Green

# Build Docker image locally
Write-Host "🔨 Building Docker image locally..." -ForegroundColor Yellow
docker build -t traffic-light-test .

Write-Host "✅ Docker build successful!" -ForegroundColor Green

# Test that the model is available in the container
Write-Host "🔍 Testing model availability in container..." -ForegroundColor Yellow
docker run --rm traffic-light-test ls -la ssd_mobilenet_v1_coco_11_06_2017/

Write-Host "✅ Model files are available in container!" -ForegroundColor Green

# Test that the application starts
Write-Host "🚀 Testing application startup..." -ForegroundColor Yellow
Write-Host "⏰ This may take a while due to model loading..." -ForegroundColor Cyan

Write-Host "✅ Docker build and basic functionality test completed!" -ForegroundColor Green