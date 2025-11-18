# إعداد المشروع للربط مع GitHub

## المستودع على GitHub
**URL**: https://github.com/amgdadel7/traffic112.git

## الخطوات السريعة

### 1. ربط المشروع المحلي مع GitHub

شغّل السكريبت:
```powershell
.\connect_to_github.ps1
```

أو نفّذ الأوامر يدوياً:

```bash
# الانتقال إلى مجلد المشروع
cd "d:\New folder (2)\New folder (2)\traffic112"

# تهيئة Git (إذا لم يكن موجوداً)
git init

# إضافة المستودع البعيد
git remote add origin https://github.com/amgdadel7/traffic112.git

# أو تحديث المستودع البعيد إذا كان موجوداً
git remote set-url origin https://github.com/amgdadel7/traffic112.git
```

### 2. إعداد Git LFS للملف الكبير

الملف `ssd_mobilenet_v1_coco_11_06_2017.tar.gz` كبير (122 MB)، لذا يُفضل استخدام Git LFS:

```bash
# تثبيت Git LFS hooks
git lfs install

# تتبع ملفات tar.gz
git lfs track "*.tar.gz"

# إضافة ملف .gitattributes
git add .gitattributes
```

### 3. رفع التغييرات إلى GitHub

```bash
# إضافة جميع الملفات
git add .

# إنشاء commit
git commit -m "Update project with model file and Dockerfile fixes"

# رفع إلى GitHub
git push -u origin main
```

### 4. إذا كان المستودع على GitHub يحتوي على ملفات

إذا كان المستودع على GitHub يحتوي على ملفات مختلفة، استخدم:

```bash
# سحب التغييرات من GitHub أولاً
git pull origin main --allow-unrelated-histories

# حل أي تعارضات إذا ظهرت
# ثم ارفع التغييرات
git push -u origin main
```

## الملفات المهمة

- ✅ `.gitattributes` - موجود بالفعل لتتبع ملفات tar.gz مع Git LFS
- ✅ `main.py` - محدث لاستخدام الملف المحلي أولاً
- ✅ `Dockerfile` - محدث لإصلاح مشاكل apt-get

## ملاحظات

1. **الملف الكبير**: الملف `ssd_mobilenet_v1_coco_11_06_2017.tar.gz` موجود بالفعل في المستودع على GitHub
2. **Render Deployment**: بعد رفع التغييرات، Render سيقوم بالنشر تلقائياً إذا كان `autoDeploy: true` في `render.yaml`
3. **Git LFS**: تأكد من أن Git LFS مثبت على جهازك وعلى Render

## التحقق من الربط

```bash
# التحقق من المستودع البعيد
git remote -v

# يجب أن يظهر:
# origin  https://github.com/amgdadel7/traffic112.git (fetch)
# origin  https://github.com/amgdadel7/traffic112.git (push)
```

## حل المشاكل

### خطأ: "fatal: refusing to merge unrelated histories"
```bash
git pull origin main --allow-unrelated-histories
```

### خطأ: "Git LFS not found"
قم بتثبيت Git LFS من: https://git-lfs.github.com/

### خطأ: "Permission denied"
تأكد من أن لديك صلاحيات الكتابة على المستودع على GitHub

