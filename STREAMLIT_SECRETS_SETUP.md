# 🔑 Streamlit Cloud Secrets Setup

## Quick Fix for AI Integration

Your app is working but returning generic results because it needs an AI API key!

## Step-by-Step Setup (5 minutes)

### Step 1: Get a FREE Groq API Key

1. Go to [console.groq.com](https://console.groq.com)
2. Click "Sign Up" (it's FREE!)
3. Verify your email
4. Click "API Keys" in the left sidebar
5. Click "Create API Key"
6. Copy your API key (starts with `gsk_...`)

### Step 2: Add to Streamlit Cloud

1. Go to your app on [share.streamlit.io](https://share.streamlit.io)
2. Click on your app
3. Click the **"⚙️ Settings"** button (top right)
4. Click **"Secrets"** in the left menu
5. Paste this into the secrets box:

```toml
AI_PROVIDER = "groq"
GROQ_API_KEY = "gsk_your_actual_key_here"
GROQ_MODEL = "llama-3.1-70b-versatile"
```

6. Replace `gsk_your_actual_key_here` with your actual Groq API key
7. Click **"Save"**

### Step 3: Redeploy

Your app will automatically restart with the new configuration!

Wait 1-2 minutes for the app to redeploy.

### Step 4: Test

1. Upload a PDF
2. Click "Detect Topics"
3. **Topics should now be relevant to your PDF!** ✅
4. Select a topic and generate mind map
5. **Mind map should now match your content!** ✅

## Visual Guide

### Where to find Settings:
```
Your App Dashboard
├── [Your App Name]
│   ├── ⚙️ Settings  ← Click here
│   │   ├── General
│   │   ├── Secrets  ← Then click here
│   │   └── ...
```

### What to paste in Secrets:
```toml
# Copy this exactly, but replace the API key
AI_PROVIDER = "groq"
GROQ_API_KEY = "gsk_paste_your_key_here"
GROQ_MODEL = "llama-3.1-70b-versatile"
```

## Alternative: OpenAI (if you prefer)

If you want to use OpenAI instead:

1. Get API key from [platform.openai.com](https://platform.openai.com)
2. Add payment method (costs ~$0.002 per request)
3. Create API key
4. In Streamlit Secrets, paste:

```toml
AI_PROVIDER = "openai"
OPENAI_API_KEY = "sk-your-openai-key-here"
OPENAI_MODEL = "gpt-3.5-turbo"
```

## Why Groq is Recommended

✅ **FREE** - No credit card needed
✅ **FAST** - 1-2 second responses
✅ **GOOD QUALITY** - Uses Llama 3.1 70B
✅ **EASY** - Just sign up and get key
✅ **GENEROUS** - 30 requests/minute free

## Verification

After setup, your app should:
- ✅ Extract actual topics from your PDF
- ✅ Generate relevant mind maps
- ✅ Filter content accurately
- ✅ Respond in 2-5 seconds

## Troubleshooting

### "API key not set" error
- Check that you saved the secrets
- Make sure there are no extra spaces
- Redeploy the app

### Still getting generic results
- Clear your browser cache
- Try a different PDF
- Check the secrets are saved correctly
- Wait for full redeploy (2-3 minutes)

### Rate limit errors
- Groq free tier: 30 requests/minute
- Wait a minute and try again
- Or upgrade to paid tier

## Security

✅ **Safe:** Secrets are encrypted by Streamlit
✅ **Private:** Only your app can access them
✅ **Secure:** Never visible in logs or code

❌ **Never:** Commit API keys to GitHub!

## Cost Estimate

### Groq (FREE):
- **Cost:** $0
- **Limit:** 30 requests/minute
- **Perfect for:** Students, personal use

### OpenAI (Paid):
- **Cost:** ~$0.002 per request
- **Monthly:** $2-5 for moderate use
- **Perfect for:** Production apps

## Done! 🎉

Your app should now:
1. Actually read your PDFs
2. Extract real topics
3. Generate accurate mind maps
4. Work like magic! ✨

---

**Need help?** Check `AI_SETUP.md` for more details!
