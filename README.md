# 🎓 CELPIP Practice Platform

**Professional CELPIP test practice application with realistic exam simulation**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## ✨ Features

### 📚 Practice Mode
- Navigate freely between questions
- View answer keys anytime
- Reset and retry parts
- Auto-save progress
- Detailed explanations

### 🎯 Test Mode
- Realistic exam simulation
- Timed sections (1 min/question)
- Sequential navigation (like real exam)
- Answer validation
- Comprehensive scoring
- Test history tracking

### 🎧 Listening Module 🆕
- Sequential state machine: Passage → Q1 → Q2 → ... → Next Passage → ...
- Practice Mode: replay audio freely, "Skip to Questions" button on all parts
- Test Mode: "Skip to Questions" button on all parts, forward-only navigation
- Parts 1-3: One question at a time with 30-second per-question timer
- Parts 1-3: Split-pane layout — left panel (image + question audio), right panel (answer options)
- Part 1: Sub-parts (1.1, 1.2, 1.3) with separate passage audio, sequential flow
- Parts 4-6: Inline dropdown select boxes (Reading Part 3/4 style, selected → completed sentence)
- Question-specific images: questions with `imageUrl` display a reference image in the left panel
- Video support (Part 5: Discussion)
- Audio hosted on Cloudinary (`.m4a` for audio, `.mp4` for video)
- 6 parts, 38 questions per test

### 🎨 Professional UI
- CELPIP-style interface
- Two-column layout (passage + questions)
- Smart inline dropdowns
- Visual timer with warnings
- Responsive design
- Google OAuth login
- Facebook OAuth login
- Guest mode (no login required)

### 📊 Progress Tracking
- **Guest Mode**: Session-based (no login required)
- **Authenticated Mode**: OAuth login (Google/Facebook)
- Persistent history across sessions
- Detailed statistics and analytics
- Answer key with comprehensive results

---

## 🚀 Quick Start

### 1. Install
```bash
git clone https://github.com/YOUR_USERNAME/celpip.git
cd celpip
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run
```bash
python app.py
```

### 3. Open
```
http://127.0.0.1:5000
```

**That's it!** 🎉

---

## 📖 Documentation

- **[Deployment Guide](docs/DEPLOYMENT.md)** — Render.com + OAuth setup
- **[Architecture](docs/ARCHITECTURE.md)** — System design & storage layer
- **[Adding Reading Tests](docs/ADDING_TESTS.md)** — Content creation for Reading
- **[Adding Listening Tests](docs/ADDING_LISTENING_TESTS.md)** — Content creation for Listening
- **[Configuration](docs/CONFIG_GUIDE.md)** — Timer & UI settings
- **[User Data](docs/USER_DATA_STRUCTURE.md)** — PostgreSQL schema & file fallback
- **[Vocabulary Notes](docs/VOCABULARY_NOTES.md)** — Vocabulary feature docs

---

## 🏗️ Project Structure

```
celpip/
├── app.py                    # Main Flask application
├── config.json              # Settings & configuration
├── requirements.txt         # Python dependencies
│
├── data/                    # Test content (JSON)
│   ├── test_1/             # Test 1 data
│   │   ├── reading/
│   │   │   ├── part1.json ... part4.json
│   │   └── listening/      # 🆕 Listening module
│   │       ├── part1.json ... part6.json
│   └── test_2/             # More tests...
│
├── static/                  # Static assets
│   └── images/             # Test & scene images
│   # Audio/video hosted on Cloudinary (referenced by URL in JSON)
│
├── templates/              # HTML templates
│   ├── test_list.html     # Home page
│   ├── test_section.html  # Reading Practice Mode
│   ├── test_mode_section.html  # Reading Test Mode
│   ├── listening_section.html  # 🆕 Listening Practice Mode
│   └── listening_test_mode_section.html  # 🆕 Listening Test Mode
│
├── utils/                  # Python utilities
│   ├── data_loader.py     # Load test data
│   ├── database.py        # PostgreSQL connection & queries
│   ├── results_tracker.py # Public facade for app.py
│   └── storage/           # Repository pattern (pluggable backends)
│       ├── interfaces.py  # Abstract contracts
│       ├── file_storage.py # File-based implementation
│       ├── db_storage.py  # PostgreSQL implementation
│       └── factory.py     # Selects backend at startup
│
├── users/                  # User data — file fallback (gitignored)
│   └── {username}/
│       ├── profile.json
│       ├── test_history.json
│       └── vocabulary_notes.json
│
└── docs/                   # Documentation
```

---

## 🎯 Current Status

### ✅ Completed
- Reading section (Tests 1-10 complete)
- **Listening section (Test 1 complete — 6 parts, 33 questions)** 🆕
- Practice Mode with full navigation
- Test Mode with realistic simulation
- CELPIP-style UI with two-column layout
- Listening state machine (Playback → Questions) 🆕
- Audio/video player with progress visualization 🆕
- Auto-save functionality
- Answer validation (all dropdowns required)
- Comprehensive answer key (Reading + Listening)
- User authentication (OAuth)
- Google login integration
- Facebook login integration
- Guest mode (no login required)
- User data management (folder-per-user + PostgreSQL)
- Vocabulary notes (per test/skill/part)
- PostgreSQL storage with file-based fallback
- Repository pattern — pluggable storage backends
- Session & persistent storage
- Deployment ready (Render.com with `render.yaml` Blueprint)

### 🚧 In Progress
- Listening content for Tests 2-10
- Tests 2-20 content (Writing, Speaking)
- Writing section
- Speaking section

### 📋 Planned
- Premium features (enhanced analytics)
- Progress analytics dashboard
- Mobile app (iOS/Android with Capacitor)
- PDF export of results
- Study recommendations based on performance
- Email notifications for milestones

---

## 🌐 Deployment

### Production: Render.com

- **Web service**: Python + gunicorn via `render.yaml` Blueprint
- **Database**: PostgreSQL (free-tier — expires after 90 days; paid plan recommended for persistence)
- **Audio/Video**: Hosted on **Cloudinary** (`.m4a` audio, `.mp4` video) — referenced by URL in test JSON
- **OAuth**: Google & Facebook login configured via environment variables

**See**: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for complete step-by-step guide

### Local Development
```bash
python app.py  # http://127.0.0.1:5000 — uses JSON file storage as fallback
```

---

## 🛠️ Tech Stack

- **Backend**: Python 3.9+, Flask 3.0+
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Templates**: Jinja2
- **Authentication**: OAuth 2.0 (Google, Facebook) via Authlib
- **Session Management**: Flask-Login
- **Test Data**: JSON files (platform-agnostic)
- **User Storage**: PostgreSQL (production) / JSON files (local dev fallback)
- **Storage Architecture**: Repository pattern — `UserRepository`, `TestRepository`, `VocabularyRepository`
- **Audio/Video Hosting**: Cloudinary (`.m4a` audio, `.mp4` video for Listening tests)
- **Deployment**: Render.com (web + PostgreSQL via Blueprint)

---

## 📊 Test Structure

### Reading Section
| Part | Type | Questions | Time |
|------|------|-----------|------|
| 1 | Correspondence | 11 | 16.5 min |
| 2 | Apply a Diagram | 8 | 12 min |
| 3 | Reading for Information | 9 | 13.5 min |
| 4 | Reading for Viewpoints | 10 | 15 min |
| **Total** | | **38** | **~57 min** |

### Listening Section 🆕
| Part | Type | Questions | Media | Layout | Question UI |
|------|------|-----------|-------|--------|-------------|
| 1 | Problem Solving | 5 (3 sub-parts) | Audio | Split pane, per-question audio | Radio buttons |
| 2 | Daily Life Conversation | 5 | Audio | Split pane, per-question audio | Radio buttons |
| 3 | Listening for Information | 5 | Audio | Split pane, per-question audio | Radio buttons |
| 4 | Listening to a News Item | 6 | Audio | Full-width | Inline dropdowns |
| 5 | Listening to a Discussion | 6 | Video | Full-width | Inline dropdowns |
| 6 | Listening for Viewpoints | 6 | Audio | Full-width | Inline dropdowns |
| **Total** | | **33** | | | |

### Future Sections
- Writing (2 tasks, ~53 min)
- Speaking (8 tasks, ~15-20 min)

---

## 👥 Use Cases

### For Test Takers
- Practice CELPIP tests anytime
- Track progress over time
- Identify weak areas
- Build confidence

### For Teachers
- Assign practice tests
- Monitor student progress
- Share on local network
- No internet required

### For Institutions
- Self-hosted solution
- Privacy-focused
- Customizable content
- No recurring fees

---

## 🔐 Privacy & Data

### Guest Mode (Default)
- No login required
- Data in browser session only
- Perfect for anonymous practice
- Progress cleared on browser close

### Authenticated Mode (OAuth)
- Login with Google or Facebook
- No passwords stored (OAuth only)
- Data stored in **PostgreSQL** (production) or `users/` JSON files (local dev)
- Persistent history across sessions
- Never shared with third parties
- GDPR-compliant data isolation

### Data Structure
```
# Production (PostgreSQL)
table: users              # Email, role, timestamps
table: test_history       # Test attempts & scores (JSONB)
table: vocabulary_notes   # Per-word notes with context

# Local dev fallback (file-based)
users/
  {username}/
    profile.json
    test_history.json
    vocabulary_notes.json
```

**See**: [docs/USER_DATA_STRUCTURE.md](docs/USER_DATA_STRUCTURE.md)

---

## 🎨 Screenshots

### Home Page
*Professional test selection interface*

### Practice Mode
*CELPIP-style two-column layout*

### Test Mode
*Realistic exam simulation with timer*

### Answer Key
*Comprehensive results with statistics*

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

See [docs/ADDING_TESTS.md](docs/ADDING_TESTS.md) for content contribution guidelines

---

## 📝 Adding Test Content

### Reading
```bash
mkdir -p data/test_X/reading
```

### Listening
```bash
mkdir -p data/test_X/listening
mkdir -p static/images/test_X/listening   # Scene images only — audio/video hosted on Cloudinary
```

Audio and video files are hosted on **Cloudinary** and referenced by URL in the JSON data.
No code changes needed — just add JSON files and the app auto-discovers them.

See [docs/ADDING_LISTENING_TESTS.md](docs/ADDING_LISTENING_TESTS.md) for details

---

## 🔧 Configuration

Edit `config.json`:

```json
{
  "time_per_question": {
    "reading": 1.0,
    "writing": 30.0
  },
  "ui_settings": {
    "timer_warning_seconds": 60,
    "auto_submit_on_timeout": true
  }
}
```

See [docs/CONFIG_GUIDE.md](docs/CONFIG_GUIDE.md) for all options

---

## 📈 Roadmap

### Phase 1: Core Features ✅
- [x] Reading section
- [x] Practice & Test modes
- [x] Answer validation
- [x] User data management
- [x] OAuth authentication (Google/Facebook)
- [x] Guest mode
- [x] Deployment guide

### Phase 2: Content 🚧
- [ ] Tests 2-20
- [x] Listening section (Test 1 complete)
- [ ] Listening content for Tests 2-10
- [ ] Writing section
- [ ] Speaking section

### Phase 3: Features 📋
- [ ] Premium analytics dashboard
- [ ] Progress recommendations
- [ ] Email notifications
- [ ] PDF export
- [ ] Mobile apps (iOS/Android)

### Phase 4: Scale 🚀
- [x] PostgreSQL database (repository pattern, auto-fallback to files)
- [x] Cloud hosting (Render.com with `render.yaml` Blueprint)
- [ ] API for mobile
- [ ] Admin dashboard

---

## 🐛 Troubleshooting

### Port already in use
```bash
python app.py --port 5001
```

### Module not found
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Images not loading
Check: `static/images/test_X/skill/image.png`

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md#troubleshooting) for deployment-specific issues

---

## 📞 Support

- **Documentation**: [docs/](docs/)
- **Issues**: GitHub Issues
- **Email**: [Your email]

---

## 📜 License

[MIT License](LICENSE) - Feel free to use for personal or commercial projects

---

## 🙏 Acknowledgments

- CELPIP for test format inspiration
- Flask community
- All contributors

---

## 📊 Stats

- **Reading Questions**: ~380 (Tests 1-10 complete)
- **Listening Questions**: 33 (Test 1 complete)
- **Skills Implemented**: Reading, Listening
- **Supported Platforms**: Web (production ready)
- **OAuth Providers**: Google, Facebook
- **Deployment**: Render.com (web + PostgreSQL + Cloudinary for media)

---

## 🔖 Version

**Current Version**: 5.0  
**Last Updated**: March 16, 2026  
**Status**: Production Ready 🚀  
**Skills**: Reading ✅ | Listening ✅ | Writing 🚧 | Speaking 🚧  
**OAuth**: ✅ Enabled (Google, Facebook)  
**Database**: ✅ PostgreSQL with file-based fallback

---

**Made with ❤️ for CELPIP test takers**

[⭐ Star this repo](https://github.com/YOUR_USERNAME/celpip) | [📖 Read the docs](docs/) | [🐛 Report issues](https://github.com/YOUR_USERNAME/celpip/issues)
