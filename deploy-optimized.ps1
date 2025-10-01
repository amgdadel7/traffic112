# Optimized deployment script for Cloud Run (PowerShell)
Write-Host "🚀 Deploying Traffic Light Detection API to Cloud Run (Optimized)..." -ForegroundColor Green

# Set your project ID
$PROJECT_ID = "your-project-id"  # Replace with your actual project ID
$SERVICE_NAME = "traffic-light-detection"
$REGION = "us-central1"

# Model will be downloaded during Docker build
Write-Host "✅ Using optimized Dockerfile with model download during build" -ForegroundColor Green

# Build Docker image using optimized Dockerfile
Write-Host "🔨 Building optimized Docker image..." -ForegroundColor Yellow
docker build -f Dockerfile.optimized -t gcr.io/$PROJECT_ID/$SERVICE_NAME .

# Push to Google Container Registry
Write-Host "📤 Pushing image to GCR..." -ForegroundColor Yellow
docker push gcr.io/$PROJECT_ID/$SERVICE_NAME

# Deploy to Cloud Run
Write-Host "☁️ Deploying to Cloud Run..." -ForegroundColor Yellow
gcloud run deploy $SERVICE_NAME `
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME `
  --platform managed `
  --region $REGION `
  --allow-unauthenticated `
  --port 8080 `
  --timeout 900 `
  --memory 4Gi `
  --cpu 2 `
  --max-instances 10 `
  --set-env-vars TF_CPP_MIN_LOG_LEVEL=2,OMP_NUM_THREADS=1,PYTHONUNBUFFERED=1

Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host "🌐 Service URL:" -ForegroundColor Cyan
gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)'

Write-Host ""
Write-Host "🔍 Check service status:" -ForegroundColor Cyan
Write-Host "curl \$(gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)')/health"