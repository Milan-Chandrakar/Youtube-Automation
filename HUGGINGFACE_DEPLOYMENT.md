# 🚀 Hugging Face Spaces Deployment Guide

This guide walks you through deploying your YouTube Automation System to Hugging Face Spaces.

## Prerequisites

- GitHub account
- Hugging Face account (free at [huggingface.co](https://huggingface.co))
- YouTube Data API key
- (Optional) Gmail app password for email delivery

## Step 1: Prepare Your Repository

### 1.1 Create a GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Create a repository named `youtube-automation`
3. Clone it locally:
```bash
git clone https://github.com/YOUR_USERNAME/youtube-automation.git
cd youtube-automation
```

### 1.2 Push Your Code to GitHub

Copy all your project files to the GitHub repository:

```bash
# Copy your youtube_automation project files here
# Then commit and push
git add .
git commit -m "Initial commit: YouTube automation system"
git push origin main
```

**Important files needed:**
- `app.py` - Gradio interface (already created ✅)
- `main.py` - Pipeline orchestration
- `config.py` - Configuration settings
- `data_collector.py` - YouTube data collection
- `analyzer.py` - Analysis logic
- `report_generator.py` - Report generation
- `email_sender.py` - Email functionality
- `requirements.txt` - Dependencies (updated ✅)

## Step 2: Get API Keys

### 2.1 YouTube Data API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable "YouTube Data API v3"
4. Create an OAuth 2.0 API key
5. Copy your API key (you'll need this in Step 3)

### 2.2 Gmail App Password (Optional)

For email delivery functionality:

1. Enable 2-Factor Authentication on your Google account
2. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Generate an app password for "Mail" and "Windows"
4. Copy the 16-character password (you'll need this in Step 3)

## Step 3: Create Hugging Face Space

### 3.1 Create the Space

1. Go to [huggingface.co/new-space](https://huggingface.co/new-space)
2. Fill in the form:
   - **Owner**: Your username
   - **Space name**: `youtube-automation`
   - **License**: OpenRAIL-M (or your preference)
   - **Space SDK**: Select **Gradio**
   - **Visibility**: Public or Private

3. Click **"Create Space"**

### 3.2 Connect GitHub Repository

In your new Space:

1. Click **"Settings"** (top right)
2. Scroll to **"Linked Repositories"**
3. Connect your GitHub repository by pasting the URL:
   ```
   https://github.com/YOUR_USERNAME/youtube-automation
   ```
4. Click **"Link Repository"**

The Space will automatically deploy from your repository!

### 3.3 Configure Secrets

Your API keys must be added as secrets in the Space:

1. Click **"Settings"** in your Space
2. Scroll down to **"Repository Secrets"**
3. Add these secrets:

| Secret Name | Value | Required |
|---|---|---|
| `YOUTUBE_API_KEY` | Your YouTube API key from Step 2.1 | ✅ Yes |
| `GMAIL_APP_PASSWORD` | Your Gmail app password from Step 2.2 | ❌ Optional |
| `GMAIL_RECIPIENT` | Email address to send reports to | ❌ Optional |
| `GMAIL_SENDER_EMAIL` | Your Gmail address | ❌ Optional |

**Example:**
```
YOUTUBE_API_KEY = AIzaSyD-1234567890ABCDEFGHIJKLMNOPQRSTUv
GMAIL_APP_PASSWORD = abcd efgh ijkl mnop
GMAIL_RECIPIENT = recipient@example.com
GMAIL_SENDER_EMAIL = your-email@gmail.com
```

## Step 4: Deploy & Test

### 4.1 Automatic Deployment

Once you connect GitHub, Hugging Face will automatically:
1. Pull your code
2. Install dependencies from `requirements.txt`
3. Run `app.py` with Gradio
4. Host it at: `https://huggingface.co/spaces/YOUR_USERNAME/youtube-automation`

### 4.2 Monitor Deployment

1. Go to your Space
2. Check the **"Logs"** tab to see build progress
3. Wait for "Building" status to complete

### 4.3 Test Your Space

1. Once deployed, your Space will have a UI at the top
2. Enter a search query (e.g., "AI automation")
3. Click **"Run Analysis"**
4. Check the output for results

## Step 5: Updates & Maintenance

### Push Updates to GitHub

When you make changes locally:

```bash
git add .
git commit -m "Description of changes"
git push origin main
```

**The Space automatically redeploys** when you push to GitHub!

### View Logs

To debug issues:
1. Open your Space
2. Click the **"Logs"** tab
3. Scroll to see error messages

## Troubleshooting

### Issue: "API Key not configured"
- **Fix**: Make sure `YOUTUBE_API_KEY` is set in Space secrets
- Go to Settings → Repository Secrets and verify the key is there

### Issue: Data collection is slow
- **Reason**: YouTube API has rate limits (10,000 units/day)
- Normal operation: 50 videos ≈ 2,500 API units
- **Fix**: Adjust `MAX_VIDEOS_PER_SEARCH` in config.py

### Issue: Email not sending
- **Fix**: Ensure Gmail app password is correct and 2FA is enabled
- **Fix**: Check `GMAIL_SENDER_EMAIL` and `GMAIL_RECIPIENT` are configured

### Issue: Space times out
- **Reason**: Large data collection with many videos
- **Fix**: Reduce `MAX_VIDEOS_PER_SEARCH` in config.py
- **Fix**: Use shorter `DAYS_BACK` period

## Space Specifications

- **CPU**: 2 vCPU
- **RAM**: 16 GB
- **Storage**: 50 GB ephemeral (resets on restart)
- **Free tier**: Suspended after 7 days of inactivity

To keep your Space active:
- Use it regularly, OR
- Upgrade to paid tier for persistent hosting

## Advanced Options

### Custom Domain
To use your own domain (paid feature):
1. Go to Space Settings
2. Click **"Custom Domain"**
3. Follow instructions

### Persistent Storage
For databases and files that persist across restarts (paid feature):
1. Contact Hugging Face support

## Example API Usage

Once deployed, you can call your Space programmatically:

```python
import requests

response = requests.post(
    "https://huggingface.co/api/spaces/YOUR_USERNAME/youtube-automation/run",
    json={
        "data": ["AI automation", False]  # query, send_email
    }
)
print(response.json())
```

## Next Steps

1. ✅ Push code to GitHub
2. ✅ Create Hugging Face Space
3. ✅ Add secrets (API keys)
4. ✅ Test the interface
5. 📊 Share with others: `https://huggingface.co/spaces/YOUR_USERNAME/youtube-automation`

---

**Need help?**
- [Hugging Face Spaces Documentation](https://huggingface.co/docs/hub/spaces)
- [Gradio Documentation](https://www.gradio.app/docs)
- Check Space Logs for error messages
