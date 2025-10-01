@echo off
REM Traffic Light Detection - Cloud Run Deployment Script for Windows
REM This script deploys the application to Google Cloud Run

setlocal enabledelayedexpansion

REM Configuration
if "%PROJECT_ID%"=="" set PROJECT_ID=your-project-id
set SERVICE_NAME=traffic-light-detection
set REGION=us-central1
set IMAGE_NAME=gcr.io/%PROJECT_ID%/%SERVICE_NAME%

echo 🚦 Deploying Traffic Light Detection to Google Cloud Run
echo Project ID: %PROJECT_ID%
echo Service Name: %SERVICE_NAME%
echo Region: %REGION%
echo Image: %IMAGE_NAME%

REM Check if PROJECT_ID is set
if "%PROJECT_ID%"=="your-project-id" (
    echo ❌ Please set PROJECT_ID environment variable or update the script
    echo    set PROJECT_ID=your-actual-project-id
    exit /b 1
)

REM Set the project
echo 📋 Setting project to %PROJECT_ID%
gcloud config set project %PROJECT_ID%

REM Enable required APIs
echo 🔧 Enabling required APIs...
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

REM Build and push the image
echo 🏗️  Building and pushing Docker image...
gcloud builds submit --tag %IMAGE_NAME%

REM Deploy to Cloud Run
echo 🚀 Deploying to Cloud Run...
gcloud run deploy %SERVICE_NAME% ^
    --image %IMAGE_NAME% ^
    --region %REGION% ^
    --platform managed ^
    --allow-unauthenticated ^
    --memory 2Gi ^
    --cpu 2 ^
    --timeout 900 ^
    --concurrency 10 ^
    --max-instances 10 ^
    --set-env-vars "PYTHONUNBUFFERED=1"

REM Get the service URL
for /f "tokens=*" %%i in ('gcloud run services describe %SERVICE_NAME% --region=%REGION% --format="value(status.url)"') do set SERVICE_URL=%%i

echo ✅ Deployment completed successfully!
echo 🌐 Service URL: %SERVICE_URL%
echo 📖 API Documentation: %SERVICE_URL%/docs
echo 🖥️  Web Interface: %SERVICE_URL%/static/index.html
echo ❤️  Health Check: %SERVICE_URL%/health

pause