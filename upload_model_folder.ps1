# Script to upload ssd_mobilenet_v1_coco_11_06_2017 folder to GitHub with Git LFS
# Run this script in PowerShell: .\upload_model_folder.ps1

Write-Host "📤 Uploading model folder to GitHub with Git LFS..." -ForegroundColor Green

$projectPath = "d:\New folder (2)\New folder (2)\traffic112"
Set-Location $projectPath

$modelFolder = "ssd_mobilenet_v1_coco_11_06_2017"

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

# Check if .gitattributes is updated
Write-Host "`n📝 Checking .gitattributes..." -ForegroundColor Yellow
if (Test-Path ".gitattributes") {
    $attributes = Get-Content ".gitattributes" -Raw
    if ($attributes -match "\.pb filter=lfs") {
        Write-Host "✅ .gitattributes is configured for large files" -ForegroundColor Green
    } else {
        Write-Host "⚠️  .gitattributes needs to be updated" -ForegroundColor Yellow
        Write-Host "   The script will update it automatically" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️  .gitattributes not found, creating it..." -ForegroundColor Yellow
}

# Check if model folder exists
if (-not (Test-Path $modelFolder)) {
    Write-Host "`n❌ Model folder not found: $modelFolder" -ForegroundColor Red
    Write-Host "   Please extract the tar.gz file first" -ForegroundColor Yellow
    exit 1
}

Write-Host "`n📁 Model folder found: $modelFolder" -ForegroundColor Green

# Calculate total size
$totalSize = 0
Get-ChildItem -Path $modelFolder -Recurse -File | ForEach-Object {
    $totalSize += $_.Length
}
$totalSizeMB = [math]::Round($totalSize / 1MB, 2)
Write-Host "📊 Total size: $totalSizeMB MB" -ForegroundColor Cyan

# List files in folder
Write-Host "`n📋 Files in model folder:" -ForegroundColor Yellow
Get-ChildItem -Path $modelFolder -File | ForEach-Object {
    $fileSize = [math]::Round($_.Length / 1MB, 2)
    Write-Host "   - $($_.Name) ($fileSize MB)" -ForegroundColor White
}

# Remove folder from .gitignore if it exists there
Write-Host "`n🔍 Checking .gitignore..." -ForegroundColor Yellow
if (Test-Path ".gitignore") {
    $gitignore = Get-Content ".gitignore" -Raw
    if ($gitignore -match "ssd_mobilenet_v1_coco_11_06_2017/") {
        Write-Host "⚠️  Folder is in .gitignore, removing it..." -ForegroundColor Yellow
        $newGitignore = $gitignore -replace "ssd_mobilenet_v1_coco_11_06_2017/", "# ssd_mobilenet_v1_coco_11_06_2017/ # Now tracked with Git LFS"
        Set-Content -Path ".gitignore" -Value $newGitignore -NoNewline
        Write-Host "✅ Updated .gitignore" -ForegroundColor Green
    } else {
        Write-Host "✅ Folder is not in .gitignore" -ForegroundColor Green
    }
}

# Add .gitattributes first
Write-Host "`n➕ Adding .gitattributes..." -ForegroundColor Yellow
git add .gitattributes
Write-Host "✅ .gitattributes added" -ForegroundColor Green

# Add .gitignore if changed
Write-Host "`n➕ Adding .gitignore..." -ForegroundColor Yellow
git add .gitignore
Write-Host "✅ .gitignore added" -ForegroundColor Green

# Add model folder files
Write-Host "`n➕ Adding model folder files with Git LFS..." -ForegroundColor Yellow
git add "$modelFolder/"
Write-Host "✅ Model folder files added" -ForegroundColor Green

# Verify files are tracked by LFS
Write-Host "`n🔍 Verifying Git LFS tracking..." -ForegroundColor Yellow
$lfsFiles = git lfs ls-files
if ($lfsFiles) {
    Write-Host "✅ Files tracked by Git LFS:" -ForegroundColor Green
    $lfsFiles | ForEach-Object {
        Write-Host "   $_" -ForegroundColor Cyan
    }
} else {
    Write-Host "⚠️  No files found in Git LFS tracking" -ForegroundColor Yellow
    Write-Host "   This might be normal if files are not yet committed" -ForegroundColor Yellow
}

# Show status
Write-Host "`n📊 Git status:" -ForegroundColor Yellow
git status --short

Write-Host "`n✅ Setup complete!" -ForegroundColor Green
Write-Host "`n📝 Next steps:" -ForegroundColor Cyan
Write-Host "   1. Review changes: git status" -ForegroundColor White
Write-Host "   2. Commit: git commit -m 'Add model folder with Git LFS'" -ForegroundColor White
Write-Host "   3. Push: git push -u origin main" -ForegroundColor White
Write-Host "`n   ⚠️  Note: This will upload ~160MB of files. Make sure you have:" -ForegroundColor Yellow
Write-Host "   - Git LFS quota available on GitHub" -ForegroundColor White
Write-Host "   - Good internet connection" -ForegroundColor White
Write-Host "   - Time for upload (may take several minutes)" -ForegroundColor White

