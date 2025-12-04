#!/usr/bin/env python3
"""
Migration Script: test_results.json → reports/ folder
Converts old single-file format to new per-user file structure
"""
import json
import os
import sys
import re
from datetime import datetime


def sanitize_email(email: str) -> str:
    """Convert email to safe filename"""
    safe_email = re.sub(r'[^\w\-.]', '_', email.lower())
    return safe_email


def migrate_results(old_file='data/test_results.json', new_dir='reports'):
    """Migrate from single file to per-user files"""
    
    # Check if old file exists
    if not os.path.exists(old_file):
        print(f"❌ Old results file not found: {old_file}")
        print("   Nothing to migrate. Starting fresh!")
        return True
    
    # Load old data
    print(f"📂 Loading old results from: {old_file}")
    try:
        with open(old_file, 'r') as f:
            old_data = json.load(f)
    except Exception as e:
        print(f"❌ Error reading old file: {e}")
        return False
    
    # Check if old format
    if 'users' not in old_data:
        print(f"❌ Invalid format in {old_file}")
        return False
    
    users = old_data.get('users', {})
    if not users:
        print("ℹ️  No users found in old file. Nothing to migrate.")
        return True
    
    print(f"👥 Found {len(users)} user(s) to migrate")
    
    # Create new directory
    os.makedirs(new_dir, exist_ok=True)
    print(f"📁 Created reports directory: {new_dir}")
    
    # Migrate each user
    migrated_count = 0
    failed_count = 0
    
    for email, user_data in users.items():
        try:
            # Create user file
            safe_email = sanitize_email(email)
            user_file = os.path.join(new_dir, f"{safe_email}.json")
            
            # Prepare new format
            new_user_data = {
                'email': email,
                'created_at': user_data.get('created_at', datetime.now().isoformat()),
                'last_accessed': datetime.now().isoformat(),
                'migrated_from': old_file,
                'migrated_at': datetime.now().isoformat(),
                'tests': user_data.get('tests', {})
            }
            
            # Save user file
            with open(user_file, 'w') as f:
                json.dump(new_user_data, f, indent=2, ensure_ascii=False)
            
            print(f"   ✅ Migrated: {email} → {user_file}")
            migrated_count += 1
            
        except Exception as e:
            print(f"   ❌ Failed to migrate {email}: {e}")
            failed_count += 1
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 Migration Summary:")
    print(f"   ✅ Successfully migrated: {migrated_count} user(s)")
    if failed_count > 0:
        print(f"   ❌ Failed: {failed_count} user(s)")
    print(f"{'='*60}\n")
    
    # Backup old file
    if migrated_count > 0:
        backup_file = f"{old_file}.backup"
        try:
            import shutil
            shutil.copy2(old_file, backup_file)
            print(f"💾 Backed up old file to: {backup_file}")
            print(f"   You can safely delete it after verifying the migration.")
        except Exception as e:
            print(f"⚠️  Could not create backup: {e}")
    
    return failed_count == 0


def verify_migration(old_file='data/test_results.json', new_dir='reports'):
    """Verify migration was successful"""
    print(f"\n🔍 Verifying migration...")
    
    # Load old data
    if not os.path.exists(old_file):
        print("   ℹ️  Old file doesn't exist, skipping verification")
        return True
    
    try:
        with open(old_file, 'r') as f:
            old_data = json.load(f)
        old_users = old_data.get('users', {})
    except:
        print("   ⚠️  Could not read old file")
        return False
    
    # Check new files
    all_verified = True
    for email in old_users.keys():
        safe_email = sanitize_email(email)
        user_file = os.path.join(new_dir, f"{safe_email}.json")
        
        if os.path.exists(user_file):
            try:
                with open(user_file, 'r') as f:
                    new_data = json.load(f)
                
                # Verify email matches
                if new_data.get('email') != email:
                    print(f"   ❌ Email mismatch for {email}")
                    all_verified = False
                else:
                    print(f"   ✅ Verified: {email}")
            except:
                print(f"   ❌ Could not read: {user_file}")
                all_verified = False
        else:
            print(f"   ❌ Missing: {email}")
            all_verified = False
    
    return all_verified


def main():
    """Main migration function"""
    print("\n" + "="*60)
    print("🔄 CELPIP Results Migration Tool")
    print("   Single file → Per-user files")
    print("="*60 + "\n")
    
    # Check command line args
    old_file = 'data/test_results.json'
    new_dir = 'reports'
    
    if len(sys.argv) > 1:
        old_file = sys.argv[1]
    if len(sys.argv) > 2:
        new_dir = sys.argv[2]
    
    print(f"Source: {old_file}")
    print(f"Target: {new_dir}/\n")
    
    # Confirm
    if os.path.exists(old_file):
        response = input("Continue with migration? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("❌ Migration cancelled")
            return
    
    # Migrate
    success = migrate_results(old_file, new_dir)
    
    if success:
        # Verify
        verify_success = verify_migration(old_file, new_dir)
        
        if verify_success:
            print("\n✅ Migration completed successfully!")
            print(f"\n📁 Your user reports are now in: {new_dir}/")
            print(f"   Each user has their own file: user@example_com.json")
        else:
            print("\n⚠️  Migration completed but verification failed")
            print("   Please check the files manually")
    else:
        print("\n❌ Migration failed")
        sys.exit(1)


if __name__ == '__main__':
    main()

