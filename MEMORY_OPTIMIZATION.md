# Memory Optimization for Cloud Deployment

## المشكلة
النموذج `faster_rcnn_resnet101_coco_11_06_2017` كبير جداً (188MB) ويستهلك أكثر من 2GB من الذاكرة عند التحميل.

## الحلول المطبقة

### 1. تبديل النموذج 🔄
- **القديم**: `faster_rcnn_resnet101_coco_11_06_2017` (188MB, دقة عالية)
- **الجديد**: `ssd_mobilenet_v1_coco_11_06_2017` (~27MB, سريع وكفء)

### 2. تحسينات الذاكرة في الكود 💾
- إعدادات TensorFlow محسنة للذاكرة
- تنظيف الذاكرة بعد تحميل كل مكون
- تعطيل XLA JIT compilation
- Garbage collection يدوي
- تخطي الاختبارات لتوفير الذاكرة

### 3. تحسينات التكوين السحابي ☁️

#### الخيار 1: زيادة حد الذاكرة (موصى به)
استخدم ملف `cloudrun-config.yaml`:

\`\`\`bash
# Deploy with configuration file
gcloud run services replace cloudrun-config.yaml \\
  --region us-central1
\`\`\`

#### الخيار 2: استخدام سطر الأوامر
\`\`\`bash
gcloud run deploy traffic-light-detection \\
  --memory 4Gi \\
  --cpu 2 \\
  --timeout 300 \\
  --concurrency 1 \\
  --region us-central1
\`\`\`

#### الخيار 3: عبر Console
1. افتح [Google Cloud Console](https://console.cloud.google.com/run)
2. اختر الخدمة
3. اضغط "Edit & Deploy New Revision"
4. في قسم "Capacity":
   - **Memory**: 4 GiB
   - **CPU**: 2
   - **Maximum requests per container**: 1
5. في قسم "Request timeout": 300 seconds

## مقارنة النماذج

| النموذج | الحجم | الدقة | السرعة | استهلاك الذاكرة |
|---------|-------|-------|--------|-----------------|
| faster_rcnn_resnet101 | 188MB | عالية جداً | بطيء | ~2.5GB |
| ssd_mobilenet_v1 | 27MB | جيدة | سريع | ~800MB |

## متطلبات الذاكرة المقدرة

### مع ssd_mobilenet_v1:
- **تحميل النموذج**: ~800MB
- **TensorFlow Runtime**: ~300MB
- **FastAPI + Dependencies**: ~200MB
- **Buffer**: ~200MB
- **المجموع**: ~1.5GB ✅

### مع faster_rcnn_resnet101:
- **تحميل النموذج**: ~2GB
- **TensorFlow Runtime**: ~400MB
- **FastAPI + Dependencies**: ~200MB
- **Buffer**: ~200MB
- **المجموع**: ~2.8GB ❌ (يتجاوز حد 2GB)

## التكلفة

زيادة الذاكرة من 2GB إلى 4GB:
- **التكلفة الإضافية**: ~$0.0000025 لكل GB-second
- **التأثير على التكلفة الشهرية**: ~$5-10 إضافية (حسب الاستخدام)

## الخطوات التالية

1. **ارفع التعديلات**:
\`\`\`bash
git add .
git commit -m "Optimize memory usage for cloud deployment"
git push
\`\`\`

2. **انشر مع التكوين الجديد**:
\`\`\`bash
# Using configuration file
gcloud run services replace cloudrun-config.yaml --region us-central1

# Or using command line
gcloud run deploy traffic-light-detection \\
  --memory 4Gi \\
  --cpu 2 \\
  --region us-central1
\`\`\`

3. **تحقق من الحالة**:
\`\`\`bash
curl https://YOUR-SERVICE-URL/model-status
\`\`\`

## نصائح إضافية

### إذا استمرت المشكلة:
1. استخدم Cloud Run Gen2 execution environment
2. قلل concurrency إلى 1
3. استخدم Cloud Storage لتخزين النموذج المحمل مسبقاً
4. فكر في استخدام Cloud Functions مع Cold Start محسّن

### للأداء الأفضل:
- استخدم **Minimum instances**: 1 (لتجنب cold starts)
- استخدم **CPU allocation**: "CPU is always allocated"
- فعّل **CPU boost** للتحميل الأسرع