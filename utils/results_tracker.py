"""
Results Tracker Module
Stores user data in organized folder structure:
  users/
    {username}/
      profile.json        # Email, role, timestamps
      test_history.json   # All test attempts & scores
"""
import json
import os
import re
from datetime import datetime
from typing import Dict, List, Any, Optional


class ResultsTracker:
    def __init__(self, users_dir='users'):
        self.users_dir = users_dir
        self._ensure_directory_exists()
    
    def _ensure_directory_exists(self):
        """Create users directory if it doesn't exist"""
        os.makedirs(self.users_dir, exist_ok=True)
    
    def _sanitize_email(self, email: str) -> str:
        """
        Convert email to safe folder name (remove domain extension)
        Example: caothienlong@gmail.com -> caothienlong_gmail
        """
        # Extract username and domain
        email = email.lower().strip()
        
        # Replace @ with underscore
        safe_name = email.replace('@', '_')
        
        # Remove domain extensions (.com, .net, .org, etc.)
        safe_name = re.sub(r'\.(com|net|org|edu|gov|io|co|uk|ca|au)$', '', safe_name)
        
        # Remove any remaining special characters
        safe_name = re.sub(r'[^\w\-]', '_', safe_name)
        
        return safe_name
    
    def _get_user_folder(self, email: str) -> str:
        """Get folder path for a specific user"""
        safe_name = self._sanitize_email(email)
        return os.path.join(self.users_dir, safe_name)
    
    def _get_profile_path(self, email: str) -> str:
        """Get profile.json path for user"""
        return os.path.join(self._get_user_folder(email), 'profile.json')
    
    def _get_test_history_path(self, email: str) -> str:
        """Get test_history.json path for user"""
        return os.path.join(self._get_user_folder(email), 'test_history.json')
    
    def _get_vocabulary_notes_path(self, email: str) -> str:
        """Get vocabulary_notes.json path for user"""
        return os.path.join(self._get_user_folder(email), 'vocabulary_notes.json')
    
    def _load_user_profile(self, email: str) -> Dict:
        """Load user profile data"""
        profile_path = self._get_profile_path(email)
        
        try:
            if os.path.exists(profile_path):
                with open(profile_path, 'r') as f:
                    return json.load(f)
            else:
                # Return default profile
                return {
                    'email': email,
                    'role': 'Basic',
                    'created_at': datetime.now().isoformat(),
                    'last_accessed': datetime.now().isoformat()
                }
        except Exception as e:
            print(f"Error loading profile for {email}: {e}")
            return {
                'email': email,
                'role': 'Basic',
                'created_at': datetime.now().isoformat(),
                'last_accessed': datetime.now().isoformat()
            }
    
    def _save_user_profile(self, email: str, profile: Dict):
        """Save user profile data"""
        user_folder = self._get_user_folder(email)
        os.makedirs(user_folder, exist_ok=True)
        
        profile_path = self._get_profile_path(email)
        try:
            with open(profile_path, 'w') as f:
                json.dump(profile, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving profile for {email}: {e}")
    
    def _load_test_history(self, email: str) -> Dict:
        """Load test history data"""
        history_path = self._get_test_history_path(email)
        
        try:
            if os.path.exists(history_path):
                with open(history_path, 'r') as f:
                    return json.load(f)
            else:
                # Return empty history
                return {'tests': {}}
        except Exception as e:
            print(f"Error loading test history for {email}: {e}")
            return {'tests': {}}
    
    def _save_test_history(self, email: str, history: Dict):
        """Save test history data"""
        user_folder = self._get_user_folder(email)
        os.makedirs(user_folder, exist_ok=True)
        
        history_path = self._get_test_history_path(email)
        try:
            with open(history_path, 'w') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving test history for {email}: {e}")
    
    def save_test_result(self, 
                        user_email: str,
                        test_num: int,
                        skill: str,
                        part_num: int,
                        answers: Dict[int, int],
                        correct_answers: Dict[int, int],
                        score: int,
                        max_score: int,
                        attempt_id: str):
        """
        Save a single part result
        
        Args:
            user_email: User's email address
            test_num: Test number (1, 2, 3, etc.)
            skill: Skill name (reading, writing, listening, speaking)
            part_num: Part number within the skill
            answers: User's answers {question_id: answer_choice}
            correct_answers: Correct answers {question_id: correct_choice}
            score: Number of correct answers
            max_score: Total number of questions
            attempt_id: Unique identifier for this test attempt
        """
        history = self._load_test_history(user_email)
        test_key = f'test_{test_num}'
        
        # Initialize test if not exists
        if test_key not in history['tests']:
            history['tests'][test_key] = {
                'test_number': test_num,
                'attempts': []
            }
        
        # Find or create attempt
        attempt = None
        for att in history['tests'][test_key]['attempts']:
            if att['attempt_id'] == attempt_id:
                attempt = att
                break
        
        if attempt is None:
            attempt = {
                'attempt_id': attempt_id,
                'started_at': datetime.now().isoformat(),
                'completed_at': None,
                'skills': {}
            }
            history['tests'][test_key]['attempts'].append(attempt)
        
        # Initialize skill if not exists
        if skill not in attempt['skills']:
            attempt['skills'][skill] = {
                'skill_name': skill,
                'parts': {},
                'total_score': 0,
                'total_max': 0
            }
        
        # Save part result
        attempt['skills'][skill]['parts'][str(part_num)] = {
            'part_number': part_num,
            'answers': answers,
            'correct_answers': correct_answers,
            'score': score,
            'max_score': max_score,
            'timestamp': datetime.now().isoformat()
        }
        
        # Update skill totals
        skill_data = attempt['skills'][skill]
        skill_data['total_score'] = sum(p['score'] for p in skill_data['parts'].values())
        skill_data['total_max'] = sum(p['max_score'] for p in skill_data['parts'].values())
        
        self._save_test_history(user_email, history)
        
        # Update last accessed in profile
        profile = self._load_user_profile(user_email)
        profile['last_accessed'] = datetime.now().isoformat()
        self._save_user_profile(user_email, profile)
    
    def complete_test_attempt(self, user_email: str, test_num: int, attempt_id: str):
        """Mark a test attempt as completed"""
        history = self._load_test_history(user_email)
        test_key = f'test_{test_num}'
        
        if test_key in history['tests']:
            for attempt in history['tests'][test_key]['attempts']:
                if attempt['attempt_id'] == attempt_id:
                    attempt['completed_at'] = datetime.now().isoformat()
                    
                    # Calculate overall total
                    total_score = 0
                    total_max = 0
                    for skill_data in attempt['skills'].values():
                        total_score += skill_data['total_score']
                        total_max += skill_data['total_max']
                    
                    attempt['total_score'] = total_score
                    attempt['total_max'] = total_max
                    attempt['percentage'] = round((total_score / total_max * 100), 1) if total_max > 0 else 0
                    break
            
            self._save_test_history(user_email, history)
    
    def get_user_test_history(self, user_email: str, test_num: int) -> Dict:
        """
        Get all attempts for a specific test by a user
        
        Returns:
            {
                'attempt_count': int,
                'latest_attempt': {...},
                'all_attempts': [...]
            }
        """
        history = self._load_test_history(user_email)
        test_key = f'test_{test_num}'
        
        if test_key not in history['tests']:
            return {
                'attempt_count': 0,
                'latest_attempt': None,
                'all_attempts': []
            }
        
        attempts = history['tests'][test_key]['attempts']
        completed_attempts = [a for a in attempts if a.get('completed_at')]
        
        latest = None
        if completed_attempts:
            latest = max(completed_attempts, key=lambda x: x['completed_at'])
        
        return {
            'attempt_count': len(completed_attempts),
            'latest_attempt': latest,
            'all_attempts': completed_attempts
        }
    
    def get_all_tests_summary(self, user_email: str) -> Dict[int, Dict]:
        """
        Get summary of all tests for a user (for main page display)
        
        Returns:
            {
                1: {'attempt_count': 3, 'latest_score': 37, 'latest_max': 38, ...},
                2: {'attempt_count': 1, 'latest_score': 35, 'latest_max': 38, ...},
                ...
            }
        """
        history = self._load_test_history(user_email)
        summary = {}
        
        for test_key, test_data in history['tests'].items():
            test_num = test_data['test_number']
            completed_attempts = [a for a in test_data['attempts'] if a.get('completed_at')]
            
            if completed_attempts:
                latest = max(completed_attempts, key=lambda x: x['completed_at'])
                summary[test_num] = {
                    'attempt_count': len(completed_attempts),
                    'latest_score': latest.get('total_score', 0),
                    'latest_max': latest.get('total_max', 0),
                    'latest_percentage': latest.get('percentage', 0),
                    'latest_date': latest.get('completed_at', '')
                }
        
        return summary
    
    def get_or_create_user(self, user_email: str) -> Dict:
        """Get or create user in the system"""
        # Create user folder if needed
        user_folder = self._get_user_folder(user_email)
        os.makedirs(user_folder, exist_ok=True)
        
        # Load or create profile
        profile = self._load_user_profile(user_email)
        
        # Update last accessed
        profile['last_accessed'] = datetime.now().isoformat()
        self._save_user_profile(user_email, profile)
        
        return profile
    
    def list_all_users(self) -> List[str]:
        """Get list of all users who have folders"""
        try:
            users = []
            if not os.path.exists(self.users_dir):
                return users
                
            for folder_name in os.listdir(self.users_dir):
                folder_path = os.path.join(self.users_dir, folder_name)
                if os.path.isdir(folder_path):
                    profile_path = os.path.join(folder_path, 'profile.json')
                    if os.path.exists(profile_path):
                        with open(profile_path, 'r') as f:
                            profile = json.load(f)
                            if 'email' in profile:
                                users.append(profile['email'])
            return users
        except Exception as e:
            print(f"Error listing users: {e}")
            return []
    
    def get_user_profile(self, user_email: str) -> Dict:
        """Get user profile"""
        return self._load_user_profile(user_email)
    
    def update_user_role(self, user_email: str, role: str):
        """Update user's role (Basic, Premium, etc.)"""
        profile = self._load_user_profile(user_email)
        profile['role'] = role
        self._save_user_profile(user_email, profile)
    
    # ==================== Vocabulary Notes Methods ====================
    
    def _load_vocabulary_notes(self, email: str) -> Dict:
        """Load vocabulary notes data"""
        notes_path = self._get_vocabulary_notes_path(email)
        
        try:
            if os.path.exists(notes_path):
                with open(notes_path, 'r') as f:
                    return json.load(f)
            else:
                # Return empty notes structure
                return {'tests': {}}
        except Exception as e:
            print(f"Error loading vocabulary notes for {email}: {e}")
            return {'tests': {}}
    
    def _save_vocabulary_notes(self, email: str, notes: Dict):
        """Save vocabulary notes data"""
        user_folder = self._get_user_folder(email)
        os.makedirs(user_folder, exist_ok=True)
        
        notes_path = self._get_vocabulary_notes_path(email)
        try:
            with open(notes_path, 'w') as f:
                json.dump(notes, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving vocabulary notes for {email}: {e}")
    
    def save_vocabulary_note(self, 
                            user_email: str,
                            test_num: int,
                            skill: str,
                            part_num: int,
                            word: str,
                            definition: str,
                            context: str = ''):
        """
        Save a vocabulary note
        
        Args:
            user_email: User's email address
            test_num: Test number (1, 2, 3, etc.)
            skill: Skill name (reading, writing, listening, speaking)
            part_num: Part number within the skill
            word: The vocabulary word or phrase
            definition: User's definition/note
            context: Optional context from the passage
        
        Returns:
            note_id: Unique identifier for the note
        """
        notes = self._load_vocabulary_notes(user_email)
        test_key = f'test_{test_num}'
        skill_key = f'{skill}_part_{part_num}'
        
        # Initialize structure if not exists
        if test_key not in notes['tests']:
            notes['tests'][test_key] = {}
        if skill_key not in notes['tests'][test_key]:
            notes['tests'][test_key][skill_key] = []
        
        # Generate note ID (timestamp-based)
        note_id = f"{test_num}_{skill}_{part_num}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        
        # Create note
        note = {
            'note_id': note_id,
            'word': word.strip(),
            'definition': definition.strip(),
            'context': context.strip(),
            'created_at': datetime.now().isoformat(),
            'test_num': test_num,
            'skill': skill,
            'part_num': part_num
        }
        
        # Add note
        notes['tests'][test_key][skill_key].append(note)
        
        # Save
        self._save_vocabulary_notes(user_email, notes)
        
        return note_id
    
    def get_vocabulary_notes(self, 
                            user_email: str,
                            test_num: Optional[int] = None,
                            skill: Optional[str] = None,
                            part_num: Optional[int] = None) -> List[Dict]:
        """
        Get vocabulary notes with optional filtering
        
        Args:
            user_email: User's email address
            test_num: Optional test number filter
            skill: Optional skill filter
            part_num: Optional part number filter
        
        Returns:
            List of vocabulary notes matching the filters
        """
        notes = self._load_vocabulary_notes(user_email)
        all_notes = []
        
        for test_key, test_data in notes.get('tests', {}).items():
            for skill_key, note_list in test_data.items():
                all_notes.extend(note_list)
        
        # Apply filters
        filtered_notes = all_notes
        
        if test_num is not None:
            filtered_notes = [n for n in filtered_notes if n.get('test_num') == test_num]
        
        if skill is not None:
            filtered_notes = [n for n in filtered_notes if n.get('skill') == skill]
        
        if part_num is not None:
            filtered_notes = [n for n in filtered_notes if n.get('part_num') == part_num]
        
        # Sort by created_at (newest first)
        filtered_notes.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return filtered_notes
    
    def delete_vocabulary_note(self, user_email: str, note_id: str) -> bool:
        """
        Delete a vocabulary note
        
        Args:
            user_email: User's email address
            note_id: ID of the note to delete
        
        Returns:
            True if deleted, False if not found
        """
        notes = self._load_vocabulary_notes(user_email)
        deleted = False
        
        # Search for and remove the note
        for test_key, test_data in notes.get('tests', {}).items():
            for skill_key, note_list in test_data.items():
                for i, note in enumerate(note_list):
                    if note.get('note_id') == note_id:
                        del note_list[i]
                        deleted = True
                        break
                if deleted:
                    break
            if deleted:
                break
        
        if deleted:
            self._save_vocabulary_notes(user_email, notes)
        
        return deleted
    
    def update_vocabulary_note(self, 
                              user_email: str,
                              note_id: str,
                              word: Optional[str] = None,
                              definition: Optional[str] = None,
                              context: Optional[str] = None) -> bool:
        """
        Update a vocabulary note
        
        Args:
            user_email: User's email address
            note_id: ID of the note to update
            word: Optional new word
            definition: Optional new definition
            context: Optional new context
        
        Returns:
            True if updated, False if not found
        """
        notes = self._load_vocabulary_notes(user_email)
        updated = False
        
        # Search for and update the note
        for test_key, test_data in notes.get('tests', {}).items():
            for skill_key, note_list in test_data.items():
                for note in note_list:
                    if note.get('note_id') == note_id:
                        if word is not None:
                            note['word'] = word.strip()
                        if definition is not None:
                            note['definition'] = definition.strip()
                        if context is not None:
                            note['context'] = context.strip()
                        note['updated_at'] = datetime.now().isoformat()
                        updated = True
                        break
                if updated:
                    break
            if updated:
                break
        
        if updated:
            self._save_vocabulary_notes(user_email, notes)
        
        return updated
