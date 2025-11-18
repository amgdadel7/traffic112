# رفع مجلد ssd_mobilenet_v1_coco_11_06_2017 إلى GitHub

## 📋 ملخص

المجلد `ssd_mobilenet_v1_coco_11_06_2017` كبير جداً (~160 MB)، لذلك سيتم رفعه باستخدام **Git LFS**.

## 🚀 الطريقة السريعة

### الخطوة 1: شغّل السكريبت

```powershell
.\upload_model_folder.ps1
```

### الخطوة 2: Commit و Push

```bash
git commit -m "Add model folder with Git LFS"
git push -u origin main
```

## 📝 الطريقة اليدوية

### 1. إعداد Git LFS

```bash
# تثبيت Git LFS hooks
git lfs install

# تتبع ملفات النموذج الكبيرة
git lfs track "*.pb"
git lfs track "*.pbtxt"
git lfs track "*.ckpt.data-*"
git lfs track "*.ckpt.index"
git lfs track "*.ckpt.meta"
```

### 2. تحديث .gitignore

المجلد موجود في `.gitignore`، يجب إزالته أو تعليقه:

```bash
# افتح .gitignore وعلّق السطر:
# ssd_mobilenet_v1_coco_11_06_2017/
```

### 3. إضافة الملفات

```bash
# إضافة .gitattributes أولاً
git add .gitattributes

# إضافة المجلد
git add ssd_mobilenet_v1_coco_11_06_2017/

# التحقق من أن الملفات يتم تتبعها مع LFS
git lfs ls-files
```

### 4. Commit و Push

```bash
git commit -m "Add model folder with Git LFS"
git push -u origin main
```

## ⚠️ ملاحظات مهمة

### حجم الملفات:
- `frozen_inference_graph.pb`: ~28 MB
- `graph.pbtxt`: ~21 MB
- `model.ckpt.data-00000-of-00001`: ~104 MB
- `model.ckpt.meta`: ~9.9 MB
- `model.ckpt.index`: ~26 KB
- **المجموع**: ~160 MB

### متطلبات:
1. ✅ Git LFS مثبت على جهازك
2. ✅ Git LFS مفعّل في المستودع على GitHub
3. ✅ مساحة كافية في Git LFS quota (GitHub يوفر 1 GB مجاناً)
4. ✅ اتصال إنترنت جيد (الرفع قد يستغرق 10-30 دقيقة)

### التحقق من Git LFS:

```bash
# التحقق من الملفات المتبعة
git lfs ls-files

# يجب أن تظهر جميع ملفات النموذج:
# ssd_mobilenet_v1_coco_11_06_2017/frozen_inference_graph.pb
# ssd_mobilenet_v1_coco_11_06_2017/graph.pbtxt
# ssd_mobilenet_v1_coco_11_06_2017/model.ckpt.data-00000-of-00001
# ssd_mobilenet_v1_coco_11_06_2017/model.ckpt.index
# ssd_mobilenet_v1_coco_11_06_2017/model.ckpt.meta
```

## 🔍 حل المشاكل

### خطأ: "Git LFS not found"
```bash
# تثبيت Git LFS
# Windows: https://git-lfs.github.com/
# أو عبر Chocolatey: choco install git-lfs
```

### خطأ: "pre-receive hook declined"
- تأكد من أن الملفات يتم تتبعها مع Git LFS
- تحقق من: `git lfs ls-files`
- إذا لم تظهر، أعد إضافة الملفات: `git add ssd_mobilenet_v1_coco_11_06_2017/`

### خطأ: "LFS quota exceeded"
- GitHub يوفر 1 GB مجاناً
- تحقق من استخدامك: https://github.com/settings/billing
- يمكنك شراء مساحة إضافية أو حذف ملفات قديمة

## ✅ بعد الرفع

بعد رفع الملفات بنجاح:

1. **تحقق على GitHub**: 
   - افتح المستودع
   - تحقق من وجود المجلد `ssd_mobilenet_v1_coco_11_06_2017/`
   - الملفات الكبيرة ستظهر مع رمز Git LFS

2. **على Render**:
   - Render سيقوم بنسخ الملفات تلقائياً
   - الكود سيستخدم المجلد مباشرة (لا حاجة للاستخراج)

3. **محلياً**:
   - المجلد موجود وسيعمل مباشرة
   - لا حاجة لاستخراج tar.gz

## 🎯 الخلاصة

- ✅ `.gitattributes` محدث لتتبع ملفات النموذج
- ✅ `.gitignore` محدث (المجلد غير متجاهل)
- ✅ السكريبت جاهز: `upload_model_folder.ps1`
- ✅ كل شيء جاهز للرفع!

شغّل السكريبت واتبع التعليمات! 🚀

