# اختبار Traffic Light Detection API

## 🔗 رابط الـ API
**URL**: https://traffic112.onrender.com

## 📋 Endpoints المتاحة

### 1. فحص الصحة
```bash
curl https://traffic112.onrender.com/health
```

### 2. الحالة التفصيلية
```bash
curl https://traffic112.onrender.com/status
```

### 3. حالة النموذج
```bash
curl https://traffic112.onrender.com/model-status
```

### 4. كشف إشارة المرور (رفع ملف) ⭐
```bash
curl -X POST \
  'https://traffic112.onrender.com/detect' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@image.jpg'
```

### 5. كشف إشارة المرور (Base64)
```bash
curl -X POST \
  'https://traffic112.onrender.com/detect-base64' \
  -H 'Content-Type: application/json' \
  -d '{
    "image_base64": "base64_string_here",
    "image_format": "jpeg"
  }'
```

### 6. كشف إشارة المرور (URL)
```bash
curl -X POST \
  'https://traffic112.onrender.com/detect-url' \
  -H 'Content-Type: application/json' \
  -d '"https://example.com/image.jpg"'
```

## 🧪 أمثلة الاختبار

### مثال 1: رفع صورة محلية
```bash
# تأكد من أن الملف موجود في نفس المجلد
curl -X POST \
  'https://traffic112.onrender.com/detect' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@your_image.jpg'
```

### مثال 2: مع verbose لرؤية التفاصيل
```bash
curl -v -X POST \
  'https://traffic112.onrender.com/detect' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@your_image.jpg'
```

### مثال 3: حفظ الاستجابة في ملف
```bash
curl -X POST \
  'https://traffic112.onrender.com/detect' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@your_image.jpg' \
  -o response.json
```

## 📊 استجابة متوقعة

### نجاح:
```json
{
  "command": "Stop",
  "confidence": 0.95,
  "traffic_light_detected": true,
  "message": "Traffic light detected: Stop command"
}
```

أو:
```json
{
  "command": "Go",
  "confidence": 0.87,
  "traffic_light_detected": false,
  "message": "Traffic light detected: Go command"
}
```

### خطأ (نموذج غير محمّل):
```json
{
  "detail": "Model not loaded yet. Error: ..."
}
```

### خطأ (صورة غير صالحة):
```json
{
  "detail": "Error processing image: ..."
}
```

## 🌐 استخدام المتصفح

### الوثائق التفاعلية (Swagger UI):
```
https://traffic112.onrender.com/docs
```

### الوثائق البديلة (ReDoc):
```
https://traffic112.onrender.com/redoc
```

## 🐍 استخدام Python

```python
import requests

# رفع صورة
with open('image.jpg', 'rb') as f:
    response = requests.post(
        'https://traffic112.onrender.com/detect',
        files={'file': f}
    )
    print(response.json())
```

## 🔧 حل المشاكل

### خطأ: "file not found"
- تأكد من أن الملف موجود في نفس المجلد
- استخدم المسار الكامل: `-F 'file=@/full/path/to/image.jpg'`

### خطأ: "Connection refused" أو "Timeout"
- تحقق من أن الخدمة تعمل على Render
- قد تستغرق الخدمة وقتاً للاستيقاظ (cold start)

### خطأ: "Model not loaded"
- انتظر قليلاً (النموذج قد يكون ما زال يحمّل)
- تحقق من `/model-status` endpoint

## ✅ التحقق السريع

```bash
# 1. فحص الصحة
curl https://traffic112.onrender.com/health

# 2. فحص حالة النموذج
curl https://traffic112.onrender.com/model-status

# 3. اختبار الكشف
curl -X POST \
  'https://traffic112.onrender.com/detect' \
  -H 'accept: application/json' \
  -F 'file=@test_image.jpg'
```

