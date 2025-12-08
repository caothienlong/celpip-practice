# 📚 Vocabulary Notes Feature

**Version**: 1.0  
**Added**: December 8, 2025  
**Status**: Complete ✅

---

## Overview

The Vocabulary Notes feature allows authenticated users to save and manage vocabulary words and phrases they encounter while practicing CELPIP tests. Notes are organized by test, skill, and part for easy review.

---

## Features

### ✅ Note-Taking
- Save word/phrase with custom definition
- Add optional context from passage
- Timestamped creation and updates
- Per-user storage (isolated and secure)

### ✅ Organization
- Grouped by test number
- Organized by skill (reading, writing, listening, speaking)
- Separated by part within each skill
- Easy filtering and searching

### ✅ Management
- View all notes for a test
- Edit existing notes
- Delete unwanted notes
- Export-ready structure (JSON)

### ✅ Integration
- Floating button on all test pages
- Quick popup modal for fast entry
- Recent notes preview (last 5)
- Full notes viewing page

---

## User Guide

### How to Add a Note

1. **While Taking a Test**:
   - Read the passage
   - Encounter an unknown word (e.g., "gregarious")

2. **Click the Vocabulary Button**:
   - Look for the golden `📚 Add Vocabulary Note` button (bottom-left)
   - Click to open the note entry modal

3. **Fill in the Form**:
   - **Word/Phrase** (required): e.g., "gregarious"
   - **Definition** (required): e.g., "sociable, enjoys being with others"
   - **Context** (optional): e.g., "Greg is very gregarious and loves hosting parties"

4. **Save**:
   - Click `💾 Save Note`
   - Confirmation message appears
   - Note added to your vocabulary

### How to View Notes

**During Practice**:
- Recent notes popup shows last 5 notes for current part
- Click `View All Vocabulary →` for full list

**From Test Overview**:
- Click `📚 Vocabulary Notes` button (top action bar)
- See all notes grouped by part
- Edit or delete as needed

### How to Edit/Delete Notes

1. Go to `/test/<number>/vocabulary` page
2. Find the note you want to modify
3. Click `✏️ Edit` to update
4. Click `🗑️ Delete` to remove

---

## Technical Details

### Data Structure

**Location**: `users/{username}/vocabulary_notes.json`

```json
{
  "tests": {
    "test_1": {
      "reading_part_1": [
        {
          "note_id": "1_reading_1_20251208123456789012",
          "word": "gregarious",
          "definition": "sociable, enjoys company",
          "context": "Greg is very gregarious...",
          "created_at": "2025-12-08T12:34:56.789012",
          "test_num": 1,
          "skill": "reading",
          "part_num": 1
        }
      ],
      "reading_part_2": [...]
    },
    "test_2": {...}
  }
}
```

### API Endpoints

#### Save Note
```http
POST /save_vocabulary_note
Content-Type: application/json
Authentication: Required

{
  "test_num": 1,
  "skill": "reading",
  "part_num": 1,
  "word": "gregarious",
  "definition": "sociable",
  "context": "optional context"
}

Response:
{
  "success": true,
  "note_id": "1_reading_1_20251208...",
  "message": "Vocabulary note saved!"
}
```

#### Get Notes
```http
GET /get_vocabulary_notes?test_num=1&skill=reading&part_num=1
Authentication: Required

Response:
{
  "success": true,
  "notes": [...],
  "count": 5
}
```

#### Delete Note
```http
POST /delete_vocabulary_note
Content-Type: application/json
Authentication: Required

{
  "note_id": "1_reading_1_20251208..."
}

Response:
{
  "success": true,
  "message": "Note deleted successfully"
}
```

#### Update Note
```http
POST /update_vocabulary_note
Content-Type: application/json
Authentication: Required

{
  "note_id": "1_reading_1_20251208...",
  "word": "new word",
  "definition": "new definition",
  "context": "new context"
}

Response:
{
  "success": true,
  "message": "Note updated successfully"
}
```

### Backend Methods

**File**: `utils/results_tracker.py`

```python
# Save a note
note_id = results_tracker.save_vocabulary_note(
    user_email="user@example.com",
    test_num=1,
    skill="reading",
    part_num=1,
    word="gregarious",
    definition="sociable",
    context="optional"
)

# Get notes with filters
notes = results_tracker.get_vocabulary_notes(
    user_email="user@example.com",
    test_num=1,           # Optional
    skill="reading",      # Optional
    part_num=1           # Optional
)

# Delete a note
deleted = results_tracker.delete_vocabulary_note(
    user_email="user@example.com",
    note_id="1_reading_1_..."
)

# Update a note
updated = results_tracker.update_vocabulary_note(
    user_email="user@example.com",
    note_id="1_reading_1_...",
    word="new word",
    definition="new definition",
    context="new context"
)
```

---

## UI Components

### Floating Button

**Location**: Bottom-left corner (fixed position)  
**Appearance**: Golden yellow (#ffc107)  
**Text**: `📚 Add Vocabulary Note`  
**Visibility**: Authenticated users only

**CSS**:
```css
.vocab-note-btn {
    position: fixed;
    bottom: 30px;
    left: 30px;
    background: #ffc107;
    /* ... */
}
```

### Modal Popup

**Trigger**: Click floating button  
**Content**: Form with 3 fields  
**Actions**: Save, Cancel  
**Close**: Click outside, ESC key, X button

**Fields**:
1. Word/Phrase (required, text input)
2. Definition (required, textarea)
3. Context (optional, textarea)

### Recent Notes Popup

**Location**: Above floating button  
**Content**: Last 5 notes for current part  
**Link**: "View All Vocabulary →"  
**Auto-hide**: After leaving page

### Vocabulary Notes Page

**URL**: `/test/<int:test_num>/vocabulary`  
**Layout**: Cards grouped by part  
**Actions**: Edit, Delete per note  
**Empty State**: Friendly message with CTA

---

## Security

### Authentication
- ✅ All API endpoints require authentication
- ✅ Returns 401 if not logged in
- ✅ Guest mode: no vocabulary button shown

### Data Isolation
- ✅ Each user has separate JSON file
- ✅ Cannot access other users' notes
- ✅ Stored in `users/` folder (gitignored)

### Validation
- ✅ Server-side validation of all inputs
- ✅ HTML escaping on display
- ✅ XSS protection built-in

---

## Use Cases

### For Students
**Learning Vocabulary**:
- Save unknown words while practicing
- Add your own translations
- Review before real exam
- Build personal vocabulary list

**Example**:
```
While reading: "The protagonist was quite loquacious"
→ Add note: "loquacious = talkative"
→ Review later: See all vocabulary from Test 1
→ Study before exam: Review all notes
```

### For Teachers
**Track Student Progress**:
- See what words students struggle with
- Identify common vocabulary gaps
- Provide targeted vocabulary lessons

### For Test Takers
**Exam Preparation**:
- Build vocabulary lists from practice tests
- Review difficult words before exam
- Export notes for flashcard apps
- Share with study groups

---

## Best Practices

### When Adding Notes

**✅ Do**:
- Write definitions in your own words
- Include context for better memory
- Be concise but clear
- Add translations if helpful

**❌ Don't**:
- Copy entire sentences as "word"
- Leave definition empty
- Add duplicate notes
- Skip context for tricky usage

### When Reviewing Notes

**Regular Review**:
- Review after each test
- Group by similar meanings
- Test yourself without definitions
- Mark mastered words

**Before Exam**:
- Quick scan of all notes
- Focus on recent additions
- Review difficult words twice
- Practice using in sentences

---

## Performance

### Storage
- Lightweight JSON format
- ~1KB per note average
- 100 notes ≈ 100KB
- Negligible impact

### Speed
- Fast JSON read/write
- Client-side rendering
- No database queries
- Instant UI updates

### Scalability
- Supports thousands of notes per user
- Efficient filtering algorithms
- Pagination ready (if needed)
- Easy migration to database

---

## Future Enhancements

### Planned Features
- [ ] Flashcard mode
- [ ] Export to CSV/Excel
- [ ] Print-friendly format
- [ ] Search/filter by word
- [ ] Audio pronunciation
- [ ] Example sentences
- [ ] Spaced repetition
- [ ] Quiz mode
- [ ] Share with friends
- [ ] Mobile app integration

### Database Migration
When user base grows:
- Migrate from JSON to PostgreSQL
- Add full-text search
- Implement caching
- Add bulk operations

---

## Troubleshooting

### Note Not Saving

**Symptoms**: Alert shows "Failed to save"

**Solutions**:
1. Check if logged in
2. Verify internet connection
3. Check browser console for errors
4. Try refreshing page
5. Clear browser cache

### Notes Not Showing

**Symptoms**: "No notes yet" when you have notes

**Solutions**:
1. Verify correct test/part
2. Check filters applied
3. Refresh the page
4. Check `users/` folder exists
5. Verify JSON file not corrupted

### Modal Won't Open

**Symptoms**: Button click does nothing

**Solutions**:
1. Check JavaScript console
2. Disable browser extensions
3. Try different browser
4. Clear cache and reload
5. Check authentication status

---

## Developer Notes

### Adding Vocabulary UI to New Pages

1. **Add CSS** (in `<style>` tag):
```html
<!-- Copy vocabulary CSS from test_section.html -->
```

2. **Add HTML** (before `</body>`):
```html
<!-- Copy vocabulary HTML from test_section.html -->
```

3. **Update JavaScript**:
```javascript
// Change test_num, skill, part_num as needed
```

### Customizing Appearance

**Change Button Color**:
```css
.vocab-note-btn {
    background: #your-color;
}
```

**Change Button Position**:
```css
.vocab-note-btn {
    bottom: 20px;  /* vertical */
    left: 20px;    /* horizontal */
}
```

**Hide Recent Notes Popup**:
```javascript
// Remove or comment out:
document.getElementById('vocabNotesList').classList.add('active');
```

---

## FAQs

**Q: Do I need to log in to use vocabulary notes?**  
A: Yes, vocabulary notes require authentication. Guest mode doesn't have access.

**Q: Are my notes private?**  
A: Yes, notes are stored per-user and cannot be accessed by others.

**Q: Can I export my notes?**  
A: Currently, notes are stored in JSON format in your user folder. Export feature coming soon.

**Q: How many notes can I save?**  
A: No limit! Save as many as you need.

**Q: Can I add notes in Test Mode?**  
A: Yes, vocabulary notes work in both Practice and Test modes.

**Q: Will notes slow down the app?**  
A: No, notes are lightweight and don't impact performance.

**Q: Can I share notes with friends?**  
A: Not yet, but this feature is planned for a future update.

**Q: What happens if I logout?**  
A: Your notes are saved and will be available when you log in again.

---

## Summary

The Vocabulary Notes feature provides a complete solution for CELPIP test takers to build and manage their vocabulary while practicing. With an intuitive UI, robust backend, and user-focused design, it enhances the learning experience and helps students prepare more effectively for their exams.

**Key Benefits**:
- 📝 Quick note-taking during practice
- 📚 Organized by test/skill/part
- 🔒 Secure and private
- 📱 Works on all devices
- ✨ Beautiful and intuitive UI

---

**Ready to start building your vocabulary? Click that golden button! 📚**

---

**Last Updated**: December 8, 2025  
**Version**: 1.0  
**Status**: Production Ready ✅

