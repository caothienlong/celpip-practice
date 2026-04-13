# Changelog

All notable changes to this project will be documented in this file.

## [2026-04-13] - Listening Answer Keys: Passage Audio Playback

### Added
- **Audio players in per-part answer key** — Listening answer key pages now show custom audio players for each passage section. Parts 1-3 (per_question_audio) show separate players for each sub-part section; Parts 4-6 (full_questions) show a single player for the passage.
- **Audio players in comprehensive answer key** — The skill-wide answer key also includes audio players per part, displayed between the answer table and the transcript toggle.
- **Play/Pause/Replay/Seek** — Each audio player supports play, pause, replay from start, click-to-seek on the progress bar, and shows current time / total duration.

### Changed
- **`app.py`** — `prepare_answer_key_data()` now extracts `audio_passages` (from `sub_parts[].passageAudioUrl` or `mediaUrl`) and passes them to the per-part answer key template.
- **`app.py`** — `comprehensive_answer_key()` now attaches `audio_passages` per part entry for listening skills.
- **`answer_key.html`** — Added CSS and JavaScript for custom audio player UI in the listening section.
- **`comprehensive_answer_key.html`** — Added CSS and JavaScript for custom audio player UI below each part's answer table.

---

## [2026-03-16] - Listening: Image-Based Questions, Audio URL Fix, Skip Button for All Parts

### Added
- **"Skip to Questions" button for Parts 4-6** — All parts now have a "Skip to Questions" button on the passage state in both Practice and Test Mode, consistent with Parts 1-3.

### Fixed
- **Passage audio URLs (Parts 2-6)** — Corrected Cloudinary filenames from `partN.m4a` to `partN_passage.m4a`. All passage audio was returning 404; now returns 200.
- **Question image display broken after first load** — The `onerror` handler on `<img id="questionImage">` was destroying the element with `outerHTML`, making it unreachable for subsequent questions. Replaced with non-destructive show/hide approach using a sibling placeholder.
- **MIME type mismatch** — Removed incorrect `type="audio/mpeg"` from `<source>` tags (files are `.m4a` = `audio/mp4`). Browser now auto-detects format.
- **Part 1 Q4 missing data in sections block** — `sections` block had `"options": [], "answer": null` for Q4. Updated to match `sub_parts` data with options, imageUrl, and correct answer.

### Changed
- **Question-specific images (Parts 1-2)** — Questions with an `imageUrl` field (e.g., Part 1 Q4) now swap the left-panel image to show the question-specific reference image instead of the passage image. Reverts to passage image for questions without `imageUrl`.
- **Answer key shows question images** — Listening answer key now displays the reference image for questions that have `imageUrl`.
- **`app.py`** — `prepare_test_data()` passes `image_url` through in question steps; `prepare_answer_key_data()` includes `image_url` for listening questions.

---

## [2026-03-16] - Listening: Practice Mode Replay & Skip Button

### Changed
- **Practice Mode: Replay allowed** — Passage and question audio can be replayed freely in Practice Mode. Button changes to "Replay" after first play.
- **Practice Mode: "Skip to Questions" button** — Added skip button on passage state so users can jump directly to questions without listening to the full passage.
- **Test Mode unchanged** — Remains play-once only, no skip button, auto-play passage.

---

## [2026-03-16] - Listening: Sequential Flow

### Changed
- **Parts 1-3: One question at a time** — Replaced multi-question display with a sequential state machine. Each question shown individually in a split-pane layout (left: image + audio player, right: single question). Per-question countdown timer (30 seconds).
- **Part 1: Sequential flow** — Replaced tab navigation with linear flow: Passage 1.1 → Q1 → Q2 → Passage 1.2 → Q3 → Q4 → Passage 1.3 → Q5 → Next Part. Continuous question numbering across sub-parts.
- **`app.py`** — `prepare_test_data()` now builds a flat `steps` array for the JS state machine to consume.

---

## [2026-03-16] - Listening Module UI Revision

### Changed
- **Parts 4-6: Dropdown select boxes** — Replaced radio buttons with inline dropdown selects (matching Reading Part 3/4 pattern). After selection, dropdown is replaced by a styled "completed sentence" text span. Clicking the text re-opens the dropdown.
- **Parts 1-3: Per-question audio** — Each question now has its own individual audio file (`audioUrl`). The audio IS the question, so no question text is displayed during the test. Each question shows a play button with progress bar.
- **Part 1: Sub-parts** — Part 1 is now split into 3 sub-parts (1.1, 1.2, 1.3), each with its own passage audio and questions.
- **JSON data** — `part1.json` through `part3.json` updated with `layout: "per_question_audio"`, individual `audioUrl` per question, and `sub_parts` for Part 1.
- **`app.py`** — Extended `prepare_test_data()` to generate dropdown HTML for Parts 4-6 and process per-question audio/sub-parts for Parts 1-3.

---

## [2026-03-16] - Listening Module Implementation

### Added
- **Listening Module** — Full implementation of the CELPIP Listening test with 6 parts
  - State machine architecture: Passage Playback → Question Set transition
  - Audio player with animated progress bar and sound visualizer
  - Video support for Part 5 (Discussion)
  - Practice Mode: replay allowed, Back + Next navigation
  - Test Mode: auto-play, no replay, forward-only navigation, progress bar

- **New Templates**
  - `listening_section.html` — Practice Mode with state machine, blue theme (`#003366`)
  - `listening_test_mode_section.html` — Test Mode with red theme (`#c8102e`)

- **Test 1 Listening Data** (6 parts, 33 questions total)
  - Part 1: Listening to Problem Solving (5 questions, audio, split pane)
  - Part 2: Daily Life Conversation (5 questions, audio, split pane)
  - Part 3: Listening for Information (5 questions, audio, split pane)
  - Part 4: Listening to a News Item (6 questions, audio, full-width)
  - Part 5: Listening to a Discussion (6 questions, video, full-width)
  - Part 6: Listening for Viewpoints (6 questions, audio, full-width)

- **Listening-specific features**
  - Auto-transition from audio/video playback to questions on media end
  - Graceful fallback when media files are missing (skip to questions)
  - Page refresh prevention during active test
  - Answer auto-save for both Practice and Test Mode
  - Vocabulary notes sidebar support
  - Comprehensive answer key for all 6 listening parts

### Changed
- `app.py` — Added `listening` type handling in `prepare_test_data()` and `prepare_answer_key_data()`
- `app.py` — Routes now select listening-specific templates when `skill == 'listening'`
- `test_detail.html` — Listening card shows dynamic parts instead of "Coming Soon"
- `test_detail.html` — Added Listening Answer Key button
- `test_detail.html` — Reset now clears all skills (not just reading)
- `answer_key.html` — Added `is_listening_type` branch for per-part answer key display

### Static Asset Directories
- `static/audio/test_1/listening/` — for MP3 files
- `static/video/test_1/listening/` — for MP4 files (Part 5)
- `static/images/test_1/listening/` — for scene illustration images

---

## [2024-12-04] - Test 1 & 2 Complete + Dynamic Timeout

### Added
- ✅ Complete Test 1 Reading (all 4 parts, 38 questions)
  - Part 1: Greg's camping letter
  - Part 2: Kids activities diagram
  - Part 3: Chewing gum information
  - Part 4: Climate change teaching viewpoints
  
- ✅ Complete Test 2 Reading (all 4 parts, 38 questions)
  - Part 1: Janice's apple picking letter
  - Part 2: Nursing jobs diagram
  - Part 3: Gatineau Park information
  - Part 4: Kayaking ecotourism viewpoints

- OCR conversion scripts for PDF text extraction
  - `pdftotext/convert_all_pages.sh` - Process all PDF pages
  - `pdftotext/convert_pages_range.sh` - Process specific page ranges
  - OCR documentation and extracted test content

### Changed
- **Refactored timeout calculation** - Removed hardcoded `timeout_minutes` field from all JSON files
  - Timeout now calculated dynamically: `num_questions × time_per_question`
  - Single source of truth in `config.json`
  - Benefits: easier maintenance, consistency, flexibility

### Refactoring History

#### Dynamic Timeout Calculation
- **Issue**: `timeout_minutes` was hardcoded in every JSON file
- **Solution**: Calculate automatically based on question count and `config.json` settings
- **Formula**: `timeout = num_questions × time_per_question`
- **Example**: 11 questions × 1.5 min = 16.5 minutes

#### Data/Code Separation
- **Date**: Earlier in development
- **Goal**: Platform-agnostic design for Web, iOS, and Android
- **Changes**:
  - Moved all test content to `data/` folder in JSON format
  - Created `utils/data_loader.py` for loading and processing test data
  - Separated configuration into `config.json`
  - Created reusable template system

### Project Structure
```
celpip/
├── app.py                 # Flask application
├── config.py             # Configuration loader
├── config.json           # Settings (time, UI, etc.)
├── data/                 # Test content (JSON)
│   ├── test_1/reading/   # ✅ Complete
│   ├── test_2/reading/   # ✅ Complete
│   └── test_3-5/         # 📝 Templates
├── utils/
│   └── data_loader.py    # Data loading utilities
├── templates/            # Jinja2 templates
├── static/              # CSS, JS, images
├── pdftotext/           # OCR scripts and extracted content
└── docs/                # Documentation

```

### Progress
- **Overall**: 8/20 parts complete (40%)
- **Test 1**: 100% ✅
- **Test 2**: 100% ✅
- **Tests 3-5**: Templates ready 📝

### Next Steps
- Extract and fill Test 3, 4, 5 content from PDF
- Add diagram images for Test 2-5
- Consider adding Writing, Speaking, Listening skills

---

## Development Notes

### Git Repository
- **Repository**: github.com:caothienlong/celpip-practice.git
- **Branch**: main
- **Contributing**: See `docs/ADDING_TESTS.md` for adding test content

### Key Design Decisions

1. **JSON-based data storage** - Platform-agnostic, easy to edit
2. **Dynamic timeout calculation** - DRY principle, single source of truth
3. **Template-driven UI** - Consistent user experience
4. **OCR-based content extraction** - Efficient test creation workflow

---

For architecture details, see `docs/ARCHITECTURE.md`  
For current progress, see `TEST_STATUS.md`

