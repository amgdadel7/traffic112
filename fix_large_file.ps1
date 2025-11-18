# Script to fix large file issue with Git LFS
# This script removes the large file from Git history and re-adds it with Git LFS

Write-Host "🔧 Fixing large file issue with Git LFS..." -ForegroundColor Green

$projectPath = "d:\New folder (2)\New folder (2)\traffic112"
Set-Location $projectPath

$modelFile = "ssd_mobilenet_v1_coco_11_06_2017.tar.gz"

# Check if Git LFS is installed
Write-Host "`n📦 Checking Git LFS installation..." -ForegroundColor Yellow
$lfsCheck = git lfs version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Git LFS is not installed!" -ForegroundColor Red
    Write-Host "   Please install Git LFS from: https://git-lfs.github.com/" -ForegroundColor Yellow
    Write-Host "   Then run this script again." -ForegroundColor Yellow
    exit 1
}
Write-Host "✅ Git LFS is installed" -ForegroundColor Green

# Install Git LFS hooks
Write-Host "`n🔧 Installing Git LFS hooks..." -ForegroundColor Yellow
git lfs install
Write-Host "✅ Git LFS hooks installed" -ForegroundColor Green

# Track tar.gz files
Write-Host "`n📝 Tracking .tar.gz files with Git LFS..." -ForegroundColor Yellow
git lfs track "*.tar.gz"
Write-Host "✅ .tar.gz files will be tracked with Git LFS" -ForegroundColor Green

# Check if file is already in Git
Write-Host "`n🔍 Checking Git status..." -ForegroundColor Yellow
$gitStatus = git status --porcelain
if ($gitStatus -match $modelFile) {
    Write-Host "⚠️  File is in staging area, removing it..." -ForegroundColor Yellow
    git reset HEAD $modelFile 2>&1 | Out-Null
}

# Remove file from Git cache if it exists
Write-Host "`n🗑️  Removing file from Git cache..." -ForegroundColor Yellow
git rm --cached $modelFile 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ File removed from Git cache" -ForegroundColor Green
} else {
    Write-Host "ℹ️  File not in Git cache (this is OK)" -ForegroundColor Cyan
}

# Add .gitattributes first
Write-Host "`n➕ Adding .gitattributes..." -ForegroundColor Yellow
git add .gitattributes
Write-Host "✅ .gitattributes added" -ForegroundColor Green

# Add the model file with Git LFS
if (Test-Path $modelFile) {
    Write-Host "`n➕ Adding model file with Git LFS..." -ForegroundColor Yellow
    git add $modelFile
    
    # Verify it's tracked by LFS
    $lfsFiles = git lfs ls-files
    if ($lfsFiles -match $modelFile) {
        Write-Host "✅ File is now tracked by Git LFS!" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Warning: File might not be tracked by LFS" -ForegroundColor Yellow
        Write-Host "   Trying to add it again..." -ForegroundColor Yellow
        git add --force $modelFile
    }
} else {
    Write-Host "⚠️  Model file not found: $modelFile" -ForegroundColor Yellow
}

# Show status
Write-Host "`n📊 Git status:" -ForegroundColor Yellow
git status

Write-Host "`n✅ Setup complete!" -ForegroundColor Green
Write-Host "`n📝 Next steps:" -ForegroundColor Cyan
Write-Host "   1. Commit: git commit -m 'Fix: Use Git LFS for large model file'" -ForegroundColor White
Write-Host "   2. Push: git push -u origin main" -ForegroundColor White
Write-Host "`n   If you still get errors, you may need to:" -ForegroundColor Yellow
Write-Host "   - Remove the file from Git history: git filter-branch" -ForegroundColor White
Write-Host "   - Or use BFG Repo-Cleaner to clean history" -ForegroundColor White

