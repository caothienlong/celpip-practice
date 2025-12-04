# Refactoring: Dynamic Timeout Calculation

## ✅ Changes Made

### Removed Hardcoded Timeouts
**Date:** December 4, 2024

**Issue:** The `timeout_minutes` field was hardcoded in every test part JSON file, violating DRY (Don't Repeat Yourself) principle.

**Solution:** Removed `timeout_minutes` from all JSON files. Timeout is now calculated dynamically based on:
- Number of questions in the test
- `time_per_question` setting from `config.json`

### Files Updated

**JSON Files (removed `timeout_minutes` field):**
- ✅ `data/test_1/reading/part1.json`
- ✅ `data/test_1/reading/part2.json`
- ✅ `data/test_1/reading/part3.json`
- ✅ `data/test_1/reading/part4.json`
- ✅ `data/test_2/reading/part2.json`
- ✅ `data/test_2/reading/part3.json`
- ✅ `data/test_2/reading/part4.json`

**Documentation:**
- ✅ `data/README.md` - Added note about dynamic timeout calculation

### How It Works Now

**Before:**
```json
{
  "part": 1,
  "title": "Reading Correspondence",
  "timeout_minutes": 16.5,
  "sections": [...]
}
```

**After:**
```json
{
  "part": 1,
  "title": "Reading Correspondence",
  "sections": [...]
}
```

**Calculation:**
- Function: `calculate_timeout(num_questions, skill)` in `config.py`
- Formula: `num_questions × time_per_question`
- Example: 11 questions × 1.5 min/question = 16.5 minutes

### Benefits

1. **Single Source of Truth:** Change `time_per_question` in `config.json` once, affects all tests
2. **Less Redundancy:** No need to manually calculate and add timeout to every JSON file
3. **Easier Maintenance:** Adding new tests requires less manual work
4. **Consistency:** All tests use the same calculation logic
5. **Flexibility:** Can override per test if needed using `custom_timeouts` in `config.json`

### Configuration

Change the time per question in `config.json`:

```json
{
  "time_per_question": {
    "reading": 1.5,
    "writing": 30.0,
    "speaking": 1.5,
    "listening": 1.5
  }
}
```

For custom overrides (optional):

```json
{
  "custom_timeouts": {
    "1_reading_1": 20.0  // Override Test 1, Reading, Part 1 to 20 minutes
  }
}
```

### Testing

Verified that timeout calculation works correctly:
- Test 1, Part 1: 11 questions → 16.5 minutes ✅
- Test 1, Part 2: 8 questions → 12.0 minutes ✅
- Test 1, Part 3: 9 questions → 13.5 minutes ✅
- Test 1, Part 4: 10 questions → 15.0 minutes ✅

Same calculation applies to Test 2 automatically.

---

**Result:** Cleaner, more maintainable codebase with dynamic configuration! 🎉

