# CELPIP Application Architecture

## Overview

This application is designed with a **data-driven, platform-agnostic architecture** to support:
- 20 test sets
- 4 skills (Reading, Writing, Speaking, Listening)
- Multiple platforms (Web, iOS, Android)

## Design Principles

### 1. Separation of Concerns
- **Data Layer**: JSON files in `data/` directory
- **Business Logic**: Python utilities in `utils/`
- **Presentation**: Flask routes and Jinja2 templates
- **Static Assets**: Images organized by set and skill

### 2. Platform Agnostic
- All test data in JSON format
- Can be consumed by any platform
- No platform-specific data structures

### 3. Scalability
- Easy to add new test sets (just add JSON files)
- Automatic discovery of available tests
- No code changes needed for new content

## Directory Structure

```
celpip/
│
├── app.py                      # Flask application (Web platform)
├── requirements.txt            # Python dependencies
│
├── data/                       # Test data (platform-agnostic)
│   ├── README.md              # Data format documentation
│   └── set_{1..20}/           # Test sets 1-20
│       ├── reading/           # Reading skill
│       │   ├── part1.json
│       │   ├── part2.json
│       │   ├── part3.json
│       │   └── part4.json
│       ├── writing/           # Writing skill
│       │   ├── part1.json
│       │   └── part2.json
│       ├── speaking/          # Speaking skill
│       │   ├── part1.json
│       │   ├── ...
│       │   └── part8.json
│       └── listening/         # Listening skill
│           ├── part1.json
│           ├── ...
│           └── part6.json
│
├── static/                    # Static assets
│   └── images/
│       └── set_{1..20}/      # Organized by test set
│           ├── reading/
│           │   └── *.png
│           ├── writing/
│           ├── speaking/
│           └── listening/
│               └── *.mp3     # Audio files for listening
│
├── templates/                 # HTML templates (Web platform)
│   ├── index.html
│   └── test_section.html
│
└── utils/                     # Business logic (reusable)
    ├── __init__.py
    └── data_loader.py        # Data loading & processing
```

## Data Flow

### Web Application Flow

```
User Request
    ↓
Flask Route (/test/<set>/<skill>/part<num>)
    ↓
TestDataLoader.load_test_part()
    ↓
Read JSON file
    ↓
Process data (dropdowns, formatting)
    ↓
Render Jinja2 Template
    ↓
HTML Response
```

### Answer Submission Flow

```
User Submits Answers
    ↓
POST /submit_answers
    ↓
TestDataLoader.load_test_part()
    ↓
TestDataLoader.get_correct_answers()
    ↓
Compare user answers with correct answers
    ↓
Calculate score
    ↓
JSON Response with results
```

## Key Components

### 1. Data Loader (`utils/data_loader.py`)

**Purpose**: Platform-agnostic data loading and processing

**Key Methods**:
- `load_test_part(set, skill, part)` - Load test data from JSON
- `get_all_questions(data)` - Extract all questions
- `get_correct_answers(data)` - Get answer key
- `process_dropdown_content(content, questions)` - Replace placeholders with HTML (Web)
- `build_question_dropdown_html(questions)` - Generate question HTML (Web)

**Platform Notes**:
- Core methods (load, get_questions, get_answers) are platform-agnostic
- HTML generation methods are Web-specific
- iOS/Android would implement their own UI generation

### 2. Flask Application (`app.py`)

**Purpose**: Web platform implementation

**Key Routes**:
- `GET /` - Home page, list all available tests
- `GET /test/<set>/<skill>/part<part>` - Display test
- `POST /submit_answers` - Process and score answers

**Platform-Specific**: Only for Web app

### 3. JSON Data Format

**Purpose**: Platform-agnostic test content

**Structure**:
```json
{
  "part": 1,
  "title": "Part Title",
  "type": "test_type",
  "instructions": "Instructions...",
  "timeout_minutes": 16.5,
  "sections": [
    {
      "section_type": "passage|questions|diagram_email|response_passage",
      "content": "Content with __DROPDOWN_X__ placeholders",
      "questions": [
        {
          "id": 1,
          "text": "Question text",
          "options": ["A", "B", "C", "D"],
          "answer": 0
        }
      ]
    }
  ]
}
```

**Platform Notes**:
- Same format for all platforms
- `__DROPDOWN_X__` placeholders replaced by platform-specific UI

## Test Types

### Reading Skill (4 parts)

| Part | Type | Questions | Time | Layout |
|------|------|-----------|------|--------|
| 1 | Correspondence | 11 | 16.5 min | Side-by-side |
| 2 | Diagram | 8 | 12 min | Side-by-side |
| 3 | Information | 9 | 13.5 min | TBD |
| 4 | Viewpoints | 10 | 15 min | TBD |

### Writing Skill (2 parts)
- Part 1: Email writing
- Part 2: Survey response

### Speaking Skill (8 parts)
- Various speaking tasks with recording

### Listening Skill (6 parts)
- Audio comprehension with multiple choice

## Future Platform Implementations

### iOS App
```swift
// Swift code would use the same JSON
struct TestDataLoader {
    func loadTestPart(set: Int, skill: String, part: Int) -> TestData {
        // Read from bundle or download
        // Parse JSON
        // Return Swift struct
    }
}

// Native iOS UI
struct QuestionView: View {
    let question: Question
    @State var selectedAnswer: Int?
    
    var body: some View {
        VStack {
            Text(question.text)
            Picker("Answer", selection: $selectedAnswer) {
                ForEach(question.options.indices) { i in
                    Text(question.options[i])
                }
            }
        }
    }
}
```

### Android App
```kotlin
// Kotlin code would use the same JSON
class TestDataLoader {
    fun loadTestPart(set: Int, skill: String, part: Int): TestData {
        // Read from assets or download
        // Parse JSON with Gson/Moshi
        // Return Kotlin data class
    }
}

// Native Android UI
@Composable
fun QuestionView(question: Question) {
    var selectedAnswer by remember { mutableStateOf<Int?>(null) }
    
    Column {
        Text(question.text)
        DropdownMenu(
            options = question.options,
            onSelect = { selectedAnswer = it }
        )
    }
}
```

## Benefits of This Architecture

### ✅ Maintainability
- Single source of truth for test data
- Easy to update content without code changes
- Clear separation of concerns

### ✅ Scalability
- Add new test sets by adding JSON files
- No code changes required
- Automatic discovery

### ✅ Reusability
- Same data for Web, iOS, Android
- Business logic can be ported across platforms
- Consistent user experience

### ✅ Testability
- Data can be validated independently
- Easy to create mock data for testing
- Platform-agnostic logic can be unit tested

## Adding New Content

### 1. New Test Set
```bash
mkdir -p data/set_X/{reading,writing,speaking,listening}
mkdir -p static/images/set_X/{reading,writing,speaking,listening}
```

### 2. New Test Part
```bash
# Create JSON file
cp data/set_1/reading/part1.json data/set_X/skill/partY.json
# Edit content
# Application automatically detects it
```

### 3. New Platform
```
1. Implement data loader in platform language
2. Parse JSON files
3. Build native UI components
4. Reuse same test data
```

## Performance Considerations

- JSON files are small (< 50KB each)
- Loaded on-demand (not all at once)
- Can be cached in production
- Images lazy-loaded
- Timer runs client-side (no server polling)

## Security Considerations

- Answers are validated server-side
- No answer keys sent to client
- Session management for user data (future)
- Input sanitization for user responses

## Future Enhancements

- [ ] Database backend for user progress
- [ ] API for mobile apps
- [ ] Real-time synchronization
- [ ] Offline mode support
- [ ] Analytics and reporting
- [ ] Admin panel for content management

