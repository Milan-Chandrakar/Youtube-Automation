# ⚡ Quick Start: Deploy to Hugging Face in 5 Minutes

## ✅ What Was Set Up

These files have been created/updated for you:

1. **`app.py`** - Gradio web interface (ready to deploy)
2. **`requirements.txt`** - Updated with `gradio>=4.0.0`
3. **`HUGGINGFACE_DEPLOYMENT.md`** - Full deployment guide

## 🚀 Deploy Now (Quick Version)

### Step 1: Push to GitHub (2 min)

```bash
cd e:\VScode\youtube_automation

# Initialize git (if not already done)
git init
git add .
git commit -m "Add Hugging Face Spaces deployment files"
git remote add origin https://github.com/YOUR_USERNAME/youtube-automation.git
git push -u origin main
```

### Step 2: Create Hugging Face Space (1 min)

1. Go to: https://huggingface.co/new-space
2. Fill form:
   - **Space name**: `youtube-automation`
   - **SDK**: Choose **Gradio**
   - Click **Create Space**

### Step 3: Connect GitHub (1 min)

In your Space:
1. Click **Settings**
2. → **Linked Repositories**
3. Paste: `https://github.com/YOUR_USERNAME/youtube-automation`
4. Click **Link**

✅ **Automatic deployment starts!**

### Step 4: Add Secrets (1 min)

In your Space Settings → **Repository Secrets**, add:

```
YOUTUBE_API_KEY = [Your YouTube API key]
GMAIL_APP_PASSWORD = [Optional: Gmail app password]
GMAIL_RECIPIENT = [Optional: recipient@example.com]
```

Get API keys:
- YouTube: https://console.cloud.google.com/ → YouTube Data API v3
- Gmail: https://myaccount.google.com/apppasswords

## 🎉 Done!

Your Space will be live at:
```
https://huggingface.co/spaces/YOUR_USERNAME/youtube-automation
```

**Test it:**
1. Enter a search query (e.g., "AI automation")
2. Click "Run Analysis"
3. Download your report!

---

## 📖 Full Details

See [HUGGINGFACE_DEPLOYMENT.md](HUGGINGFACE_DEPLOYMENT.md) for:
- Detailed setup instructions with screenshots
- Troubleshooting guide
- Advanced features
- API usage examples

## 💡 Tips

- **Keep it active**: Space auto-suspends after 7 days of inactivity
- **Share it**: Just send the Hugging Face URL to anyone!
- **Update**: Push changes to GitHub → Space auto-redeploys
- **Monitor**: Check Logs tab if something goes wrong

---

**Next**: Follow the steps above, then open your Space URL! 🎬
