# استكشاف أخطاء Cloud Run

## المشكلة الحالية
```
ERROR: Revision 'fastapi-api-00004-d57' is not ready and cannot serve traffic. 
The user-provided container failed to start and listen on the port defined 
provided by the PORT-8888 environment variable within the allocated timeout.
```

## الحلول

### 1. استخدام Dockerfile محسن
```bash
# استخدم Dockerfile الجديد
docker build -t gcr.io/traffic-light-2025/fastapi-api .
docker push gcr.io/traffic-light-2025/fastapi-api
```

### 2. نشر مع إعدادات محسنة
```bash
gcloud run deploy fastapi-api \
  --image gcr.io/traffic-light-2025/fastapi-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --timeout 300 \
  --memory 2Gi \
  --cpu 1 \
  --max-instances 10
```

### 3. استخدام سكريبت النشر
```bash
chmod +x deploy.sh
./deploy.sh
```

### 4. اختبار محلي
```bash
# بناء الصورة محلياً
docker build -t fastapi-api .

# تشغيل الحاوية محلياً
docker run -p 8080:8080 -e PORT=8080 fastapi-api

# اختبار
curl http://localhost:8080/health
```

## التحقق من الأخطاء

### 1. فحص السجلات
```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=fastapi-api" --limit 50
```

### 2. فحص الحاوية محلياً
```bash
docker run --rm -it -p 8080:8080 -e PORT=8080 fastapi-api /bin/bash
```

### 3. اختبار المنفذ
```bash
# داخل الحاوية
netstat -tlnp | grep :8080
```

## إعدادات Cloud Run الموصى بها

- **Memory**: 2Gi (مطلوب لـ TensorFlow)
- **CPU**: 1
- **Timeout**: 300s
- **Port**: 8080
- **Max Instances**: 10

## متغيرات البيئة المطلوبة

```yaml
env_vars:
  - name: PORT
    value: "8080"
  - name: PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION
    value: "python"
  - name: PYTHONUNBUFFERED
    value: "1"
```

## بدائل النشر

### 1. App Engine
```bash
gcloud app deploy app.yaml
```

### 2. Cloud Build
```bash
gcloud builds submit --config cloudbuild.yaml
```

### 3. Render (بديل)
استخدم `render.yaml` الموجود في المشروع

## نصائح إضافية

1. **تأكد من أن التطبيق يستمع على 0.0.0.0**
2. **استخدم المنفذ المحدد في متغير PORT**
3. **تأكد من أن جميع المكتبات مثبتة بشكل صحيح**
4. **اختبر التطبيق محلياً قبل النشر**