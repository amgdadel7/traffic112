# تعليمات رفع ملف ssd_mobilenet_v1_coco_11_06_2017.tar.gz إلى Render

## الطريقة 1: استخدام Git LFS (مُوصى بها)

### الخطوات:

1. **تهيئة Git LFS في المشروع:**
```bash
cd "d:\New folder (2)\New folder (2)\traffic112"
git lfs install
```

2. **تتبع ملفات tar.gz:**
```bash
git lfs track "*.tar.gz"
```

3. **إضافة الملفات:**
```bash
git add .gitattributes
git add ssd_mobilenet_v1_coco_11_06_2017.tar.gz
git add .
```

4. **الالتزام والرفع:**
```bash
git commit -m "Add model file with Git LFS"
git remote add origin <YOUR_GIT_REPO_URL>
git push -u origin main
```

## الطريقة 2: السماح للكود بتحميل الملف تلقائياً

الكود المعدل في `main.py` سيقوم بتحميل الملف تلقائياً من الإنترنت إذا لم يجده محلياً. هذا يعني أنك لست بحاجة لرفع الملف يدوياً - Render سيقوم بتحميله عند أول تشغيل.

### المزايا:
- لا حاجة لرفع ملف كبير (122 MB)
- التحديثات التلقائية للموديل
- توفير مساحة في المستودع

### العيوب:
- يستغرق وقتاً أطول في أول تشغيل
- يحتاج اتصال بالإنترنت

## الطريقة 3: استخدام Render Disk (للملفات الكبيرة)

إذا كان لديك Render Disk متاح:
1. اربط Disk بخدمتك
2. ارفع الملف عبر SSH أو Render Shell
3. عدّل الكود ليقرأ من مسار Disk

## ملاحظات مهمة:

- **الطريقة الحالية**: الكود يتحقق من وجود الملف محلياً أولاً، ثم يحمله إذا لم يجده
- **للملفات الكبيرة**: استخدم Git LFS لتجنب مشاكل الأداء في Git
- **Render Service ID**: srv-d4cieuc9c44c738r935g

## التحقق من الرفع:

بعد الرفع، تحقق من أن الملف موجود في Render:
1. افتح Render Dashboard
2. اذهب إلى خدمتك
3. افتح Shell/SSH
4. تحقق من وجود الملف: `ls -lh ssd_mobilenet_v1_coco_11_06_2017.tar.gz`

