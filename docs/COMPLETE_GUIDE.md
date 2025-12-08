# 📚 CELPIP Practice Platform - Documentation

**Complete guide for the CELPIP Practice Test application**

Version: 2.0  
Last Updated: December 8, 2025

---

## 📖 Quick Navigation

### For Users
- [Getting Started](#getting-started) - Setup and installation
- [Using the App](#using-the-app) - Practice and Test modes
- [Features](#features) - What's available

### For Developers
- [Architecture](#architecture) - System design
- [Adding Content](#adding-content) - Adding new tests
- [Configuration](#configuration) - Settings and customization
- [Deployment](#deployment) - Hosting options

### For Administrators
- [User Data](#user-data-management) - Data structure and management
- [Maintenance](#maintenance) - Backups and updates

---

## Getting Started

### System Requirements
- Python 3.9 or higher
- 50MB disk space (+ test content)
- Modern web browser

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/celpip.git
cd celpip
```

2. **Set up virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

5. **Access the app**
```
http://127.0.0.1:5000
```

---

## Using the App

### Two Modes

#### 1. Practice Mode 📚
- **Purpose**: Learn and practice at your own pace
- **Features**:
  - Navigate back and forth between questions
  - View answer key anytime
  - See correct answers immediately
  - Reset and retry parts
  - Track progress per session

#### 2. Test Mode 🎯
- **Purpose**: Simulate real CELPIP exam conditions
- **Features**:
  - Timed sections (1 min per question)
  - Sequential navigation (no going back)
  - Answer validation (must answer all questions)
  - Comprehensive score at the end
  - Test history tracking (with email)

### Test Structure

**Available Tests**: 1-20 (expandable)

**Skills**:
- **Reading**: 4 parts, ~38 questions, ~57 minutes
- **Writing**: 2 tasks (future)
- **Listening**: 6 parts (future)
- **Speaking**: 8 tasks (future)

**Reading Parts**:
- **Part 1**: Correspondence (11 questions, 16.5 min)
- **Part 2**: Apply a Diagram (8 questions, 12 min)
- **Part 3**: Reading for Information (9 questions, 13.5 min)
- **Part 4**: Reading for Viewpoints (10 questions, 15 min)

### User Flow

```
Home Page
  ↓
Select Test
  ↓
Choose Mode (Practice / Test)
  ↓
Complete Parts
  ↓
View Results / Answer Key
```

---

## Features

### Current Features ✅

#### Practice Mode
- ✅ Navigate freely between questions
- ✅ View answer key anytime
- ✅ Reset individual parts or entire test
- ✅ Auto-save answers (session-based)
- ✅ Visual timer with warnings
- ✅ Comprehensive answer key with statistics

#### Test Mode
- ✅ Realistic exam simulation
- ✅ Timed sections (1 min/question)
- ✅ Sequential navigation only
- ✅ Answer validation (must complete all)
- ✅ Progress tracking
- ✅ Pause & resume functionality
- ✅ Final score calculation
- ✅ Test history (with email)

#### UI/UX
- ✅ CELPIP-style professional interface
- ✅ Two-column layout (passage left, questions right)
- ✅ Smart dropdown behavior
- ✅ Inline question dropdowns
- ✅ Responsive design
- ✅ Visual feedback for answers
- ✅ Scroll-independent columns

#### Data Management
- ✅ Folder-per-user structure
- ✅ Separate profile and test history
- ✅ Session-only mode (no email)
- ✅ Role system (Basic, Premium)
- ✅ Privacy-first (gitignored)

### Upcoming Features 🚀

#### Content
- ⏳ Tests 2-20 completion
- ⏳ Writing section
- ⏳ Listening section
- ⏳ Speaking section

#### Features
- ⏳ User accounts (login/register)
- ⏳ Premium features
- ⏳ Progress analytics
- ⏳ Study recommendations
- ⏳ Mobile app (iOS/Android)
- ⏳ PDF export of results
- ⏳ Spaced repetition
- ⏳ Vocabulary builder

---

## Architecture

### Project Structure

```
celpip/
├── app.py                     # Main Flask application
├── config.json               # Application settings
├── requirements.txt          # Python dependencies
│
├── data/                     # Test content (JSON)
│   ├── test_1/
│   │   ├── reading/
│   │   │   ├── part1.json   # 11 questions
│   │   │   ├── part2.json   # 8 questions
│   │   │   ├── part3.json   # 9 questions
│   │   │   └── part4.json   # 10 questions
│   │   ├── writing/
│   │   ├── listening/
│   │   └── speaking/
│   ├── test_2/
│   └── ...
│
├── static/                   # Static assets
│   └── images/
│       └── test_1/
│           └── reading/
│               └── diagram.png
│
├── templates/                # HTML templates
│   ├── test_list.html       # Home page
│   ├── test_detail.html     # Test overview
│   ├── test_section.html    # Practice Mode
│   ├── test_mode_section.html  # Test Mode
│   └── comprehensive_answer_key.html
│
├── utils/                    # Python utilities
│   ├── data_loader.py       # Load test data
│   └── results_tracker.py   # User data management
│
├── users/                    # User data (gitignored)
│   └── {username}/
│       ├── profile.json
│       └── test_history.json
│
└── docs/                     # Documentation
```

### Data Flow

```
User Request
  ↓
Flask Route (app.py)
  ↓
Data Loader (utils/data_loader.py)
  ↓
Load JSON (data/test_X/...)
  ↓
Process & Prepare Data
  ↓
Render Template (templates/...)
  ↓
Response to User
```

### Design Principles

1. **Separation of Concerns**
   - Data: JSON files
   - Logic: Python utilities
   - Presentation: Flask + Jinja2
   - Static: Images organized by test

2. **Platform Agnostic**
   - JSON data can be consumed by any platform
   - Ready for mobile apps (iOS/Android)
   - API-ready structure

3. **Scalability**
   - Easy to add new tests (just add JSON)
   - Modular code structure
   - Database-ready design

4. **Privacy First**
   - User data gitignored
   - Optional email (session-only mode)
   - GDPR-compliant deletion

---

## Adding Content

### Adding a New Test

1. **Create test folder**
```bash
mkdir -p data/test_X/reading
```

2. **Create part files**
```bash
cd data/test_X/reading
touch part1.json part2.json part3.json part4.json
```

3. **Fill in content** (see JSON structure below)

4. **Add images** (if needed)
```bash
mkdir -p static/images/test_X/reading
# Add diagram.png, etc.
```

### JSON Structure

#### Part 1: Correspondence
```json
{
  "title": "Reading Correspondence",
  "type": "correspondence",
  "instructions": "Read the message and answer questions 1-11.",
  "timeout_minutes": 16.5,
  "sections": [
    {
      "type": "passage",
      "title": "Message from Greg",
      "content": "Hi everyone,\n\nI wanted to let you know..."
    },
    {
      "type": "questions",
      "questions": [
        {
          "id": 1,
          "text": "What is the main purpose of this message?",
          "options": [
            "To announce a meeting",
            "To cancel an event",
            "To request feedback"
          ],
          "answer": 0
        }
      ]
    },
    {
      "type": "response_passage",
      "title": "Response Message",
      "content": "Hi Greg,\n\nThanks for <<Q7>>. I think <<Q8>>...",
      "questions": [
        {
          "id": 7,
          "options": ["the update", "your email", "the information"],
          "answer": 0
        }
      ]
    }
  ]
}
```

**Key Fields**:
- `id`: Unique question number within part
- `answer`: Index of correct option (0-based)
- `options`: Array of answer choices
- `<<QX>>`: Placeholder for inline dropdown

---

## Configuration

### config.json

```json
{
  "time_per_question": {
    "reading": 1.0,     // 1 minute per question
    "writing": 30.0,    // 30 minutes per task
    "speaking": 1.0,
    "listening": 1.0
  },
  "default_time_per_question": 1.0,
  
  "ui_settings": {
    "timer_warning_seconds": 60,
    "auto_submit_on_timeout": true,
    "show_question_numbers": true
  },
  
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

### Environment Variables

Create `.env` file (optional):
```bash
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
PORT=5000
```

---

## Deployment

### Local Network

Share on your local network:

```python
# app.py
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',  # Allow external connections
        port=5000,
        debug=False
    )
```

Access from other devices:
```
http://YOUR_IP:5000
```

### Free Hosting Options

#### 1. Render.com ⭐ RECOMMENDED
- **Free tier**: 750 hours/month
- **Auto-deploy** from GitHub
- **Easy setup**: Connect repo → Deploy
- **HTTPS** included
- **URL**: `your-app.onrender.com`

**Steps**:
1. Push code to GitHub
2. Sign up at render.com
3. New → Web Service
4. Connect GitHub repo
5. Deploy!

#### 2. PythonAnywhere
- **Free tier**: 1 web app
- **URL**: `username.pythonanywhere.com`
- **Easy Flask setup**

#### 3. Heroku (Limited Free)
- **Free tier**: 550-1000 hours/month
- **Add-ons** available
- **CLI tools**

### Production Deployment

For production with many users:

1. **Use PostgreSQL** instead of JSON files
2. **Add caching** (Redis)
3. **Use gunicorn** web server
4. **Set up monitoring**
5. **Enable backups**

---

## User Data Management

### Data Structure

```
users/
  username/
    ├── profile.json         # User metadata
    └── test_history.json    # Test attempts
```

### Profile Structure

```json
{
  "email": "user@example.com",
  "role": "Basic",
  "created_at": "2025-12-08T...",
  "last_accessed": "2025-12-08T..."
}
```

### Test History Structure

```json
{
  "tests": {
    "test_1": {
      "test_number": 1,
      "attempts": [
        {
          "attempt_id": "uuid",
          "started_at": "...",
          "completed_at": "...",
          "skills": {
            "reading": {
              "parts": {
                "1": {
                  "answers": {"1": 0, "2": 1, ...},
                  "score": 8,
                  "max_score": 11
                }
              },
              "total_score": 30,
              "total_max": 38
            }
          },
          "total_score": 30,
          "total_max": 38,
          "percentage": 78.9
        }
      ]
    }
  }
}
```

### Session-Only Mode

**Without email**:
- Data stored in Flask session only
- No persistent storage
- Lost when browser closes
- Perfect for anonymous practice

**With email**:
- Persistent storage in `users/` folder
- Track history across sessions
- View progress over time

### User Roles

**Current**:
- `Basic`: Default, free access

**Future**:
- `Premium`: Advanced features
- `Admin`: Management access

---

## Maintenance

### Backups

#### Manual Backup
```bash
# Backup all users
tar -czf users_backup_$(date +%Y%m%d).tar.gz users/

# Restore
tar -xzf users_backup_20251208.tar.gz
```

#### Automated (Future)
- Daily backups to cloud storage
- Incremental backups
- Point-in-time recovery

### Database Migration (Future)

When ready for PostgreSQL:

1. Install PostgreSQL on Render ($7/month)
2. Run migration script (TBD)
3. Keep JSON as backup
4. Sync both ways initially

**When to migrate**:
- 100+ active users
- Need complex queries
- Want analytics dashboard
- Multiple concurrent users

### Monitoring

**Check**:
- User count: `python -c "from utils.results_tracker import ResultsTracker; t=ResultsTracker(); print(len(t.list_all_users()))"`
- Disk usage: `du -sh users/`
- Error logs: Check Flask console

### Updates

**Updating the app**:
```bash
git pull origin main
pip install -r requirements.txt
# Restart server
```

**Adding test content**:
1. Create JSON files in `data/test_X/`
2. Add images to `static/images/test_X/`
3. No code changes needed!

---

## Troubleshooting

### Common Issues

#### Port already in use
```bash
# Use different port
python app.py --port 5001
```

#### Module not found
```bash
# Activate virtual environment
source venv/bin/activate  # Unix
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### Images not loading
- Check path: `static/images/test_X/skill/image.png`
- Verify image exists
- Check file permissions

#### User data not saving
- Ensure `users/` directory exists
- Check write permissions
- Verify email format
- Check Flask session configuration

---

## Contributing

### Code Style
- PEP 8 for Python
- 4 spaces indentation
- Clear variable names
- Comments for complex logic

### Pull Request Process
1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit PR with clear description

### Adding Features
1. Update documentation
2. Add tests if applicable
3. Follow existing patterns
4. Keep it simple

---

## Support & Contact

### Issues
Report bugs or request features on GitHub Issues

### Documentation
All docs in `/docs` folder

### Updates
Check GitHub for latest version

---

## License

[Your License Here]

---

## Changelog

### Version 2.0 (Dec 8, 2025)
- ✅ Folder-per-user data structure
- ✅ Practice & Test Mode complete
- ✅ CELPIP-style UI
- ✅ Auto-save functionality
- ✅ Answer validation
- ✅ Comprehensive answer key

### Version 1.0 (Earlier)
- Initial release
- Basic test functionality
- Single test support

---

**Happy Practicing! 🎓**

