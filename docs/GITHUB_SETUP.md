# 🌐 Publishing to GitHub

Follow these steps to publish your CELPIP Practice App to GitHub.

## 📋 Prerequisites

- Git installed on your computer
- GitHub account (free at https://github.com)

## 🎯 Step-by-Step Instructions

### 1️⃣ Create a New Repository on GitHub

1. Go to https://github.com
2. Click the **"+"** button (top right) → **"New repository"**
3. Fill in:
   - **Repository name**: `celpip-practice` (or your preferred name)
   - **Description**: "CELPIP Test Practice Application - Reading, Writing, Speaking, Listening"
   - **Public** or **Private**: Your choice
   - **DO NOT** initialize with README (we already have one)
4. Click **"Create repository"**

### 2️⃣ Connect Your Local Repository to GitHub

Copy the commands from GitHub (they'll look similar to this):

```bash
cd /Users/longcao/workspace/github/celpip

# Add GitHub as remote (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/celpip-practice.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

### 3️⃣ Verify on GitHub

1. Refresh your GitHub repository page
2. You should see all your files uploaded
3. The README.md will display automatically

## 🔄 Making Updates

### After making changes:

```bash
# Stage changes
git add .

# Commit changes
git commit -m "Description of your changes"

# Push to GitHub
git push
```

### Pull latest changes (if working from multiple computers):

```bash
git pull origin main
```

## 🎨 Customizing Your Repository

### Add Topics/Tags

On GitHub repository page:
1. Click the gear icon ⚙️ next to "About"
2. Add topics: `celpip`, `test-practice`, `education`, `flask`, `python`, `reading`, `learning`
3. Save changes

### Update Repository Description

1. Click the gear icon ⚙️ next to "About"
2. Add website: `http://localhost:5000` (or your deployed URL)
3. Check "Releases" and "Packages" if needed
4. Save changes

## 🌟 Optional: Add a License

```bash
# Add MIT License (or choose another)
# Create LICENSE file on GitHub:
# Add file → Create new file → Name: LICENSE
# Choose template → MIT License → Commit
```

## 👥 Collaborating

### Invite collaborators:

1. Go to repository **Settings** → **Collaborators**
2. Click **"Add people"**
3. Search by username or email
4. They can then clone and contribute

### Clone for others:

Share this command:
```bash
git clone https://github.com/YOUR_USERNAME/celpip-practice.git
cd celpip-practice
./setup.sh  # or setup.bat on Windows
```

## 📱 Repository Badges (Optional)

Add to top of README.md:

```markdown
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
```

## 🚀 Deploying Online (Optional)

### Deploy to Heroku, Railway, or Render:

1. Add `Procfile`:
```
web: python app.py
```

2. Update `app.py` for production:
```python
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

3. Follow platform-specific deployment instructions

## 📊 GitHub Pages (for documentation only)

You can host documentation on GitHub Pages:

1. Go to repository **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: **main** → **/docs** (create docs folder)
4. Save

## 🔐 Security Best Practices

### Never commit:
- ❌ Passwords or API keys
- ❌ Secret keys (use environment variables)
- ❌ Personal information
- ❌ Large binary files (use Git LFS)

### Use environment variables:
```python
import os
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(16))
```

## 📝 Git Best Practices

### Commit messages:
```bash
# Good commit messages:
git commit -m "Add: Reading Part 3 test data"
git commit -m "Fix: Timer not resetting between tests"
git commit -m "Update: Improve dropdown styling"

# Bad commit messages:
git commit -m "changes"
git commit -m "fix"
```

### Branching strategy:
```bash
# Create feature branch
git checkout -b feature/add-writing-tests

# Work on feature...
git add .
git commit -m "Add: Writing test Part 1"

# Merge back to main
git checkout main
git merge feature/add-writing-tests
git push
```

## 🆘 Common Issues

### Problem: Push rejected

```bash
# Solution: Pull first, then push
git pull origin main
git push origin main
```

### Problem: Merge conflicts

```bash
# View conflicts
git status

# Edit conflicted files manually
# Then:
git add .
git commit -m "Resolve merge conflicts"
git push
```

### Problem: Forgot to add .gitignore

```bash
# Remove tracked files that should be ignored
git rm -r --cached venv/
git rm -r --cached __pycache__/
git commit -m "Remove ignored files from tracking"
git push
```

## ✅ Your Repository is Ready!

Share your repository URL with others:
```
https://github.com/YOUR_USERNAME/celpip-practice
```

Anyone can now:
1. Clone your repository
2. Run `setup.sh` (or `setup.bat`)
3. Start practicing CELPIP tests!

---

**Need help?** Check [GitHub Docs](https://docs.github.com) or open an issue!

