# 🚀 Complete Deployment Guide

**Deploy CELPIP Practice Platform with OAuth Authentication**

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Setup OAuth (Google & Facebook)](#setup-oauth)
3. [Deploy to Render.com](#deploy-to-render)
4. [Post-Deployment Configuration](#post-deployment)
5. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### What You Need

✅ **GitHub Account** - To host your code  
✅ **Render.com Account** (free) - For hosting  
✅ **Google Cloud Account** (free) - For OAuth  
✅ **Domain/URL** - Will be provided by Render (e.g., `your-app.onrender.com`)

### Local Setup First

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/celpip.git
cd celpip

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Test locally
python app.py
```

Visit `http://127.0.0.1:5000` to verify it works locally.

---

## Setup OAuth

### Google OAuth Setup

#### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **"Select a project"** → **"New Project"**
3. Enter project name: `CELPIP Practice` → **Create**
4. Wait for project creation (~30 seconds)

#### 2. Configure OAuth Consent Screen

1. In left sidebar: **APIs & Services** → **OAuth consent screen**
2. Choose **External** → **Create**
3. Fill in:
   - **App name**: `CELPIP Practice Platform`
   - **User support email**: Your email
   - **Developer contact**: Your email
4. Click **Save and Continue**
5. **Scopes**: Click **Add or Remove Scopes**
   - Select: `userinfo.email`, `userinfo.profile`, `openid`
   - Click **Update** → **Save and Continue**
6. **Test users** (optional): Add your email → **Save and Continue**
7. Click **Back to Dashboard**

#### 3. Create OAuth Credentials

1. In left sidebar: **Credentials** → **Create Credentials** → **OAuth client ID**
2. Choose **Web application**
3. Fill in:
   - **Name**: `CELPIP Web Client`
   - **Authorized JavaScript origins**:
     ```
     http://localhost:5000
     http://127.0.0.1:5000
     https://your-app.onrender.com
     ```
   - **Authorized redirect URIs**:
     ```
     http://localhost:5000/callback/google
     http://127.0.0.1:5000/callback/google
     https://your-app.onrender.com/callback/google
     ```
4. Click **Create**
5. **Copy and save**:
   - ✅ Client ID (ends with `.apps.googleusercontent.com`)
   - ✅ Client Secret (random string)

> ⚠️ **Important**: Update redirect URIs after deploying to Render!

---

### Facebook OAuth Setup (Optional)

#### 1. Create Facebook App

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Click **My Apps** → **Create App**
3. Choose **Consumer** → **Next**
4. Fill in:
   - **App name**: `CELPIP Practice`
   - **Contact email**: Your email
5. Click **Create App**

#### 2. Add Facebook Login

1. In dashboard: Find **Facebook Login** → **Set Up**
2. Choose **Web** platform
3. Enter Site URL: `https://your-app.onrender.com`
4. Click **Save**

#### 3. Configure OAuth Settings

1. In left sidebar: **Facebook Login** → **Settings**
2. **Valid OAuth Redirect URIs**:
   ```
   http://localhost:5000/callback/facebook
   http://127.0.0.1:5000/callback/facebook
   https://your-app.onrender.com/callback/facebook
   ```
3. Click **Save Changes**

#### 4. Get App Credentials

1. In left sidebar: **Settings** → **Basic**
2. **Copy and save**:
   - ✅ App ID (numeric)
   - ✅ App Secret (click **Show**)

#### 5. Switch to Live Mode

1. Toggle **App Mode** from Development to **Live** (top right)
2. May require additional verification

---

## Deploy to Render

### 1. Prepare Repository

#### Create `.env.example` (for reference)

Create file `.env.example` in your project root:

```bash
# Flask Secret Key (generate with: python -c "import secrets; print(secrets.token_hex(32))")
SECRET_KEY=your-secret-key-here

# Google OAuth
GOOGLE_CLIENT_ID=your-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-secret

# Facebook OAuth (Optional)
FACEBOOK_CLIENT_ID=your-facebook-app-id
FACEBOOK_CLIENT_SECRET=your-facebook-app-secret

# App URLs (update after deployment)
APP_URL=http://127.0.0.1:5000
REDIRECT_URI_BASE=http://127.0.0.1:5000
```

#### Update `.gitignore`

Ensure `.gitignore` includes:

```
# Environment variables
.env

# User data
users/
reports/

# Python
venv/
__pycache__/
*.pyc

# OS
.DS_Store
```

#### Commit and Push

```bash
git add -A
git commit -m "Prepare for Render deployment with OAuth"
git push origin main
```

---

### 2. Create Render Web Service

#### 2.1 Sign Up & Connect

1. Go to [render.com](https://render.com)
2. Sign up with **GitHub** (recommended)
3. Authorize Render to access your repositories

#### 2.2 Create New Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your repository:
   - Click **"Connect account"** (if needed)
   - Select your CELPIP repository
3. Click **"Connect"**

#### 2.3 Configure Service

**Name & Region:**
- **Name**: `celpip-practice` (will be `celpip-practice.onrender.com`)
- **Region**: Choose closest to your users
- **Branch**: `main`

**Build Settings:**
- **Runtime**: `Python 3`
- **Build Command**: 
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command**:
  ```bash
  gunicorn app:app
  ```

**Instance Type:**
- **Free** - Good for testing (spins down after 15 min of inactivity)
- **Starter** ($7/month) - Recommended for production (always on)

#### 2.4 Add Environment Variables

**Before clicking "Create Web Service"**, scroll down to **Environment Variables** and add:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | Generate with: `python -c "import secrets; print(secrets.token_hex(32))"` |
| `GOOGLE_CLIENT_ID` | Your Google Client ID |
| `GOOGLE_CLIENT_SECRET` | Your Google Client Secret |
| `APP_URL` | `https://celpip-practice.onrender.com` (use your actual URL) |
| `REDIRECT_URI_BASE` | `https://celpip-practice.onrender.com` (same as APP_URL) |
| `FACEBOOK_CLIENT_ID` | (Optional) Your Facebook App ID |
| `FACEBOOK_CLIENT_SECRET` | (Optional) Your Facebook App Secret |

> 💡 **Tip**: You can also add these after deployment in the **Environment** tab.

#### 2.5 Deploy!

1. Click **"Create Web Service"**
2. Wait 2-5 minutes for deployment
3. Watch the build logs for any errors
4. Once deployed, you'll see: ✅ **"Live"** with a green dot

Your app is now live at: `https://your-app.onrender.com` 🎉

---

### 3. Update OAuth Redirect URIs

**CRITICAL STEP:** Now that you have your Render URL, update OAuth settings:

#### Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. **APIs & Services** → **Credentials**
3. Click on your **OAuth 2.0 Client ID**
4. **Authorized redirect URIs** → Add:
   ```
   https://your-actual-app.onrender.com/callback/google
   ```
5. Click **Save**

#### Facebook Developer Console (if using)

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Select your app
3. **Facebook Login** → **Settings**
4. **Valid OAuth Redirect URIs** → Add:
   ```
   https://your-actual-app.onrender.com/callback/facebook
   ```
5. Click **Save Changes**

---

## Post-Deployment

### 1. Test OAuth Login

1. Visit your Render URL: `https://your-app.onrender.com`
2. Click **"🔐 Login"**
3. Try **"Continue with Google"**
4. Authorize the app
5. You should be redirected back and see your profile

### 2. Verify User Data Storage

1. Take a test (after logging in)
2. Check that your progress is saved
3. Logout and login again
4. Verify your test history is still there

### 3. Test Guest Mode

1. Logout
2. Click **"Continue as Guest"**
3. Take a test
4. Verify it works but shows no history after browser close

---

## Configuration

### Update App Settings

Edit `config.json` to customize:

```json
{
  "time_per_question": {
    "reading": 1.5,
    "writing": 30.0,
    "listening": 1.5,
    "speaking": 1.5
  },
  "ui_settings": {
    "timer_warning_seconds": 60,
    "timer_critical_seconds": 30,
    "auto_submit_on_timeout": true,
    "show_timer": true,
    "show_progress_bar": true
  }
}
```

After updating, commit and push:

```bash
git add config.json
git commit -m "Update configuration"
git push
```

Render will automatically redeploy (if auto-deploy is enabled).

---

## Troubleshooting

### OAuth Issues

#### "Error 400: redirect_uri_mismatch"

**Problem**: Redirect URI not registered in Google/Facebook console.

**Solution**:
1. Check your Render URL is exact (with https://)
2. Update Google Cloud Console → Credentials → OAuth 2.0 Client IDs
3. Add exact redirect URI: `https://your-app.onrender.com/callback/google`
4. Wait 5 minutes for Google to update

#### "Error: OAuth provider not configured"

**Problem**: Environment variables not set correctly.

**Solution**:
1. Go to Render dashboard → Your service → **Environment**
2. Verify all OAuth variables are set
3. Click **Save Changes** (will trigger redeploy)

#### Login Button Not Working

**Problem**: JavaScript error or missing provider.

**Solution**:
1. Open browser console (F12)
2. Check for errors
3. Verify `/login` endpoint is accessible
4. Check Render logs for backend errors

---

### Deployment Issues

#### Build Failed

**Problem**: Missing dependencies or Python version mismatch.

**Solution**:
```bash
# Ensure requirements.txt is complete
pip freeze > requirements.txt

# Commit and push
git add requirements.txt
git commit -m "Update dependencies"
git push
```

#### "ModuleNotFoundError"

**Problem**: Dependency not in `requirements.txt`.

**Solution**:
1. Add missing package to `requirements.txt`:
   ```
   requests==2.31.0
   ```
2. Commit and push
3. Render will auto-redeploy

#### App Not Starting

**Problem**: Gunicorn command incorrect or port issues.

**Solution**:
- Verify Start Command: `gunicorn app:app`
- Check Render logs for specific error
- Ensure `app.py` has: `if __name__ == '__main__': app.run()`

---

### Performance Issues

#### Slow First Load (Free Tier)

**Problem**: Free tier spins down after 15 min inactivity.

**Solution**:
- Upgrade to **Starter** plan ($7/month) for always-on service
- Or use a service like [UptimeRobot](https://uptimerobot.com/) to ping every 14 minutes

#### Database Errors

**Problem**: JSON file storage conflicts in multi-instance deployments.

**Solution**:
- Consider upgrading to PostgreSQL for production
- Use Render's PostgreSQL addon
- Follow migration guide: `docs/USER_DATA_STRUCTURE.md`

---

## Security Best Practices

### 1. Environment Variables

✅ **Never commit** `.env` to Git  
✅ Keep `SECRET_KEY` secure and random  
✅ Rotate keys if exposed  
✅ Use different keys for dev/prod

### 2. OAuth Security

✅ Use HTTPS in production (Render provides this)  
✅ Verify redirect URIs are exact  
✅ Don't share OAuth secrets publicly  
✅ Review OAuth scopes regularly

### 3. User Data

✅ User data stored in `users/` folder (gitignored)  
✅ No passwords stored (OAuth only)  
✅ Email addresses sanitized in folder names  
✅ Data isolated per user

---

## Updating Your Deployment

### Code Updates

```bash
# Make changes locally
git add -A
git commit -m "Your update message"
git push origin main
```

Render will **auto-deploy** (if enabled) within 1-2 minutes.

### Manual Redeploy

1. Go to Render dashboard
2. Select your service
3. Click **"Manual Deploy"** → **"Deploy latest commit"**

### Environment Variable Updates

1. Render dashboard → Your service → **Environment**
2. Update variable
3. Click **"Save Changes"**
4. Service will automatically restart

---

## Monitoring & Logs

### View Logs

1. Render dashboard → Your service
2. Click **"Logs"** tab
3. See real-time application logs

### Monitor Usage

1. Render dashboard → Your service
2. Click **"Metrics"** tab
3. View:
   - CPU usage
   - Memory usage
   - Request count
   - Response times

---

## Cost Breakdown

### Free Tier
- **Price**: $0/month
- **Limitations**:
  - Spins down after 15 min inactivity
  - Slower cold starts (~30 sec)
  - 750 hours/month (sufficient for personal use)
- **Best for**: Development, testing, personal use

### Starter Tier
- **Price**: $7/month
- **Benefits**:
  - Always on (no spin down)
  - Fast response times
  - More CPU/RAM
  - Custom domains
- **Best for**: Production, multiple users, professional use

---

## Next Steps

### 1. Custom Domain (Optional)

1. Purchase domain (e.g., `celpip-practice.com`)
2. Render dashboard → Your service → **Settings**
3. Click **"Add Custom Domain"**
4. Follow DNS setup instructions

### 2. Database Upgrade (Future)

When you outgrow JSON files:

1. Add PostgreSQL to Render
2. Update code to use database
3. Migrate existing user data
4. See: `docs/USER_DATA_STRUCTURE.md`

### 3. Add More Tests

1. Create test content in `data/test_X/`
2. Follow format in existing tests
3. No code changes needed!
4. See: `docs/ADDING_TESTS.md`

---

## Support & Resources

### Documentation
- **Complete Guide**: `docs/COMPLETE_GUIDE.md`
- **OAuth Setup**: `docs/OAUTH_SETUP.md`
- **User Data**: `docs/USER_DATA_STRUCTURE.md`

### External Resources
- [Render Documentation](https://render.com/docs)
- [Google OAuth Guide](https://developers.google.com/identity/protocols/oauth2)
- [Flask Documentation](https://flask.palletsprojects.com/)

### Getting Help
- Check Render logs for errors
- Open GitHub issue
- Review `docs/` folder

---

## Summary Checklist

### Pre-Deployment
- [ ] Tested locally with OAuth
- [ ] Created `.env.example`
- [ ] Updated `.gitignore`
- [ ] Pushed to GitHub
- [ ] Set up Google OAuth
- [ ] Set up Facebook OAuth (optional)

### Deployment
- [ ] Created Render web service
- [ ] Set environment variables
- [ ] Deployed successfully
- [ ] Updated OAuth redirect URIs
- [ ] Tested login with Google
- [ ] Tested login with Facebook (if enabled)
- [ ] Verified guest mode works

### Post-Deployment
- [ ] Took a test as logged-in user
- [ ] Verified data persistence
- [ ] Checked logout functionality
- [ ] Tested on mobile device
- [ ] Reviewed Render logs

---

**🎉 Congratulations! Your CELPIP Practice Platform is live!**

Share your URL: `https://your-app.onrender.com`

---

**Last Updated**: December 8, 2025  
**Version**: 3.0 (with OAuth)

