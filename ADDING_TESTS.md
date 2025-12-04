# Adding Test Content Guide

## 📋 Tests 2-5 Templates Created

Template files have been created for Tests 2-5. Now you need to fill in the actual content from your PDFs.

## 📁 Structure

```
data/
├── test_2/
│   └── reading/
│       ├── part1.json  ← Fill in content
│       ├── part2.json  ← Fill in content
│       ├── part3.json  ← Fill in content
│       └── part4.json  ← Fill in content
├── test_3/
├── test_4/
└── test_5/
```

## ✏️ How to Fill In Content

### Step 1: Open a JSON file

```bash
# Example: Edit Test 2, Part 1
code data/test_2/reading/part1.json
# or
nano data/test_2/reading/part1.json
```

### Step 2: Find TODO markers

Look for lines starting with `"TODO:"`:

```json
{
  "content": "TODO: Add the reading passage here."
}
```

### Step 3: Replace with actual content

From your PDF, copy the passage and replace the TODO:

```json
{
  "content": "Dear John,\n\nThank you for your letter..."
}
```

### Step 4: Update questions

Replace placeholder question text:

**Before:**
```json
{
  "id": 1,
  "text": "Question 1 text here",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "answer": 0
}
```

**After:**
```json
{
  "id": 1,
  "text": "The writer is",
  "options": [
    "thanking someone for a gift.",
    "apologizing for being late.",
    "asking for advice.",
    "declining an invitation."
  ],
  "answer": 0
}
```

### Step 5: Update correct answers

Change the `"answer"` field to the correct option index (0-3):
- 0 = first option
- 1 = second option
- 2 = third option
- 3 = fourth option

## 📝 Part-Specific Instructions

### Part 1: Reading Correspondence

**Fill in:**
1. Main passage (letter/email)
2. Questions 1-6 text and options
3. Response passage with __DROPDOWN_X__ placeholders
4. Questions 7-11 options

**Example placeholder usage:**
```json
"content": "Dear Friend,\n\nI would love to __DROPDOWN_7__. I think we should __DROPDOWN_8__..."
```

### Part 2: Reading to Apply a Diagram

**Fill in:**
1. Email subject, to, from fields
2. Email content with __DROPDOWN_1__ through __DROPDOWN_5__
3. Questions 1-5 options (embedded in email)
4. Questions 6-8 text and options

**Add diagram image:**
```bash
# Copy diagram image
cp /path/to/diagram.png static/images/test_2/reading/part2_diagram.png
```

### Part 3: Reading for Information

**Fill in:**
1. Paragraph A content
2. Paragraph B content
3. Paragraph C content
4. Paragraph D content
5. All 9 statement questions

**Note:** Answers are 0-4 where:
- 0 = Paragraph A
- 1 = Paragraph B
- 2 = Paragraph C
- 3 = Paragraph D
- 4 = Not given (E)

### Part 4: Reading for Viewpoints

**Fill in:**
1. Article passage
2. Questions 1-5 text and options
3. Comment passage with __DROPDOWN_6__ through __DROPDOWN_10__
4. Questions 6-10 options

## 🔍 Quick Check Script

After filling in content, verify your JSON is valid:

```bash
# Check a specific file
python -m json.tool data/test_2/reading/part1.json

# Check all Test 2 files
for file in data/test_2/reading/*.json; do
    echo "Checking $file..."
    python -m json.tool "$file" > /dev/null && echo "✓ Valid" || echo "✗ Invalid"
done
```

## 📊 Progress Tracker

Mark tests as you complete them:

- [ ] **Test 2**
  - [ ] Part 1: Reading Correspondence
  - [ ] Part 2: Reading to Apply a Diagram
  - [ ] Part 3: Reading for Information
  - [ ] Part 4: Reading for Viewpoints
  
- [ ] **Test 3**
  - [ ] Part 1: Reading Correspondence
  - [ ] Part 2: Reading to Apply a Diagram
  - [ ] Part 3: Reading for Information
  - [ ] Part 4: Reading for Viewpoints
  
- [ ] **Test 4**
  - [ ] Part 1: Reading Correspondence
  - [ ] Part 2: Reading to Apply a Diagram
  - [ ] Part 3: Reading for Information
  - [ ] Part 4: Reading for Viewpoints
  
- [ ] **Test 5**
  - [ ] Part 1: Reading Correspondence
  - [ ] Part 2: Reading to Apply a Diagram
  - [ ] Part 3: Reading for Information
  - [ ] Part 4: Reading for Viewpoints

## 🎯 Tips

### For Text Content

1. **Line breaks**: Use `\n` for new lines
   ```json
   "content": "First paragraph.\n\nSecond paragraph."
   ```

2. **Quotes**: Escape quotes with backslash
   ```json
   "text": "She said, \"Hello\""
   ```

3. **Special characters**: Generally work fine in JSON
   ```json
   "text": "Cost: $50 (50% off!)"
   ```

### For Dropdowns

1. **Part 1 & 4 Response**: Use `__DROPDOWN_X__` where X is question ID
2. **Part 2 Email**: Use `__DROPDOWN_1__` through `__DROPDOWN_5__`
3. **Spacing**: Add spaces around dropdown for readability
   ```json
   "content": "I think __DROPDOWN_7__ is the best option."
   ```

### For Questions

1. **Keep it concise**: Question text should be brief
2. **Options**: Exactly 4 options for most, 5 for Part 3 (A-E)
3. **Answer index**: Double-check! 0 = first option
4. **Consistent format**: Follow Test 1 examples

## 🚀 After Filling In

1. **Validate JSON**:
   ```bash
   python -m json.tool data/test_2/reading/part1.json
   ```

2. **Test in browser**:
   ```bash
   python app.py
   # Visit http://localhost:5000
   ```

3. **Commit changes**:
   ```bash
   git add data/test_2/
   git commit -m "Add: Test 2 Reading content"
   git push
   ```

## 🆘 Common Issues

### JSON Syntax Error

**Problem:** Missing comma or bracket

**Solution:** Use a JSON validator or editor with syntax highlighting
```bash
python -m json.tool file.json
```

### Dropdown Not Showing

**Problem:** Wrong placeholder format

**Solution:** Use `__DROPDOWN_X__` (double underscore, all caps)

### Wrong Answer

**Problem:** Answer index is off by one

**Solution:** Remember: 0 = first option, not 1

## 📞 Need Help?

- Check `data/test_1/reading/` for examples
- See `data/README.md` for data format details
- Run validation scripts to check JSON

## 🎉 When Complete

Once you've filled in all content:

1. All JSON files have real content (no TODO)
2. All answer indices are correct
3. All diagram images are added
4. Tests work in browser
5. Committed and pushed to GitHub

Then you'll have 5 complete Reading tests with 20 parts total! 🎊

