# PowerShell script to build and test Docker container

Write-Host "🚀 Building and testing Traffic Light Detection API Docker container..." -ForegroundColor Green

# Build the Docker image
Write-Host "📦 Building Docker image..." -ForegroundColor Yellow
docker build -t traffic-light-detection .

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Docker image built successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Docker build failed!" -ForegroundColor Red
    exit 1
}

# Stop and remove existing container if it exists
Write-Host "🧹 Cleaning up existing container..." -ForegroundColor Yellow
docker stop traffic-light-test 2>$null
docker rm traffic-light-test 2>$null

# Run the container
Write-Host "🐳 Starting Docker container..." -ForegroundColor Yellow
docker run -d `
  --name traffic-light-test `
  -p 8080:8080 `
  -v "${PWD}/test_images:/app/test_images:ro" `
  -v "${PWD}/output_images:/app/output_images" `
  traffic-light-detection

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Docker container started successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to start Docker container!" -ForegroundColor Red
    exit 1
}

# Wait for the container to start
Write-Host "⏳ Waiting for container to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check container logs
Write-Host "📋 Container logs:" -ForegroundColor Cyan
docker logs traffic-light-test

# Test the API
Write-Host "🧪 Testing API..." -ForegroundColor Yellow
Start-Sleep -Seconds 30  # Give more time for model loading

# Test health endpoint
Write-Host "Testing health endpoint..." -ForegroundColor Cyan
try {
    $healthResponse = Invoke-WebRequest -Uri "http://localhost:8080/health" -Method GET
    Write-Host "Health check response: $($healthResponse.Content)" -ForegroundColor Green
} catch {
    Write-Host "Health check failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test model status
Write-Host "Testing model status..." -ForegroundColor Cyan
try {
    $modelStatusResponse = Invoke-WebRequest -Uri "http://localhost:8080/model-status" -Method GET
    Write-Host "Model status response: $($modelStatusResponse.Content)" -ForegroundColor Green
} catch {
    Write-Host "Model status check failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test detection with a sample image
Write-Host "Testing detection endpoint..." -ForegroundColor Cyan
if (Test-Path "test_images/img_1.jpg") {
    try {
        $imagePath = "test_images/img_1.jpg"
        $imageBytes = [System.IO.File]::ReadAllBytes($imagePath)
        $boundary = [System.Guid]::NewGuid().ToString()
        $LF = "`r`n"
        $bodyLines = (
            "--$boundary",
            "Content-Disposition: form-data; name=`"file`"; filename=`"img_1.jpg`"",
            "Content-Type: image/jpeg",
            "",
            [System.Text.Encoding]::GetEncoding("iso-8859-1").GetString($imageBytes),
            "--$boundary--",
            ""
        ) -join $LF
        
        $detectionResponse = Invoke-WebRequest -Uri "http://localhost:8080/detect" -Method POST -ContentType "multipart/form-data; boundary=$boundary" -Body $bodyLines
        Write-Host "Detection response: $($detectionResponse.Content)" -ForegroundColor Green
    } catch {
        Write-Host "Detection test failed: $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "No test image found, skipping detection test" -ForegroundColor Yellow
}

# Show container status
Write-Host "📊 Container status:" -ForegroundColor Cyan
docker ps | Select-String "traffic-light-test"

Write-Host "🎉 Testing completed!" -ForegroundColor Green
Write-Host "To stop the container: docker stop traffic-light-test" -ForegroundColor Yellow
Write-Host "To remove the container: docker rm traffic-light-test" -ForegroundColor Yellow