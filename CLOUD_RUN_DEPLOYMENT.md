# 🚦 Traffic Light Detection - Cloud Run Deployment Guide

This guide will help you deploy the Traffic Light Detection API to Google Cloud Run using Python 3.7.17.

## 📋 Prerequisites

1. **Google Cloud Account**: You need a Google Cloud account with billing enabled
2. **Google Cloud SDK**: Install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
3. **Docker**: Install [Docker](https://docs.docker.com/get-docker/) (optional, for local testing)

## 🚀 Quick Deployment

### Method 1: Using the Deployment Script (Recommended)

1. **Set your project ID**:
   ```bash
   export PROJECT_ID=your-actual-project-id
   ```

2. **Run the deployment script**:
   ```bash
   ./deploy.sh
   ```

### Method 2: Manual Deployment

1. **Set your project ID**:
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   ```

2. **Enable required APIs**:
   ```bash
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable run.googleapis.com
   gcloud services enable containerregistry.googleapis.com
   ```

3. **Build and deploy**:
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/traffic-light-detection
   gcloud run deploy traffic-light-detection \
     --image gcr.io/YOUR_PROJECT_ID/traffic-light-detection \
     --region us-central1 \
     --platform managed \
     --allow-unauthenticated \
     --memory 2Gi \
     --cpu 2 \
     --timeout 900 \
     --concurrency 10 \
     --max-instances 10
   ```

## 🔧 Configuration Details

### Cloud Run Service Configuration

- **Memory**: 2GB (required for TensorFlow model)
- **CPU**: 2 vCPUs
- **Timeout**: 15 minutes (900 seconds)
- **Concurrency**: 10 requests per instance
- **Max Instances**: 10
- **Region**: us-central1 (can be changed)

### Environment Variables

The application uses these environment variables:
- `PORT`: 8080 (default)
- `PYTHONUNBUFFERED`: 1 (for proper logging)

## 🌐 Accessing Your Application

After deployment, you'll get a URL like:
```
https://traffic-light-detection-xxxxx-uc.a.run.app
```

### Available Endpoints

- **Root**: `GET /` - Service information
- **Health Check**: `GET /health` - Health status
- **API Documentation**: `GET /docs` - Interactive API docs
- **Web Interface**: `GET /static/index.html` - Web UI
- **File Upload**: `POST /detect` - Upload image file
- **Base64 Upload**: `POST /detect-base64` - Send base64 image
- **URL Detection**: `POST /detect-url` - Detect from image URL

## 🧪 Testing the Deployment

### 1. Health Check
```bash
curl https://your-service-url/health
```

### 2. Upload Image
```bash
curl -X POST "https://your-service-url/detect" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test_images/img_1.jpg"
```

### 3. Base64 Image
```bash
curl -X POST "https://your-service-url/detect-base64" \
  -H "Content-Type: application/json" \
  -d '{"image_base64": "your_base64_string", "image_format": "jpeg"}'
```

## 📊 Monitoring and Logs

### View Logs
```bash
gcloud logs read --service=traffic-light-detection --limit=50
```

### Monitor Performance
- Go to [Google Cloud Console](https://console.cloud.google.com)
- Navigate to Cloud Run
- Select your service
- View metrics and logs

## 🔄 Updating the Service

To update your service with new code:

1. **Make your changes** to the code
2. **Run the deployment script again**:
   ```bash
   ./deploy.sh
   ```

Or manually:
```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/traffic-light-detection
gcloud run deploy traffic-light-detection --image gcr.io/YOUR_PROJECT_ID/traffic-light-detection
```

## 🛠️ Troubleshooting

### Common Issues

1. **Model Loading Timeout**:
   - The first request might take longer due to model download
   - Consider using a warm-up request

2. **Memory Issues**:
   - Ensure you're using at least 2GB memory
   - Monitor memory usage in Cloud Console

3. **Cold Start**:
   - First request after inactivity takes longer
   - Consider setting minimum instances to 1

### Debug Commands

```bash
# Check service status
gcloud run services describe traffic-light-detection --region=us-central1

# View recent logs
gcloud logs read --service=traffic-light-detection --limit=100

# Check build logs
gcloud builds list --limit=5
```

## 💰 Cost Optimization

- **Set minimum instances to 0** to avoid idle costs
- **Use appropriate memory allocation** (2GB is minimum for this app)
- **Monitor usage** and adjust max instances as needed

## 🔒 Security Considerations

- The service is currently set to allow unauthenticated access
- For production, consider adding authentication
- Use HTTPS (enabled by default on Cloud Run)
- Consider using Cloud Armor for DDoS protection

## 📈 Scaling

Cloud Run automatically scales based on traffic:
- **0 to 10 instances** (as configured)
- **Scales to zero** when no traffic
- **Handles up to 10 concurrent requests** per instance

## 🆘 Support

If you encounter issues:
1. Check the logs using `gcloud logs read`
2. Verify your project has billing enabled
3. Ensure all required APIs are enabled
4. Check the Cloud Run service status in the console