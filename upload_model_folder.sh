#!/bin/bash
# Script to upload ssd_mobilenet_v1_coco_11_06_2017 folder to GitHub with Git LFS
# Run this script in Git Bash: bash upload_model_folder.sh

echo "📤 Uploading model folder to GitHub with Git LFS..."

MODEL_FOLDER="ssd_mobilenet_v1_coco_11_06_2017"

# Check if Git LFS is installed
echo ""
echo "📦 Checking Git LFS installation..."
if ! command -v git-lfs &> /dev/null; then
    echo "❌ Git LFS is not installed!"
    echo "   Please install Git LFS from: https://git-lfs.github.com/"
    exit 1
fi
echo "✅ Git LFS is installed"

# Install Git LFS hooks
echo ""
echo "🔧 Installing Git LFS hooks..."
git lfs install
echo "✅ Git LFS hooks installed"

# Check if model folder exists
if [ ! -d "$MODEL_FOLDER" ]; then
    echo ""
    echo "❌ Model folder not found: $MODEL_FOLDER"
    echo "   Please extract the tar.gz file first"
    exit 1
fi

echo ""
echo "📁 Model folder found: $MODEL_FOLDER"

# Calculate total size
TOTAL_SIZE=$(du -sm "$MODEL_FOLDER" | cut -f1)
echo "📊 Total size: ${TOTAL_SIZE} MB"

# List files in folder
echo ""
echo "📋 Files in model folder:"
ls -lh "$MODEL_FOLDER" | awk '{print "   - " $9 " (" $5 ")"}'

# Add .gitattributes first
echo ""
echo "➕ Adding .gitattributes..."
git add .gitattributes
echo "✅ .gitattributes added"

# Add .gitignore
echo ""
echo "➕ Adding .gitignore..."
git add .gitignore
echo "✅ .gitignore added"

# Add model folder files
echo ""
echo "➕ Adding model folder files with Git LFS..."
git add "$MODEL_FOLDER/"
echo "✅ Model folder files added"

# Verify files are tracked by LFS
echo ""
echo "🔍 Verifying Git LFS tracking..."
LFS_FILES=$(git lfs ls-files)
if [ -n "$LFS_FILES" ]; then
    echo "✅ Files tracked by Git LFS:"
    echo "$LFS_FILES" | sed 's/^/   /'
else
    echo "⚠️  No files found in Git LFS tracking"
    echo "   This might be normal if files are not yet committed"
fi

# Show status
echo ""
echo "📊 Git status:"
git status --short

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "   1. Pull remote changes: git pull origin main --allow-unrelated-histories"
echo "   2. Commit: git commit -m 'Add model folder with Git LFS'"
echo "   3. Push: git push -u origin main"
echo ""
echo "   ⚠️  Note: This will upload ~160MB of files. Make sure you have:"
echo "   - Git LFS quota available on GitHub"
echo "   - Good internet connection"
echo "   - Time for upload (may take several minutes)"

