# User Data Structure

## Overview

User data is organized in a **folder-per-user** structure for better organization and scalability.

## Directory Structure

```
users/
  caothienlong_gmail/           # Username (domain extension removed)
    ├── profile.json            # User profile & metadata
    └── test_history.json       # Test attempts & scores
  another_user/
    ├── profile.json
    └── test_history.json
```

## File Formats

### profile.json
```json
{
  "email": "caothienlong@gmail.com",
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
| `caothienlong@gmail.com` | `caothienlong_gmail` |
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
  caothienlong_gmail.com.json
```

To:
```
users/
  caothienlong_gmail/
    ├── profile.json
    └── test_history.json
```

## Database Migration (Future)

When ready for PostgreSQL:

1. **Keep folder structure** for backups
2. **Import to database** via migration script
3. **Sync both ways** (DB primary, files backup)
4. **Easy rollback** if needed

See `docs/DATABASE_MIGRATION.md` for details (when ready).

## API Usage

```python
from utils.results_tracker import ResultsTracker

tracker = ResultsTracker(users_dir='users')

# Get or create user
profile = tracker.get_or_create_user('user@example.com')

# Get test history
history = tracker.get_all_tests_summary('user@example.com')

# Update role
tracker.update_user_role('user@example.com', 'Premium')

# Get profile
profile = tracker.get_user_profile('user@example.com')
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

**Last Updated:** December 7, 2025  
**Version:** 1.0

