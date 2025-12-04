# Configuration Guide

## 📝 config.json

All application settings are stored in `config.json` for easy modification.

## ⏱️ Time Configuration

### Time Per Question

Edit `time_per_question` to change time allocation for each skill:

```json
{
  "time_per_question": {
    "reading": 1.5,     // 1.5 minutes per reading question
    "writing": 30.0,    // 30 minutes per writing task
    "speaking": 1.5,    // 1.5 minutes per speaking task
    "listening": 1.5    // 1.5 minutes per listening question
  }
}
```

**Example:** To give 2 minutes per reading question:
```json
"reading": 2.0
```

### Custom Timeouts

Override time for specific test parts:

```json
{
  "custom_timeouts": {
    "1_reading_1": 20.0,    // Test 1, Reading, Part 1: 20 minutes
    "1_reading_3": 15.0,    // Test 1, Reading, Part 3: 15 minutes
    "2_writing_1": 35.0     // Test 2, Writing, Part 1: 35 minutes
  }
}
```

**Format:** `"test_skill_part": minutes`

## 🎨 UI Settings

```json
{
  "ui_settings": {
    "timer_warning_seconds": 60,      // Show warning when < 60 seconds left
    "auto_submit_on_timeout": true,   // Auto-submit when time expires
    "show_question_numbers": true     // Display question numbers
  }
}
```

### Change Warning Time

To show warning at 2 minutes (120 seconds):
```json
"timer_warning_seconds": 120
```

### Disable Auto-Submit

To prevent automatic submission on timeout:
```json
"auto_submit_on_timeout": false
```

## 📊 Test Metadata

Information about test structure:

```json
{
  "test_metadata": {
    "total_tests": 20,
    "skills": ["reading", "writing", "speaking", "listening"],
    "reading_parts": 4,
    "writing_parts": 2,
    "speaking_parts": 8,
    "listening_parts": 6
  }
}
```

## 🔧 How to Make Changes

### 1. Edit config.json

```bash
# Open in your favorite editor
nano config.json
# or
code config.json
```

### 2. Make Your Changes

```json
{
  "time_per_question": {
    "reading": 2.0  // Changed from 1.5 to 2.0
  }
}
```

### 3. Save and Restart

```bash
# Restart the Flask app
python app.py
```

Changes take effect immediately!

## 📋 Common Scenarios

### Scenario 1: Give More Time for Reading

**Before:**
```json
"reading": 1.5  // 11 questions = 16.5 minutes
```

**After:**
```json
"reading": 2.0  // 11 questions = 22 minutes
```

### Scenario 2: Different Time for Specific Test

**Problem:** Test 1 Part 3 is harder, needs more time

**Solution:**
```json
{
  "custom_timeouts": {
    "1_reading_3": 18.0  // Extra time for this specific part
  }
}
```

### Scenario 3: Change Warning Alert Time

**Before:**
```json
"timer_warning_seconds": 60  // Warning at 1 minute
```

**After:**
```json
"timer_warning_seconds": 300  // Warning at 5 minutes
```

## 🔄 Reload Configuration

The application automatically loads config on startup. To reload without restarting:

```python
from config import reload_config
reload_config()  # Reloads from config.json
```

## ✅ Validation

The app uses sensible defaults if config values are missing:

| Setting | Default | Valid Range |
|---------|---------|-------------|
| `time_per_question` | 1.5 | 0.5 - 60.0 |
| `timer_warning_seconds` | 60 | 10 - 300 |
| `auto_submit_on_timeout` | true | true/false |

## 📦 Default Configuration

If `config.json` is missing, these defaults are used:

```json
{
  "time_per_question": {
    "reading": 1.5,
    "writing": 30.0,
    "speaking": 1.5,
    "listening": 1.5
  },
  "default_time_per_question": 1.5,
  "custom_timeouts": {}
}
```

## 🆘 Troubleshooting

### Config not loading?

1. Check file exists: `ls -la config.json`
2. Check JSON syntax: `python -m json.tool config.json`
3. Check file permissions: `chmod 644 config.json`

### Changes not taking effect?

1. Restart the Flask app
2. Clear browser cache
3. Check for typos in config.json

### Invalid JSON?

Use a JSON validator:
```bash
python -m json.tool config.json
```

If valid, you'll see formatted output.
If invalid, you'll see an error message.

## 💡 Tips

✅ **Do:**
- Use a JSON editor with syntax highlighting
- Test changes on one test part first
- Keep backups of working config
- Document custom timeouts with comments in code

❌ **Don't:**
- Set time < 0.5 minutes (too short)
- Set time > 60 minutes (too long)
- Remove required fields
- Use trailing commas in JSON

## 📖 Example Configurations

### For Testing (Quick Tests)
```json
{
  "time_per_question": {
    "reading": 0.5,  // 30 seconds per question
    "writing": 5.0,
    "speaking": 0.5,
    "listening": 0.5
  }
}
```

### For Practice (Standard)
```json
{
  "time_per_question": {
    "reading": 1.5,
    "writing": 30.0,
    "speaking": 1.5,
    "listening": 1.5
  }
}
```

### For Learning (Extended Time)
```json
{
  "time_per_question": {
    "reading": 3.0,   // Double time for learning
    "writing": 45.0,
    "speaking": 3.0,
    "listening": 3.0
  }
}
```

---

**Need help?** Open an issue on GitHub or check the documentation!

