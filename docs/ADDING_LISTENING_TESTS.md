# Adding Listening Test Content Guide

## Overview

This guide explains how to convert the **LISTENING SET 1-5 PDF** into structured JSON data for the CELPIP Listening module. The process involves:

1. Converting PDF pages to text using `pdftotext`
2. Identifying questions, options, and answer keys from the extracted text
3. Filling in the JSON files in `data/test_X/listening/`

---

## Prerequisites

### Install pdftotext (part of Poppler)

```bash
# macOS
brew install poppler

# Ubuntu/Debian
sudo apt-get install poppler-utils
```

Verify installation:
```bash
pdftotext -v
```

### Source PDF

The source file is located at:
```
pdftotext/LISTENING SET 1-5.pdf
```

---

## Step 1: Convert PDF to Text

### Quick Command

Use `pdftotext` with the `-layout` flag to preserve formatting:

```bash
pdftotext -f START_PAGE -l END_PAGE -layout "pdftotext/LISTENING SET 1-5.pdf" -
```

- `-f` = first page
- `-l` = last page
- `-layout` = preserves spatial layout (important for matching options to questions)
- `-` = output to stdout (use a filename instead to save to file)

### Page Ranges per Test

| Test | Pages | Command |
|------|-------|---------|
| Test 1 | 1–21 | `pdftotext -f 1 -l 21 -layout "pdftotext/LISTENING SET 1-5.pdf" output_test1.txt` |
| Test 2 | 22–42 | `pdftotext -f 22 -l 42 -layout "pdftotext/LISTENING SET 1-5.pdf" output_test2.txt` |
| Test 3 | 43–63 | Adjust based on actual PDF structure |
| Test 4 | 64–84 | Adjust based on actual PDF structure |
| Test 5 | 85–105 | Adjust based on actual PDF structure |

> **Note:** Page ranges are approximate. Each test covers 6 parts with questions and answer keys. Look for "Practice Test X" headers to identify boundaries.

### Saving to File (Recommended)

```bash
pdftotext -f 1 -l 21 -layout "pdftotext/LISTENING SET 1-5.pdf" pdftotext/listening_test1.txt
```

Then review:
```bash
less pdftotext/listening_test1.txt
```

---

## Step 2: Understand the PDF Structure

Each test in the PDF follows this pattern for each of the 6 parts:

```
Practice Test X - Listening Part Y: [Title]

[Instructions]
[Context description]

[Questions with options]

[Answer Key section]
  Listening Part Y: [Title] - Q1   [correct answer text]
  Listening Part Y: [Title] - Q2   [correct answer text]
  ...
```

### What to Extract

For each part, you need:
1. **Part title** (e.g., "Listening to Problem Solving")
2. **Instructions** (the instruction paragraph)
3. **Context** (the scenario description)
4. **Questions** with their numbered options (bullet points)
5. **Answer key** (the "Listening Part Y - Q1" lines at the end)

### CELPIP Listening Parts Reference

| Part | Title | # Questions | Layout | Special |
|------|-------|-------------|--------|---------|
| 1 | Listening to Problem Solving | 8 | `per_question_audio` | 3 sub-parts (sections) |
| 2 | Listening to a Daily Life Conversation | 5 | `per_question_audio` | Single conversation |
| 3 | Listening for Information | 6 | `per_question_audio` | Single conversation |
| 4 | Listening to a News Item | 5 | `full_questions` | Dropdown-style questions |
| 5 | Listening to a Discussion | 8 | `full_questions` | Video-based, dropdown-style |
| 6 | Listening for Viewpoints | 6 | `full_questions` | Dropdown-style questions |

---

## Step 3: Identify the Correct Answer Index

The PDF answer key gives the **text** of the correct answer. You need to find which option index (0-based) it corresponds to.

**Example from PDF:**
```
Question 1 options:
  • to get a membership          ← index 0
  • to receive a discount        ← index 1
  • to check his account         ← index 2
  • to take a cardio class       ← index 3

Answer key: "to check his account"
→ answer: 2
```

### Answer Index Quick Reference

| Index | Meaning |
|-------|---------|
| 0 | First option (first bullet) |
| 1 | Second option |
| 2 | Third option |
| 3 | Fourth option |

---

## Step 4: Create the Data Directory

```bash
# Create listening data directory for a new test
mkdir -p data/test_X/listening

# Create media directories
mkdir -p static/audio/test_X/listening
mkdir -p static/video/test_X/listening
mkdir -p static/images/test_X/listening
```

---

## Step 5: Fill In JSON Files

### Part 1 Template (per_question_audio with sub_parts)

Part 1 has 3 sub-parts (sections of conversation), each with its own passage audio and 2-3 questions per section. Total: 8 questions.

```json
{
  "part": 1,
  "title": "Listening to Problem Solving",
  "type": "listening",
  "listening_type": "audio",
  "instructions": "You will hear a conversation in 3 sections...",
  "mediaType": "audio",
  "imageAlt": "Description of the scene",
  "layout": "per_question_audio",
  "context": "You will hear a conversation between...",
  "sub_parts": [
    {
      "id": "1.1",
      "title": "Section 1",
      "passageAudioUrl": "https://your-cloud-url/part1_1_passage.m4a",
      "imageUrl": "/static/images/test_X/listening/p1_passage.png",
      "questions": [
        {
          "id": 1,
          "audioUrl": "https://your-cloud-url/part1_q1.m4a",
          "text": "Question 1",
          "options": ["Option A", "Option B", "Option C", "Option D"],
          "answer": 2
        }
      ]
    },
    {
      "id": "1.2",
      "title": "Section 2",
      "passageAudioUrl": "https://your-cloud-url/part1_2_passage.m4a",
      "imageUrl": "/static/images/test_X/listening/p1_passage.png",
      "questions": [...]
    },
    {
      "id": "1.3",
      "title": "Section 3",
      "passageAudioUrl": "https://your-cloud-url/part1_3_passage.m4a",
      "imageUrl": "/static/images/test_X/listening/p1_passage.png",
      "questions": [...]
    }
  ],
  "sections": [
    {
      "section_type": "questions",
      "questions": [
        { "id": 1, "text": "Question 1", "options": [...], "answer": 2 },
        { "id": 2, "text": "Question 2", "options": [...], "answer": 0 }
      ]
    }
  ]
}
```

**Important:** The `sections` array is a flat list of ALL 8 questions (used by the answer key page). The `sub_parts` array organizes questions by conversation section (used by the listening UI).

### Parts 2-3 Template (per_question_audio, no sub_parts)

```json
{
  "part": 2,
  "title": "Listening to a Daily Life Conversation",
  "type": "listening",
  "listening_type": "audio",
  "instructions": "You will hear a conversation followed by 5 questions...",
  "mediaType": "audio",
  "mediaUrl": "https://your-cloud-url/part2_passage.m4a",
  "imageUrl": "/static/images/test_X/listening/p2_passage.png",
  "imageAlt": "Description of the scene",
  "layout": "per_question_audio",
  "context": "You will hear a conversation...",
  "sections": [
    {
      "section_type": "questions",
      "questions": [
        {
          "id": 1,
          "audioUrl": "https://your-cloud-url/part2_q1.m4a",
          "text": "Question 1",
          "options": ["Option A", "Option B", "Option C", "Option D"],
          "answer": 2
        }
      ]
    }
  ]
}
```

### Parts 4-6 Template (full_questions, dropdown-style)

For these parts, the question `text` is a **sentence stem** that gets completed by the selected option (dropdown style).

```json
{
  "part": 4,
  "title": "Listening to a News Item",
  "type": "listening",
  "listening_type": "audio",
  "instructions": "You will hear a news item once...",
  "mediaType": "audio",
  "mediaUrl": "https://your-cloud-url/part4_passage.m4a",
  "imageUrl": "/static/images/test_X/listening/p4_passage.png",
  "imageAlt": "Description of the scene",
  "layout": "full_questions",
  "context": "You will hear a news item about...",
  "sections": [
    {
      "section_type": "questions",
      "questions": [
        {
          "id": 1,
          "text": "Michael Jansen was driving back to the campsite when",
          "options": [
            "he nearly hit a person crossing the road.",
            "he hit a deer that crossed the road.",
            "he saw an accident on the highway.",
            "a large bird flew into his windshield."
          ],
          "answer": 1
        }
      ]
    }
  ]
}
```

### Part 5 Special Case (Video)

Part 5 uses video instead of audio:

```json
{
  "part": 5,
  "listening_type": "video",
  "mediaType": "video",
  "mediaUrl": "https://your-cloud-url/part5_passage.mp4"
}
```

---

## Step 6: Validate JSON Files

### Check a single file

```bash
python -m json.tool data/test_X/listening/part1.json > /dev/null && echo "Valid" || echo "Invalid"
```

### Check all parts

```bash
for file in data/test_X/listening/part*.json; do
    echo -n "Checking $file... "
    python -m json.tool "$file" > /dev/null 2>&1 && echo "✓ Valid" || echo "✗ Invalid"
done
```

### Verify answers match the PDF answer key

```bash
python3 -c "
import json, glob
for f in sorted(glob.glob('data/test_X/listening/part*.json')):
    with open(f) as fp:
        d = json.load(fp)
    print(f'Part {d[\"part\"]}: {d[\"title\"]}')
    for section in d.get('sections', []):
        for q in section.get('questions', []):
            ans = q['answer']
            if ans is not None and q['options']:
                print(f'  Q{q[\"id\"]}: [{ans}] {q[\"options\"][ans]}')
            else:
                print(f'  Q{q[\"id\"]}: No answer')
    print()
"
```

---

## Step 7: Test in Browser

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

## Complete Workflow Example

Here's the full workflow used to create Test 1 Listening data:

```bash
# 1. Convert PDF pages 1-21 (Test 1 Listening)
pdftotext -f 1 -l 21 -layout "pdftotext/LISTENING SET 1-5.pdf" pdftotext/listening_test1.txt

# 2. Review the extracted text
less pdftotext/listening_test1.txt

# 3. Identify questions, options, and answer keys for each of the 6 parts

# 4. Create/update JSON files
#    data/test_1/listening/part1.json  (8 questions, 3 sub-parts)
#    data/test_1/listening/part2.json  (5 questions)
#    data/test_1/listening/part3.json  (6 questions)
#    data/test_1/listening/part4.json  (5 questions)
#    data/test_1/listening/part5.json  (8 questions)
#    data/test_1/listening/part6.json  (6 questions)

# 5. Validate all JSON files
for file in data/test_1/listening/part*.json; do
    echo -n "Checking $file... "
    python -m json.tool "$file" > /dev/null 2>&1 && echo "✓" || echo "✗"
done

# 6. Test in browser
python app.py
```

---

## Known PDF Issues

When extracting text from the Listening PDF, be aware of these common issues:

1. **Missing questions/options:** Some questions are audio-only in the actual test. The PDF may not contain the question text or options (e.g., Test 1 Part 1 Q4 has no options in the PDF).

2. **Duplicate answer keys:** The PDF sometimes duplicates an answer key section from a previous part instead of the current part (e.g., Test 1 has Part 3 answer key duplicated on pages 14-15 where Part 4 answers should be).

3. **Missing Part 4 answer keys:** For some tests, the Part 4 answer key is not present in the expected page range. Check later pages or other sections of the PDF.

4. **Split text across pages:** Long answer texts may be split across lines in the extracted text. Look for continuation lines that are indented.

5. **Page headers/footers:** Lines containing "Complied by Toan Lam" and "Source: Celipip-General practice test" are footers — ignore them.

---

## Audio/Video Files

The JSON files reference audio and video URLs. These can be:

### Cloud-hosted (Cloudinary)
```
https://res.cloudinary.com/dga4ax7q2/video/upload/v.../filename.m4a
```

### Locally-hosted
```
/static/audio/test_X/listening/partY_passage.mp3
/static/audio/test_X/listening/partY_qN.mp3
/static/video/test_X/listening/part5.mp4
```

### Audio File Naming Convention

| File | Purpose |
|------|---------|
| `partY_passage.m4a` | Main passage audio for parts 2-6 |
| `part1_1_passage.m4a` | Part 1, Section 1 passage audio |
| `part1_2_passage.m4a` | Part 1, Section 2 passage audio |
| `part1_3_passage.m4a` | Part 1, Section 3 passage audio |
| `partY_qN.m4a` | Per-question audio for parts 1-3 |
| `part5_passage.mp4` | Part 5 video file |

> **Important:** When updating JSON data, do NOT change existing `audioUrl`, `passageAudioUrl`, or `mediaUrl` values unless you are also replacing the media files.

---

## Progress Tracker

Mark tests as you complete them:

- [x] **Test 1** — Completed
  - [x] Part 1: Listening to Problem Solving (8 questions)
  - [x] Part 2: Listening to a Daily Life Conversation (5 questions)
  - [x] Part 3: Listening for Information (6 questions)
  - [x] Part 4: Listening to a News Item (5 questions)
  - [x] Part 5: Listening to a Discussion (8 questions)
  - [x] Part 6: Listening for Viewpoints (6 questions)

- [ ] **Test 2**
  - [ ] Part 1–6

- [ ] **Test 3**
  - [ ] Part 1–6

- [ ] **Test 4**
  - [ ] Part 1–6

- [ ] **Test 5**
  - [ ] Part 1–6

---

## Related Documentation

| Document | Description |
|----------|-------------|
| `pdftotext/README_OCR.md` | OCR conversion scripts for Reading tests |
| `docs/ADDING_TESTS.md` | Adding Reading test content |
| `docs/listening-module-prompt.md` | Listening module engineering spec & UI details |
| `docs/ARCHITECTURE.md` | Overall project architecture |
| `data/README.md` | Data format reference |
