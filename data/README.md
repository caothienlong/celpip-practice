# CELPIP Test Data Structure

This folder contains all test data in JSON format, separated from the application code for easy maintenance and reusability across platforms (Web, iOS, Android).

## Folder Structure

```
data/
├── set_1/
│   ├── reading/
│   │   ├── part1.json
│   │   ├── part2.json
│   │   ├── part3.json
│   │   └── part4.json
│   ├── writing/
│   │   ├── part1.json
│   │   └── part2.json
│   ├── speaking/
│   │   ├── part1.json
│   │   ├── ...
│   │   └── part8.json
│   └── listening/
│       ├── part1.json
│       ├── ...
│       └── part6.json
├── set_2/
│   └── ... (same structure)
├── ...
└── set_20/
    └── ... (same structure)
```

## JSON Data Format

Each test part is a self-contained JSON file with the following structure:

### Reading Parts

```json
{
  "part": 1,
  "title": "Reading Correspondence",
  "type": "correspondence|diagram|information|viewpoints",
  "instructions": "Instructions text",
  "timeout_minutes": 16.5,
  "sections": [
    {
      "section_type": "passage|questions|response_passage|diagram_email",
      "title": "Section title (optional)",
      "instruction_text": "Section instructions (optional)",
      "content": "Text content with __DROPDOWN_X__ placeholders",
      "diagram_image": "filename.png (for diagram sections)",
      "question_format": "dropdown|radio|text",
      "questions": [
        {
          "id": 1,
          "text": "Question text",
          "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
          "answer": 0
        }
      ]
    }
  ]
}
```

### Key Fields

- **part**: Part number (1-4 for reading, varies by skill)
- **title**: Display title for the part
- **type**: Type of test (correspondence, diagram, information, viewpoints)
- **instructions**: Overall instructions for the part
- **timeout_minutes**: Time limit (calculated as questions × 1.5 minutes)
- **sections**: Array of content sections

### Section Types

1. **passage**: Reading passage only (no questions)
2. **questions**: Standalone questions with dropdowns
3. **response_passage**: Text with embedded dropdown placeholders
4. **diagram_email**: Email with diagram image and embedded dropdowns

### Dropdown Placeholders

Use `__DROPDOWN_X__` format where X is the question ID:
- `__DROPDOWN_1__`
- `__DROPDOWN_2__`
- etc.

### Answer Format

Answers are 0-indexed integers corresponding to the option position:
- `0` = first option
- `1` = second option
- `2` = third option
- `3` = fourth option

## Adding New Test Sets

1. Create a new folder: `set_X/` (where X is 1-20)
2. Create skill subfolders: `reading/`, `writing/`, `speaking/`, `listening/`
3. Add JSON files for each part following the format above
4. Add any image assets to `static/images/set_X/`

## Platform Compatibility

This JSON structure is designed to be platform-agnostic:
- **Web App**: Flask/Python reads JSON and renders HTML
- **iOS App**: Swift/SwiftUI can parse JSON and render native UI
- **Android App**: Kotlin/Java can parse JSON and render native UI

All platforms can share the same test data without modification.

## Image Assets

Store images in: `static/images/set_X/skill/partY_diagram.png`

Example:
- `static/images/set_1/reading/part2_diagram.png`
- `static/images/set_2/listening/part3_audio.mp3`

## Future Skills

### Writing (2 parts)
- Part 1: Email writing
- Part 2: Survey response

### Speaking (8 parts)
- Parts 1-8: Various speaking tasks

### Listening (6 parts)
- Parts 1-6: Audio comprehension tasks
- Include audio file references in JSON

## Validation

Each JSON file should be valid and include:
- ✅ All required fields
- ✅ Correct answer indices (0-based)
- ✅ Matching dropdown placeholders and question IDs
- ✅ Valid timeout calculations

Run validation: `python validate_data.py` (to be implemented)

