# CELPIP Test Practice Application

A comprehensive web-based practice application for CELPIP (Canadian English Language Proficiency Index Program) tests, designed with a scalable architecture for 20 test sets across 4 skills.

## 🏗️ Project Structure

```
celpip/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── data/                  # Test data in JSON format
│   ├── README.md         # Data structure documentation
│   ├── set_1/            # Test Set 1
│   │   ├── reading/
│   │   │   ├── part1.json
│   │   │   ├── part2.json
│   │   │   ├── part3.json (coming soon)
│   │   │   └── part4.json (coming soon)
│   │   ├── writing/      (coming soon)
│   │   ├── speaking/     (coming soon)
│   │   └── listening/    (coming soon)
│   ├── set_2/            (coming soon)
│   └── ... (up to set_20)
├── static/
│   └── images/
│       └── set_1/
│           └── reading/
│               └── part2_diagram.png
├── templates/
│   ├── index.html        # Home page
│   └── test_section.html # Test interface
└── utils/
    ├── __init__.py
    └── data_loader.py    # Data loading utilities
```

## 🚀 Installation & Setup

### 1. Create Virtual Environment

```bash
python3 -m venv venv
```

### 2. Activate Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Running the Application

1. Make sure your virtual environment is activated (you should see `(venv)` in your terminal prompt)

2. Start the Flask server:

```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

## 📚 Available Test Content

### Test Set 1 - Reading

#### Part 1: Reading Correspondence
- **11 questions** divided into 2 sections
- **16.5 minutes** time limit (11 × 1.5)
- Side-by-side layout: Message and Questions
- Questions 1-6: Dropdown menus
- Questions 7-11: Inline dropdowns in response message

#### Part 2: Reading to Apply a Diagram
- **8 questions**
- **12 minutes** time limit (8 × 1.5)
- Side-by-side layout: Diagram and Email
- Questions 1-5: Inline dropdowns in email
- Questions 6-8: Dropdown menus
- Uses image for authentic diagram display

## ✨ Features

### Current Features
- ✅ JSON-based data structure (platform-agnostic)
- ✅ Scalable architecture for 20 test sets × 4 skills
- ✅ Dynamic test loading from JSON files
- ✅ Side-by-side layouts for better readability
- ✅ Inline dropdown menus embedded in text
- ✅ Visual timer with warning alerts
- ✅ Instant scoring and detailed feedback
- ✅ Auto-submit when time expires
- ✅ Modern, responsive UI with gradient design
- ✅ Clean numbered list format for questions

### Upcoming Features
- 🔄 Additional reading parts (3 & 4)
- 🔄 Writing skill tests
- 🔄 Speaking skill tests
- 🔄 Listening skill tests
- 🔄 More test sets (2-20)
- 🔄 Progress tracking
- 🔄 Performance analytics

## 📱 Platform Compatibility

The JSON data structure is designed to be **platform-agnostic**:
- **Web App**: Flask/Python (current implementation)
- **iOS App**: Can use the same JSON data (future)
- **Android App**: Can use the same JSON data (future)

See `data/README.md` for detailed data format documentation.

## 🎯 Adding New Test Data

### Option 1: Manual Creation

1. Create JSON file: `data/set_X/skill/partY.json`
2. Follow the format in `data/README.md`
3. Add any images to: `static/images/set_X/skill/`

### Option 2: Use the Data Loader

```python
from utils.data_loader import TestDataLoader

loader = TestDataLoader()
data = loader.load_test_part(set_number=1, skill='reading', part_number=1)
```

## 🖼️ Adding Diagram Images

For tests with diagrams (like Reading Part 2):

1. Extract the diagram from the PDF
2. Save it to: `static/images/set_X/skill/partY_diagram.png`
3. Reference it in JSON: `"diagram_image": "partY_diagram.png"`

Example for Set 1, Reading Part 2:
```bash
static/images/set_1/reading/part2_diagram.png
```

## 🧪 Test Data Format

Each test part is a self-contained JSON file with:
- Metadata (title, type, timeout)
- Sections (passages, questions, diagrams)
- Questions with options and correct answers

Example structure:
```json
{
  "part": 1,
  "title": "Reading Correspondence",
  "type": "correspondence",
  "instructions": "Read the message and answer questions...",
  "timeout_minutes": 16.5,
  "sections": [...]
}
```

See `data/README.md` for complete documentation.

## 🛠️ Technology Stack

- **Backend**: Flask (Python 3.9+)
- **Frontend**: HTML5, CSS3, JavaScript
- **Data Format**: JSON
- **Styling**: CSS Grid, Flexbox, Custom Animations

## 📝 URL Structure

New RESTful URL format:
```
/test/<set_num>/<skill>/part<part_num>
```

Examples:
- `/test/1/reading/part1` - Set 1, Reading, Part 1
- `/test/1/reading/part2` - Set 1, Reading, Part 2
- `/test/2/listening/part3` - Set 2, Listening, Part 3

Legacy URLs still work:
- `/test1/part1` → redirects to `/test/1/reading/part1`
- `/test1/part2` → redirects to `/test/1/reading/part2`

## 🤝 Contributing

To add new test sets or skills:

1. Create JSON files in `data/set_X/skill/`
2. Follow the format guidelines in `data/README.md`
3. Add any required images to `static/images/set_X/skill/`
4. The application will automatically detect and display them

## 📄 License

Educational use only.

## 🔗 Future Roadmap

- [ ] Complete all 20 test sets
- [ ] Add all 4 skills (Reading, Writing, Speaking, Listening)
- [ ] iOS app using shared JSON data
- [ ] Android app using shared JSON data
- [ ] User authentication and progress tracking
- [ ] Performance analytics and recommendations
- [ ] Audio support for Listening tests
- [ ] Recording capability for Speaking tests
- [ ] AI-powered essay evaluation for Writing tests
