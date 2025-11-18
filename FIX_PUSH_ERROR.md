# حل مشكلة Push Error

## المشكلة
```
! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'https://github.com/amgdadel7/traffic112.git'
hint: Updates were rejected because the remote contains work that you do not
hint: have locally.
```

## الحل

### الخطوة 1: سحب التغييرات من GitHub

```bash
# سحب التغييرات مع السماح بدمج التاريخ غير المرتبط
git pull origin main --allow-unrelated-histories
```

إذا ظهرت تعارضات (conflicts):
```bash
# حل التعارضات يدوياً، ثم:
git add .
git commit -m "Merge remote changes"
```

### الخطوة 2: إعداد Git LFS وإضافة الملفات

```bash
# إعداد Git LFS
git lfs install

# إضافة الملفات
git add .gitattributes
git add .gitignore
git add ssd_mobilenet_v1_coco_11_06_2017/

# التحقق من Git LFS
git lfs ls-files
```

### الخطوة 3: Commit و Push

```bash
# Commit
git commit -m "Add model folder with Git LFS"

# Push
git push -u origin main
```

## الطريقة البديلة (إذا استمرت المشاكل)

### استخدام rebase:

```bash
# سحب مع rebase
git pull --rebase origin main

# ثم push
git push -u origin main
```

### أو force push (⚠️ احذر - فقط إذا كنت متأكداً):

```bash
# ⚠️ هذا سيستبدل التاريخ على GitHub
git push -u origin main --force
```

## الأوامر الكاملة (نسخ ولصق)

```bash
# 1. سحب التغييرات
git pull origin main --allow-unrelated-histories

# 2. إعداد Git LFS
git lfs install

# 3. إضافة الملفات
git add .gitattributes .gitignore ssd_mobilenet_v1_coco_11_06_2017/

# 4. التحقق
git lfs ls-files
git status

# 5. Commit
git commit -m "Add model folder with Git LFS"

# 6. Push
git push -u origin main
```

