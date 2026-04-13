# Product Context: CELPIP Practice Platform

## Problem Being Solved

CELPIP test takers need affordable, accessible practice that simulates the real exam experience. Commercial practice materials are expensive, and there is no open-source alternative with realistic test simulation.

## User Experience Goals

### Practice Mode
- Navigate freely between questions (back/forward)
- View answer keys anytime during practice
- Reset and retry individual parts
- Auto-save progress so users can resume later
- Detailed explanations with comprehensive answer keys
- Listening answer keys with passage audio playback (play, pause, replay, seek)

### Test Mode
- Realistic exam conditions with countdown timers
- Sequential navigation only (like the real CELPIP exam)
- Auto-submit when time expires
- Comprehensive scoring with pass/fail analytics
- Test history tracking across sessions

### Listening Module
- **Parts 1-3**: Sequential state machine — one question at a time with 30-second per-question timer, split-pane layout (left: image + audio, right: answer options)
- **Parts 4-6**: Full-width layout with inline dropdown select boxes
- **Practice Mode**: Replay audio freely, "Skip to Questions" button
- **Test Mode**: Play-once audio, forward-only navigation, auto-play passage
- Audio hosted on Cloudinary (.m4a), video for Part 5 (.mp4)

### Authentication Flow
- **Guest Mode**: No login required, session-based storage, data lost on browser close
- **OAuth Mode**: Google/Facebook login, persistent history, vocabulary notes, cross-session access
- Login page with provider buttons + "Continue as Guest" option

## Content Structure

### CELPIP Test Format
| Section | Parts | Questions/Part | Total Questions |
|---------|-------|----------------|-----------------|
| Reading | 4 | 8-11 | 38 per test |
| Listening | 6 | 5-8 | 33 per test |
| Writing | 2 | - | Planned |
| Speaking | 8 | - | Planned |

### Reading Parts
1. **Correspondence** (11 Q): Letter/email with dropdown responses
2. **Apply a Diagram** (8 Q): Email + diagram with dropdowns
3. **Reading for Information** (9 Q): 4 paragraphs + "Not Given" option (5 choices)
4. **Reading for Viewpoints** (10 Q): Article + comment with dropdowns

### Listening Parts
1. **Problem Solving** (8 Q): 3 sub-parts, per-question audio, radio buttons
2. **Daily Life Conversation** (5 Q): Per-question audio, radio buttons
3. **Listening for Information** (6 Q): Per-question audio, radio buttons
4. **Listening to a News Item** (5 Q): Passage audio, inline dropdowns
5. **Listening to a Discussion** (8 Q): Video, inline dropdowns
6. **Listening for Viewpoints** (6 Q): Passage audio, inline dropdowns

## Key Design Decisions

1. **Data-driven content**: All test content in JSON — no code changes for new tests
2. **Dynamic timeouts**: Calculated from `config.json` (questions x time_per_question)
3. **Repository pattern**: Storage backend is transparent to the application
4. **Cloudinary for media**: Audio/video hosted externally, referenced by URL
5. **Two-column layout**: CELPIP-style interface with passage + questions side-by-side
