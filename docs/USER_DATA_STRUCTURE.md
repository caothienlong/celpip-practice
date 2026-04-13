# User Data Structure

## Overview

User data is stored in **PostgreSQL** when `DATABASE_URL` is configured (production on Render), and falls back transparently to a **folder-per-user JSON structure** for local development.

The application never hard-codes which backend to use — it is selected at startup by `utils/storage/factory.py` via the repository pattern.

## Storage Backends

| Environment | Backend | Location |
|-------------|---------|----------|
| Production (Render) | PostgreSQL | `users`, `test_history`, `vocabulary_notes` tables |
| Local development | JSON files | `users/{sanitized_email}/*.json` |

## PostgreSQL Schema

```sql
users (
    email          TEXT PRIMARY KEY,
    name           TEXT,
    provider       TEXT,       -- 'google' or 'facebook'
    picture        TEXT,
    role           TEXT DEFAULT 'Basic',
    created_at     TIMESTAMPTZ,
    last_accessed  TIMESTAMPTZ
)

test_history (
    id          SERIAL PRIMARY KEY,
    user_email  TEXT REFERENCES users(email) ON DELETE CASCADE,
    test_num    INTEGER,
    data        JSONB,         -- full attempt history
    updated_at  TIMESTAMPTZ,
    UNIQUE(user_email, test_num)
)

vocabulary_notes (
    note_id     TEXT PRIMARY KEY,
    user_email  TEXT REFERENCES users(email) ON DELETE CASCADE,
    test_num    INTEGER,
    skill       TEXT,
    part_num    INTEGER,
    word        TEXT,
    definition  TEXT,
    context     TEXT,
    created_at  TIMESTAMPTZ,
    updated_at  TIMESTAMPTZ
)
```

Tables are **auto-created** on first startup — no manual migrations needed.

## File-Based Fallback Directory Structure

```
users/
  john_doe_gmail/               # Sanitized email (domain extension removed)
    ├── profile.json            # User profile & metadata
    ├── test_history.json       # Test attempts & scores
    └── vocabulary_notes.json   # Vocabulary notes
  another_user/
    ├── profile.json
    ├── test_history.json
    └── vocabulary_notes.json
```

## File Formats

### profile.json
```json
{
  "email": "john.doe@gmail.com",
  "role": "Basic",
  "created_at": "2025-12-07T16:29:55.909360",
  "last_accessed": "2025-12-07T23:12:00.000000"
}
```

**Fields:**
- `email`: User's email address (unique identifier)
- `role`: User role (currently all "Basic", future: Premium, Admin)
- `created_at`: When user first used the system
- `last_accessed`: Last activity timestamp

### test_history.json
```json
{
  "tests": {
    "test_1": {
      "test_number": 1,
      "attempts": [
        {
          "attempt_id": "uuid-here",
          "started_at": "2025-12-07T16:30:15.291996",
          "completed_at": "2025-12-07T16:31:03.959520",
          "skills": {
            "reading": {
              "skill_name": "reading",
              "parts": {
                "1": {
                  "part_number": 1,
                  "answers": {"1": 0, "2": 1, ...},
                  "correct_answers": {"1": 1, "2": 2, ...},
                  "score": 5,
                  "max_score": 11,
                  "timestamp": "2025-12-07T16:30:15.292013"
                }
              },
              "total_score": 25,
              "total_max": 38
            }
          },
          "total_score": 25,
          "total_max": 38,
          "percentage": 65.8
        }
      ]
    }
  }
}
```

## Username Sanitization

Email addresses are converted to safe folder names:

| Email | Folder Name |
|-------|-------------|
| `john.doe@gmail.com` | `john_doe_gmail` |
| `user@yahoo.com` | `user_yahoo` |
| `test.user@example.org` | `test_user_example` |

**Rules:**
- Replace `@` with `_`
- Remove domain extensions (`.com`, `.net`, `.org`, etc.)
- Remove special characters
- Convert to lowercase

## Session-Only Mode

**When no email is provided:**
- ✅ Practice Mode works (session storage only)
- ✅ Test Mode works (session storage only)
- ❌ No persistent storage
- ❌ Data lost when session expires
- ❌ No history across sessions

**Use case:** Quick practice without account

## Privacy & Security

**Gitignore:**
```gitignore
# User data excluded from git
users/
!users/.gitkeep
```

**Benefits:**
- User data never committed to repository
- Each user isolated in own folder
- Easy to backup individual users
- GDPR-compliant deletion (just delete folder)

## Future Enhancements

### Roles & Permissions
```json
{
  "role": "Premium",
  "subscription": {
    "plan": "Monthly",
    "started_at": "2025-01-01",
    "expires_at": "2025-02-01"
  }
}
```

### User Preferences
```json
{
  "preferences": {
    "theme": "dark",
    "notifications": true,
    "timer_warnings": true
  }
}
```

### Statistics
```json
{
  "statistics": {
    "total_attempts": 15,
    "average_score": 82.5,
    "best_score": 95.0,
    "total_time_spent": 3600
  }
}
```

## Migration

### From Old Structure (reports/)

Run the migration script:
```bash
python migrate_user_data.py
```

This converts:
```
reports/
  john_doe_gmail.com.json
```

To:
```
users/
  john_doe_gmail/
    ├── profile.json
    └── test_history.json
```

## Migrating from File Storage to PostgreSQL

If you have existing users stored in `users/` JSON files and want to move them to PostgreSQL:

```bash
# Ensure DATABASE_URL is set in your .env
python migrate_user_data.py
```

This reads all `users/*/profile.json`, `test_history.json`, and `vocabulary_notes.json` files and upserts them into PostgreSQL.  The original files are left intact as a backup.

## API Usage

`ResultsTracker` is the single entry point for all user data operations.  
Storage backend is chosen automatically — no changes to call sites.

```python
import os
from utils.results_tracker import ResultsTracker

tracker = ResultsTracker(
    users_dir='users',
    database_url=os.getenv('DATABASE_URL'),  # None → file fallback
)

# --- User profile ---
profile = tracker.get_or_create_user('user@example.com')
profile = tracker.get_user_profile('user@example.com')
tracker.save_user_profile('user@example.com', profile)
tracker.update_user_role('user@example.com', 'Premium')
users   = tracker.list_all_users()

# --- Test history ---
tracker.save_test_result(user_email, test_num, skill, part_num,
                         answers, correct_answers, score, max_score, attempt_id)
tracker.complete_test_attempt(user_email, test_num, attempt_id)
history = tracker.get_user_test_history(user_email, test_num)
summary = tracker.get_all_tests_summary(user_email)

# --- Vocabulary notes ---
note_id = tracker.save_vocabulary_note(user_email, test_num, skill, part_num,
                                        word, definition, context)
notes   = tracker.get_vocabulary_notes(user_email, test_num=1, skill='reading')
tracker.update_vocabulary_note(user_email, note_id, definition='new definition')
tracker.delete_vocabulary_note(user_email, note_id)
```

### Direct repository access (advanced)

```python
from utils.storage import make_repositories

user_repo, test_repo, vocab_repo = make_repositories(
    users_dir='users',
    database_url=os.getenv('DATABASE_URL'),
)
```

## Backup Strategy

### Manual Backup
```bash
# Backup all users
tar -czf users_backup_$(date +%Y%m%d).tar.gz users/

# Backup single user
tar -czf user_backup_$(date +%Y%m%d).tar.gz users/username/
```

### Restore
```bash
tar -xzf users_backup_20251207.tar.gz
```

### Automated (Future)
- Daily backups to cloud storage
- Incremental backups
- Point-in-time recovery

## Maintenance

### Delete User Data
```bash
# Delete user folder (GDPR compliance)
rm -rf users/username/
```

### List All Users
```python
users = tracker.list_all_users()
print(users)  # ['user1@example.com', 'user2@example.com']
```

### Cleanup Old Data
```python
# Delete attempts older than X days
# TBD: Add cleanup utility
```

---

**Last Updated:** March 16, 2026  
**Version:** 2.0 (PostgreSQL + repository pattern)

