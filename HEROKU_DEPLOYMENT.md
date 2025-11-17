# Heroku Deployment Guide

## Slug Size Optimization

This project has been optimized to reduce the Heroku slug size below the 500MB limit.

### Optimizations Applied

1. **`.slugignore` file**: Excludes unnecessary files from the slug:
   - Test files and test utilities
   - Documentation files (except README.md)
   - Docker files and deployment scripts
   - Jupyter notebooks
   - Model files (downloaded at runtime)
   - Development files and caches

2. **TensorFlow Version**: Using `tensorflow-cpu==2.8.0` instead of 2.11.0 for a smaller footprint

3. **Minimal Dependencies**: Only essential packages are included in `requirements-heroku.txt`

4. **Environment Variables**: Set in `app.json` to optimize TensorFlow:
   - `TF_DISABLE_MKL=1`: Disables Intel MKL to reduce size
   - `TF_CPP_MIN_LOG_LEVEL=2`: Reduces logging overhead

### Deployment Steps

1. **Ensure you have the required files**:
   - `Procfile` - Defines the web process
   - `requirements-heroku.txt` - Heroku-specific dependencies
   - `.slugignore` - Excludes files from slug
   - `app.json` - Heroku app configuration (optional)

2. **Set environment variables** (via Heroku dashboard or CLI):
   ```bash
   heroku config:set TF_DISABLE_MKL=1
   heroku config:set TF_CPP_MIN_LOG_LEVEL=2
   ```

3. **Deploy to Heroku**:
   ```bash
   git add .
   git commit -m "Optimize for Heroku deployment"
   git push heroku main
   ```

### If Slug Size Still Exceeds 500MB

If the slug size is still too large, consider:

1. **Use TensorFlow Lite**: Convert the model to TensorFlow Lite format (requires code changes)

2. **Use External Model Storage**: Store models in S3/Cloud Storage and download at runtime

3. **Use Docker Deployment**: Deploy using Docker instead of Heroku's buildpack (no slug size limit)

4. **Upgrade Heroku Plan**: Some Heroku plans have higher slug size limits

5. **Remove More Dependencies**: Review if all utils files are needed, or if some can be removed

### Troubleshooting

- **Build fails with "slug too large"**: Check `.slugignore` is working, verify no large files are being included
- **Model download fails**: The model is downloaded at runtime, ensure network access is available
- **Memory issues**: Heroku free tier has 512MB RAM limit, consider upgrading

### Alternative: Use Docker on Heroku

If slug size continues to be an issue, consider using Heroku Container Registry:

```bash
heroku container:push web
heroku container:release web
```

This bypasses the slug size limit entirely.

