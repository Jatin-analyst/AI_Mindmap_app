# Deployment Guide for Streamlit Cloud

## 🚀 Quick Deploy

Your app is now **standalone** and ready to deploy to Streamlit Cloud without any backend setup!

## Prerequisites

1. GitHub account
2. Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))
3. Your code pushed to a GitHub repository

## Step-by-Step Deployment

### 1. Prepare Your Repository

Make sure these files are in your repo:
- ✅ `streamlit_app.py` (standalone version)
- ✅ `requirements.txt` (Python dependencies)
- ✅ `packages.txt` (system dependencies for PDF processing)
- ✅ `blocks/` directory (all processing modules)
- ✅ `utils/` directory (utility modules)

### 2. Push to GitHub

```bash
git add .
git commit -m "Deploy PDF Mind Map Generator"
git push origin main
```

### 3. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **"New app"**
4. Fill in the form:
   - **Repository:** Select your GitHub repo
   - **Branch:** `main` (or your branch name)
   - **Main file path:** `streamlit_app.py`
5. Click **"Deploy!"**

### 4. Wait for Deployment

Streamlit Cloud will:
- Clone your repository
- Install Python packages from `requirements.txt`
- Install system packages from `packages.txt` (poppler-utils for PDF)
- Start your app

This usually takes 2-5 minutes.

### 5. Your App is Live! 🎉

You'll get a URL like: `https://your-app-name.streamlit.app`

## Troubleshooting

### Issue: "Module not found" errors

**Solution:** Make sure all required packages are in `requirements.txt`:
```
fastapi>=0.104.0
pdfplumber>=0.10.0
hypothesis>=6.92.0
streamlit>=1.28.0
reportlab>=4.0.0
```

### Issue: PDF processing fails

**Solution:** Ensure `packages.txt` contains:
```
poppler-utils
```

This installs system-level PDF tools needed by pdfplumber.

### Issue: Import errors for blocks/utils

**Solution:** Make sure your directory structure is correct:
```
your-repo/
├── streamlit_app.py
├── requirements.txt
├── packages.txt
├── blocks/
│   ├── __init__.py
│   ├── extract_pdf.py
│   ├── detect_topics.py
│   ├── filter_topic_text.py
│   └── generate_mindmap.py
└── utils/
    ├── __init__.py
    ├── ai_helper.py
    ├── validation.py
    ├── file_manager.py
    └── error_handler.py
```

### Issue: App is slow or times out

**Possible causes:**
1. Large PDF files (>10MB) take longer to process
2. AI processing can take 10-30 seconds
3. Streamlit Cloud free tier has resource limits

**Solutions:**
- Use smaller PDFs for testing
- Be patient with AI processing
- Consider upgrading to Streamlit Cloud paid tier for better performance

## Configuration

### Environment Variables (Optional)

If you need to configure the app, go to:
1. Your app dashboard on Streamlit Cloud
2. Click "Settings" → "Secrets"
3. Add any environment variables

Example:
```toml
TEMP_DIR = "./temp"
MAX_FILE_SIZE = 83886080
```

## Updating Your App

To update your deployed app:

1. Make changes locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update app"
   git push origin main
   ```
3. Streamlit Cloud will automatically redeploy!

## Monitoring

- View logs in the Streamlit Cloud dashboard
- Check app status and resource usage
- See deployment history

## Local vs Cloud Differences

### Local Development:
- Can run with separate FastAPI backend
- Use `streamlit_app_api.py` for API mode
- Full control over resources

### Streamlit Cloud:
- Runs standalone (no separate backend)
- Uses `streamlit_app.py`
- Shared resources (free tier)
- Automatic HTTPS
- Easy sharing with URL

## Best Practices

1. **Test locally first:**
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Keep dependencies minimal:**
   - Only include packages you actually use
   - Specify version ranges for stability

3. **Handle errors gracefully:**
   - The app already has error handling
   - Users will see friendly error messages

4. **Monitor usage:**
   - Check Streamlit Cloud dashboard
   - Watch for resource limits

5. **Keep PDFs reasonable:**
   - Recommend users upload PDFs < 20MB
   - Larger files work but take longer

## Support

- Streamlit Docs: [docs.streamlit.io](https://docs.streamlit.io)
- Streamlit Community: [discuss.streamlit.io](https://discuss.streamlit.io)
- GitHub Issues: Your repo's issues page

## Success! 🎊

Your PDF Mind Map Generator is now live and accessible to anyone with the URL!

Share it with:
- Classmates
- Study groups
- Social media
- Your portfolio

Happy mind mapping! 🧠✨
