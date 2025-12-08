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

### 🎨 Professional UI
- CELPIP-style interface
- Two-column layout (passage + questions)
- Smart inline dropdowns
- Visual timer with warnings
- Responsive design

### 📊 Progress Tracking
- Session-based (no email required)
- Persistent history (with email)
- Detailed statistics
- Answer key with explanations

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

### 📘 [Complete Guide](docs/COMPLETE_GUIDE.md) ⭐ START HERE
Everything you need in one comprehensive document

### 📂 Quick Links
- **Setup**: [docs/SETUP.md](docs/SETUP.md)
- **Architecture**: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Adding Tests**: [docs/ADDING_TESTS.md](docs/ADDING_TESTS.md)
- **Deployment**: [docs/FREE_HOSTING.md](docs/FREE_HOSTING.md)
- **All Docs**: [docs/README.md](docs/README.md)

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
│   │   └── reading/
│   │       ├── part1.json
│   │       ├── part2.json
│   │       ├── part3.json
│   │       └── part4.json
│   └── test_2/             # More tests...
│
├── static/                  # Static assets
│   └── images/             # Test images
│
├── templates/              # HTML templates
│   ├── test_list.html     # Home page
│   ├── test_section.html  # Practice Mode
│   └── test_mode_section.html  # Test Mode
│
├── utils/                  # Python utilities
│   ├── data_loader.py     # Load test data
│   └── results_tracker.py # Manage user data
│
├── users/                  # User data (gitignored)
│   └── {username}/
│       ├── profile.json
│       └── test_history.json
│
└── docs/                   # Documentation
```

---

## 🎯 Current Status

### ✅ Completed
- Reading section (Test 1 complete, Test 2 template)
- Practice Mode
- Test Mode
- CELPIP-style UI
- Auto-save functionality
- Answer validation
- Comprehensive answer key
- User data management
- Session & persistent storage

### 🚧 In Progress
- Tests 2-20 content
- Writing section
- Listening section
- Speaking section

### 📋 Planned
- User accounts (login/register)
- Premium features
- Progress analytics
- Mobile app (iOS/Android)
- PDF export
- Study recommendations

---

## 🌐 Deployment

### Local Network
```python
# app.py
app.run(host='0.0.0.0', port=5000)
```
Access from any device: `http://YOUR_IP:5000`

### Free Hosting

**Render.com** (Recommended)
1. Push to GitHub
2. Sign up at render.com
3. Connect repo
4. Deploy! ✨

**Other Options:**
- PythonAnywhere
- Heroku
- Railway

See [docs/FREE_HOSTING.md](docs/FREE_HOSTING.md) for details

---

## 🛠️ Tech Stack

- **Backend**: Python 3.9+, Flask 3.0+
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Templates**: Jinja2
- **Data**: JSON files (future: PostgreSQL)
- **Storage**: File-based (scalable to database)

---

## 📊 Test Structure

### Reading Section (Current)
| Part | Type | Questions | Time |
|------|------|-----------|------|
| 1 | Correspondence | 11 | 16.5 min |
| 2 | Apply a Diagram | 8 | 12 min |
| 3 | Reading for Information | 9 | 13.5 min |
| 4 | Reading for Viewpoints | 10 | 15 min |
| **Total** | | **38** | **~57 min** |

### Future Sections
- Writing (2 tasks, ~53 min)
- Listening (38 questions, ~47 min)
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

### Session-Only Mode
- No email required
- Data in browser session only
- Perfect for anonymous practice

### Persistent Mode
- Optional email for tracking
- Data stored locally
- Never shared
- GDPR-compliant deletion

### Data Structure
```
users/
  username/
    profile.json       # Email, role, timestamps
    test_history.json  # Test attempts & scores
```

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

See [docs/COMPLETE_GUIDE.md](docs/COMPLETE_GUIDE.md#contributing) for guidelines

---

## 📝 Adding Test Content

1. Create test folder:
```bash
mkdir -p data/test_X/reading
```

2. Add JSON files:
```json
{
  "title": "Reading Part 1",
  "type": "correspondence",
  "instructions": "Read and answer...",
  "sections": [...]
}
```

3. No code changes needed!

See [docs/ADDING_TESTS.md](docs/ADDING_TESTS.md) for details

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

### Phase 2: Content 🚧
- [ ] Tests 2-20
- [ ] Writing section
- [ ] Listening section
- [ ] Speaking section

### Phase 3: Features 📋
- [ ] User accounts
- [ ] Progress analytics
- [ ] Premium features
- [ ] Mobile apps

### Phase 4: Scale 🚀
- [ ] PostgreSQL database
- [ ] API for mobile
- [ ] Admin dashboard
- [ ] Cloud hosting

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

See [docs/COMPLETE_GUIDE.md#troubleshooting](docs/COMPLETE_GUIDE.md#troubleshooting) for more

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

- **Lines of Code**: ~5,000+
- **Test Questions**: 38+ (Test 1)
- **Documentation**: 14 comprehensive guides
- **Supported Platforms**: Web (iOS/Android coming)

---

## 🔖 Version

**Current Version**: 2.0  
**Last Updated**: December 8, 2025  
**Status**: Production Ready 🚀

---

**Made with ❤️ for CELPIP test takers**

[⭐ Star this repo](https://github.com/YOUR_USERNAME/celpip) | [📖 Read the docs](docs/) | [🐛 Report issues](https://github.com/YOUR_USERNAME/celpip/issues)
