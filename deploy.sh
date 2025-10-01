#!/bin/bash
# Deploy script for Google Cloud Run

echo "🚀 Deploying Traffic Light Detection API to Cloud Run..."

# Set variables
PROJECT_ID="traffic-light-2025"
SERVICE_NAME="fastapi-api"
REGION="us-central1"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "📦 Building Docker image..."
docker build -t $IMAGE_NAME .

echo "📤 Pushing image to Container Registry..."
docker push $IMAGE_NAME

echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image $IMAGE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8080 \
  --timeout 300 \
  --memory 2Gi \
  --cpu 1 \
  --max-instances 10 \
  --set-env-vars "PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python,PYTHONUNBUFFERED=1"

echo "✅ Deployment completed!"
echo "🌐 Service URL: https://$SERVICE_NAME-$(gcloud config get-value project).$REGION.run.app"