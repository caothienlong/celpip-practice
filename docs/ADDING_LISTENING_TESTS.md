# Adding Listening Test Content Guide

## Overview

This guide explains how to parse the **LISTENING SET 1-5 PDF** and **TRANSCRIPT 1-5 PDF** into structured JSON data for the CELPIP Listening module.

### Source Files

| File | Contents | Location |
|------|----------|----------|
| **Questions PDF** | Questions, options, answer keys, instructions | `pdftotext/LISTENING SET 1-5.pdf` (311 pages) |
| **Transcript PDF** | Full conversation/passage transcripts | `pdftotext/TRANSCRIPT 1-5 - Celpip Listening.pdf` (74 pages) |

### How the PDFs Are Organized

The PDFs are opened directly in Cursor (which renders them as text). Line numbers in this document refer to the line numbers shown when reading these PDF files with the Read tool.

---

## PDF Structure: SETs, TESTs, and Parts

### Hierarchy

```
SET 1 (pages 1–67)
  ├── Practice Test 1 (= Test 1)  → Parts 1–6 with questions + answer keys
  ├── Practice Test 2 (= Test 2)  → Parts 1–6 with questions + answer keys
  └── TRANSCRIPT section
       ├── TEST 1 → Full transcripts for Parts 1–6
       └── TEST 2 → Full transcripts for Parts 1–6

SET 2 (pages 68–129)
  ├── Practice Test 1 (= Test 3)
  ├── Practice Test 2 (= Test 4)
  └── TRANSCRIPT section (TEST 1 + TEST 2)

SET 3 (pages 130–192) → Test 5 + Test 6
SET 4 (pages 193–250) → Test 7 + Test 8
SET 5 (pages 251–311) → Test 9 + Test 10
```

### SET → Test Number Mapping

| SET | Practice Test 1 | Practice Test 2 | Data Directory |
|-----|----------------|----------------|----------------|
| SET 1 | Test 1 | Test 2 | `data/test_1/`, `data/test_2/` |
| SET 2 | Test 3 | Test 4 | `data/test_3/`, `data/test_4/` |
| SET 3 | Test 5 | Test 6 | `data/test_5/`, `data/test_6/` |
| SET 4 | Test 7 | Test 8 | `data/test_7/`, `data/test_8/` |
| SET 5 | Test 9 | Test 10 | `data/test_9/`, `data/test_10/` |

### SET Boundaries in Questions PDF (Line Numbers)

| SET | Start Line | Start Page | End Line | End Page | Marker Text |
|-----|-----------|------------|----------|----------|-------------|
| SET 1 | 1 | 1 | ~1530 | 67 | `LISTENING SET 1` |
| SET 2 | ~1535 | 68 | ~2989 | 129 | `SET 2` |
| SET 3 | ~2994 | 130 | ~4493 | 192 | `SET 3` |
| SET 4 | ~4498 | 193 | ~5927 | 250 | `SET 4` |
| SET 5 | ~5928 | 251 | ~6799 | 289 | `SET 5` |
| Transcripts | ~6800 | 290 | ~7402 | 311 | `TRANSCRIPT` |

> **Note**: SET 5's last pages (290–311) contain transcripts for all of SET 5, duplicating what's in the Transcript PDF.

### SET Boundaries in Transcript PDF (Line Numbers)

| Section | Start Line | End Line | Marker |
|---------|-----------|----------|--------|
| SET 1 TEST 1 | 7 | ~256 | `SET 1 - TEST 1` |
| SET 1 TEST 2 | ~257 | ~495 | `SET 1 - TEST 2` |
| SET 2 TEST 1 | ~496 | ~739 | `SET 2 - TEST 1` |
| SET 2 TEST 2 | ~740 | ~978 | `SET 2 - TEST 2` |
| SET 3 TEST 1 | ~986 | ~1227 | `SET 3 - TEST 1` |
| SET 3 TEST 2 | ~1228 | ~1468 | `SET 3 - TEST 2` |
| SET 4 TEST 1 | ~1477 | ~1707 | `SET 4 - TEST 1` |
| SET 4 TEST 2 | ~1708 | ~1925 | `SET 4 - TEST 2` |
| SET 5 TEST 1 | ~1934 | ~2157 | `SET 5 - TEST 1` |
| SET 5 TEST 2 | ~2166 | ~2400 | `SET 5 - TEST 2` |

### Within Each SET: Test Boundaries

Inside each SET in the Questions PDF, the structure is:

```
SET X
Practice Test 1 - Listening Part 1: Listening to Problem Solving
  [instructions, questions, answer key]
Practice Test 1 - Listening Part 2: Listening to a Daily Life Conversation
  [instructions, questions, answer key]
  ...through Part 6...

TEST 2   ← or "Practice Test 2 - Listening Part 1: ..."
Practice Test 2 - Listening Part 1: Listening to Problem Solving
  [instructions, questions, answer key]
  ...through Part 6...

TRANSCRIPT   ← only in SET 5 (pages 290–311)
```

The boundary between Practice Test 1 and Practice Test 2 is marked by either:
- The text `TEST 2` on its own line
- The first occurrence of `Practice Test 2` after all 6 parts of Test 1

---

## CELPIP Listening Parts Reference

| Part | Title | # Questions | Layout | Media | Special Notes |
|------|-------|-------------|--------|-------|---------------|
| 1 | Listening to Problem Solving | 8 | `per_question_audio` | audio | 3 `sub_parts` (sections), each with own passage audio |
| 2 | Listening to a Daily Life Conversation | 5 | `per_question_audio` | audio | Single conversation passage |
| 3 | Listening for Information | 6 | `per_question_audio` | audio | Single conversation passage |
| 4 | Listening to a News Item | 5 | `full_questions` | audio | Sentence-stem questions (dropdown style) |
| 5 | Listening to a Discussion | 8 | `full_questions` | **video** | `listening_type: "video"`, `mediaType: "video"` |
| 6 | Listening for Viewpoints | 6 | `full_questions` | audio | Sentence-stem questions (dropdown style) |

### Part 1 Section Split Pattern

Part 1 always has 3 sections with 8 total questions. The split varies by test, but common patterns:
- Section 1: Q1–Q2, Section 2: Q3–Q5, Section 3: Q6–Q8
- Section 1: Q1–Q3, Section 2: Q4–Q5, Section 3: Q6–Q8

Look for these markers in the PDF to determine splits:
- `"You will hear the second section of the conversation shortly."`
- `"You will hear the third section of the conversation shortly."`
- In transcripts: `"Now answer questions X-Y."` or `"Section 2:"`, `"Section 3:"`

---

## Step-by-Step: AI Parsing Procedure

This is the procedure for having an AI assistant (Cursor Agent) parse the PDFs into JSON data.

### Step 1: Identify Target SET and Line Ranges

Using the boundary tables above, determine:
- Which SET to parse
- The line ranges in the Questions PDF for that SET
- The line ranges in the Transcript PDF for that SET's TEST 1 and TEST 2

**Example for SET 3 (Test 5 + Test 6):**
- Questions PDF: lines ~2994 to ~4493
- Transcript PDF TEST 1 (Test 5): lines ~986 to ~1227
- Transcript PDF TEST 2 (Test 6): lines ~1228 to ~1468

### Step 2: Read the Questions PDF Content

Read the Questions PDF in chunks of ~200-300 lines within the identified range. For each part, extract:

1. **Instructions**: The text after "Listening Part X: [Title]"
2. **Context**: The text after "Instructions:" describing the scenario
3. **Questions**: Lines starting with `Question X of Y`, followed by `•` bullet options
4. **Answer Key**: Lines like `Listening Part X: [Title] - Q1 [answer text]`

### Step 3: Read the Transcript PDF Content

Read the Transcript PDF for the matching SET/TEST section. For each part, extract the full conversation text between part headers.

**Cleanup rules for transcripts:**
- Remove page numbers, headers (`Compiled by Toan Lam`), footers, page breaks (`-- X of Y --`)
- Keep speaker labels (`MAN:`, `WOMAN:`, character names like `Larry:`)
- For Part 1, preserve `Section 1:`, `Section 2:`, `Section 3:` labels
- Join lines that were split by page breaks

### Step 4: Determine Answer Indices

The `answer` field is a **0-based index** into the `options` array.

```
Question 1 options:
  • to get a membership          ← index 0
  • to receive a discount        ← index 1
  • to check his account         ← index 2  ← CORRECT
  • to take a cardio class       ← index 3

Answer key text: "to check his account"
→ answer: 2
```

Match the answer key text to the exact option string. Be careful with partial matches or slight wording differences.

### Step 5: Determine Part 1 Section Splits

Look for these markers in the Questions PDF or Transcript PDF:
- `"You will hear the second section"` → marks end of Section 1 questions
- `"You will hear the third section"` → marks end of Section 2 questions
- In transcripts: `"Now answer questions X-Y."` gives exact ranges

### Step 6: Create JSON Files

Create 6 files per test in `data/test_X/listening/partY.json`. Use the templates below.

### Step 7: Validate

```bash
for file in data/test_X/listening/part*.json; do
    echo -n "Checking $file... "
    python -m json.tool "$file" > /dev/null 2>&1 && echo "✓ Valid" || echo "✗ Invalid"
done
```

### Step 8: Spot Check Answers

```bash
python3 -c "
import json, glob
for f in sorted(glob.glob('data/test_X/listening/part*.json')):
    d = json.load(open(f))
    print(f'Part {d[\"part\"]}: {d[\"title\"]}')
    for section in d.get('sections', []):
        for q in section.get('questions', []):
            ans = q['answer']
            if ans is not None and q['options']:
                print(f'  Q{q[\"id\"]}: [{ans}] {q[\"options\"][ans]}')
    print()
"
```

---

## JSON Templates

### Part 1 Template (per_question_audio with sub_parts)

Part 1 has 3 sub-parts (sections of conversation), each with its own passage audio and 2-3 questions per section. Total: 8 questions.

**Important:** The `sections` array is a flat list of ALL 8 questions (used by the answer key page). The `sub_parts` array organizes questions by conversation section (used by the listening UI).

```json
{
  "part": 1,
  "title": "Listening to Problem Solving",
  "type": "listening",
  "listening_type": "audio",
  "instructions": "You will hear a conversation in 3 sections. You will hear each section only once. After each section, you will hear 2 or 3 questions. You will hear the questions only once. Choose the best answer to each question.",
  "mediaType": "audio",
  "imageAlt": "Description of the scene",
  "layout": "per_question_audio",
  "context": "You will hear a conversation between...",
  "sub_parts": [
    {
      "id": "1.1",
      "title": "Section 1",
      "passageAudioUrl": "",
      "imageUrl": "",
      "questions": [
        {
          "id": 1,
          "audioUrl": "",
          "text": "Question 1",
          "options": ["Option A", "Option B", "Option C", "Option D"],
          "answer": 2
        }
      ]
    },
    {
      "id": "1.2",
      "title": "Section 2",
      "passageAudioUrl": "",
      "imageUrl": "",
      "questions": []
    },
    {
      "id": "1.3",
      "title": "Section 3",
      "passageAudioUrl": "",
      "imageUrl": "",
      "questions": []
    }
  ],
  "transcript": "Section 1:\nMAN: ...\nWOMAN: ...\n\nSection 2:\n...\n\nSection 3:\n...",
  "sections": [
    {
      "section_type": "questions",
      "questions": [
        { "id": 1, "text": "Question 1", "options": ["..."], "answer": 2 },
        { "id": 2, "text": "Question 2", "options": ["..."], "answer": 0 }
      ]
    }
  ]
}
```

### Parts 2-3 Template (per_question_audio)

```json
{
  "part": 2,
  "title": "Listening to a Daily Life Conversation",
  "type": "listening",
  "listening_type": "audio",
  "instructions": "You will hear a conversation followed by 5 questions. Listen to each question. You will hear the questions only once. Choose the best answer to each question.",
  "mediaType": "audio",
  "mediaUrl": "",
  "imageUrl": "",
  "imageAlt": "Description of the scene",
  "layout": "per_question_audio",
  "context": "You will hear a conversation...",
  "transcript": "MAN: ...\nWOMAN: ...",
  "sections": [
    {
      "section_type": "questions",
      "questions": [
        {
          "id": 1,
          "audioUrl": "",
          "text": "Question 1",
          "options": ["Option A", "Option B", "Option C", "Option D"],
          "answer": 2
        }
      ]
    }
  ]
}
```

### Parts 4 and 6 Template (full_questions, audio)

Question `text` is a **sentence stem** completed by the selected option (dropdown style).

```json
{
  "part": 4,
  "title": "Listening to a News Item",
  "type": "listening",
  "listening_type": "audio",
  "instructions": "You will hear a news item once. It is about 1.5 minutes long. Then 5 questions will appear. Choose the best way to complete each statement from the drop-down menu.",
  "mediaType": "audio",
  "mediaUrl": "",
  "imageUrl": "",
  "imageAlt": "Description of the news item",
  "layout": "full_questions",
  "context": "You will hear a news item about...",
  "transcript": "Full news item text...",
  "sections": [
    {
      "section_type": "questions",
      "questions": [
        {
          "id": 1,
          "text": "The sentence stem that needs completing",
          "options": ["completion option A.", "completion option B.", "completion option C.", "completion option D."],
          "answer": 1
        }
      ]
    }
  ]
}
```

### Part 5 Template (full_questions, VIDEO)

```json
{
  "part": 5,
  "title": "Listening to a Discussion",
  "type": "listening",
  "listening_type": "video",
  "instructions": "You will watch a 2-minute video. Then 8 questions will appear. Choose the best way to answer each question.",
  "mediaType": "video",
  "mediaUrl": "",
  "imageUrl": "",
  "imageAlt": "Description of the discussion",
  "layout": "full_questions",
  "context": "You will watch a discussion between...",
  "transcript": "Name1: ...\nName2: ...",
  "sections": [
    {
      "section_type": "questions",
      "questions": [
        {
          "id": 1,
          "text": "Why is the party being organized?",
          "options": ["option A", "option B", "option C", "option D"],
          "answer": 0
        }
      ]
    }
  ]
}
```

---

## Batch Validation Commands

### Validate all JSON files for a range of tests

```bash
for f in data/test_{3,4,5,6,7,8,9,10}/listening/part*.json; do
    echo -n "$f: "
    python3 -m json.tool "$f" > /dev/null 2>&1 && echo "OK" || echo "INVALID"
done
```

### Check file counts (should be 6 per test)

```bash
for t in 1 2 3 4 5 6 7 8 9 10; do
    count=$(ls data/test_$t/listening/part*.json 2>/dev/null | wc -l)
    echo "test_$t: $count files"
done
```

### Verify question counts and layouts

```bash
for f in data/test_*/listening/part*.json; do
    part=$(python3 -c "import json; print(json.load(open('$f')).get('part','?'))")
    qcount=$(python3 -c "import json; d=json.load(open('$f')); print(len(d.get('sections',[{}])[0].get('questions',[])))")
    layout=$(python3 -c "import json; print(json.load(open('$f')).get('layout','?'))")
    echo "$f: part=$part, questions=$qcount, layout=$layout"
done
```

Expected question counts: Part 1=8, Part 2=5, Part 3=6, Part 4=5, Part 5=8, Part 6=6.

### Verify Part 5 uses video type

```bash
for t in 1 2 3 4 5 6 7 8 9 10; do
    lt=$(python3 -c "import json; print(json.load(open('data/test_$t/listening/part5.json')).get('listening_type','MISSING'))" 2>/dev/null)
    echo "test_$t part5: listening_type=$lt"
done
```

### Verify Part 1 has 3 sub_parts

```bash
for t in 1 2 3 4 5 6 7 8 9 10; do
    sp=$(python3 -c "import json; print(len(json.load(open('data/test_$t/listening/part1.json')).get('sub_parts',[])))" 2>/dev/null)
    echo "test_$t part1: sub_parts=$sp"
done
```

### Print all answers for manual verification

```bash
python3 -c "
import json, glob
for f in sorted(glob.glob('data/test_X/listening/part*.json')):
    d = json.load(open(f))
    print(f'Part {d[\"part\"]}: {d[\"title\"]}')
    for section in d.get('sections', []):
        for q in section.get('questions', []):
            ans = q['answer']
            if ans is not None and q['options']:
                print(f'  Q{q[\"id\"]}: [{ans}] {q[\"options\"][ans]}')
    print()
"
```

Replace `test_X` with the actual test number.

---

## Test in Browser

```bash
python app.py
# Visit http://localhost:5000
# Navigate to the test and select Listening
```

Verify:
- [ ] All 6 parts load correctly
- [ ] Questions display with correct options
- [ ] Answer key shows correct answers
- [ ] Parts 1-3: Per-question audio layout works
- [ ] Parts 4-6: Dropdown-style questions work
- [ ] Part 1: Sub-part navigation works

---

## Known PDF Issues and Quirks

When parsing the Listening PDFs, be aware of these issues discovered during the SET 1-5 extraction:

### Missing Questions

The PDF occasionally **skips a question number** — the question exists in the audio but is not printed. Known instances:

| Test | Part | Question | Notes |
|------|------|----------|-------|
| Test 3 | Part 5 | Q3 | Jumps from Q2 to Q4 in the PDF |
| Test 4 | Part 1 | Q1 | Q1 bullets missing; page starts at Q2 |
| Test 6 | Part 1 | Q6 | Jumps from Section 3 intro to Q7 |
| Test 8 | Part 1 | Q6 | Missing between Section 3 and Q7 |
| Test 9 | Part 1 | Q2 | Jumps from Q1 to Q3 |
| Test 10 | Part 1 | Q2 | Missing between Q1 and Q3 |

**Workaround:** Use the transcript and answer key to reconstruct the missing question. The answer key usually still has the answer text. Create a plausible question stem and options based on context, with the correct answer matching the key.

### Missing Answer Key Lines

Some answer key lines are **blank** (the question number is there but no answer text):

| Test | Part | Question | Notes |
|------|------|----------|-------|
| Test 1 | Part 1 | Q4 | Image-based question (options are "1","2","3","4") |
| Test 6 | Part 1 | Q6 | Answer key line blank |
| Test 8 | Part 1 | Q6 | Answer key line blank |

**Workaround:** Infer the answer from the transcript context. Mark these as needing verification.

### Page Headers/Footers to Strip

Every page in the PDF contains noise lines. Strip these when extracting content:
- `Complied by Toan Lam` (sic — "Complied" not "Compiled")
- `Source: Celipip-General practice test (sets 1-5)`
- `-- X of Y --` (page markers)
- Page numbers (standalone numbers at line start)
- `Compiled by Toan Lam` / `Biên soạn & tổng hợp bởi Toàn Lâm` (in Transcript PDF)

### Other Issues

- **Split text across pages:** Long option text or answer key text may wrap across lines. Look for continuation lines.
- **Duplicate instructions:** Some Part 1s repeat the "Instructions:" block twice.
- **Transcript PDF has Part 3 Q6 misplaced in SET 5 TEST 2:** The Part 3 conversation text continues, then Part 4 news text appears, then Part 3 Q6 follow-up dialogue appears. This is a PDF layout quirk — the conversation is complete, just oddly placed.

---

## Audio/Video Files

The JSON files reference audio and video URLs. These can be:

### Cloud-hosted (Cloudinary)
```
https://res.cloudinary.com/YOUR_CLOUD_NAME/video/upload/v.../filename.m4a
```

### Locally-hosted
```
/static/audio/test_X/listening/pY-pas.mp3
/static/audio/test_X/listening/pY-qN.mp3
/static/video/test_X/listening/p5-pas.mp4
```

### Placeholder URLs

For tests without audio/video yet, use empty strings `""` as placeholders:
```json
"mediaUrl": "",
"audioUrl": "",
"passageAudioUrl": ""
```

### Cloudinary Setup (One-Time)

Audio and video files are hosted on [Cloudinary](https://cloudinary.com/) (free tier is sufficient).

1. **Create an account** at [cloudinary.com/users/register_free](https://cloudinary.com/users/register_free)
2. **Get your API credentials** from [console.cloudinary.com/settings/api-keys](https://console.cloudinary.com/settings/api-keys):
   - Cloud Name (from your Cloudinary dashboard)
   - API Key
   - API Secret
3. **Add them to your `.env`** file:
   ```
   CLOUDINARY_CLOUD_NAME=your-cloud-name
   CLOUDINARY_API_KEY=your-api-key-here
   CLOUDINARY_API_SECRET=your-api-secret-here
   ```
4. **Install the Python packages** (in your venv):
   ```bash
   pip install gdown cloudinary
   ```

> **Note:** The app itself does NOT need Cloudinary credentials — it just uses public Cloudinary URLs in `<audio>`/`<video>` tags. The API key is only needed for the upload scripts below.

### Migrating from Google Drive to Cloudinary

If your audio/video files are hosted on Google Drive, use the migration script
to bulk-upload them to Cloudinary:

```bash

# Upload a single file
python scripts/gdrive_to_cloudinary.py \
  --url "https://drive.google.com/file/d/FILE_ID/view"

# Upload an entire shared Google Drive folder
python scripts/gdrive_to_cloudinary.py \
  --folder "https://drive.google.com/drive/folders/FOLDER_ID" \
  --cloudinary-folder "celpip/test_3/listening"

# Upload AND auto-update the JSON test files with new URLs
python scripts/gdrive_to_cloudinary.py \
  --folder "https://drive.google.com/drive/folders/FOLDER_ID" \
  --cloudinary-folder "celpip/test_3/listening" \
  --update-json data/test_3/listening

# Dry run (download only, see what would happen)
python scripts/gdrive_to_cloudinary.py \
  --folder "FOLDER_URL" --dry-run
```

See `scripts/gdrive_to_cloudinary.py --help` for all options.

### Audio File Naming Convention

Use **short names**, **hyphens** as separators, and these abbreviations:
- `p` = part, `q` = question, `pas` = passage

| Pattern | Example | Purpose |
|---------|---------|---------|
| `pY-pas.m4a` | `p2-pas.m4a` | Main passage audio (parts 2-4, 6) |
| `pY-qN.m4a` | `p2-q1.m4a` | Per-question audio (parts 1-3) |
| `p1-S-pas.m4a` | `p1-1-pas.m4a` | Part 1, Section S passage audio |
| `p5-pas.mp4` | `p5-pas.mp4` | Part 5 video file |

Full file list per test:

| File | Purpose |
|------|---------|
| `p1-1-pas.m4a` | Part 1, Section 1 passage |
| `p1-2-pas.m4a` | Part 1, Section 2 passage |
| `p1-3-pas.m4a` | Part 1, Section 3 passage |
| `p1-q1.m4a` .. `p1-q8.m4a` | Part 1, Questions 1-8 |
| `p2-pas.m4a` | Part 2 passage |
| `p2-q1.m4a` .. `p2-q5.m4a` | Part 2, Questions 1-5 |
| `p3-pas.m4a` | Part 3 passage |
| `p3-q1.m4a` .. `p3-q6.m4a` | Part 3, Questions 1-6 |
| `p4-pas.m4a` | Part 4 passage |
| `p5-pas.mp4` | Part 5 video |
| `p6-pas.m4a` | Part 6 passage |

> **Important:** When updating JSON data, do NOT change existing `audioUrl`, `passageAudioUrl`, or `mediaUrl` values unless you are also replacing the media files.

---

## Content Summary: All Tests

### SET 1 (Tests 1–2) — Has audio/video assets

| Test | Part 1 | Part 2 | Part 3 | Part 4 | Part 5 | Part 6 |
|------|--------|--------|--------|--------|--------|--------|
| 1 | Health club | Restaurant servers | Art supply store | Family camping trip | Company anniversary | School uniforms |
| 2 | Norgus hat / outdoor store | Volunteering | New employee orientation | Cooper College courses | Vacation policy | Free trade (CFTA) |

### SET 2 (Tests 3–4) — JSON only, no audio yet

| Test | Part 1 | Part 2 | Part 3 | Part 4 | Part 5 | Part 6 |
|------|--------|--------|--------|--------|--------|--------|
| 3 | Veterinary clinic (cat Tiger) | Thrift store donation | Renting apartment | Stolen wallet (GPS) | Parking lot aphids | E-textbooks |
| 4 | Shirt shopping/exchange | Weekend activities | Workplace massage | Lost engagement ring | Montreal trip | Urban chicken bylaws |

### SET 3 (Tests 5–6) — JSON only, no audio yet

| Test | Part 1 | Part 2 | Part 3 | Part 4 | Part 5 | Part 6 |
|------|--------|--------|--------|--------|--------|--------|
| 5 | University course registration | Bus stop conversation | Wedding catering | Hikers lost on mountain | Hostile workplace lecture | Traffic congestion |
| 6 | Eyeglass store | Top Employee Award | Wedding photographer | Billboard protest | Writing skills tutors | Working from home |

### SET 4 (Tests 7–8) — JSON only, no audio yet

| Test | Part 1 | Part 2 | Part 3 | Part 4 | Part 5 | Part 6 |
|------|--------|--------|--------|--------|--------|--------|
| 7 | Rented house heating | CableTron appointment | Student music club | Raccoons news | Hospital gift shop | Buying vs leasing cars |
| 8 | Pharmacy eye drops | Printer return | Tree removal/landscaping | Yard sale book | Weekend shift scheduling | Green bins composting |

### SET 5 (Tests 9–10) — JSON only, no audio yet

| Test | Part 1 | Part 2 | Part 3 | Part 4 | Part 5 | Part 6 |
|------|--------|--------|--------|--------|--------|--------|
| 9 | Tour bus guide | Sprinkler playground | Music store instruments | Community garden | Sales presentations | Suburbs viewpoints |
| 10 | Walk-in medical clinic | Pick-your-own farm | Renters' legal clinic | Thrift store amber rings | Workplace favouritism | Humanities in universities |

---

## Progress Tracker

- [x] **Test 1** — Complete (JSON + audio/video)
- [x] **Test 2** — Complete (JSON + audio/video)
- [x] **Test 3** — JSON complete, needs audio/video
- [x] **Test 4** — JSON complete, needs audio/video
- [x] **Test 5** — JSON complete, needs audio/video
- [x] **Test 6** — JSON complete, needs audio/video
- [x] **Test 7** — JSON complete, needs audio/video
- [x] **Test 8** — JSON complete, needs audio/video
- [x] **Test 9** — JSON complete, needs audio/video
- [x] **Test 10** — JSON complete, needs audio/video

### Items Needing Manual Verification

These questions were reconstructed from transcript context because the PDF was missing the question text or answer key. Verify against the official test book:

| Test | Part | Q# | Issue |
|------|------|----|-------|
| 3 | 5 | Q3 | Question missing from PDF |
| 4 | 1 | Q1 | Question bullets missing from PDF |
| 6 | 1 | Q6 | Question and answer missing from PDF |
| 8 | 1 | Q6 | Question and answer missing from PDF |
| 9 | 1 | Q2 | Question missing from PDF |
| 10 | 1 | Q2 | Question missing from PDF |

---

## Related Documentation

| Document | Description |
|----------|-------------|
| `docs/ADDING_TESTS.md` | Adding Reading test content |
| `docs/ARCHITECTURE.md` | Overall project architecture |
