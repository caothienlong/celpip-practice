# Active Context: CELPIP Practice Platform

## Current State (as of April 2026)

The platform is **production-ready** at version 5.0, deployed on Render.com.

### What's Working
- Reading section: 10 complete tests (40 parts, ~380 questions)
- Listening section: Test 1 complete with audio/video (6 parts, 33 questions)
- Listening section: Tests 2-10 JSON content complete, awaiting audio/video assets
- Practice Mode and Test Mode for both Reading and Listening
- OAuth authentication (Google enabled, Facebook code present but commented out)
- Guest mode with session-only storage
- PostgreSQL storage with file-based fallback
- Vocabulary notes feature (authenticated users only)
- Comprehensive answer keys for both skills
- Production deployment on Render.com with Blueprint

### Recent Changes (April 2026)
- **Listening Answer Keys: Audio playback** — Per-part and comprehensive answer keys now include audio players for passage audio. Users can play, pause, replay, and seek through each passage while reading the transcript and reviewing correct answers.

### Previous Changes (March 2026)
- Image-based questions support for Listening (e.g., Part 1 Q4)
- "Skip to Questions" button added to all Listening parts (both modes)
- Fixed Cloudinary audio URLs (corrected filename pattern)
- Fixed question image display bug (non-destructive show/hide)
- Fixed MIME type for `.m4a` files
- Listening Tests 2-10 JSON data created from PDF parsing

## Active Development Areas

### In Progress
1. **Listening content for Tests 2-10**: JSON data is complete but audio/video assets need to be uploaded to Cloudinary
2. **Content expansion**: Tests 11-20 not yet started

### Known Issues
- Facebook OAuth registration is **commented out** in `utils/oauth_providers.py` — README mentions it as enabled
- `static/` directory has no tracked files — images are referenced but may not exist
- `package.json` is missing (only `package-lock.json` for Capacitor exists)
- Some reconstructed Listening questions need manual verification (see `docs/ADDING_LISTENING_TESTS.md` for list)

### Questions Needing Manual Verification
| Test | Part | Q# | Issue |
|------|------|----|-------|
| 3 | 5 | Q3 | Question missing from source PDF |
| 4 | 1 | Q1 | Question bullets missing from source PDF |
| 6 | 1 | Q6 | Question and answer missing from source PDF |
| 8 | 1 | Q6 | Question and answer missing from source PDF |
| 9 | 1 | Q2 | Question missing from source PDF |
| 10 | 1 | Q2 | Question missing from source PDF |

## Current Technical Debt
- `app.py` is a large single file containing all routes — could benefit from Blueprint refactoring
- No automated tests (pytest, unittest)
- No CI/CD pipeline
- No linting/formatting configuration (no flake8, black, isort)
- Render free-tier database expires after 90 days — needs upgrade for persistence
