#!/usr/bin/env python3
"""
Migration script: reports/ → users/ folder structure
Converts old single-file structure to new folder-per-user structure
"""
import json
import os
import re
from pathlib import Path


def sanitize_email(email):
    """Convert email to folder name (remove domain extension)"""
    email = email.lower().strip()
    safe_name = email.replace('@', '_')
    safe_name = re.sub(r'\.(com|net|org|edu|gov|io|co|uk|ca|au)$', '', safe_name)
    safe_name = re.sub(r'[^\w\-]', '_', safe_name)
    return safe_name


def migrate_user_data(reports_dir='reports', users_dir='users'):
    """Migrate all user data from reports/ to users/"""
    
    if not os.path.exists(reports_dir):
        print(f"⚠️  No {reports_dir}/ directory found - nothing to migrate")
        return
    
    # Create users directory
    os.makedirs(users_dir, exist_ok=True)
    
    # Find all JSON files in reports/
    json_files = list(Path(reports_dir).glob('*.json'))
    
    if not json_files:
        print("✅ No user data files to migrate")
        return
    
    print(f"📦 Found {len(json_files)} user(s) to migrate\n")
    
    migrated = 0
    for json_file in json_files:
        try:
            # Load old data
            with open(json_file, 'r') as f:
                old_data = json.load(f)
            
            email = old_data.get('email')
            if not email:
                print(f"⚠️  Skipping {json_file.name} - no email found")
                continue
            
            # Create user folder
            folder_name = sanitize_email(email)
            user_folder = os.path.join(users_dir, folder_name)
            os.makedirs(user_folder, exist_ok=True)
            
            # Create profile.json
            profile = {
                'email': email,
                'role': 'Basic',
                'created_at': old_data.get('created_at', ''),
                'last_accessed': old_data.get('last_accessed', '')
            }
            
            profile_path = os.path.join(user_folder, 'profile.json')
            with open(profile_path, 'w') as f:
                json.dump(profile, f, indent=2, ensure_ascii=False)
            
            # Create test_history.json
            test_history = {
                'tests': old_data.get('tests', {})
            }
            
            history_path = os.path.join(user_folder, 'test_history.json')
            with open(history_path, 'w') as f:
                json.dump(test_history, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Migrated: {email} → users/{folder_name}/")
            migrated += 1
            
        except Exception as e:
            print(f"❌ Error migrating {json_file.name}: {e}")
    
    print(f"\n🎉 Migration complete! {migrated}/{len(json_files)} users migrated")
    print(f"\n📁 New structure:")
    print(f"   users/")
    for folder in sorted(os.listdir(users_dir)):
        folder_path = os.path.join(users_dir, folder)
        if os.path.isdir(folder_path) and folder != '.gitkeep':
            print(f"     {folder}/")
            print(f"       ├── profile.json")
            print(f"       └── test_history.json")


if __name__ == '__main__':
    print("=" * 60)
    print("  CELPIP User Data Migration")
    print("  reports/ → users/ folder structure")
    print("=" * 60)
    print()
    
    migrate_user_data()
    
    print()
    print("=" * 60)
    print("✨ You can now safely delete the reports/ folder if desired")
    print("=" * 60)

