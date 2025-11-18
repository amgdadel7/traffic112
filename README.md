# Traffic Light Detection API

API لتحديد إشارات المرور وتحديد أوامر Go/Stop باستخدام TensorFlow و FastAPI.

## المميزات

- 🔍 كشف إشارات المرور في الصور
- 🚦 تحديد حالة الإشارة (Go/Stop)
- 📊 تقديم مستوى الثقة للكشف
- 🚀 API سريع باستخدام FastAPI
- ☁️ جاهز للنشر على Render و Cloud Run

## التقنيات المستخدمة

- **FastAPI**: إطار عمل الويب
- **TensorFlow**: نموذج SSD MobileNet V1
- **OpenCV**: معالجة الصور
- **Pillow**: معالجة الصور

## التثبيت

### المتطلبات

- Python 3.7+
- TensorFlow 2.11.0
- FastAPI
- OpenCV

### التثبيت المحلي

```bash
# استنساخ المستودع
git clone https://github.com/amgdadel7/traffic112.git
cd traffic112

# تثبيت المتطلبات
pip install -r requirements.txt

# تشغيل الخادم
python run.py
```

## الاستخدام

### تشغيل الخادم

```bash
python run.py
```

الخادم سيعمل على `http://localhost:8000`

### API Endpoints

#### 1. الصفحة الرئيسية
```
GET /
```

#### 2. فحص الصحة
```
GET /health
```

#### 3. كشف إشارة المرور (رفع ملف)
```
POST /detect
Content-Type: multipart/form-data
Body: file (image file)
```

#### 4. كشف إشارة المرور (Base64)
```
POST /detect-base64
Content-Type: application/json
Body: {
  "image_base64": "base64_string",
  "image_format": "jpeg"
}
```

#### 5. كشف إشارة المرور (URL)
```
POST /detect-url
Body: "https://example.com/image.jpg"
```

#### 6. حالة النموذج
```
GET /model-status
```

### مثال على الاستخدام

#### باستخدام curl

```bash
# رفع صورة
curl -X POST "http://localhost:8000/detect" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@image.jpg"

# استخدام Base64
curl -X POST "http://localhost:8000/detect-base64" \
  -H "Content-Type: application/json" \
  -d '{"image_base64": "base64_string", "image_format": "jpeg"}'
```

#### باستخدام Python

```python
import requests

# رفع صورة
with open('image.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/detect',
        files={'file': f}
    )
    print(response.json())
```

### استجابة API

```json
{
  "command": "Stop",
  "confidence": 0.95,
  "traffic_light_detected": true,
  "message": "Traffic light detected: Stop command"
}
```

## النشر

### النشر على Render

المشروع جاهز للنشر على Render. المستودع مرتبط تلقائياً:

1. اربط المستودع على Render
2. Render سيقوم بالنشر التلقائي عند الرفع إلى GitHub
3. الملف `render.yaml` يحتوي على الإعدادات

### النشر باستخدام Docker

```bash
# بناء الصورة
docker build -t traffic-light-detection .

# تشغيل الحاوية
docker run -p 8000:8000 traffic-light-detection
```

## الملفات المهمة

- `main.py`: الكود الرئيسي للـ API
- `Dockerfile`: إعدادات Docker
- `render.yaml`: إعدادات Render
- `requirements.txt`: المتطلبات
- `ssd_mobilenet_v1_coco_11_06_2017.tar.gz`: نموذج TensorFlow

## النموذج

يستخدم المشروع نموذج **SSD MobileNet V1** المدرب على COCO dataset.

- **النموذج**: ssd_mobilenet_v1_coco_11_06_2017
- **الحجم**: ~122 MB
- **التنزيل**: يتم التنزيل تلقائياً عند أول تشغيل إذا لم يكن موجوداً محلياً

## التطوير

### هيكل المشروع

```
traffic112/
├── main.py                 # الكود الرئيسي
├── run.py                  # سكريبت التشغيل
├── requirements.txt        # المتطلبات
├── Dockerfile             # إعدادات Docker
├── render.yaml            # إعدادات Render
├── utils/                 # أدوات TensorFlow
└── ssd_mobilenet_v1_coco_11_06_2017.tar.gz  # النموذج
```

## المساهمة

1. Fork المشروع
2. أنشئ branch جديد (`git checkout -b feature/AmazingFeature`)
3. Commit التغييرات (`git commit -m 'Add some AmazingFeature'`)
4. Push إلى Branch (`git push origin feature/AmazingFeature`)
5. افتح Pull Request

## الترخيص

هذا المشروع مفتوح المصدر.

## الدعم

للدعم، افتح issue على GitHub: https://github.com/amgdadel7/traffic112/issues

## الروابط

- **المستودع**: https://github.com/amgdadel7/traffic112
- **API Documentation**: بعد التشغيل، افتح `http://localhost:8000/docs`

