# 🔄 Migration Guide: Results Storage Refactoring

## Overview

The CELPIP Practice Platform has been refactored to use a more scalable storage system for user test results.

### Old Structure (v1)
```
data/
  └── test_results.json   ← All users in one file
```

### New Structure (v2)
```
reports/
  ├── user_example_com.json      ← One file per user
  ├── john_doe_email_com.json
  └── sarah_chen_email_com.json
```

---

## Why This Change?

### Problems with Single File:
- ❌ Gets large with many users
- ❌ Slower read/write operations
- ❌ All data loads even for one user
- ❌ Risk of data corruption
- ❌ Difficult to manage individual users

### Benefits of Per-User Files:
- ✅ **Scalable**: Handle thousands of users
- ✅ **Fast**: Only load needed user data
- ✅ **Isolated**: Each user's data separate
- ✅ **Manageable**: Easy to backup/delete users
- ✅ **Privacy**: Better data isolation
- ✅ **Organized**: Clear folder structure

---

## Migration Steps

### Automatic Migration (Recommended)

Run the migration script:

```bash
# From project root
python scripts/migrate_results.py
```

The script will:
1. Read old `data/test_results.json`
2. Create `reports/` directory
3. Split data into per-user files
4. Backup the old file
5. Verify migration success

**Example Output:**
```
============================================================
🔄 CELPIP Results Migration Tool
   Single file → Per-user files
============================================================

Source: data/test_results.json
Target: reports/

Continue with migration? (yes/no): yes

📂 Loading old results from: data/test_results.json
👥 Found 3 user(s) to migrate
📁 Created reports directory: reports
   ✅ Migrated: user@example.com → reports/user_example_com.json
   ✅ Migrated: john.doe@email.com → reports/john_doe_email_com.json
   ✅ Migrated: sarah.chen@email.com → reports/sarah_chen_email_com.json

============================================================
📊 Migration Summary:
   ✅ Successfully migrated: 3 user(s)
============================================================

💾 Backed up old file to: data/test_results.json.backup
   You can safely delete it after verifying the migration.

🔍 Verifying migration...
   ✅ Verified: user@example.com
   ✅ Verified: john.doe@email.com
   ✅ Verified: sarah.chen@email.com

✅ Migration completed successfully!

📁 Your user reports are now in: reports/
   Each user has their own file: user@example_com.json
```

---

## Manual Migration (If Needed)

If the automatic script doesn't work:

### 1. Create Reports Directory
```bash
mkdir reports
```

### 2. Extract User Data

For each user in `data/test_results.json`:

```json
{
  "users": {
    "user@example.com": {
      "email": "user@example.com",
      "tests": {...}
    }
  }
}
```

Create `reports/user_example_com.json`:
```json
{
  "email": "user@example.com",
  "created_at": "2025-12-04T10:00:00",
  "last_accessed": "2025-12-04T15:30:00",
  "tests": {...}
}
```

### 3. Email to Filename Conversion

Replace special characters:
- `@` → `_`
- `.` → `_`
- Other special chars → `_`
- Convert to lowercase

**Examples:**
```
user@example.com      → user_example_com.json
John.Doe@Email.COM    → john_doe_email_com.json
sarah+test@site.co.uk → sarah_test_site_co_uk.json
```

---

## Verification

After migration, verify:

### 1. Check Reports Directory
```bash
ls -la reports/
```

You should see `.json` files for each user.

### 2. Check File Content
```bash
cat reports/user_example_com.json
```

Verify:
- Email is correct
- Tests data is present
- Created/accessed timestamps exist

### 3. Test the Application
```bash
python app.py
```

- Log in with a migrated user's email
- Check test history displays correctly
- Take a new test
- Verify scores are saved

---

## File Format Reference

### Per-User File Structure

```json
{
  "email": "user@example.com",
  "created_at": "2025-12-04T10:00:00.000000",
  "last_accessed": "2025-12-04T15:30:00.000000",
  "tests": {
    "test_1": {
      "test_number": 1,
      "attempts": [
        {
          "attempt_id": "uuid-1234-5678",
          "started_at": "2025-12-04T10:30:00",
          "completed_at": "2025-12-04T11:45:00",
          "total_score": 37,
          "total_max": 38,
          "percentage": 97.4,
          "skills": {
            "reading": {
              "skill_name": "reading",
              "total_score": 37,
              "total_max": 38,
              "parts": {
                "1": {
                  "part_number": 1,
                  "score": 10,
                  "max_score": 11,
                  "answers": {
                    "1": 2,
                    "2": 0
                  },
                  "correct_answers": {
                    "1": 2,
                    "2": 1
                  },
                  "timestamp": "2025-12-04T10:35:00"
                }
              }
            }
          }
        }
      ]
    }
  }
}
```

---

## Backward Compatibility

The new system is **NOT backward compatible** with the old single-file format.

### If You Need to Rollback:

1. **Restore backup:**
   ```bash
   cp data/test_results.json.backup data/test_results.json
   ```

2. **Update `app.py`:**
   ```python
   # Change this line:
   results_tracker = ResultsTracker(reports_dir='reports')
   
   # Back to:
   results_tracker = ResultsTracker(results_file='data/test_results.json')
   ```

3. **Use old `results_tracker.py`:**
   ```bash
   git checkout HEAD~1 utils/results_tracker.py
   ```

---

## Troubleshooting

### Issue 1: Migration Script Not Found

**Error:** `python: can't open file 'scripts/migrate_results.py'`

**Solution:**
```bash
# Make sure you're in project root
cd /path/to/celpip
python scripts/migrate_results.py
```

### Issue 2: Permission Denied

**Error:** `Permission denied: reports/`

**Solution:**
```bash
# Create directory with proper permissions
mkdir -p reports
chmod 755 reports
```

### Issue 3: Invalid JSON in Old File

**Error:** `JSONDecodeError: Expecting value`

**Solution:**
1. Check if `data/test_results.json` is valid JSON
2. Restore from backup if corrupted
3. Start fresh if no backup exists

### Issue 4: Missing Users After Migration

**Problem:** Some users don't show up

**Check:**
```bash
# Count users in old file
grep -o '"email"' data/test_results.json | wc -l

# Count files in new directory
ls -1 reports/*.json | wc -l
```

Should match!

### Issue 5: File Naming Conflicts

**Problem:** Multiple emails map to same filename

**Example:**
- `user@example.com`
- `user.example@com`

Both become: `user_example_com.json`

**Solution:** Manual rename required:
```bash
mv reports/user_example_com.json reports/user_example_com_1.json
```

Then update the email in the file.

---

## FAQ

**Q: Will I lose my test history?**  
A: No! Migration preserves all data. Backup is created automatically.

**Q: Can I run both systems simultaneously?**  
A: No, choose one. New system is recommended.

**Q: What if migration fails halfway?**  
A: Old file remains intact. Delete `reports/` and try again.

**Q: Can I manually edit per-user files?**  
A: Yes, they're just JSON files. Be careful with format.

**Q: How do I delete a user?**  
A: Simply delete their file: `rm reports/user_example_com.json`

**Q: Can I export a user's data?**  
A: Yes, just copy their file: `cp reports/user_example_com.json backup/`

**Q: Is the old file needed after migration?**  
A: No, but keep the backup until you verify everything works.

---

## Best Practices

### After Migration:

1. **Test thoroughly** - Verify all features work
2. **Keep backup** - Don't delete old file immediately
3. **Monitor performance** - Should be faster now
4. **Regular backups** - Backup `reports/` directory

### For Production:

1. **Schedule migration** during low usage
2. **Notify users** of potential downtime
3. **Test on staging** environment first
4. **Have rollback plan** ready

### For Development:

1. **Use version control** - Commit before migration
2. **Test script** with sample data first
3. **Document** any custom changes

---

## Summary

| Aspect | Old System | New System |
|--------|-----------|------------|
| Storage | Single file | Per-user files |
| Location | `data/test_results.json` | `reports/*.json` |
| Scalability | Limited | Unlimited |
| Performance | Slower with many users | Fast |
| User Management | Difficult | Easy |
| Privacy | All users together | Isolated |
| Backup | All or nothing | Per user |

---

**Migration Complete?** 🎉

You're now using the new, more scalable results storage system!

---

*Last Updated: December 2025*

