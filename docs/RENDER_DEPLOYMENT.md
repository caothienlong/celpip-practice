# 🚀 Deploy to Render.com Guide

## Quick Deploy to Render

Deploy your CELPIP Practice Platform to Render.com in under 10 minutes!

---

## Prerequisites

✅ Git repository (GitHub, GitLab, or Bitbucket)  
✅ Render.com account (free)  
✅ Google OAuth credentials (optional, for login feature)

---

## Step 1: Prepare Your Repository

### 1.1 Ensure Files Are Ready

Make sure these files exist:
- ✅ `requirements.txt` - Python dependencies
- ✅ `app.py` - Main Flask app
- ✅ `.gitignore` - Excludes users/, .env

### 1.2 Push to GitHub

```bash
git add -A
git commit -m "Prepare for Render deployment"
git push origin main
```

---

## Step 2: Create Web Service on Render

### 2.1 Sign Up / Log In

1. Go to [render.com](https://render.com)
2. Sign up with GitHub (recommended) or email
3. Authorize Render to access your repositories

### 2.2 Create New Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your Git repository
3. Select your CELPIP repository

### 2.3 Configure Service

**Basic Settings:**
- **Name**: `celpip-practice` (or your choice)
- **Region**: Choose closest to your users
- **Branch**: `main`
- **Root Directory**: (leave blank)
- **Runtime**: `Python 3`

**Build & Deploy:**
- **Build Command**: 
  ```bash
  pip install -r requirements.txt
  ```
  
- **Start Command**:
  ```bash
  gunicorn app:app
  ```

**Instance Type:**
- **Free** (0.1 CPU, 512MB RAM) - Good for testing
- **Starter** ($7/month) - Recommended for production

### 2.4 Click "Create Web Service"

Wait 2-5 minutes for initial deployment...

---

## Step 3: Configure Environment Variables

### 3.1 Add Environment Variables

In your Render dashboard:

1. Go to your service
2. Click **"Environment"** tab
3. Add these variables:

**Required:**
```
SECRET_KEY = [generate-random-32-char-hex]
```

**For OAuth Login (Optional):**
```
GOOGLE_CLIENT_ID = your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET = your-client-secret
APP_URL = https://your-app.onrender.com
REDIRECT_URI_BASE = https://your-app.onrender.com
```

**To Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3.2 Save Changes

Click **"Save Changes"** → Service will redeploy automatically

---

## Step 4: Update OAuth Callback URLs

If using Google OAuth:

### 4.1 Update Google Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to your OAuth client
3. Add to **Authorized redirect URIs**:
   ```
   https://your-app.onrender.com/callback/google
   ```
4. Add to **Authorized JavaScript origins**:
   ```
   https://your-app.onrender.com
   ```
5. Save

---

## Step 5: Access Your App

Your app will be available at:
```
https://your-app.onrender.com
```

🎉 **Done!** Your CELPIP app is live!

---

## Deployment Configuration Options

### Using `render.yaml` (Recommended)

Create `render.yaml` in your repo root:

```yaml
services:
  - type: web
    name: celpip-practice
    runtime: python
    plan: free  # or 'starter' for paid
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: APP_URL
        value: https://celpip-practice.onrender.com
      - key: REDIRECT_URI_BASE
        value: https://celpip-practice.onrender.com
```

**Benefits:**
- Version control your configuration
- Easy redeployment
- Multiple environments

---

## Free Tier Limitations

**Render Free Tier:**
- ✅ 750 hours/month (enough for 24/7)
- ✅ Automatic HTTPS
- ✅ Custom domains
- ⚠️ Spins down after 15min inactivity (cold start ~30s)
- ⚠️ 512MB RAM
- ⚠️ 0.1 CPU

**Workaround for Cold Starts:**

Use a free uptime monitor:
- [UptimeRobot](https://uptimerobot.com) (free)
- [Cronit or](https://cron-job.org) (free)
- Ping your app every 10 minutes

---

## Upgrading to Paid Plan

### Why Upgrade? ($7/month)

✅ No cold starts (always on)  
✅ More RAM (512MB)  
✅ Better CPU  
✅ Priority support  

**When to upgrade:**
- 50+ active users
- Need fast response times
- Professional use

### How to Upgrade

1. Go to your service settings
2. Click **"Instance Type"**
3. Select **"Starter"**
4. Confirm payment

---

## Custom Domain Setup

### 1. Add Custom Domain

In Render:
1. Go to your service → **"Settings"**
2. Scroll to **"Custom Domains"**
3. Add your domain: `practice.yourdomain.com`

### 2. Update DNS

Add CNAME record in your DNS provider:
```
Type: CNAME
Name: practice
Value: your-app.onrender.com
```

### 3. Update OAuth

Update Google OAuth URLs with your custom domain

---

## Continuous Deployment

### Auto-Deploy on Git Push

**Enabled by default!**

```bash
# Make changes
git add -A
git commit -m "Update feature"
git push origin main

# Render automatically:
# 1. Detects push
# 2. Builds app
# 3. Deploys new version
# 4. ~2-3 minutes total
```

### Manual Deploy

In Render dashboard:
1. Go to your service
2. Click **"Manual Deploy"** → **"Deploy latest commit"**

### Disable Auto-Deploy

Settings → **"Auto-Deploy"** → Toggle off

---

## Monitoring & Logs

### View Logs

1. Go to your service
2. Click **"Logs"** tab
3. Real-time logs appear

**Useful for:**
- Debugging errors
- Monitoring traffic
- Checking OAuth flows

### Metrics

**Free tier metrics:**
- CPU usage
- Memory usage
- Request count
- Response times

**Paid tier adds:**
- Detailed analytics
- Longer retention
- Export options

---

## Troubleshooting

### Build Fails

**Check:**
1. `requirements.txt` has all dependencies
2. Python version compatible (3.9+)
3. No syntax errors in `app.py`

**View build logs** in Render dashboard

### App Crashes on Start

**Common causes:**
1. Missing `SECRET_KEY` env var
2. Port configuration (Render sets `PORT` automatically)
3. Import errors

**Fix:**
```python
# app.py - Use Render's port
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

### OAuth Not Working

**Check:**
1. Callback URLs updated in Google Console
2. `APP_URL` and `REDIRECT_URI_BASE` set correctly
3. HTTPS (not HTTP) in all URLs
4. Google OAuth credentials in environment variables

### Slow First Load (Cold Start)

**On free tier:**
- App sleeps after 15min inactivity
- First request takes ~30s
- Subsequent requests fast

**Solutions:**
1. Upgrade to paid plan ($7/month)
2. Use uptime monitor to keep awake
3. Show loading message to users

### User Data Not Persisting

**Issue:** Free tier uses ephemeral storage

**Solutions:**
1. **Use PostgreSQL** (Render offers free PostgreSQL)
2. **Use external storage** (AWS S3, Google Cloud Storage)
3. **Stick with current setup** (works, but data lost on redeploy)

---

## Database Migration (Optional)

### Add PostgreSQL Database

**For persistent user data:**

1. In Render dashboard: **"New +"** → **"PostgreSQL"**
2. Name: `celpip-db`
3. Plan: **Free** (90 days, then $7/month)
4. Create

5. Link to your web service:
   - Copy **Internal Database URL**
   - Add to web service env vars as `DATABASE_URL`

6. Update code to use PostgreSQL:
   ```python
   import os
   import psycopg2
   
   DATABASE_URL = os.getenv('DATABASE_URL')
   conn = psycopg2.connect(DATABASE_URL)
   ```

**See:** Migration guide for full implementation

---

## Performance Optimization

### 1. Enable Gzip Compression

Already handled by `gunicorn`!

### 2. Static File Caching

Add to `app.py`:
```python
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'public, max-age=31536000'
    return response
```

### 3. Use CDN for Images

For static images, consider:
- Cloudflare (free CDN)
- AWS CloudFront
- Google Cloud CDN

---

## Security Checklist

✅ **HTTPS enabled** (automatic on Render)  
✅ **SECRET_KEY is random** (not default)  
✅ **Environment variables secured** (not in code)  
✅ **.env not in git** (in .gitignore)  
✅ **OAuth credentials secured**  
✅ **No sensitive data in logs**  

---

## Backup Strategy

### User Data Backup

**Option 1: Manual Download**
```bash
# Use Render shell
render shell your-service-name
tar -czf backup.tar.gz users/
# Download via SFTP
```

**Option 2: Automated Backups**
- Set up cron job to backup to cloud storage
- Use Render cron jobs (paid plan)

### Database Backup

If using PostgreSQL:
- **Automatic backups** included (7-day retention)
- Manual backups available in dashboard
- Export via pg_dump

---

## Cost Breakdown

| Plan | Price | Features |
|------|-------|----------|
| **Free** | $0/month | 750hrs, cold starts, 512MB RAM |
| **Starter** | $7/month | Always on, 512MB RAM, better CPU |
| **Standard** | $25/month | 2GB RAM, more CPU |
| **PostgreSQL Free** | $0 | 90 days, then $7/month |

**Recommended Setup:**
- Starting: **Free** ($0)
- Growing: **Web Starter** ($7) + **PostgreSQL** ($7) = $14/month
- Production: **Web Standard** ($25) + **PostgreSQL** ($7) = $32/month

---

## Alternative: Deploy with Docker

### 1. Create `Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

### 2. Deploy to Render

- Choose **"Docker"** as runtime
- Render will build and deploy automatically

---

## Next Steps

1. ✅ Deploy app to Render
2. ⏳ Set up Google OAuth
3. ⏳ Add custom domain
4. ⏳ Set up uptime monitoring
5. ⏳ Configure backups
6. ⏳ Monitor performance
7. ⏳ Consider PostgreSQL upgrade

---

## Support & Help

**Render Support:**
- [Render Docs](https://render.com/docs)
- [Community Forum](https://community.render.com)
- [Status Page](https://status.render.com)

**This Project:**
- Check `docs/COMPLETE_GUIDE.md`
- Review logs in Render dashboard
- Check environment variables

---

**🎉 Your CELPIP app is now live and accessible worldwide!**

**App URL:** `https://your-app.onrender.com`

