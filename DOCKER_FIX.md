# إصلاح مشكلة تحميل النموذج في Docker

## المشكلة
كان `wget` يفشل في تحميل النموذج أثناء بناء Docker image.

## الحلول المطبقة

### الحل 1: استخدام curl مع إعادة المحاولة (مطبوع في Dockerfile)
- تم استبدال `wget` بـ `curl`
- إضافة إعادة محاولة تلقائية (5 مرات)
- رابط بديل من GitHub إذا فشل الرابط الأساسي
- مهلة زمنية أطول (300 ثانية)

### الحل 2: تحميل النموذج عند التشغيل (Dockerfile.no-model-download)
- النموذج سيتم تحميله تلقائياً عند أول طلب
- يقلل من وقت البناء
- يتجنب مشاكل الشبكة أثناء البناء

## كيفية الاستخدام

### استخدام Dockerfile العادي (مع تحميل النموذج أثناء البناء):
```bash
docker build -t traffic-light-detection .
```

### استخدام Dockerfile بدون تحميل النموذج أثناء البناء:
```bash
docker build -f Dockerfile.no-model-download -t traffic-light-detection .
```

## ملاحظات

1. **إذا استمرت المشكلة**: استخدم `Dockerfile.no-model-download` - النموذج سيتم تحميله تلقائياً عند التشغيل
2. **التحقق من الاتصال**: تأكد من أن Docker يمكنه الوصول للإنترنت أثناء البناء
3. **التحقق من الرابط**: يمكنك اختبار الرابط يدوياً:
   ```bash
   curl -I https://storage.googleapis.com/download.tensorflow.org/models/object_detection/ssd_mobilenet_v1_coco_11_06_2017.tar.gz
   ```

## بناء وتشغيل

```bash
# بناء الصورة
docker build -t traffic-light-detection .

# أو بدون تحميل النموذج أثناء البناء
docker build -f Dockerfile.no-model-download -t traffic-light-detection .

# تشغيل الحاوية
docker run -p 8080:8080 traffic-light-detection
```

