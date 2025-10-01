# Docker Troubleshooting Guide

## المشكلة: النموذج لا يتم تحميله في Docker

### 🔍 **تشخيص المشكلة:**

#### 1. **فحص السجلات (Logs)**
```bash
# عرض سجلات الحاوية
docker logs <container_name>

# متابعة السجلات في الوقت الفعلي
docker logs -f <container_name>
```

#### 2. **فحص حالة النموذج**
```bash
# فحص حالة النموذج
curl http://localhost:8080/model-status

# فحص الصحة العامة
curl http://localhost:8080/health
```

#### 3. **فحص محتويات الحاوية**
```bash
# الدخول إلى الحاوية
docker exec -it <container_name> /bin/bash

# فحص الملفات
ls -la /app/
ls -la /app/ssd_mobilenet_v1_coco_11_06_2017/
```

### 🛠️ **الحلول المطبقة:**

#### 1. **تحسين Dockerfile**
- ✅ إضافة أدوات إضافية (wget, tar)
- ✅ إنشاء مجلدات النماذج مع الصلاحيات الصحيحة
- ✅ متغيرات البيئة المحسنة لـ TensorFlow
- ✅ Health check للتحقق من الحالة
- ✅ إعدادات الذاكرة المحسنة

#### 2. **تحسين main.py**
- ✅ كشف البيئة (Docker vs Local)
- ✅ وقت انتظار أطول في Docker
- ✅ تسجيل مفصل للمسارات والملفات
- ✅ التحقق من وجود ملفات النموذج
- ✅ رسائل خطأ واضحة

#### 3. **ملفات مساعدة جديدة**
- ✅ `.dockerignore` - استبعاد الملفات غير الضرورية
- ✅ `docker-compose.yml` - تكوين سهل للاختبار
- ✅ `build-and-test.ps1` - سكريبت اختبار تلقائي

### 🚀 **خطوات الاختبار:**

#### الطريقة 1: استخدام Docker Compose
```bash
# بناء وتشغيل
docker-compose up --build

# في نافذة منفصلة - اختبار API
curl http://localhost:8080/health
```

#### الطريقة 2: استخدام السكريبت
```powershell
# تشغيل سكريبت الاختبار
.\build-and-test.ps1
```

#### الطريقة 3: يدوياً
```bash
# بناء الصورة
docker build -t traffic-light-detection .

# تشغيل الحاوية
docker run -d \
  --name traffic-light-test \
  -p 8080:8080 \
  -v "$(pwd)/test_images:/app/test_images:ro" \
  traffic-light-detection

# فحص السجلات
docker logs traffic-light-test

# اختبار API
curl http://localhost:8080/model-status
```

### 🔧 **حلول المشاكل الشائعة:**

#### 1. **مشكلة: "Model not loaded yet"**
**السبب:** النموذج لم يتم تحميله بعد
**الحل:**
```bash
# انتظر أكثر (قد يستغرق 2-5 دقائق)
sleep 60
curl http://localhost:8080/model-status

# أو أعد تحميل النموذج يدوياً
curl -X POST http://localhost:8080/reload-model
```

#### 2. **مشكلة: "Connection refused"**
**السبب:** الحاوية لم تبدأ بعد
**الحل:**
```bash
# تحقق من حالة الحاوية
docker ps

# إذا لم تكن تعمل، ابدأها
docker start <container_name>

# أو أعد تشغيلها
docker restart <container_name>
```

#### 3. **مشكلة: "Permission denied"**
**السبب:** مشاكل في الصلاحيات
**الحل:**
```bash
# إعادة بناء الصورة مع الصلاحيات الصحيحة
docker build --no-cache -t traffic-light-detection .

# أو تشغيل مع صلاحيات root
docker run --user root -p 8080:8080 traffic-light-detection
```

#### 4. **مشكلة: "Out of memory"**
**السبب:** عدم كفاية الذاكرة
**الحل:**
```bash
# تشغيل مع ذاكرة أكثر
docker run -m 4g -p 8080:8080 traffic-light-detection

# أو استخدام Docker Compose مع إعدادات الذاكرة
```

### 📊 **مراقبة الأداء:**

#### 1. **استخدام الموارد**
```bash
# مراقبة استخدام الذاكرة والمعالج
docker stats <container_name>
```

#### 2. **فحص السجلات**
```bash
# البحث عن أخطاء محددة
docker logs <container_name> 2>&1 | grep -i error
docker logs <container_name> 2>&1 | grep -i "model"
```

#### 3. **اختبار شامل**
```bash
# اختبار جميع endpoints
curl http://localhost:8080/
curl http://localhost:8080/health
curl http://localhost:8080/model-status
curl http://localhost:8080/docs
```

### 🎯 **نصائح للأداء الأمثل:**

1. **استخدم Docker Compose** للاختبار المحلي
2. **راقب السجلات** باستمرار أثناء التطوير
3. **استخدم Health Checks** للتحقق من الحالة
4. **اختبر مع صور حقيقية** للتأكد من عمل الكشف
5. **استخدم Volume mounts** للصور والنتائج

### 🚨 **مؤشرات المشاكل:**

| المؤشر | المشكلة المحتملة | الحل |
|--------|------------------|------|
| `model_loaded: false` | النموذج لم يتم تحميله | انتظر أو أعد التحميل |
| `Connection refused` | الحاوية لا تعمل | أعد تشغيل الحاوية |
| `Permission denied` | مشاكل صلاحيات | إعادة بناء مع صلاحيات صحيحة |
| `Out of memory` | ذاكرة غير كافية | زيادة حد الذاكرة |
| `Download failed` | مشكلة شبكة | تحقق من الاتصال |

### ✅ **التحقق من النجاح:**

عندما يعمل كل شيء بشكل صحيح، يجب أن ترى:
```json
{
  "model_loaded": true,
  "model_error": null,
  "status": "ready",
  "message": "Model is ready for inference"
}
```

واختبار الكشف يجب أن يعطي نتيجة مثل:
```json
{
  "command": "Stop",
  "confidence": 0.6875222325325012,
  "traffic_light_detected": true,
  "message": "Traffic light detected: Stop command"
}
```