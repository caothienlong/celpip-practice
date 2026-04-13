# System Patterns: CELPIP Practice Platform

## Architecture Overview

Monolithic Flask application with data-driven test content and pluggable storage backends.

```
User Request
    ↓
Flask Routes (app.py)
    ↓
Data Loader (utils/data_loader.py) ─── reads ──→ data/test_N/skill/partM.json
    ↓
Jinja2 Templates (templates/)
    ↓
HTML Response
```

## Key Architecture Patterns

### 1. Repository Pattern (Storage Layer)

User data access is decoupled from storage via abstract interfaces in `utils/storage/`.

```
make_repositories(users_dir, database_url)
    ├── DATABASE_URL set & reachable → Db*Repository (PostgreSQL)
    │                                    └── utils/database.py (psycopg2 pool)
    └── no DATABASE_URL             → File*Repository (JSON files)
                                         └── users/{email}/*.json
```

**Interfaces** (`utils/storage/interfaces.py`):
- `UserRepository` — profiles, roles
- `TestRepository` — test attempts, results, history
- `VocabularyRepository` — vocabulary notes CRUD

**Factory** (`utils/storage/factory.py`): Auto-selects DB vs file backend at startup.

**Facade** (`utils/results_tracker.py`): Single entry point (`ResultsTracker`) for all user data operations — delegates to the three repositories.

### 2. Data-Driven Test Content

- All test content in `data/test_N/{skill}/partM.json`
- Auto-discovery: app scans `data/` directory for available tests
- No code changes needed to add new tests — just add JSON files
- `__DROPDOWN_X__` placeholders in content replaced by HTML at render time

### 3. Listening State Machine

Listening parts use a client-side JavaScript state machine:

**Parts 1-3 (per_question_audio)**:
```
Passage Audio → Q1 (30s timer) → Q2 → ... → Next Passage → Q(n+1) → ...
```
- `steps` array built in `app.py:prepare_test_data()` for JS consumption
- Split-pane layout: left (image + audio player), right (single question)

**Parts 4-6 (full_questions)**:
```
Passage Audio/Video → All Questions (inline dropdowns)
```
- "Skip to Questions" button on passage state
- Dropdowns replaced by styled text spans after selection

### 4. Template Selection by Skill

Routes auto-select templates based on skill type:
- `skill == 'listening'` → `listening_section.html` / `listening_test_mode_section.html`
- All others → `test_section.html` / `test_mode_section.html`

### 5. Dynamic Timeout Calculation

```
timeout = (num_questions × time_per_question) + time_adjustment
```
- `time_per_question` from `config.json` per skill
- `time_adjustments` from `config.json` per skill_partN
- Calculated in `config.py:calculate_timeout()`

## File Organization

```
app.py              ← All Flask routes, the main application entry point
config.py           ← Load config.json, timeout helpers
config.json         ← Timer, UI, test metadata settings
data/               ← Test content JSON (platform-agnostic)
templates/          ← Jinja2 HTML templates (13 templates)
utils/
  auth.py           ← Flask-Login User model, login decorators
  oauth_providers.py ← Authlib OAuth setup (Google, Facebook)
  data_loader.py    ← Load JSON, process dropdowns, extract questions
  database.py       ← PostgreSQL pool, schema, raw SQL
  results_tracker.py ← Facade over storage repositories
  storage/
    interfaces.py   ← Abstract base classes (3 interfaces)
    factory.py      ← Backend selection
    file_storage.py ← File-based implementations
    db_storage.py   ← PostgreSQL implementations
scripts/            ← Migration, template generation, media tools
docs/               ← Project documentation (8 files)
pdftotext/          ← OCR source text + conversion scripts
```

## Critical Code Paths

### Adding a new test (no code changes needed)
1. Create `data/test_X/reading/part{1-4}.json`
2. Create `data/test_X/listening/part{1-6}.json`
3. App auto-discovers on next request

### Answer submission flow
1. `POST /submit_answers` or `POST /submit_test_mode`
2. Load correct answers from JSON via `data_loader`
3. Compare user answers with correct answers
4. Calculate score, save via `ResultsTracker`
5. Return JSON response

### OAuth login flow
1. User clicks provider button on `/login`
2. Redirect to OAuth provider (Google/Facebook)
3. Callback at `/callback/{provider}`
4. Create/update user via `ResultsTracker`
5. Login with Flask-Login, redirect to home

## Error Handling Patterns

- **Missing media**: Listening templates gracefully skip to questions if audio/video fails
- **No database**: Factory falls back to file storage transparently
- **Missing config**: `config.py` uses sensible defaults
- **Guest mode**: All features work without login (session-only storage)
