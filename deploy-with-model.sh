#!/bin/bash

# Deploy script for Cloud Run with model included in Docker image
set -e

echo "🚀 Deploying Traffic Light Detection API to Cloud Run with model included..."

# Set your project ID
PROJECT_ID="your-project-id"  # Replace with your actual project ID
SERVICE_NAME="traffic-light-detection"
REGION="us-central1"

# Model will be downloaded during Docker build
echo "✅ Model will be downloaded during Docker build process"

# Build Docker image
echo "🔨 Building Docker image..."
docker build -t gcr.io/$PROJECT_ID/$SERVICE_NAME .

# Push to Google Container Registry
echo "📤 Pushing image to GCR..."
docker push gcr.io/$PROJECT_ID/$SERVICE_NAME

# Deploy to Cloud Run
echo "☁️ Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8080 \
  --timeout 900 \
  --memory 4Gi \
  --cpu 2 \
  --max-instances 10 \
  --set-env-vars TF_CPP_MIN_LOG_LEVEL=2,OMP_NUM_THREADS=1,PYTHONUNBUFFERED=1

echo "✅ Deployment complete!"
echo "🌐 Service URL:"
gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)'

echo ""
echo "🔍 Check service status:"
echo "curl \$(gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)')/health"