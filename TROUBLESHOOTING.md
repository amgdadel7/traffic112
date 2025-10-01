# Troubleshooting Render Deployment

## Python 3.12 Compatibility Issues

If you're getting the `pkgutil.ImpImporter` error, this is due to Python 3.12 compatibility issues. Here are the solutions:

### Solution 1: Use the Build Script (Recommended)

1. **Use the build script approach:**
   - The `render.yaml` is configured to use `build.sh`
   - This installs packages in the correct order
   - Handles Python 3.12 compatibility issues

2. **Deploy with:**
   ```bash
   git add .
   git commit -m "Fix Python 3.12 compatibility"
   git push origin main
   ```

### Solution 2: Use Minimal Requirements

If the build script doesn't work, try the minimal requirements:

1. **Rename files:**
   ```bash
   mv render.yaml render-complex.yaml
   mv render-simple.yaml render.yaml
   ```

2. **Deploy again**

### Solution 3: Manual Package Installation

If both approaches fail, try this step-by-step approach:

1. **Update render.yaml:**
   ```yaml
   buildCommand: |
     pip install --upgrade pip setuptools wheel
     pip install numpy==1.24.4
     pip install Pillow==10.0.1
     pip install protobuf==4.24.4
     pip install opencv-python==4.8.1.78
     pip install scikit-learn==1.3.2
     pip install scipy==1.11.4
     pip install pandas==2.0.3
     pip install tensorflow==2.13.0
     pip install matplotlib==3.7.2
     pip install seaborn==0.12.2
     pip install imageio==2.31.6
     pip install fastapi==0.104.1
     pip install uvicorn[standard]==0.24.0
     pip install python-multipart==0.0.6
     pip install pydantic==2.5.0
     pip install aiofiles==23.2.1
   ```

### Solution 4: Use Python 3.11

If all else fails, you can specify Python 3.11 in your render.yaml:

```yaml
services:
  - type: web
    name: traffic-light-detection
    env: python
    plan: starter
    buildCommand: pip install --upgrade pip setuptools wheel && pip install -r requirements.txt
    startCommand: python main.py
    envVars:
      - key: PORT
        value: 10000
      - key: PYTHONPATH
        value: /opt/render/project/src
      - key: PYTHONUNBUFFERED
        value: 1
      - key: PYTHON_VERSION
        value: 3.11
    healthCheckPath: /health
```

## Common Build Errors

### 1. Memory Issues
- **Error:** Out of memory during build
- **Solution:** Upgrade to a higher Render plan (Professional or higher)

### 2. TensorFlow Installation Issues
- **Error:** TensorFlow fails to install
- **Solution:** Use the build script which installs TensorFlow after other dependencies

### 3. OpenCV Issues
- **Error:** OpenCV compilation fails
- **Solution:** Use the pre-compiled wheel: `opencv-python==4.8.1.78`

### 4. Model Download Issues
- **Error:** Model fails to download during startup
- **Solution:** The model will download on first request, not during build

## Testing Locally

Before deploying, test locally:

```bash
# Install dependencies
pip install -r requirements-minimal.txt

# Test the API
python main.py

# In another terminal
python test_api.py
```

## Render Logs

Check Render logs for detailed error messages:
1. Go to your Render dashboard
2. Click on your service
3. Go to "Logs" tab
4. Look for build errors or runtime errors

## Alternative Deployment Options

If Render continues to have issues:

1. **Heroku:** Similar to Render, good for Python apps
2. **Railway:** Modern alternative with better Python 3.12 support
3. **Google Cloud Run:** More complex but very reliable
4. **AWS Lambda:** Serverless option (requires code changes)

## Getting Help

If you're still having issues:
1. Check the Render documentation
2. Look at the specific error in the logs
3. Try the minimal requirements approach
4. Consider using Python 3.11 instead of 3.12