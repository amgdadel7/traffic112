# Test Local Deployment Script
# This script helps you test the application locally before deploying to Cloud Run

Write-Host "🚦 Testing Traffic Light Detection Application Locally" -ForegroundColor Green

# Check if Python is installed
Write-Host "`n📋 Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "❌ Python not found. Please install Python 3.7.17" -ForegroundColor Red
    exit 1
}

# Check if pip is available
Write-Host "`n📋 Checking pip..." -ForegroundColor Yellow
try {
    $pipVersion = pip --version 2>&1
    Write-Host "✅ pip found: $pipVersion" -ForegroundColor Green
}
catch {
    Write-Host "❌ pip not found. Please install pip" -ForegroundColor Red
    exit 1
}

# Install requirements
Write-Host "`n📦 Installing requirements..." -ForegroundColor Yellow
pip install -r requirements.txt

# Check if Docker is available (optional)
Write-Host "`n🐳 Checking Docker (optional)..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version 2>&1
    Write-Host "✅ Docker found: $dockerVersion" -ForegroundColor Green
    $dockerAvailable = $true
}
catch {
    Write-Host "⚠️  Docker not found. You can still test with Python directly" -ForegroundColor Yellow
    $dockerAvailable = $false
}

# Test with Python directly
Write-Host "`n🧪 Testing with Python..." -ForegroundColor Yellow
Write-Host "Starting the application on http://localhost:8080" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Cyan
Write-Host "`n🌐 Once running, you can test:" -ForegroundColor Green
Write-Host "  - Web Interface: http://localhost:8080/static/index.html" -ForegroundColor White
Write-Host "  - API Docs: http://localhost:8080/docs" -ForegroundColor White
Write-Host "  - Health Check: http://localhost:8080/health" -ForegroundColor White

# Start the application
python main.py

# If Docker is available, offer to test with Docker
if ($dockerAvailable) {
    Write-Host "`n🐳 Docker is available. Would you like to test with Docker? (y/n)" -ForegroundColor Yellow
    $response = Read-Host
    if ($response -eq "y" -or $response -eq "Y") {
        Write-Host "`n🏗️  Building Docker image..." -ForegroundColor Yellow
        docker build -t traffic-light-detection .
        
        Write-Host "`n🚀 Running Docker container..." -ForegroundColor Yellow
        Write-Host "Application will be available at http://localhost:8080" -ForegroundColor Cyan
        Write-Host "Press Ctrl+C to stop the container" -ForegroundColor Cyan
        
        docker run -p 8080:8080 traffic-light-detection
    }
}

Write-Host "`n✅ Testing completed!" -ForegroundColor Green
Write-Host "`n📖 Next steps:" -ForegroundColor Yellow
Write-Host "1. Install Google Cloud SDK from: https://cloud.google.com/sdk/docs/install-sdk#windows" -ForegroundColor White
Write-Host "2. Or use Google Cloud Console: https://console.cloud.google.com" -ForegroundColor White
Write-Host "3. Follow the deployment guide in CLOUD_RUN_DEPLOYMENT.md" -ForegroundColor White