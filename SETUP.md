# 🚀 Quick Setup Guide

Get the CELPIP Practice App running in 3 simple steps!

## Prerequisites

- Python 3.9 or higher
- Git (for cloning)

## Quick Start

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/celpip.git
cd celpip
```

### 2️⃣ Run the Setup Script

**On macOS/Linux:**
```bash
./setup.sh
```

**On Windows:**
```bash
setup.bat
```

### 3️⃣ Start the Application

```bash
# Activate virtual environment (if not already activated)
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Run the app
python app.py
```

Open your browser and go to: **http://localhost:5000**

---

## Manual Setup (if scripts don't work)

### Step 1: Create Virtual Environment

```bash
python3 -m venv venv
```

### Step 2: Activate Virtual Environment

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
python app.py
```

Visit: **http://localhost:5000**

---

## 🎯 What's Included

After setup, you'll have:

✅ **Test 1 - Reading**
- Part 1: Reading Correspondence (11 questions, 16.5 min)
- Part 2: Reading to Apply a Diagram (8 questions, 12 min)

✅ **Features**
- Timed tests with visual countdown
- Instant scoring and feedback
- Side-by-side layouts for easy reference
- Modern, responsive design

---

## 📁 Project Structure

```
celpip/
├── app.py              # Flask application
├── requirements.txt    # Python dependencies
├── data/              # Test data (JSON)
│   └── test_1/
│       └── reading/
├── static/            # Images and assets
├── templates/         # HTML templates
└── utils/            # Utilities
```

---

## 🛠️ Troubleshooting

### Port 5000 Already in Use

```bash
# Run on different port
python app.py --port 5001
```

Or modify `app.py`:
```python
app.run(debug=True, port=5001)
```

### Permission Denied on setup.sh

```bash
chmod +x setup.sh
./setup.sh
```

### Module Not Found

Make sure virtual environment is activated:
```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

Then reinstall:
```bash
pip install -r requirements.txt
```

---

## 🔄 Updating

Pull latest changes:
```bash
git pull origin main
```

Update dependencies (if changed):
```bash
pip install -r requirements.txt --upgrade
```

---

## 💡 Adding More Tests

To add more test content:

1. Create JSON files in `data/test_X/skill/`
2. Add images to `static/images/test_X/skill/`
3. Restart the app - new tests appear automatically!

See `data/README.md` for data format details.

---

## 🆘 Need Help?

- Check `README.md` for full documentation
- See `ARCHITECTURE.md` for technical details
- Open an issue on GitHub

---

## 📝 License

Educational use only.

