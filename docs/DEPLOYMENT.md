# 🚀 Complete Deployment Guide

**Deploy CELPIP Practice Platform with PostgreSQL Database & OAuth Authentication**

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Setup OAuth (Google & Facebook)](#setup-oauth)
3. [Deploy to Render.com](#deploy-to-render)
4. [Database Setup](#database-setup)
5. [Post-Deployment Configuration](#post-deployment)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### What You Need

✅ **GitHub Account** - To host your code  
✅ **Render.com Account** (free) - For hosting  
✅ **Google Cloud Account** (free) - For OAuth  
✅ **Domain/URL** - Will be provided by Render (e.g., `your-app.onrender.com`)

> 💡 **Database is built-in**: This project ships with full PostgreSQL support via `render.yaml`. No extra database setup is needed — Render provisions it automatically.

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

#### Commit and Push

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

Then push your latest code:

```bash
git add -A
git commit -m "Prepare for Render deployment"
git push origin main
```

---

### 2. Deploy via Blueprint (Recommended)

The project ships with a `render.yaml` that provisions **both the web service and a PostgreSQL database** automatically.

#### 2.1 Sign Up & Connect

1. Go to [render.com](https://render.com)
2. Sign up with **GitHub** (recommended)
3. Authorize Render to access your repositories

#### 2.2 Create Blueprint

1. Click **"New +"** → **"Blueprint"**
2. Select your CELPIP repository
3. Render will detect `render.yaml` and show a preview:
   - 🗄️ `celpip-db` — Free PostgreSQL database
   - 🌐 `celpip-practice` — Python web service
4. Click **"Apply"**

Render will provision both resources and **automatically wire `DATABASE_URL`** from the database to the web service — no manual copy-paste needed.

#### 2.3 Add OAuth Environment Variables

After the Blueprint deploys, go to **Dashboard → celpip-practice → Environment** and add:

| Key | Value |
|-----|-------|
| `GOOGLE_CLIENT_ID` | Your Google Client ID |
| `GOOGLE_CLIENT_SECRET` | Your Google Client Secret |
| `APP_URL` | `https://your-app.onrender.com` |
| `REDIRECT_URI_BASE` | `https://your-app.onrender.com` (same as `APP_URL`) |
| `FACEBOOK_CLIENT_ID` | (Optional) Your Facebook App ID |
| `FACEBOOK_CLIENT_SECRET` | (Optional) Your Facebook App Secret |

> ⚠️ **Do NOT manually add `DATABASE_URL` or `SECRET_KEY`** — these are already handled by `render.yaml` (`DATABASE_URL` is linked from the DB, `SECRET_KEY` is auto-generated).

Click **"Save Changes"** — the service will restart with the new variables.

#### 2.4 Your app is live! 🎉

Visit: `https://your-app.onrender.com`

**Instance Type:**
- **Free** - Good for testing (spins down after 15 min of inactivity; ~30s cold start)
- **Starter** ($7/month) - Recommended for production (always on)

---

### 3. Manual Deploy (Alternative to Blueprint)

If you prefer to set everything up manually:

#### 3.1 Create PostgreSQL Database

1. **New +** → **PostgreSQL**
2. Set:
   - **Name**: `celpip-db`
   - **Database**: `celpip`
   - **User**: `celpip_user`
   - **Plan**: Free
3. Click **Create Database**
4. Copy the **Internal Database URL** from the database dashboard

#### 3.2 Create Web Service

1. **New +** → **Web Service**
2. Connect your repository, then configure:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Plan**: Free or Starter

#### 3.3 Add Environment Variables

| Key | Value |
|-----|-------|
| `SECRET_KEY` | Run locally: `python -c "import secrets; print(secrets.token_hex(32))"` |
| `DATABASE_URL` | Paste the **Internal Database URL** from step 3.1 |
| `GOOGLE_CLIENT_ID` | Your Google Client ID |
| `GOOGLE_CLIENT_SECRET` | Your Google Client Secret |
| `APP_URL` | `https://your-app.onrender.com` |
| `REDIRECT_URI_BASE` | `https://your-app.onrender.com` |
| `FACEBOOK_CLIENT_ID` | (Optional) Your Facebook App ID |
| `FACEBOOK_CLIENT_SECRET` | (Optional) Your Facebook App Secret |

3. Click **Create Web Service**

---

---

## Database Setup

### How It Works

The app uses **PostgreSQL as the primary data store** with a transparent fallback to JSON files when no database is configured (useful for local development).

| Scenario | Storage |
|----------|---------|
| `DATABASE_URL` is set | PostgreSQL |
| `DATABASE_URL` is not set | JSON files in `users/` |

On first startup, the app **automatically creates all required tables** — no manual migrations needed.

### Database Schema

```sql
-- User profiles
users (
    email          TEXT PRIMARY KEY,
    name           TEXT,
    provider       TEXT,       -- 'google' or 'facebook'
    picture        TEXT,
    role           TEXT,       -- 'Basic' or 'Premium'
    created_at     TIMESTAMPTZ,
    last_accessed  TIMESTAMPTZ
)

-- Test results per user per test number
test_history (
    id          SERIAL PRIMARY KEY,
    user_email  TEXT REFERENCES users(email),
    test_num    INTEGER,
    data        JSONB,         -- full attempt history
    updated_at  TIMESTAMPTZ,
    UNIQUE(user_email, test_num)
)

-- Individual vocabulary notes
vocabulary_notes (
    note_id     TEXT PRIMARY KEY,
    user_email  TEXT REFERENCES users(email),
    test_num    INTEGER,
    skill       TEXT,          -- 'reading', 'listening', etc.
    part_num    INTEGER,
    word        TEXT,
    definition  TEXT,
    context     TEXT,
    created_at  TIMESTAMPTZ,
    updated_at  TIMESTAMPTZ
)
```

### Verify Database Connection

After deployment, check the Render logs for:
```
PostgreSQL database connected successfully
```

If you see `DATABASE_URL not set - using file-based storage`, the env var is missing or not linked correctly.

### Free Tier Database Expiry

> ⚠️ **IMPORTANT**: Render's **free PostgreSQL databases expire after 90 days** and all data is deleted.
>
> **Current status**: The project uses the free-tier database. For persistent data, upgrade to a paid PostgreSQL plan ($7/month).
>
> If the free DB expires:
> 1. Create a new free DB (or upgrade to paid)
> 2. Update the `DATABASE_URL` env var in the web service
> 3. The app will auto-create tables on first startup — but previous user data is lost

---

## Audio & Video Hosting (Cloudinary)

Listening test audio (`.m4a`) and video (`.mp4`) files are hosted on **Cloudinary** and referenced by URL in the JSON test data files (`data/test_X/listening/partY.json`).

- **No Cloudinary SDK or API keys needed** — the app simply embeds Cloudinary URLs in `<audio>` and `<video>` tags
- Media URLs follow the pattern: `https://res.cloudinary.com/YOUR_CLOUD_NAME/video/upload/v.../filename.m4a`
- To add new Listening tests, upload audio/video to Cloudinary and put the URLs in the JSON files
- See `docs/ADDING_LISTENING_TESTS.md` for the full workflow

---

### 4. Update OAuth Redirect URIs

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

#### Database Connection Failed

**Problem**: App starts but logs show `Failed to connect to PostgreSQL`.

**Solution**:
1. Go to Render dashboard → **celpip-practice** → **Environment**
2. Verify `DATABASE_URL` is present (it should be auto-linked if you used Blueprint)
3. If missing, go to your **celpip-db** database dashboard and copy the **Internal Database URL**
4. Add it as `DATABASE_URL` in the web service environment
5. Click **Save Changes** to restart the service

#### App Falling Back to File Storage

**Problem**: Logs show `DATABASE_URL not set - using file-based storage`.

**Solution**:
- Same as above — ensure `DATABASE_URL` is set and linked correctly
- This fallback is intentional for local development without a database

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

✅ User data stored in **PostgreSQL** (when `DATABASE_URL` is set)  
✅ Falls back to `users/` JSON files for local dev (gitignored)  
✅ No passwords stored (OAuth only)  
✅ Data isolated per user with foreign key constraints

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

### 2. Migrate Existing User Data (from JSON files)

If you had users stored in `users/` JSON files before the database was set up:

```bash
# Run the migration script locally (ensure DATABASE_URL is set in .env)
python migrate_user_data.py
```

This script reads from `users/` and writes all profiles, test history, and vocabulary notes into PostgreSQL.

### 3. Add More Tests

1. Create test content in `data/test_X/`
2. Follow format in existing tests
3. No code changes needed!
4. See: `docs/ADDING_TESTS.md`

---

## Support & Resources

### Documentation
- **Architecture**: `docs/ARCHITECTURE.md`
- **User Data**: `docs/USER_DATA_STRUCTURE.md`
- **Adding Tests**: `docs/ADDING_TESTS.md`

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
- [ ] Deployed via Blueprint (or manually created DB + web service)
- [ ] Confirmed `DATABASE_URL` is linked in web service environment
- [ ] Added OAuth environment variables (`GOOGLE_CLIENT_ID`, etc.)
- [ ] Deployed successfully — service shows ✅ Live
- [ ] Updated OAuth redirect URIs in Google/Facebook console
- [ ] Tested login with Google
- [ ] Tested login with Facebook (if enabled)
- [ ] Verified guest mode works

### Post-Deployment
- [ ] Render logs show `PostgreSQL database connected successfully`
- [ ] Took a test as logged-in user
- [ ] Verified test history is saved (logout → login → check history)
- [ ] Verified vocabulary notes persist across sessions
- [ ] Checked logout functionality
- [ ] Tested on mobile device
- [ ] Reviewed Render logs for any errors

---

**🎉 Congratulations! Your CELPIP Practice Platform is live!**

Share your URL: `https://your-app.onrender.com`

---

**Last Updated**: March 16, 2026  
**Version**: 4.0 (with PostgreSQL + OAuth)

