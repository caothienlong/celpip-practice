## Engineering Prompt: CELPIP Listening Module

### **Objective**

Develop a React/Vue-based testing interface that mimics the CELPIP General Listening test. The core requirement is a **State Machine** that manages two distinct views: **Passage Playback**, and **Question Set**.

### **1. Core Layout & Styling**

> **Design parity target:** Mirror `test_section.html` (Practice Mode) and `test_mode_section.html` (Test Mode) exactly. Only swap the text-passage panel for an audio/media panel.

#### **Typography & Base**
* **Font:** `Arial, Helvetica, sans-serif` — matches all Reading test pages.
* **Page background:** `#f0f0f0` (light grey) — same as Reading.
* **Box model:** `* { margin: 0; padding: 0; box-sizing: border-box; }`

#### **Header (`celpip-header`)**
* Fixed top bar, `padding: 15px 30px`, `box-shadow: 0 2px 5px rgba(0,0,0,0.2)`.
* **Practice Mode color:** `background: #003366` (dark navy) — identical to Reading Practice.
* **Test Mode color:** `background: #c8102e` (red) — identical to Reading Test Mode.
* **Left:** `Test N – Listening – Part Title` in white, `font-size: 1.3em`, `font-weight: normal`.
* **Right group** (flex, `gap: 20px`, `align-items: center`):
  * **Practice Mode only** — 📝 Answer Key button: `background: #28a745`, `padding: 8px 16px`, `border-radius: 5px`.
  * **Test Mode only** — `🎯 TEST MODE` badge: `background: rgba(255,255,255,0.2)`, `padding: 8px 16px`, `border-radius: 5px`.
  * Question count badge: `background: rgba(255,255,255,0.1)`, `padding: 8px 15px`, `border-radius: 5px`.
  * Countdown timer box: `background: #00509e` (Practice) / `background: rgba(255,255,255,0.2)` (Test), `padding: 8px 20px`, `border-radius: 5px`, `font-size: 1.1em`, `font-weight: bold`, `min-width: 100px`. Turns `#c8102e` with a CSS pulse animation when ≤ 60 s remaining.

#### **Main Container**
* `max-width: 1400px`, `margin: 0 auto`, `padding: 20px`.

#### **Instructions Bar**
* **Practice Mode:** `background: #e6f2ff`, `border-left: 4px solid #0066cc`, `padding: 15px 20px`, `border-radius: 4px`.
* **Test Mode:** `background: #fff3cd`, `border-left: 4px solid #c8102e`, `padding: 15px 20px`, `border-radius: 4px`.

#### **Progress Bar (Test Mode only)**
* Sits between the header and the instructions bar.
* Outer container: `background: white`, `border-radius: 5px`, `padding: 15px 20px`, `box-shadow: 0 1px 3px rgba(0,0,0,0.1)`.
* Track: `background: #e0e0e0`, `height: 10px`, `border-radius: 10px`.
* Fill: `background: #c8102e`, driven by `(part_num / total_parts) * 100`%.
* Label below track: `"Part N/6 – Listening"`, `color: #666`, `font-size: 0.9em`, centered.

#### **Content Area — Two-Column Split Pane**
* CSS Grid: `grid-template-columns: 1fr 1fr` (50 / 50). Collapses to single column at `max-width: 1024px`.
* Gap between panels: `20px`.

**Panel shared styles (`.content-panel`):**
* `background: white`, `border: 1px solid #ccc`, `border-radius: 5px`, `padding: 20px`.
* `box-shadow: 0 1px 3px rgba(0,0,0,0.1)`.
* `max-height: calc(100vh - 280px)` (Practice) / `calc(100vh - 350px)` (Test, to account for progress bar).
* `overflow-y: auto`, `overflow-x: hidden`.
* Custom scrollbar thumb: `#0066cc` (Practice) / `#c8102e` (Test), `border-radius: 4px`.
* Panel heading (`h3`): `color: #003366` (Practice) / `color: #c8102e` (Test), `font-size: 1.1em`, `border-bottom: 2px solid` matching accent color.

#### **Left Panel — Audio / Media Panel**
Replaces the text passage panel from Reading. Internally uses the same `.content-panel` shell.
* Contains: a static illustrative image or a video player centered within a `.diagram-container`-style wrapper (`border: 2px solid <accent>`, `border-radius: 5px`).
* Below the media: a minimal HTML5 audio progress bar (Practice Mode allows replay; Test Mode shows "Replay Not Available" after first play-through).
* **Practice Mode accent:** `#0066cc`. **Test Mode accent:** `#c8102e`.

#### **Right Panel — Questions Panel**
Identical structure to Reading's question panel.
* `.question` cards: `background: #f9f9f9`, `border: 1px solid #e0e0e0`, `border-radius: 4px`, `padding: 15px`, `margin-bottom: 25px`.
* Question numbers: `color: #003366` (Practice) / `color: #c8102e` (Test), `font-weight: bold`.
* Radio option tiles (`.option`): `background: white`, `border: 2px solid #ddd`, `border-radius: 4px`, `padding: 10px 12px`. On hover → `border-color: #0066cc` / `#c8102e`. On selected → `background: #e6f2ff` (Practice) / `background: #ffe6e6` (Test).
* Inline dropdowns (if used): `border: 2px solid #0066cc` (Practice) / `#c8102e` (Test), `width: 150px`, `border-radius: 3px`.

#### **Navigation Buttons**
* Container: `display: flex`, `justify-content: center`, `gap: 15px`, `margin: 20px 0`.
* **Practice Mode:** `← Back` (grey `#6c757d`) + `Next →` / `Finish` (blue `#0066cc`).
* **Test Mode:** Forward-only. Single `Next Part →` / `Finish Test` button (`background: #c8102e`, hover `#8b0000`), `padding: 12px 40px`, `font-size: 1.1em`.

#### **Mode Differentiation Summary**

| Token | Practice Mode | Test Mode |
|---|---|---|
| Header background | `#003366` | `#c8102e` |
| Accent / borders | `#0066cc` / `#003366` | `#c8102e` / `#8b0000` |
| Instructions bar | Blue-tinted `#e6f2ff` | Yellow-tinted `#fff3cd` |
| Progress bar | ❌ Not shown | ✅ Red fill |
| Answer Key button | ✅ Shown | ❌ Hidden |
| Scrollbar thumb | `#0066cc` | `#c8102e` |
| Selected answer highlight | `#e6f2ff` (blue tint) | `#ffe6e6` (red tint) |
| Audio replay | ✅ Allowed | ❌ Disabled after first play |
| Navigation | Back + Next (free) | Forward-only |
| Floating sidebar back action | ⬅️ Back to Test Overview | ⏸ Pause & Exit |

#### **Floating Right Sidebar (authenticated users only)**
Identical to Reading — `position: fixed; right: 0; top: 50%` pill, `width: 60px`, expands to `240px` on hover, `border-radius: 15px 0 0 15px`.
* 3 items: ⬅️/⏸ Back or Pause, 📚 View Vocabulary, ✏️ Add Note.
* Add Note opens the same slide-in modal from the right (`animation: slideInFromRight 0.3s ease`).

### **2. Component Logic (The "Passage" State)**

* **Full-Screen Media:** When a "Part" starts, render a full-width centered component.
* **Part 1-4, 6:** Display a static illustrative image + custom HTML5 audio player.
* **Part 5:** Display a video player (16:9 ratio).


* **Restriction:** Disable all playback controls (no seek, no pause).
* **Auto-Transition:** On `audio.onEnded` or `video.onEnded`, automatically switch the state to the **Question Set View**.

* **Layout-blueprint:**
______________________________________________________________________
| [CELPIP-GENERAL]          [PART 4: NEWS ITEM]         [TIME: 20:00] |
|____________________________________________________________________|
|                                                                    |
|                                                                    |
|                   ____________________________                     |
|                  |                            |                    |
|                  |       PASSAGE IMAGE        |                    |
|                  |             OR             |                    |
|                  |        VIDEO PLAYER        |                    |
|                  |____________________________|                    |
|                                                                    |
|                     [== Listening... 45% ==]                       |
|                                                                    |
|____________________________________________________________________|
| [ PROGRESS: PART 4 ]                                    [ (NEXT) ] |
|____________________________________________________________________|

### **3. Component Logic (The "Question Set" State)**

* **Split-Pane Layout:** * **Left (40%):** A "Review" version of the media (image or video thumbnail) + a "Replay Not Available" message.
* **Right (60%):** A scrollable container (`overflow-y-auto`) containing the question list.


* **Question Format:** * Each question must be an individual card.
* Options should be large radio button tiles.
* **State Change:** When an option is clicked, the tile background should change to light blue (Paragon style).


* **Navigation:** The "Next" button in the footer should only become active once at least one question is answered (or based on your specific validation preference).

* **Layout-blueprint:**
______________________________________________________________________
| [CELPIP LISTENING]          [Part 1: Identifying Action]   [18:42] | <- Header
|____________________________________________________________________|
|                                  |                                 |
|         [ AUDIO VISUAL ]         |          [ QUESTIONS ]          |
|                                  |                                 |
|      (Image of a park or         |    1. What is the man doing?    |
|       audio wave graphic)        |       ( ) Jogging               |
|                                  |       ( ) Reading               |
|          [ Playback ]            |       ( ) Sleeping              |
|                                  |                                 |
|__________________________________|_________________________________|
| [|||||||||||||||||||||        ]                            [NEXT >]| <- Footer
|____________________________________________________________________|

### **4. Data Structure (JSON Example)**

The developer should use a JSON structure to feed the UI:

```json
{
  "part": 5,
  "title": "Listening to a Discussion",
  "mediaType": "video",
  "mediaUrl": "/assets/discussion_05.mp4",
  "questions": [
    {
      "id": "q1",
      "text": "What is the main topic?",
      "options": ["Office policy", "Holiday", "Budget"],
      "correct": 0
    }
  ]
}

```
### **5. Test Structure**
For Test Part 1 -> 3, *The "Question Set" State* will have layout as above. 1 screen for 1 question
For Test Part 4 -> 6, *The "Question Set" State* will have layout similar "Passage state", only contains list of Questions. The remainng time will multily number of questions


### **6. Technical Constraints**

* **Prevent Refresh:** Add a listener to warn users if they try to refresh the page (which would reset the test).
* **Timer Sync:** The Global Timer must persist across the transitions from Passage to Question.
* **The mediaUrl**: It can be either cloud URL or local URL

---

### **7. Implementation Status** ✅

> **Implemented: March 16, 2026**

#### Files Created
| File | Purpose |
|------|---------|
| `templates/listening_section.html` | Practice Mode — state machine, blue theme, replay allowed |
| `templates/listening_test_mode_section.html` | Test Mode — state machine, red theme, no replay, forward-only |
| `data/test_1/listening/part1.json` – `part6.json` | Sample test data (6 parts, 33 questions) |
| `static/audio/test_1/listening/` | Directory for MP3 audio files |
| `static/video/test_1/listening/` | Directory for MP4 video files (Part 5) |
| `static/images/test_1/listening/` | Directory for scene illustration images |

#### Files Modified
| File | Changes |
|------|---------|
| `app.py` | Added `listening` type in `prepare_test_data()` and `prepare_answer_key_data()`; routes auto-select listening templates |
| `templates/test_detail.html` | Listening card shows dynamic parts; added Listening Answer Key button; reset covers all skills |
| `templates/answer_key.html` | Added `is_listening_type` branch for per-part answer display |

#### Spec Coverage
| Requirement | Status |
|-------------|--------|
| State Machine (Playback → Questions) | ✅ |
| Full-screen media in Passage state | ✅ |
| Audio player with progress bar | ✅ |
| Video player for Part 5 | ✅ |
| Auto-transition on media end | ✅ |
| Split pane for Parts 1-3 | ✅ |
| Full-width questions for Parts 4-6 | ✅ |
| Practice Mode: replay, back+next | ✅ |
| Test Mode: no replay, forward-only | ✅ |
| Header/accent color differentiation | ✅ |
| Progress bar (Test Mode only) | ✅ |
| Timer with pulse warning at ≤60s | ✅ |
| Page refresh prevention | ✅ |
| Vocabulary sidebar (authenticated) | ✅ |
| Answer auto-save | ✅ |
| Comprehensive answer key | ✅ |

#### Adding Content for More Tests
```bash
# 1. Create data files
mkdir -p data/test_X/listening
# Copy and edit part1.json through part6.json

# 2. Create media directories
mkdir -p static/audio/test_X/listening
mkdir -p static/video/test_X/listening
mkdir -p static/images/test_X/listening

# 3. Place media files matching the URLs in JSON
# No code changes needed — auto-discovered by data_loader
```

---

### **8. Revision: Updated Question UI (March 16, 2026)** ✅

#### Parts 4-6: Dropdown Select Boxes
Parts 4-6 now use **inline dropdown select boxes** (same pattern as Reading Part 3/4) instead of radio buttons. When an option is chosen, the dropdown is replaced by a styled `.selected-text` span showing the completed sentence. Clicking the span restores the dropdown.

#### Parts 1-3: Per-Question Audio
Each question in Parts 1-3 now has its **own individual audio file**. The audio IS the question, so no question text transcript is displayed. Instead, each question shows:
- A numbered play button with a progress bar
- Radio button answer options below
- In Practice Mode, audio can be replayed per question
- In Test Mode, each question audio plays only once

**Layout (Parts 1-3):**
```
______________________________________________________________________
| [CELPIP LISTENING]          [Part 1: Identifying Action]   [18:42] |
|____________________________________________________________________|
|                                  |                                 |
|         [ AUDIO VISUAL ]        |          [ QUESTIONS ]          |
|                                  |                                 |
|      (Image of a park or        |    1.  [▶ Play] [====    ]     |
|       audio wave graphic)        |       ( ) Jogging               |
|                                  |       ( ) Reading               |
|                                  |       ( ) Sleeping              |
|                                  |                                 |
|                                  |    2.  [▶ Play] [====    ]     |
|                                  |       ( ) Option A              |
|                                  |       ( ) Option B              |
|__________________________________|_________________________________|
| [|||||||||||||||||||||        ]                            [NEXT >]|
|____________________________________________________________________|
```

#### Part 1: Sub-Parts (1.1, 1.2, 1.3)
Part 1 is split into 3 sub-parts, each with its own passage audio. A **tab navigation** bar at the top lets users switch between sub-parts. Each sub-part contains:
- Its own passage audio player
- Its own set of questions with per-question audio

**JSON `sub_parts` structure:**
```json
{
  "sub_parts": [
    {
      "id": "1.1",
      "title": "Conversation about a Lost File",
      "passageAudioUrl": "/static/audio/test_1/listening/part1_1_passage.mp3",
      "imageUrl": "/static/images/test_1/listening/part1_scene.png",
      "questions": [
        {
          "id": 1,
          "audioUrl": "/static/audio/test_1/listening/part1_q1.mp3",
          "text": "What is the woman's main problem?",
          "options": ["Option A", "Option B", "Option C", "Option D"],
          "answer": 3
        }
      ]
    }
  ]
}
```

#### Updated JSON Data Structure

**Parts 1-3** (`layout: "per_question_audio"`):
- Each question has an `audioUrl` field for its individual audio clip
- Part 1 additionally has a `sub_parts` array with passage audio per sub-part
- The `sections` array is kept for backward compatibility with the answer key

**Parts 4-6** (`layout: "full_questions"`):
- Questions are rendered as dropdown select boxes via server-generated `questions_dropdown_html`
- Same JSON structure as before, but rendered differently

#### Files Modified in This Revision
| File | Changes |
|------|---------|
| `app.py` | Extended `prepare_test_data()` to process `per_question_audio` layout (question audio URLs, sub-parts) and `full_questions` layout (generates dropdown HTML) |
| `templates/listening_section.html` | Complete rewrite: 3 layout branches — `per_question_audio` with sub-parts, `per_question_audio` without sub-parts, `full_questions` with dropdowns |
| `templates/listening_test_mode_section.html` | Complete rewrite: same 3 layout branches with Test Mode restrictions (no replay, forward-only, play-once audio) |
| `data/test_1/listening/part1.json` | Added `sub_parts` array with 3 sub-parts (1.1, 1.2, 1.3), `audioUrl` per question, `layout: "per_question_audio"` |
| `data/test_1/listening/part2.json` | Added `audioUrl` per question, `layout: "per_question_audio"` |
| `data/test_1/listening/part3.json` | Added `audioUrl` per question, `layout: "per_question_audio"` |

#### Updated Spec Coverage
| Requirement | Status |
|-------------|--------|
| Parts 4-6: Dropdown select boxes (Reading Part 3/4 style) | ✅ |
| Parts 4-6: Selected option shows as completed sentence | ✅ |
| Parts 1-3: Per-question audio files | ✅ |
| Parts 1-3: No question text transcript (audio IS the question) | ✅ |
| Part 1: Sub-parts 1.1, 1.2, 1.3 with tab navigation | ✅ → Replaced with sequential flow |
| Part 1: Each sub-part has own passage audio | ✅ |
| Practice Mode: Replay per-question audio | ❌ Removed — play once only |
| Test Mode: Play-once per-question audio | ✅ |

---

### **9. Revision: Sequential Flow & Play-Once Audio (March 16, 2026)** ✅

#### Changes

1. **All audio plays once only** — Both passage and per-question audio play exactly once in both Practice and Test Mode. No replay button. After playing, button shows "✓ Played" and is disabled.

2. **Parts 1-3: One question at a time** — Instead of showing all questions simultaneously, the UI now shows a single question per screen in a split-pane layout:
   - **Left panel:** Scene image + question audio player (play button + progress bar)
   - **Right panel:** Single question with radio button options
   - **Timer (top-right):** Per-question countdown (30 seconds per question)
   - When timer expires or user clicks "Next", advances to the next step

3. **Part 1 sub-parts: Sequential flow** — No more tab navigation. The flow is strictly sequential:
   ```
   Passage 1.1 → Q1 → Q2 → Passage 1.2 → Q3 → Q4 → Passage 1.3 → Q5 → [Next Part]
   ```
   Questions are numbered sequentially across all sub-parts (Q1-Q5 continuous).

4. **`app.py` builds a `steps` array** — The `prepare_test_data()` function now builds a flat `steps` list for Parts 1-3:
   ```python
   steps = [
       {"type": "passage", "sub_part_id": "1.1", "title": "...", "audio_url": "..."},
       {"type": "question", "id": 1, "audio_url": "...", "options": [...]},
       {"type": "question", "id": 2, "audio_url": "...", "options": [...]},
       {"type": "passage", "sub_part_id": "1.2", ...},
       ...
   ]
   ```
   This array is serialized to JSON and consumed by the JavaScript state machine.

**Layout (Parts 1-3 — one question at a time):**
```
______________________________________________________________________
| [CELPIP LISTENING]     [Part 1: Problem Solving]   [Q1/5]  [0:30] |
|____________________________________________________________________|
|                                  |                                 |
|         [ AUDIO VISUAL ]        |          [ QUESTION 1 ]         |
|                                  |                                 |
|      (Image of a park or        |       ( ) Jogging               |
|       audio wave graphic)        |       ( ) Reading               |
|                                  |       ( ) Sleeping              |
|   [▶ Play] [==========    ]    |       ( ) Walking               |
|                                  |                                 |
|   🔊 Audio plays once only     |                                 |
|__________________________________|_________________________________|
|                                                           [NEXT >]|
|____________________________________________________________________|
```

**Passage State (Practice Mode — with skip and replay):**
```
______________________________________________________________________
| [CELPIP LISTENING]                                          [--:--] |
|_____________________________________________________________________|
|                                                                     |
|              Listen to Passage 1.1: Title                           |
|           +--------------------------------+                        |
|           |      (Image / Illustration)    |                        |
|           +--------------------------------+                        |
|           [==============        ] 1:24 / 2:15                      |
|                                                                     |
|              [> Play Recording]                                     |
|              [Skip to Questions >]                                  |
|_____________________________________________________________________|
```

#### Practice Mode vs Test Mode (Parts 1-3)

| Feature | Practice Mode | Test Mode |
|---------|--------------|-----------|
| Passage audio | Plays on click, can replay by revisiting | Auto-plays, no replay |
| "Skip to Questions" button | Yes | No |
| Question audio | Can replay freely (Play / Replay) | Play once only (Played) |
| Per-question timer | 30 seconds, auto-advance | 30 seconds, auto-advance |
| Navigation | Forward-only (sequential) | Forward-only (sequential) |

#### Files Modified
| File | Changes |
|------|---------|
| `app.py` | `prepare_test_data()` now builds a flat `steps` array (passage + question sequence) for `per_question_audio` layout |
| `templates/listening_section.html` | JS state machine: passage-question flow, 1 question at a time, 30s timer, replay allowed, skip button on passage |
| `templates/listening_test_mode_section.html` | Same sequential state machine, Test Mode styling, auto-play passage, play-once only, no skip |

#### Updated Spec Coverage
| Requirement | Status |
|-------------|--------|
| Practice Mode: Replay passage and question audio | Done |
| Practice Mode: "Skip to Questions" on passage state | Done |
| Test Mode: Play-once only, no skip | Done |
| Parts 1-3: One question at a time | Done |
| Parts 1-3: Per-question timer (30s) | Done |
| Parts 1-3: Question audio on LEFT panel | Done |
| Part 1: Sequential flow (Passage 1.1 - Qs - Passage 1.2 - Qs - ...) | Done |
| Part 1: Continuous question numbering across sub-parts | Done |
| Tab navigation removed (replaced by sequential flow) | Done |

---

In folder pdftotext. Please use script to convert file @pdftotext/LISTENING SET 1-5.pdf from page 22 to page 43. The converted file is Questions and Answers key for Listening Test 2. After converting it, please help to fill data for Listening Test 2 in folder "data/test_2/listening"
The value of mediaUrl/passageAudioUrl/audioUrl would follow patern
Part 6: https://res.cloudinary.com/dga4ax7q2/video/upload/v1773688398/p6.m4a
Part 1.1: https://res.cloudinary.com/dga4ax7q2/video/upload/v1773688412/p1-1.m4a
Quesiton 2 of Part 2: https://res.cloudinary.com/dga4ax7q2/video/upload/v1773688463/p2-q2.m4a
For the transcript of LISTENING TEST, please use file "LISTENING TRANSCRIPT SET 1-5.pdf" from page 8 to page 15