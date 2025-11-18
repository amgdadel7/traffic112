# Script to connect local project to GitHub repository
# Repository: https://github.com/amgdadel7/traffic112.git

Write-Host "🔗 Connecting to GitHub repository..." -ForegroundColor Green

$repoUrl = "https://github.com/amgdadel7/traffic112.git"
$projectPath = "d:\New folder (2)\New folder (2)\traffic112"

# Navigate to project directory
Set-Location $projectPath

# Check if Git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "`n📁 Initializing Git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "`n✅ Git repository already exists" -ForegroundColor Green
}

# Check current remote
Write-Host "`n🔍 Checking current remote configuration..." -ForegroundColor Yellow
$currentRemote = git remote get-url origin 2>&1

if ($LASTEXITCODE -eq 0) {
    if ($currentRemote -eq $repoUrl) {
        Write-Host "✅ Already connected to: $repoUrl" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Current remote: $currentRemote" -ForegroundColor Yellow
        Write-Host "🔄 Updating remote to: $repoUrl" -ForegroundColor Yellow
        git remote set-url origin $repoUrl
        Write-Host "✅ Remote updated" -ForegroundColor Green
    }
} else {
    Write-Host "➕ Adding remote origin..." -ForegroundColor Yellow
    git remote add origin $repoUrl
    Write-Host "✅ Remote added: $repoUrl" -ForegroundColor Green
}

# Check if Git LFS is needed for the model file
Write-Host "`n📦 Checking for large files..." -ForegroundColor Yellow
$modelFile = "ssd_mobilenet_v1_coco_11_06_2017.tar.gz"
if (Test-Path $modelFile) {
    $fileSize = (Get-Item $modelFile).Length / 1MB
    Write-Host "📦 Model file found: $modelFile ($([math]::Round($fileSize, 2)) MB)" -ForegroundColor Cyan
    
    if ($fileSize -gt 50) {
        Write-Host "⚠️  Large file detected! Consider using Git LFS" -ForegroundColor Yellow
        Write-Host "   Run: git lfs install" -ForegroundColor White
        Write-Host "   Run: git lfs track '*.tar.gz'" -ForegroundColor White
    }
}

# Show current status
Write-Host "`n📊 Current Git status:" -ForegroundColor Yellow
git status

Write-Host "`n✅ Setup complete!" -ForegroundColor Green
Write-Host "`n📝 Next steps to push to GitHub:" -ForegroundColor Cyan
Write-Host "   1. Add files: git add ." -ForegroundColor White
Write-Host "   2. Commit: git commit -m 'Update project'" -ForegroundColor White
Write-Host "   3. Push: git push -u origin main" -ForegroundColor White
Write-Host "`n   Or if you want to pull from GitHub first:" -ForegroundColor Yellow
Write-Host "   git pull origin main --allow-unrelated-histories" -ForegroundColor White

