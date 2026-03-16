# CELPIP Application Architecture

## Overview

This application is designed with a **data-driven, platform-agnostic architecture** to support:
- 20 test sets
- 4 skills (Reading, Writing, Speaking, Listening)
- Multiple platforms (Web, iOS, Android)

## Design Principles

### 1. Separation of Concerns
- **Test Data Layer**: JSON files in `data/` directory
- **Storage Layer**: Repository pattern in `utils/storage/` (pluggable backends)
- **Business Logic**: Python utilities in `utils/`
- **Presentation**: Flask routes and Jinja2 templates
- **Static Assets**: Images organized by set and skill

### 2. Repository Pattern (Storage)
User data access is decoupled from storage technology via abstract repository interfaces:
- `UserRepository` — profiles and roles
- `TestRepository` — test attempts and results
- `VocabularyRepository` — vocabulary notes

Concrete implementations (`FileUserRepository`, `DbUserRepository`, etc.) are selected at startup by a factory, keeping the rest of the application storage-agnostic.

### 3. Platform Agnostic
- All test data in JSON format
- Can be consumed by any platform
- No platform-specific data structures

### 4. Scalability
- Easy to add new test sets (just add JSON files)
- Automatic discovery of available tests
- No code changes needed for new content
- Adding a new storage backend only requires implementing three interfaces

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
│   ├── test_section.html              # Reading Practice Mode
│   ├── test_mode_section.html         # Reading Test Mode
│   ├── listening_section.html         # Listening Practice Mode (state machine)
│   └── listening_test_mode_section.html # Listening Test Mode (state machine)
│
└── utils/                          # Business logic (reusable)
    ├── __init__.py
    ├── auth.py                     # Flask-Login integration
    ├── data_loader.py              # Test data loading & processing
    ├── database.py                 # PostgreSQL connection pool & raw SQL
    ├── oauth_providers.py          # OAuth provider configuration
    ├── results_tracker.py          # Thin facade — public API for app.py
    └── storage/                    # Storage layer (repository pattern)
        ├── __init__.py             # Public exports + make_repositories()
        ├── interfaces.py           # Abstract base classes
        ├── file_storage.py         # File-based implementations (local dev)
        ├── db_storage.py           # PostgreSQL implementations
        └── factory.py              # Selects backend from DATABASE_URL
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

**Purpose**: Platform-agnostic test data loading and processing

**Key Methods**:
- `load_test_part(set, skill, part)` — Load test data from JSON
- `get_all_questions(data)` — Extract all questions
- `get_correct_answers(data)` — Get answer key
- `process_dropdown_content(content, questions)` — Replace placeholders with HTML (Web)
- `build_question_dropdown_html(questions)` — Generate question HTML (Web)

### 2. Storage Layer (`utils/storage/`)

**Purpose**: Pluggable persistence for user data

**Architecture**:
```
make_repositories(users_dir, database_url)
        │
        ├─ DATABASE_URL set & reachable ──► DbUserRepository
        │                                   DbTestRepository
        │                                   DbVocabularyRepository
        │                                         │
        │                                   utils/database.py (psycopg2 pool)
        │
        └─ no DATABASE_URL (local dev) ──► FileUserRepository
                                            FileTestRepository
                                            FileVocabularyRepository
                                                  │
                                            users/{email}/*.json
```

**Interfaces** (`utils/storage/interfaces.py`):

| Interface | Responsibility |
|-----------|----------------|
| `UserRepository` | `get`, `save`, `get_or_create`, `update_role`, `list_all` |
| `TestRepository` | `save_result`, `complete_attempt`, `get_history`, `get_all_summary` |
| `VocabularyRepository` | `save`, `get`, `delete`, `update` |

### 3. Results Tracker (`utils/results_tracker.py`)

**Purpose**: Thin application-level facade over the storage layer

Exposes a single stable public API to the rest of the app.  
Contains **no storage logic** — delegates entirely to the three repositories.

```python
tracker = ResultsTracker(users_dir='users', database_url=os.getenv('DATABASE_URL'))

# All three domains through one object:
tracker.get_user_profile(email)
tracker.save_test_result(...)
tracker.save_vocabulary_note(...)
```

### 4. Database (`utils/database.py`)

**Purpose**: Raw PostgreSQL access — connection pooling, table creation, SQL queries

Used exclusively by `DbUserRepository`, `DbTestRepository`, and `DbVocabularyRepository`.  
Not imported directly anywhere else in the application.

**Tables**: `users`, `test_history`, `vocabulary_notes`

### 5. Flask Application (`app.py`)

**Purpose**: Web platform implementation

**Key Routes**:
- `GET /` — Home page, list all available tests
- `GET /test/<set>/<skill>/part<part>` — Display test (auto-selects template by skill)
- `GET /test/<set>/exam/<skill>/part<part>` — Test Mode (auto-selects template by skill)
- `POST /submit_answers` — Process and score answers (Practice)
- `POST /submit_test_mode` — Process and score answers (Test Mode)

**Template Selection**: Routes automatically select the appropriate template based on skill:
- `skill == 'listening'` → `listening_section.html` / `listening_test_mode_section.html`
- All other skills → `test_section.html` / `test_mode_section.html`

**Platform-Specific**: Only for Web app

### 3. JSON Data Format

**Purpose**: Platform-agnostic test content

**Reading Structure**:
```json
{
  "part": 1,
  "title": "Part Title",
  "type": "correspondence|diagram|information|viewpoints",
  "instructions": "Instructions...",
  "sections": [
    {
      "section_type": "passage|questions|diagram_email|response_passage",
      "content": "Content with __DROPDOWN_X__ placeholders",
      "questions": [
        { "id": 1, "text": "Question text", "options": ["A", "B", "C", "D"], "answer": 0 }
      ]
    }
  ]
}
```

**Listening Structure (Parts 1-3, per-question audio)**:
```json
{
  "part": 1,
  "title": "Part Title",
  "type": "listening",
  "mediaType": "audio",
  "mediaUrl": "/static/audio/test_X/listening/partN.mp3",
  "imageUrl": "/static/images/test_X/listening/partN_scene.png",
  "layout": "per_question_audio",
  "sub_parts": [
    {
      "id": "1.1", "title": "Sub-part Title",
      "passageAudioUrl": "/static/audio/test_X/listening/part1_1_passage.mp3",
      "imageUrl": "/static/images/test_X/listening/part1_scene.png",
      "questions": [
        { "id": 1, "audioUrl": "/static/audio/test_X/listening/part1_q1.mp3", "text": "...", "options": ["A","B","C","D"], "answer": 0 }
      ]
    }
  ],
  "sections": [{ "section_type": "questions", "questions": [...] }]
}
```

**Listening Structure (Parts 4-6, dropdown selects)**:
```json
{
  "part": 4,
  "title": "Part Title",
  "type": "listening",
  "mediaType": "audio|video",
  "mediaUrl": "/static/audio/test_X/listening/partN.mp3",
  "imageUrl": "/static/images/test_X/listening/partN_scene.png",
  "layout": "full_questions",
  "sections": [
    {
      "section_type": "questions",
      "questions": [
        { "id": 1, "text": "Question text", "options": ["A", "B", "C", "D"], "answer": 0 }
      ]
    }
  ]
}
```

**Platform Notes**:
- Same format for all platforms
- Reading: `__DROPDOWN_X__` placeholders replaced by platform-specific UI
- Listening Parts 1-3: `audioUrl` per question, optional `sub_parts` array
- Listening Parts 4-6: Questions rendered as inline dropdowns
- Listening: `mediaUrl` can point to local files or cloud URLs (e.g., Cloudinary)
- Listening: Questions can have optional `imageUrl` for image-based answer options (displayed in left panel during question state)

## Test Types

### Reading Skill (4 parts)

| Part | Type | Questions | Time | Layout |
|------|------|-----------|------|--------|
| 1 | Correspondence | 11 | 16.5 min | Side-by-side |
| 2 | Diagram | 8 | 12 min | Side-by-side |
| 3 | Information | 9 | 13.5 min | Side-by-side |
| 4 | Viewpoints | 10 | 15 min | Side-by-side |

### Listening Skill (6 parts) ✅ Implemented

| Part | Type | Questions | Media | Layout | Question UI |
|------|------|-----------|-------|--------|-------------|
| 1 | Problem Solving | 5 (3 sub-parts) | Audio | Sequential: 1 question at a time, 30s timer | Radio buttons |
| 2 | Daily Life Conversation | 5 | Audio | Sequential: 1 question at a time, 30s timer | Radio buttons |
| 3 | Listening for Information | 5 | Audio | Sequential: 1 question at a time, 30s timer | Radio buttons |
| 4 | News Item | 6 | Audio | Full-width, all questions at once | Inline dropdowns |
| 5 | Discussion | 6 | Video | Full-width, all questions at once | Inline dropdowns |
| 6 | Viewpoints | 6 | Audio | Full-width, all questions at once | Inline dropdowns |

**Listening Architecture — State Machine:**

Parts 1-3: Sequential flow driven by a JS `steps` array. Audio plays once only.
```
┌─────────────┐     ended     ┌─────────────┐     ended     ┌─────────────┐
│ PASSAGE 1.1 │ ───────────► │  QUESTION 1  │ ──── next ──► │  QUESTION 2  │
│  (auto-play │               │  - Split pane│               │  (30s timer) │
│   once)     │               │  - Audio L   │               │              │
└─────────────┘               │  - Options R │               └──────┬───────┘
                              │  - 30s timer │                      │
                              └──────────────┘                      ▼
                                                          ┌─────────────┐
                                                          │ PASSAGE 1.2 │ → Q3 → Q4 → ...
                                                          └─────────────┘
```

Parts 4-6: Passage → All Questions (dropdowns).
```
┌──────────────────┐     audio.onEnded     ┌────────────────────────────┐
│  PASSAGE STATE   │ ───────────────────►  │  QUESTIONS (dropdowns)     │
│  - Play button   │                       │  - Full-width              │
│  - Progress bar  │     skip button       │  - Inline selects          │
│  - Visualizer    │ ───────────────────►  │  - Selected → text span    │
│  - Skip button   │                       │                            │
└──────────────────┘                       └────────────────────────────┘
```

**Question-level images**: Questions can have an optional `imageUrl` field. When present, the left panel displays the question-specific image instead of the passage image (e.g., Part 1 Q4 where answer options reference numbered areas in an image).

### Writing Skill (2 parts) — Planned
- Part 1: Email writing
- Part 2: Survey response

### Speaking Skill (8 parts) — Planned
- Various speaking tasks with recording

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

- [x] Database backend for user progress (PostgreSQL via repository pattern)
- [ ] API for mobile apps
- [ ] Real-time synchronization
- [ ] Offline mode support
- [ ] Analytics and reporting
- [ ] Admin panel for content management
- [ ] Additional storage backends (e.g. Redis cache, S3 backup) via new repository implementations

