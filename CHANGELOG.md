# Changelog

All notable changes to this project will be documented in this file.

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
- **Setup**: See `docs/SETUP.md` for local installation
- **Contributing**: See `docs/ADDING_TESTS.md` for adding test content

### Key Design Decisions

1. **JSON-based data storage** - Platform-agnostic, easy to edit
2. **Dynamic timeout calculation** - DRY principle, single source of truth
3. **Template-driven UI** - Consistent user experience
4. **OCR-based content extraction** - Efficient test creation workflow

---

For detailed setup instructions, see `docs/SETUP.md`  
For architecture details, see `docs/ARCHITECTURE.md`  
For current progress, see `TEST_STATUS.md`

