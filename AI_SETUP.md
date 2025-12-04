# AI Setup Guide

## The Problem

The app was returning mock/dummy data because it wasn't connected to a real AI model. Now it's configured to use **real AI providers**!

## Supported AI Providers

Choose one of these providers:

### 1. **OpenAI (GPT-3.5/GPT-4)** - Recommended
- **Cost:** ~$0.002 per request (GPT-3.5-turbo)
- **Speed:** Fast (2-5 seconds)
- **Quality:** Excellent
- **Setup:** Easy

### 2. **Groq (Llama 3)** - Fast & Cheap
- **Cost:** FREE (with limits)
- **Speed:** Very fast (1-2 seconds)
- **Quality:** Very good
- **Setup:** Easy

### 3. **Anthropic (Claude)**
- **Cost:** ~$0.003 per request
- **Speed:** Fast (2-5 seconds)
- **Quality:** Excellent
- **Setup:** Easy

## Quick Setup (Recommended: Groq)

### Option 1: Groq (FREE & FAST) ⚡

1. **Get API Key:**
   - Go to [console.groq.com](https://console.groq.com)
   - Sign up (free)
   - Create an API key

2. **Configure Streamlit Cloud:**
   - Go to your app on Streamlit Cloud
   - Click "Settings" → "Secrets"
   - Add:
   ```toml
   AI_PROVIDER = "groq"
   GROQ_API_KEY = "your-groq-api-key-here"
   GROQ_MODEL = "llama-3.1-70b-versatile"
   ```

3. **Redeploy** - Your app will restart automatically!

### Option 2: OpenAI (Most Popular)

1. **Get API Key:**
   - Go to [platform.openai.com](https://platform.openai.com)
   - Sign up and add payment method
   - Create an API key

2. **Configure Streamlit Cloud:**
   - Go to your app on Streamlit Cloud
   - Click "Settings" → "Secrets"
   - Add:
   ```toml
   AI_PROVIDER = "openai"
   OPENAI_API_KEY = "sk-your-openai-key-here"
   OPENAI_MODEL = "gpt-3.5-turbo"
   ```

3. **Redeploy** - Your app will restart automatically!

### Option 3: Anthropic (Claude)

1. **Get API Key:**
   - Go to [console.anthropic.com](https://console.anthropic.com)
   - Sign up and add payment method
   - Create an API key

2. **Configure Streamlit Cloud:**
   - Go to your app on Streamlit Cloud
   - Click "Settings" → "Secrets"
   - Add:
   ```toml
   AI_PROVIDER = "anthropic"
   ANTHROPIC_API_KEY = "your-anthropic-key-here"
   ANTHROPIC_MODEL = "claude-3-sonnet-20240229"
   ```

3. **Redeploy** - Your app will restart automatically!

## Local Development Setup

### For Groq (Recommended):

1. **Install package:**
   ```bash
   pip install groq
   ```

2. **Create `.env` file:**
   ```bash
   AI_PROVIDER=groq
   GROQ_API_KEY=your-groq-api-key-here
   GROQ_MODEL=llama-3.1-70b-versatile
   ```

3. **Run app:**
   ```bash
   streamlit run streamlit_app.py
   ```

### For OpenAI:

1. **Install package:**
   ```bash
   pip install openai
   ```

2. **Create `.env` file:**
   ```bash
   AI_PROVIDER=openai
   OPENAI_API_KEY=sk-your-key-here
   OPENAI_MODEL=gpt-3.5-turbo
   ```

3. **Run app:**
   ```bash
   streamlit run streamlit_app.py
   ```

## Cost Comparison

### Groq (FREE Tier):
- **Free requests:** 30 requests/minute
- **Cost:** $0 (free tier)
- **Best for:** Students, testing, low-volume use

### OpenAI GPT-3.5-turbo:
- **Cost:** ~$0.002 per request
- **Monthly estimate:** $2-5 for moderate use
- **Best for:** Production, high quality

### OpenAI GPT-4:
- **Cost:** ~$0.03 per request
- **Monthly estimate:** $30-50 for moderate use
- **Best for:** Maximum quality

## Recommended Models

### For Speed (Groq):
```toml
AI_PROVIDER = "groq"
GROQ_MODEL = "llama-3.1-70b-versatile"
```

### For Balance (OpenAI):
```toml
AI_PROVIDER = "openai"
OPENAI_MODEL = "gpt-3.5-turbo"
```

### For Quality (OpenAI):
```toml
AI_PROVIDER = "openai"
OPENAI_MODEL = "gpt-4"
```

## Testing Your Setup

1. **Deploy with AI configured**
2. **Upload a PDF**
3. **Click "Detect Topics"**
4. **Check if topics are relevant to your PDF** ✅
5. **Generate a mind map**
6. **Check if mind map matches your topic** ✅

## Troubleshooting

### Error: "API key not set"
**Solution:** Add your API key to Streamlit Cloud secrets

### Error: "Package not installed"
**Solution:** The package should auto-install from requirements.txt. Check deployment logs.

### Topics are still generic
**Solution:** 
1. Check that secrets are set correctly
2. Redeploy the app
3. Clear browser cache

### AI responses are slow
**Expected:** 
- Groq: 1-3 seconds
- OpenAI: 2-5 seconds
- Large PDFs: 5-15 seconds

### Rate limit errors
**Solution:**
- Groq: Wait a minute (30 req/min limit)
- OpenAI: Upgrade your plan or wait

## Security Notes

⚠️ **Never commit API keys to GitHub!**

✅ **Always use:**
- Streamlit Cloud Secrets for deployment
- `.env` file for local (add to `.gitignore`)

## What Changed

### Before (Mock AI):
```python
def llm(prompt):
    return json.dumps(["Generic Topic 1", "Generic Topic 2"])
```

### After (Real AI):
```python
def llm(prompt):
    # Calls OpenAI/Groq/Anthropic
    # Returns actual analysis of your PDF!
    return ai_provider.generate(prompt)
```

## Next Steps

1. ✅ Choose an AI provider (Groq recommended for free)
2. ✅ Get API key
3. ✅ Add to Streamlit Cloud secrets
4. ✅ Redeploy
5. ✅ Test with your PDF
6. ✅ Enjoy real AI-powered mind maps! 🎉

---

**Your app will now actually analyze your PDFs and generate relevant mind maps!** 🚀
