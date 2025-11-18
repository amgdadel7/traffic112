# حل سريع لمشكلة رفض GitHub للملف الكبير

## المشكلة
GitHub يرفض الملف `ssd_mobilenet_v1_coco_11_06_2017.tar.gz` لأنه أكبر من 100 MB.

## الحل السريع (3 خطوات)

### الخطوة 1: شغّل السكريبت
```powershell
.\fix_large_file.ps1
```

### الخطوة 2: Commit التغييرات
```bash
git commit -m "Fix: Use Git LFS for large model file"
```

### الخطوة 3: Push إلى GitHub
```bash
git push -u origin main
```

## إذا لم يعمل السكريبت

نفّذ هذه الأوامر يدوياً:

```bash
# 1. إعداد Git LFS
git lfs install
git lfs track "*.tar.gz"

# 2. إزالة الملف من Git
git rm --cached ssd_mobilenet_v1_coco_11_06_2017.tar.gz

# 3. إضافة .gitattributes
git add .gitattributes

# 4. إضافة الملف مع Git LFS
git add ssd_mobilenet_v1_coco_11_06_2017.tar.gz

# 5. التحقق
git lfs ls-files

# 6. Commit و Push
git commit -m "Fix: Use Git LFS for large model file"
git push -u origin main
```

## بديل: عدم رفع الملف

إذا استمرت المشاكل، يمكنك تجاهل الملف والسماح للكود بتحميله تلقائياً:

```bash
# إضافة إلى .gitignore
echo "ssd_mobilenet_v1_coco_11_06_2017.tar.gz" >> .gitignore
git add .gitignore
git commit -m "Ignore model file, download automatically"
git push
```

الكود معدّ لتحميل الملف تلقائياً إذا لم يجده محلياً.

