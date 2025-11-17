# Heroku Slug Size Optimization - Final Steps

## Current Status
- **Initial slug size**: 862.9M
- **After first optimization**: 609.6M
- **Target**: < 500M
- **Still need to reduce**: ~110MB

## Changes Applied

### 1. TensorFlow Version
- Changed from `tensorflow==2.8.0` to `tensorflow-cpu==2.6.0`
- CPU-only version is significantly smaller
- TensorFlow 2.6.0 is smaller than 2.8.0

### 2. `.slugignore` Optimizations
- Removed all wildcard patterns that could affect TensorFlow
- Added specific exclusions for numpy, scipy, pandas examples
- Excluded more documentation and test files from non-TensorFlow packages

## Additional Steps to Reduce Slug Size

### Step 1: Purge Heroku Build Cache
The build cache can accumulate over time. Clear it:

```bash
heroku plugins:install heroku-repo
heroku repo:purge_cache --app your-app-name
```

Then redeploy:
```bash
git push heroku main
```

### Step 2: Verify TensorFlow 2.6.0 Compatibility
Test locally first to ensure TensorFlow 2.6.0 works with your code:

```bash
pip install tensorflow-cpu==2.6.0
python main.py
```

### Step 3: If Still Over 500MB - Consider Alternatives

#### Option A: Use Docker Deployment (No Slug Limit)
```bash
# Create Dockerfile
# Then deploy with:
heroku container:push web
heroku container:release web
```

#### Option B: Use External Model Storage
- Store TensorFlow models in S3/Cloud Storage
- Download models at runtime instead of including in slug
- This could save 50-100MB

#### Option C: Upgrade Heroku Plan
- Some paid Heroku plans have higher slug size limits
- Check: https://devcenter.heroku.com/articles/slug-compiler#slug-size-limits

#### Option D: Use TensorFlow Lite (Requires Code Changes)
- Convert model to TensorFlow Lite format
- Much smaller footprint (~10-20MB vs 200-300MB)
- Requires code modifications

### Step 4: Monitor Slug Size
After deploying, check the slug size:

```bash
heroku run du -sh /app
```

Or check in Heroku dashboard under "Metrics" → "Slug Size"

## Expected Results

With TensorFlow 2.6.0 CPU-only:
- TensorFlow package: ~200-250MB (vs ~300-350MB for 2.8.0)
- Excluded files: ~50-80MB saved
- **Expected final size**: ~450-480MB (should be under 500MB)

## Troubleshooting

If you still get "slug too large" error:
1. Check if build cache was purged
2. Verify TensorFlow 2.6.0 is actually being used (check build logs)
3. Consider removing more dependencies if not essential
4. Use Docker deployment as a workaround

## Next Deployment

```bash
git add requirements.txt .slugignore
git commit -m "Optimize for Heroku: TensorFlow 2.6.0 CPU-only, aggressive exclusions"
git push heroku main
```

