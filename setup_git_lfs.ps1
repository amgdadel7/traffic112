# Script to set up Git LFS and prepare files for upload to Render
# Run this script in PowerShell: .\setup_git_lfs.ps1

Write-Host "🚀 Setting up Git LFS for model file upload..." -ForegroundColor Green

# Navigate to project directory
$projectPath = "d:\New folder (2)\New folder (2)\traffic112"
Set-Location $projectPath

# Check if Git LFS is installed
Write-Host "`n📦 Checking Git LFS installation..." -ForegroundColor Yellow
$lfsVersion = git lfs version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Git LFS is not installed. Please install it first." -ForegroundColor Red
    Write-Host "   Download from: https://git-lfs.github.com/" -ForegroundColor Yellow
    exit 1
}
Write-Host "✅ Git LFS is installed: $lfsVersion" -ForegroundColor Green

# Initialize Git repository if not already initialized
if (-not (Test-Path ".git")) {
    Write-Host "`n📁 Initializing Git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "`n✅ Git repository already exists" -ForegroundColor Green
}

# Install Git LFS hooks
Write-Host "`n🔧 Installing Git LFS hooks..." -ForegroundColor Yellow
git lfs install
Write-Host "✅ Git LFS hooks installed" -ForegroundColor Green

# Track tar.gz files
Write-Host "`n📝 Tracking .tar.gz files with Git LFS..." -ForegroundColor Yellow
git lfs track "*.tar.gz"
Write-Host "✅ .tar.gz files will be tracked with Git LFS" -ForegroundColor Green

# Check if model file exists
$modelFile = "ssd_mobilenet_v1_coco_11_06_2017.tar.gz"
if (Test-Path $modelFile) {
    $fileSize = (Get-Item $modelFile).Length / 1MB
    Write-Host "`n📦 Model file found: $modelFile ($([math]::Round($fileSize, 2)) MB)" -ForegroundColor Green
} else {
    Write-Host "`n⚠️  Model file not found: $modelFile" -ForegroundColor Yellow
    Write-Host "   The code will download it automatically on first run." -ForegroundColor Yellow
}

# Add files to Git
Write-Host "`n➕ Adding files to Git..." -ForegroundColor Yellow
git add .gitattributes
if (Test-Path $modelFile) {
    git add $modelFile
    Write-Host "✅ Model file added to Git LFS" -ForegroundColor Green
}
git add .
Write-Host "✅ All files added to Git" -ForegroundColor Green

# Show status
Write-Host "`n📊 Git status:" -ForegroundColor Yellow
git status

Write-Host "`n✅ Setup complete!" -ForegroundColor Green
Write-Host "`n📝 Next steps:" -ForegroundColor Cyan
Write-Host "   1. Connect to your Git remote (GitHub/GitLab/Bitbucket)" -ForegroundColor White
Write-Host "   2. Run: git remote add origin <YOUR_REPO_URL>" -ForegroundColor White
Write-Host "   3. Run: git commit -m 'Add model file with Git LFS'" -ForegroundColor White
Write-Host "   4. Run: git push -u origin main" -ForegroundColor White
Write-Host "`n   Render will automatically deploy when you push to the repository." -ForegroundColor Yellow

