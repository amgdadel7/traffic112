# 🌐 Google Cloud Console Deployment Guide

Since you don't have Google Cloud SDK installed, you can deploy using the Google Cloud Console web interface.

## 📋 Prerequisites

1. **Google Cloud Account** with billing enabled
2. **Google Cloud Project** created
3. **Docker** installed on your local machine (optional)

## 🚀 Method 1: Using Cloud Shell (Recommended)

### Step 1: Open Cloud Shell
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click the Cloud Shell icon (terminal icon) in the top right
3. Wait for Cloud Shell to initialize

### Step 2: Upload Your Code
1. In Cloud Shell, click the "Upload" button (folder with up arrow)
2. Select all your project files and upload them
3. Or clone from GitHub if you've pushed your code there

### Step 3: Deploy to Cloud Run
```bash
# Set your project ID
export PROJECT_ID=your-actual-project-id
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build and deploy
gcloud builds submit --tag gcr.io/$PROJECT_ID/traffic-light-detection
gcloud run deploy traffic-light-detection \
  --image gcr.io/$PROJECT_ID/traffic-light-detection \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 900 \
  --concurrency 10 \
  --max-instances 10
```

## 🚀 Method 2: Using Cloud Build (Web Interface)

### Step 1: Prepare Your Code
1. Create a ZIP file of your project
2. Or push your code to GitHub

### Step 2: Use Cloud Build
1. Go to [Cloud Build](https://console.cloud.google.com/cloud-build)
2. Click "Create Trigger"
3. Connect your repository or upload source code
4. Use the `cloudbuild.yaml` file we created
5. Click "Create" and "Run"

### Step 3: Deploy to Cloud Run
1. Go to [Cloud Run](https://console.cloud.google.com/run)
2. Click "Create Service"
3. Select "Deploy one revision from an existing container image"
4. Choose your built image
5. Configure the service:
   - **Memory**: 2 GiB
   - **CPU**: 2
   - **Timeout**: 900 seconds
   - **Concurrency**: 10
   - **Max instances**: 10
6. Click "Create"

## 🚀 Method 3: Using Docker Desktop + Cloud Run

If you have Docker Desktop installed:

### Step 1: Build Locally
```bash
# Build the Docker image
docker build -t traffic-light-detection .

# Test locally
docker run -p 8080:8080 traffic-light-detection
```

### Step 2: Push to Google Container Registry
```bash
# Tag for GCR
docker tag traffic-light-detection gcr.io/YOUR_PROJECT_ID/traffic-light-detection

# Configure Docker for GCR
gcloud auth configure-docker

# Push the image
docker push gcr.io/YOUR_PROJECT_ID/traffic-light-detection
```

### Step 3: Deploy to Cloud Run
Use the Google Cloud Console to deploy from the pushed image.

## 🔧 Configuration Details

### Required Settings:
- **Memory**: 2 GiB (minimum for TensorFlow)
- **CPU**: 2 vCPUs
- **Timeout**: 900 seconds (15 minutes)
- **Concurrency**: 10 requests per instance
- **Max Instances**: 10
- **Region**: us-central1 (or your preferred region)

### Environment Variables:
- `PYTHONUNBUFFERED=1`

## 🌐 After Deployment

Your service will be available at:
```
https://traffic-light-detection-xxxxx-uc.a.run.app
```

### Test Endpoints:
- **Health Check**: `GET /health`
- **API Docs**: `GET /docs`
- **Web Interface**: `GET /static/index.html`
- **Upload Image**: `POST /detect`

## 🧪 Testing

### Health Check
```bash
curl https://your-service-url/health
```

### Upload Image
```bash
curl -X POST "https://your-service-url/detect" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test_images/img_1.jpg"
```

## 💡 Tips

1. **First Request**: May take longer due to model download
2. **Cold Starts**: Service scales to zero when idle
3. **Monitoring**: Check logs in Cloud Console
4. **Costs**: Only pay when requests are being processed

## 🆘 Troubleshooting

1. **Build Fails**: Check the build logs in Cloud Build
2. **Service Won't Start**: Check Cloud Run logs
3. **Memory Issues**: Ensure 2GB memory is allocated
4. **Timeout**: Increase timeout if model loading takes long