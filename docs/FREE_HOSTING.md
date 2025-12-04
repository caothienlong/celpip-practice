# 🌐 Free Hosting Options for CELPIP Practice Platform

## Overview

This guide covers the best **free** hosting options for deploying your CELPIP Practice Test Platform online.

---

## 🏆 Top Free Hosting Recommendations

### 1. **Render.com** ⭐ BEST CHOICE

**Why It's Great:**
- ✅ **Free tier** with 750 hours/month
- ✅ **Easy deployment** from GitHub
- ✅ **Automatic HTTPS**
- ✅ **Python/Flask native support**
- ✅ **Auto-deploy** on git push
- ✅ **Good performance**
- ✅ **No credit card** required

**Limitations:**
- ⚠️ Spins down after 15 min inactivity (cold starts)
- ⚠️ 512 MB RAM
- ⚠️ Shared CPU

**Best For:** Production-ready deployment

**Setup Time:** 5-10 minutes

---

### 2. **PythonAnywhere** ⭐ RUNNER UP

**Why It's Great:**
- ✅ **Python-focused** hosting
- ✅ **Always-on** free tier
- ✅ **Web-based console**
- ✅ **Easy file upload**
- ✅ **Good documentation**
- ✅ **No cold starts**

**Limitations:**
- ⚠️ Only 1 web app on free tier
- ⚠️ 512 MB storage
- ⚠️ Limited daily CPU seconds
- ⚠️ Restricted internet access (whitelist only)
- ⚠️ Must manually update (no auto-deploy)

**Best For:** Simple, stable deployment

**Setup Time:** 10-15 minutes

---

### 3. **Fly.io**

**Why It's Great:**
- ✅ **Generous free tier**
- ✅ **Global CDN**
- ✅ **No cold starts**
- ✅ **Excellent performance**
- ✅ **Docker-based** (flexible)

**Limitations:**
- ⚠️ Requires credit card
- ⚠️ 3 GB persistent volume (per app)
- ⚠️ More complex setup

**Best For:** Advanced users

**Setup Time:** 15-20 minutes

---

### 4. **Railway.app**

**Why It's Great:**
- ✅ **$5/month free credit**
- ✅ **GitHub integration**
- ✅ **Auto-deploy**
- ✅ **Easy setup**
- ✅ **Good dashboard**

**Limitations:**
- ⚠️ Limited free hours (~500 hrs/month)
- ⚠️ Credit card required after trial
- ⚠️ May exceed free tier quickly

**Best For:** Short-term or low-traffic apps

**Setup Time:** 5-10 minutes

---

### 5. **Heroku** (Free tier ending, but worth mentioning)

**Status:** ⚠️ No longer offers free tier (as of Nov 2022)

**Alternative:** Use Heroku's paid tier ($5-7/month) if you need reliability

---

## 📊 Comparison Table

| Platform | Free Tier | Cold Starts | Persistent Storage | Auto-Deploy | Credit Card | Setup |
|----------|-----------|-------------|-------------------|-------------|-------------|-------|
| **Render** | ✅ 750 hrs | Yes (15 min) | Limited | ✅ Yes | No | Easy |
| **PythonAnywhere** | ✅ Always-on | No | 512 MB | No | No | Easy |
| **Fly.io** | ✅ Good | No | 3 GB | ✅ Yes | Yes | Medium |
| **Railway** | ✅ $5 credit | Rare | Good | ✅ Yes | Yes | Easy |

---

## 🚀 Deployment Guide: Render.com (Recommended)

### Step 1: Prepare Your Repository

Ensure these files exist in your GitHub repo:

**`requirements.txt`** (already have it):
```txt
Flask==3.0.0
Werkzeug==3.0.0
```

**`render.yaml`** (create new file):
```yaml
services:
  - type: web
    name: celpip-practice
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "gunicorn app:app"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: FLASK_HOST
        value: 0.0.0.0
```

**Update `requirements.txt`** to include gunicorn:
```txt
Flask==3.0.0
Werkzeug==3.0.0
gunicorn==21.2.0
```

### Step 2: Sign Up for Render

1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub account

### Step 3: Create New Web Service

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `celpip-practice`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Plan**: Free

### Step 4: Deploy

1. Click "Create Web Service"
2. Wait 2-5 minutes for deployment
3. Your app will be live at: `https://celpip-practice.onrender.com`

### Step 5: Enable Auto-Deploy

In Render dashboard:
1. Go to Settings
2. Enable "Auto-Deploy" from GitHub
3. Every git push will automatically deploy!

---

## 🚀 Deployment Guide: PythonAnywhere

### Step 1: Sign Up

1. Go to https://www.pythonanywhere.com
2. Create free "Beginner" account
3. Verify email

### Step 2: Upload Your Code

**Option A: Git Clone**
```bash
# In PythonAnywhere Bash console
git clone https://github.com/YOUR_USERNAME/celpip-practice.git
cd celpip-practice
```

**Option B: Upload ZIP**
1. Zip your project locally
2. Upload via Files tab
3. Unzip in console

### Step 3: Install Dependencies

```bash
# Create virtual environment
mkvirtualenv --python=/usr/bin/python3.10 myenv

# Install requirements
pip install -r requirements.txt
```

### Step 4: Configure Web App

1. Go to "Web" tab
2. Click "Add a new web app"
3. Select "Manual configuration"
4. Choose Python 3.10
5. Set these paths:
   - **Source code**: `/home/YOUR_USERNAME/celpip-practice`
   - **Working directory**: `/home/YOUR_USERNAME/celpip-practice`
   - **Virtualenv**: `/home/YOUR_USERNAME/.virtualenvs/myenv`

### Step 5: Edit WSGI File

In WSGI configuration file, replace everything with:
```python
import sys
import os

# Add your project directory
path = '/home/YOUR_USERNAME/celpip-practice'
if path not in sys.path:
    sys.path.append(path)

# Set environment variables
os.environ['FLASK_HOST'] = '0.0.0.0'

from app import app as application
```

### Step 6: Reload & Test

1. Click "Reload" button
2. Visit: `https://YOUR_USERNAME.pythonanywhere.com`

---

## 🔧 Deployment Preparation Checklist

Before deploying to any platform:

### 1. **Update `app.py`** for Production

```python
if __name__ == '__main__':
    import os
    
    # Production-safe defaults
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    
    app.run(host=host, port=port, debug=debug)
```

### 2. **Add Production Dependencies**

Update `requirements.txt`:
```txt
Flask==3.0.0
Werkzeug==3.0.0
gunicorn==21.2.0  # For production
```

### 3. **Set Environment Variables**

On hosting platform, set:
```
FLASK_DEBUG=False
FLASK_HOST=0.0.0.0
PORT=5000  # Usually auto-set
```

### 4. **Security Considerations**

```python
# In app.py, update secret key
import os

app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(16))
```

Set `SECRET_KEY` in environment:
```bash
# Generate a secure key
python -c "import secrets; print(secrets.token_hex(32))"
```

### 5. **Test Locally First**

```bash
# Test with gunicorn locally
gunicorn app:app --bind 0.0.0.0:5000

# Visit http://localhost:5000
```

---

## ⚠️ Important Considerations

### Storage Limitations

**Problem:** Most free hosting has ephemeral storage
- User data in `reports/` folder may be lost on restart

**Solutions:**

#### Option 1: Use Database (Recommended)
Switch to PostgreSQL (free tiers available):
- Render: Free PostgreSQL database
- ElephantSQL: 20 MB free
- Supabase: 500 MB free

#### Option 2: Use Cloud Storage
Store `reports/` in cloud:
- AWS S3 (free tier)
- Google Cloud Storage (free tier)
- Cloudinary (free tier)

#### Option 3: Warning Message
Add notice to users:
```python
# In templates
<div class="warning">
  ⚠️ This is a demo deployment. Data may be reset periodically.
  For production use, host on persistent storage.
</div>
```

---

## 💰 Cost Comparison (if you outgrow free tier)

| Platform | Paid Tier | Price/Month | Best For |
|----------|-----------|-------------|----------|
| Render | Standard | $7 | Most apps |
| PythonAnywhere | Hacker | $5 | Python apps |
| Fly.io | Pay-as-you-go | ~$3-10 | Flexible scaling |
| Railway | Pay-as-you-go | ~$5-10 | Simple apps |
| DigitalOcean | Droplet | $6 | Full control |
| AWS | EC2 t2.micro | $8-10 | Enterprise |

---

## 🎯 My Recommendation for You

### Best Overall: **Render.com**

**Why:**
1. ✅ Easy setup (5 minutes)
2. ✅ Auto-deploy from GitHub
3. ✅ No credit card required
4. ✅ Good free tier
5. ✅ Upgrade path available

**Caveat:**
- Cold starts after inactivity
- **Solution**: Use cron job to ping app every 10 min

### For Always-On: **PythonAnywhere**

**Why:**
1. ✅ No cold starts
2. ✅ Python-focused
3. ✅ Reliable
4. ✅ Good for education

**Caveat:**
- Manual updates (no auto-deploy)
- **Solution**: Use their API or manual re-upload

---

## 🔗 Quick Start Links

### Render
- **Sign Up**: https://render.com
- **Docs**: https://render.com/docs/deploy-flask
- **Free Tier**: https://render.com/docs/free

### PythonAnywhere
- **Sign Up**: https://www.pythonanywhere.com/registration/register/beginner/
- **Docs**: https://help.pythonanywhere.com/pages/Flask/
- **Free Tier**: Beginner account (always free)

### Fly.io
- **Sign Up**: https://fly.io/app/sign-up
- **Docs**: https://fly.io/docs/languages-and-frameworks/python/
- **Free Tier**: https://fly.io/docs/about/pricing/

### Railway
- **Sign Up**: https://railway.app
- **Docs**: https://docs.railway.app/deploy/deployments
- **Free Tier**: $5/month credit

---

## 📝 Next Steps

1. **Choose a platform** (I recommend Render)
2. **Prepare your repo** (add gunicorn, update app.py)
3. **Deploy!** (follow guide above)
4. **Share your URL** with users!

---

## 🆘 Need Help?

Common issues and solutions:

**Q: App crashes on startup**
- Check logs in platform dashboard
- Verify `requirements.txt` is correct
- Ensure `app.py` has proper config

**Q: Data doesn't persist**
- Add database (see Storage Limitations section)
- Or accept ephemeral storage for demo

**Q: Slow/timeout after inactivity**
- Normal for free tier (cold starts)
- Upgrade to paid tier or use PythonAnywhere

**Q: Domain name?**
- Free tier gives subdomain (e.g., app.onrender.com)
- Custom domain requires paid tier ($7/month)

---

## 🎉 Summary

**Quick Recommendation:**
```
For most users: Render.com
- Easy, fast, reliable
- Auto-deploy from GitHub
- Good free tier

For always-on: PythonAnywhere
- No cold starts
- Educational use
- Stable
```

**Deploy in 5 minutes:** Use Render.com with the guide above!

---

*Last Updated: December 2025*

