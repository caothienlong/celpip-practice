# 🔐 OAuth Login Setup Guide

## Overview

The CELPIP Practice Platform supports login via **Google** and **Facebook** OAuth providers. This allows users to sign in with their existing accounts without creating new passwords.

---

## Features

✅ **Sign in with Google**  
✅ **Sign in with Facebook**  
✅ **Guest mode** (session-only, no login required)  
✅ **Automatic user profile creation**  
✅ **Profile picture from OAuth provider**  
✅ **Persistent test history** (when logged in)  

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**New dependencies:**
- `authlib` - OAuth library
- `flask-login` - User session management  
- `python-dotenv` - Environment variable loader

### 2. Configure Environment Variables

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

### 3. Set Up OAuth Providers

Choose which providers you want to enable:
- [Google OAuth Setup](#google-oauth-setup)
- [Facebook OAuth Setup](#facebook-oauth-setup)

---

## Google OAuth Setup

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **"Create Project"** or select existing project
3. Give it a name: `CELPIP Practice`

### Step 2: Enable Google+ API

1. Go to **APIs & Services** → **Library**
2. Search for **"Google+ API"**
3. Click **"Enable"**

### Step 3: Create OAuth Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **"Create Credentials"** → **"OAuth client ID"**
3. Configure consent screen if prompted:
   - **User Type**: External
   - **App name**: CELPIP Practice
   - **User support email**: Your email
   - **Scopes**: Add `email` and `profile`
   - **Authorized domains**: Add your domain (or `localhost` for development)
   
4. **Application type**: Web application
5. **Name**: CELPIP Practice Web
6. **Authorized JavaScript origins**:
   ```
   http://localhost:5000
   http://127.0.0.1:5000
   ```
   Add your production URL when deploying

7. **Authorized redirect URIs**:
   ```
   http://localhost:5000/callback/google
   http://127.0.0.1:5000/callback/google
   ```
   Add production callback URL when deploying

8. Click **"Create"**

### Step 4: Copy Credentials

You'll receive:
- **Client ID**: `xxx.apps.googleusercontent.com`
- **Client Secret**: `xxxxx`

Add to `.env`:
```bash
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
```

---

## Facebook OAuth Setup

### Step 1: Create Facebook App

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Click **"My Apps"** → **"Create App"**
3. Choose **"Consumer"** or **"None"**
4. **App Name**: CELPIP Practice
5. **App Contact Email**: Your email
6. Click **"Create App"**

### Step 2: Add Facebook Login

1. In your app dashboard, click **"Add Product"**
2. Find **"Facebook Login"** and click **"Set Up"**
3. Choose **"Web"**
4. Skip the quick start

### Step 3: Configure OAuth Settings

1. Go to **Facebook Login** → **Settings**
2. **Valid OAuth Redirect URIs**:
   ```
   http://localhost:5000/callback/facebook
   http://127.0.0.1:5000/callback/facebook
   ```
   Add production callback URL when deploying

3. **Save Changes**

### Step 4: Get App Credentials

1. Go to **Settings** → **Basic**
2. Copy:
   - **App ID**
   - **App Secret** (click "Show")

Add to `.env`:
```bash
FACEBOOK_CLIENT_ID=your-app-id
FACEBOOK_CLIENT_SECRET=your-app-secret
```

### Step 5: Make App Public (for production)

1. Go to **Settings** → **Basic**
2. Toggle **"App Mode"** to **"Live"**
3. Provide required information (privacy policy URL, etc.)

---

## Environment Configuration

### `.env` File

```bash
# Flask Secret Key (generate new one!)
SECRET_KEY=your-secret-key-change-this-to-random-string

# Google OAuth
GOOGLE_CLIENT_ID=123456789.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxxxxxxxxxxxx

# Facebook OAuth  
FACEBOOK_CLIENT_ID=1234567890123456
FACEBOOK_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Application URLs
APP_URL=http://127.0.0.1:5000
REDIRECT_URI_BASE=http://127.0.0.1:5000
```

### Generate Secret Key

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output to `SECRET_KEY` in `.env`

---

## Testing Locally

### 1. Start the App

```bash
source venv/bin/activate  # Windows: venv\Scripts\activate
python app.py
```

### 2. Test OAuth Flow

1. Open `http://127.0.0.1:5000`
2. Click **"🔐 Login"**
3. Choose provider (Google or Facebook)
4. Authorize the app
5. You'll be redirected back and logged in!

### 3. Verify User Data

Check `users/{username}/profile.json`:
```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "provider": "google",
  "picture": "https://...",
  "role": "Basic",
  "created_at": "...",
  "last_accessed": "..."
}
```

---

## Production Deployment

### Update OAuth Settings

When deploying to production (e.g., `myapp.com`):

1. **Google Console**:
   - Add `https://myapp.com` to **Authorized JavaScript origins**
   - Add `https://myapp.com/callback/google` to **Authorized redirect URIs**

2. **Facebook Developers**:
   - Add `https://myapp.com/callback/facebook` to **Valid OAuth Redirect URIs**
   - Make app **"Live"** (not Development)

3. **Update `.env`**:
   ```bash
   APP_URL=https://myapp.com
   REDIRECT_URI_BASE=https://myapp.com
   ```

### Security Checklist

✅ Generate strong `SECRET_KEY`  
✅ Use HTTPS in production  
✅ Don't commit `.env` to git  
✅ Set up proper CORS if needed  
✅ Review OAuth scopes (minimal required)  
✅ Enable app verification (Google/Facebook)  

---

## User Flows

### First-Time User

```
1. Visit site → See "Guest Mode"
2. Click "🔐 Login"
3. Choose provider (Google/Facebook)
4. Authorize app
5. Redirected back → Logged in
6. Profile created automatically
7. Test history tracked
```

### Returning User

```
1. Visit site → Auto-logged in (if cookies valid)
2. See name and avatar
3. All previous test history available
```

### Guest Mode

```
1. Visit site → No login required
2. Take tests normally
3. Progress saved in session only
4. Lost when browser closes
5. Can login anytime to save permanently
```

---

## Troubleshooting

### "Redirect URI mismatch" Error

**Fix**: Ensure callback URL in OAuth console matches exactly:
```
http://127.0.0.1:5000/callback/google
```
(Note: Use `127.0.0.1`, not `localhost`, or add both)

### "App not verified" Warning (Google)

**For Development**: Click "Advanced" → "Go to app (unsafe)"

**For Production**: Submit app for verification in Google Cloud Console

### "App is in Development Mode" (Facebook)

**Fix**: Make app "Live" in Facebook settings, or add test users

### No OAuth Buttons Showing

**Check**:
1. `.env` file exists and has correct credentials
2. Credentials are loaded: `print(os.getenv('GOOGLE_CLIENT_ID'))`
3. No typos in provider names

### User Not Saving

**Check**:
1. Email is returned by provider
2. `users/` folder has write permissions
3. Check Flask console for errors

---

## Features Enabled by Login

| Feature | Guest Mode | Logged In |
|---------|------------|-----------|
| Take tests | ✅ | ✅ |
| View answers | ✅ | ✅ |
| Session progress | ✅ | ✅ |
| **Persistent history** | ❌ | ✅ |
| **Cross-device sync** | ❌ | ✅ |
| **Analytics** | ❌ | ✅ |
| **Leaderboards** | ❌ | ✅ (future) |
| **Premium features** | ❌ | ✅ (future) |

---

## Adding More Providers

Want to add more OAuth providers? (GitHub, Twitter, Microsoft, etc.)

### 1. Register Provider in `utils/oauth_providers.py`

```python
oauth.register(
    name='github',
    client_id=os.getenv('GITHUB_CLIENT_ID'),
    client_secret=os.getenv('GITHUB_CLIENT_SECRET'),
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)
```

### 2. Add to `get_oauth_providers()`

```python
if os.getenv('GITHUB_CLIENT_ID'):
    providers.append({
        'name': 'github',
        'display_name': 'GitHub',
        'icon': '🐙',
        'color': '#333'
    })
```

### 3. Add User Info Extraction

```python
elif provider == 'github':
    return {
        'email': token_data.get('email'),
        'name': token_data.get('name'),
        'picture': token_data.get('avatar_url'),
        'provider': 'github',
        'provider_user_id': token_data.get('id')
    }
```

### 4. Update `.env`

```bash
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
```

Done! The provider will automatically appear on the login page.

---

## Security Best Practices

1. **Secret Key**: Generate strong random key, never reuse
2. **HTTPS Only**: Use HTTPS in production (OAuth requires it)
3. **Minimal Scopes**: Only request email and profile
4. **Validate Tokens**: Always verify OAuth tokens server-side
5. **Session Security**: Use secure cookies in production
6. **Rate Limiting**: Add rate limits to login endpoints
7. **CSRF Protection**: Flask-Login provides CSRF protection

---

##API Reference

### Auth Functions

```python
from utils.auth import get_current_user_email
from flask_login import current_user

# Get current user's email
email = get_current_user_email()  # Works for both OAuth and session

# Check if user is logged in
if current_user.is_authenticated:
    print(current_user.name)
    print(current_user.email)
    print(current_user.provider)  # 'google', 'facebook', etc.
```

### Protecting Routes

```python
from flask_login import login_required

@app.route('/premium-feature')
@login_required
def premium():
    # Only accessible to logged-in users
    return "Premium content"
```

---

## Next Steps

- [ ] Add email/password authentication (optional)
- [ ] Implement role-based access (Basic/Premium)
- [ ] Add user profile edit page
- [ ] Enable/disable specific providers
- [ ] Add user deletion (GDPR compliance)
- [ ] Implement "Remember Me" functionality

---

**Last Updated**: December 8, 2025  
**Version**: 1.0

