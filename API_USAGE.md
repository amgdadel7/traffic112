# Traffic Light Detection API - Usage Guide

## API Endpoints

### 1. Health Check
```bash
GET /
GET /health
```

### 2. File Upload Detection
```bash
POST /detect
Content-Type: multipart/form-data
Body: file (image file)
```

### 3. Base64 Image Detection
```bash
POST /detect-base64
Content-Type: application/json
Body: {
    "image_base64": "base64_encoded_string",
    "image_format": "jpeg"  // optional, defaults to "jpeg"
}
```

### 4. URL Image Detection
```bash
POST /detect-url
Content-Type: application/json
Body: {
    "image_url": "https://example.com/image.jpg"
}
```

## Base64 Usage Examples

### Python Example
```python
import requests
import base64
from PIL import Image
import io

# Method 1: From file
def detect_from_file(file_path):
    with open(file_path, 'rb') as f:
        image_data = f.read()
        base64_data = base64.b64encode(image_data).decode('utf-8')
    
    response = requests.post('http://localhost:8080/detect-base64', json={
        'image_base64': base64_data,
        'image_format': 'jpeg'
    })
    return response.json()

# Method 2: From PIL Image
def detect_from_pil_image(pil_image):
    buffer = io.BytesIO()
    pil_image.save(buffer, format='JPEG')
    base64_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    response = requests.post('http://localhost:8080/detect-base64', json={
        'image_base64': base64_data,
        'image_format': 'jpeg'
    })
    return response.json()

# Method 3: With data URL prefix
def detect_with_data_url(base64_string):
    # base64_string can be: "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."
    response = requests.post('http://localhost:8080/detect-base64', json={
        'image_base64': base64_string,
        'image_format': 'jpeg'
    })
    return response.json()
```

### JavaScript Example
```javascript
// Convert file to base64
function fileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(error);
    });
}

// Detect traffic light
async function detectTrafficLight(file) {
    const base64Data = await fileToBase64(file);
    
    const response = await fetch('/detect-base64', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            image_base64: base64Data,
            image_format: 'jpeg'
        })
    });
    
    return await response.json();
}
```

### cURL Examples
```bash
# Base64 detection
curl -X POST "http://localhost:8080/detect-base64" \
  -H "Content-Type: application/json" \
  -d '{
    "image_base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
    "image_format": "png"
  }'

# File upload
curl -X POST "http://localhost:8080/detect" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@image.jpg"

# URL detection
curl -X POST "http://localhost:8080/detect-url" \
  -H "Content-Type: application/json" \
  -d '{"image_url": "https://example.com/image.jpg"}'
```

## Response Format

All endpoints return the same response format:

```json
{
    "command": "Stop" | "Go",
    "confidence": 0.95,
    "traffic_light_detected": true,
    "message": "Traffic light detected: Stop command"
}
```

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff)
- WebP (.webp)

## Error Handling

The API returns appropriate HTTP status codes:

- `200`: Success
- `400`: Bad Request (invalid image data)
- `503`: Service Unavailable (model not loaded)

Error response format:
```json
{
    "detail": "Error message describing what went wrong"
}
```

## Web Interface

Visit `/static/index.html` for a user-friendly web interface that supports:
- Drag & drop file upload
- URL-based detection
- Base64 paste functionality
- Real-time results display

## Performance Notes

- Model loading takes time on first startup
- Use the `/health` endpoint to check if the model is ready
- Base64 images are processed in memory, so very large images may cause memory issues
- Consider resizing images before sending for better performance