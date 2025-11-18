# حل مشكلة رفض GitHub للملفات الكبيرة

## المشكلة
```
! [remote rejected] main -> main (pre-receive hook declined)
error: failed to push some refs to 'https://github.com/amgdadel7/traffic112.git'
```

هذا الخطأ يحدث لأن GitHub يرفض الملفات الكبيرة (أكبر من 100 MB) بدون Git LFS.

## الحل السريع

### الطريقة 1: استخدام السكريبت (مُوصى بها)

```powershell
.\fix_large_file.ps1
```

ثم:
```bash
git commit -m "Fix: Use Git LFS for large model file"
git push -u origin main
```

### الطريقة 2: يدوياً

```bash
# 1. إعداد Git LFS
git lfs install
git lfs track "*.tar.gz"

# 2. إزالة الملف من Git cache
git rm --cached ssd_mobilenet_v1_coco_11_06_2017.tar.gz

# 3. إضافة .gitattributes
git add .gitattributes

# 4. إضافة الملف مرة أخرى (سيتم تتبعه مع LFS)
git add ssd_mobilenet_v1_coco_11_06_2017.tar.gz

# 5. التحقق من أن الملف يتم تتبعه مع LFS
git lfs ls-files

# 6. Commit و Push
git commit -m "Fix: Use Git LFS for large model file"
git push -u origin main
```

## إذا استمرت المشكلة

إذا كان الملف موجوداً في Git history السابق، قد تحتاج لتنظيف التاريخ:

### الطريقة 1: إزالة الملف من آخر commit

```bash
# إزالة الملف من آخر commit
git reset --soft HEAD~1
git reset HEAD ssd_mobilenet_v1_coco_11_06_2017.tar.gz

# إعداد Git LFS
git lfs install
git lfs track "*.tar.gz"
git add .gitattributes
git add ssd_mobilenet_v1_coco_11_06_2017.tar.gz

# Commit جديد
git commit -m "Fix: Use Git LFS for large model file"
git push -u origin main --force
```

### الطريقة 2: استخدام BFG Repo-Cleaner (للملفات في التاريخ القديم)

1. تحميل BFG من: https://rtyley.github.io/bfg-repo-cleaner/
2. تشغيل:
```bash
java -jar bfg.jar --strip-blobs-bigger-than 100M
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force
```

### الطريقة 3: حذف الملف من المستودع (إذا لم يكن ضرورياً)

إذا كان الملف موجوداً بالفعل على GitHub، يمكنك:
1. حذفه من `.gitignore` (إذا كان موجوداً)
2. السماح للكود بتحميله تلقائياً
3. إضافة الملف إلى `.gitignore`:

```bash
echo "ssd_mobilenet_v1_coco_11_06_2017.tar.gz" >> .gitignore
git add .gitignore
git commit -m "Ignore large model file, download automatically"
git push
```

## التحقق من الحل

بعد الرفع، تحقق من:

```bash
# التحقق من أن الملف يتم تتبعه مع LFS
git lfs ls-files

# يجب أن يظهر:
# ssd_mobilenet_v1_coco_11_06_2017.tar.gz
```

## ملاحظات مهمة

1. **Git LFS**: تأكد من تثبيت Git LFS على جهازك
2. **المستودع على GitHub**: يجب أن يكون Git LFS مفعّل في المستودع
3. **Render**: Render يدعم Git LFS تلقائياً
4. **الحجم**: الملف 122 MB، وهو أكبر من حد GitHub البالغ 100 MB

## بديل: عدم رفع الملف

إذا استمرت المشاكل، يمكنك:
1. إضافة الملف إلى `.gitignore`
2. السماح للكود بتحميله تلقائياً (الكود معدّ لذلك)
3. الملف سيتم تحميله عند أول تشغيل على Render

```bash
# إضافة إلى .gitignore
echo "ssd_mobilenet_v1_coco_11_06_2017.tar.gz" >> .gitignore
git add .gitignore
git commit -m "Ignore model file, download automatically"
git push
```

