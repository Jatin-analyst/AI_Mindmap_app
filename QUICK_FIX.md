# 🚀 QUICK FIX - Get Real AI Working in 5 Minutes

## The Problem
Your app works but returns **generic/mock data** instead of analyzing your actual PDF.

## The Solution
Add a FREE AI API key to Streamlit Cloud!

---

## 3 Simple Steps:

### 1️⃣ Get FREE Groq API Key (2 minutes)

**Go to:** [console.groq.com](https://console.groq.com)

1. Sign up (FREE, no credit card)
2. Click "API Keys"
3. Click "Create API Key"
4. **Copy the key** (starts with `gsk_...`)

---

### 2️⃣ Add to Streamlit Cloud (2 minutes)

**Go to:** Your app on [share.streamlit.io](https://share.streamlit.io)

1. Click **⚙️ Settings** (top right)
2. Click **Secrets** (left menu)
3. **Paste this:**

```toml
AI_PROVIDER = "groq"
GROQ_API_KEY = "gsk_paste_your_actual_key_here"
GROQ_MODEL = "llama-3.1-70b-versatile"
```

4. Replace `gsk_paste_your_actual_key_here` with your real key
5. Click **Save**

---

### 3️⃣ Test (1 minute)

1. Wait for app to redeploy (1-2 minutes)
2. Upload a PDF
3. Click "Detect Topics"
4. **See real topics from your PDF!** ✅

---

## Before vs After

### ❌ Before (Mock Data):
```
Topics: Introduction, Background, Methodology...
(Same for every PDF)
```

### ✅ After (Real AI):
```
Topics: Machine Learning Algorithms, Neural Networks, 
Deep Learning Applications...
(Actual topics from YOUR PDF!)
```

---

## Why Groq?

- ✅ **100% FREE** (no credit card)
- ✅ **Super FAST** (1-2 seconds)
- ✅ **High Quality** (Llama 3.1 70B)
- ✅ **Easy Setup** (just sign up)

---

## Alternative: OpenAI

If you prefer OpenAI (costs ~$0.002/request):

1. Get key from [platform.openai.com](https://platform.openai.com)
2. In Streamlit Secrets:

```toml
AI_PROVIDER = "openai"
OPENAI_API_KEY = "sk-your-key-here"
OPENAI_MODEL = "gpt-3.5-turbo"
```

---

## That's It!

Your app will now:
- 🎯 Extract **real topics** from PDFs
- 🗺️ Generate **accurate mind maps**
- ⚡ Process in **2-5 seconds**
- 🎉 Work like **magic**!

---

## Need More Help?

- 📖 Full guide: `AI_SETUP.md`
- 🔑 Secrets setup: `STREAMLIT_SECRETS_SETUP.md`
- 🚀 Deployment: `DEPLOYMENT.md`

---

**Your app is almost perfect - just needs this one API key!** 🔑✨
