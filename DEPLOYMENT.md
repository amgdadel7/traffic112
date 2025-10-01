# Traffic Light Detection API - Render Deployment Guide

This guide will help you deploy the Traffic Light Detection API on Render.

## Prerequisites

1. A Render account (sign up at https://render.com)
2. Your project code in a Git repository (GitHub, GitLab, or Bitbucket)

## Deployment Steps

### 1. Prepare Your Repository

Make sure your repository contains these files:
- `main.py` - The FastAPI application
- `requirements.txt` - Python dependencies
- `render.yaml` - Render configuration
- `mscoco_label_map.pbtxt` - Label map for COCO dataset
- `utils/` directory - Utility functions for object detection
- `static/index.html` - Web interface for testing

### 2. Deploy on Render

1. **Connect Repository:**
   - Log in to your Render dashboard
   - Click "New +" and select "Web Service"
   - Connect your Git repository

2. **Configure Service:**
   - **Name:** traffic-light-detection (or your preferred name)
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python main.py`
   - **Plan:** Starter (free tier) or higher

3. **Environment Variables:**
   - `PORT`: 10000 (Render will set this automatically)
   - `PYTHONPATH`: `/opt/render/project/src` (if needed)

4. **Deploy:**
   - Click "Create Web Service"
   - Render will automatically build and deploy your application

### 3. Using the API

Once deployed, your API will be available at:
- **API Base URL:** `https://your-app-name.onrender.com`
- **Web Interface:** `https://your-app-name.onrender.com/static/index.html`
- **API Documentation:** `https://your-app-name.onrender.com/docs`

#### API Endpoints:

1. **GET /** - Health check and service info
2. **GET /health** - Detailed health status
3. **POST /detect** - Upload image file for detection
4. **POST /detect-url** - Provide image URL for detection

#### Example Usage:

**Upload Image:**
```bash
curl -X POST "https://your-app-name.onrender.com/detect" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your-image.jpg"
```

**Image URL:**
```bash
curl -X POST "https://your-app-name.onrender.com/detect-url" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"image_url": "https://example.com/image.jpg"}'
```

### 4. Model Loading

The application will automatically download the TensorFlow model on first startup. This may take a few minutes during the initial deployment.

**Note:** The model download happens during the build process, so the first request might take longer while the model loads.

### 5. Troubleshooting

**Common Issues:**

1. **Model Loading Errors:**
   - Check the logs in Render dashboard
   - Ensure all dependencies are correctly installed
   - Verify the model download URLs are accessible

2. **Memory Issues:**
   - Consider upgrading to a higher plan if you encounter memory errors
   - The starter plan has limited memory which might not be sufficient for large models

3. **Timeout Issues:**
   - Model loading can take time on first startup
   - Consider implementing a health check that waits for model loading

**Logs:**
- Check the Render dashboard logs for detailed error messages
- Look for any import errors or missing dependencies

### 6. Performance Optimization

1. **Model Size:**
   - The current configuration uses SSD MobileNet (lighter model)
   - For better accuracy, you can switch to Faster R-CNN (requires more memory)

2. **Caching:**
   - Consider implementing model caching to avoid re-downloading
   - Use Redis or similar for caching detection results

3. **Scaling:**
   - Upgrade to higher plans for better performance
   - Consider using Render's auto-scaling features

### 7. Monitoring

- Use Render's built-in monitoring dashboard
- Set up alerts for service health
- Monitor memory and CPU usage
- Track API response times

## Support

For issues specific to this deployment:
1. Check the Render documentation
2. Review the application logs
3. Verify all dependencies are correctly specified
4. Test the API endpoints using the provided web interface

## Cost Considerations

- **Starter Plan:** Free tier with limitations
- **Professional Plan:** $7/month with better performance
- **Enterprise Plan:** Custom pricing for high-traffic applications

Choose the plan based on your expected usage and performance requirements.