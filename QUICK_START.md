# دليل التشغيل السريع - Quick Start Guide

## تشغيل المشروع محلياً

### الطريقة 1: استخدام ملف التشغيل (الأسهل)

#### على Windows:
```bash
run.bat
```

#### على Linux/Mac:
```bash
chmod +x start.sh
./start.sh
```

### الطريقة 2: استخدام Python مباشرة

```bash
# تثبيت المتطلبات أولاً
pip install -r requirements.txt

# تشغيل التطبيق
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### الطريقة 3: استخدام ملف run.py

```bash
python run.py
```

## الوصول للتطبيق

بعد التشغيل، سيكون التطبيق متاحاً على:

- **الواجهة الرئيسية**: http://localhost:8000
- **وثائق API (Swagger)**: http://localhost:8000/docs
- **وثائق API (ReDoc)**: http://localhost:8000/redoc
- **فحص الحالة**: http://localhost:8000/health

## ملاحظات مهمة

1. **تحميل النموذج**: عند أول تشغيل، سيتم تحميل نموذج TensorFlow تلقائياً (قد يستغرق بضع دقائق)

2. **المتطلبات**:
   - Python 3.7 أو أحدث
   - جميع المكتبات المطلوبة في `requirements.txt`

3. **المنافذ**: التطبيق يعمل على المنفذ 8000 افتراضياً

4. **إعادة التحميل التلقائي**: عند استخدام `--reload`، سيتم إعادة تحميل التطبيق تلقائياً عند تغيير الكود

## استكشاف الأخطاء

### خطأ في تحميل TensorFlow:
```bash
# تأكد من تثبيت TensorFlow
pip install tensorflow==2.11.0
```

### خطأ في المنفذ مشغول:
```bash
# استخدم منفذ آخر
python -m uvicorn main:app --host 0.0.0.0 --port 8001
```

### مشاكل في Protobuf:
```bash
# على Linux/Mac
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# على Windows
set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
```

## اختبار API

بعد التشغيل، يمكنك اختبار API من المتصفح أو باستخدام curl:

```bash
# فحص الحالة
curl http://localhost:8000/health

# فحص حالة النموذج
curl http://localhost:8000/model-status
```

