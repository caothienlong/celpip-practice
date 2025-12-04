"""
Results Tracker Module
Handles storing and retrieving user test results to/from JSON files
Each user gets their own file for better scalability and privacy
"""
import json
import os
import re
from datetime import datetime
from typing import Dict, List, Any, Optional


class ResultsTracker:
    def __init__(self, reports_dir='reports'):
        self.reports_dir = reports_dir
        self._ensure_directory_exists()
    
    def _ensure_directory_exists(self):
        """Create reports directory if it doesn't exist"""
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def _sanitize_email(self, email: str) -> str:
        """Convert email to safe filename"""
        # Replace @ and . with underscores, remove other special chars
        safe_email = re.sub(r'[^\w\-.]', '_', email.lower())
        return safe_email
    
    def _get_user_file_path(self, email: str) -> str:
        """Get file path for a specific user"""
        safe_email = self._sanitize_email(email)
        return os.path.join(self.reports_dir, f"{safe_email}.json")
    
    def _load_user_data(self, email: str) -> Dict:
        """Load results for a specific user"""
        file_path = self._get_user_file_path(email)
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    return json.load(f)
            else:
                # Return empty user structure
                return {
                    'email': email,
                    'created_at': datetime.now().isoformat(),
                    'tests': {}
                }
        except Exception as e:
            print(f"Error loading user data for {email}: {e}")
            return {
                'email': email,
                'created_at': datetime.now().isoformat(),
                'tests': {}
            }
    
    def _save_user_data(self, email: str, data: Dict):
        """Save results for a specific user"""
        file_path = self._get_user_file_path(email)
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving user data for {email}: {e}")
    
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
        user_data = self._load_user_data(user_email)
        test_key = f'test_{test_num}'
        
        # Initialize test if not exists
        if test_key not in user_data['tests']:
            user_data['tests'][test_key] = {
                'test_number': test_num,
                'attempts': []
            }
        
        # Find or create attempt
        attempt = None
        for att in user_data['tests'][test_key]['attempts']:
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
            user_data['tests'][test_key]['attempts'].append(attempt)
        
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
        
        self._save_user_data(user_email, user_data)
    
    def complete_test_attempt(self, user_email: str, test_num: int, attempt_id: str):
        """Mark a test attempt as completed"""
        user_data = self._load_user_data(user_email)
        test_key = f'test_{test_num}'
        
        if test_key in user_data['tests']:
            for attempt in user_data['tests'][test_key]['attempts']:
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
            
            self._save_user_data(user_email, user_data)
    
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
        user_data = self._load_user_data(user_email)
        test_key = f'test_{test_num}'
        
        if test_key not in user_data['tests']:
            return {
                'attempt_count': 0,
                'latest_attempt': None,
                'all_attempts': []
            }
        
        attempts = user_data['tests'][test_key]['attempts']
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
        user_data = self._load_user_data(user_email)
        summary = {}
        
        for test_key, test_data in user_data['tests'].items():
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
        user_data = self._load_user_data(user_email)
        
        # If tests dict is empty, this might be a new user
        if not user_data.get('tests'):
            user_data['created_at'] = datetime.now().isoformat()
            user_data['last_accessed'] = datetime.now().isoformat()
            self._save_user_data(user_email, user_data)
        else:
            # Update last accessed time
            user_data['last_accessed'] = datetime.now().isoformat()
            self._save_user_data(user_email, user_data)
        
        return user_data
    
    def list_all_users(self) -> List[str]:
        """Get list of all users who have taken tests"""
        try:
            users = []
            for filename in os.listdir(self.reports_dir):
                if filename.endswith('.json'):
                    # Read email from file
                    file_path = os.path.join(self.reports_dir, filename)
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        if 'email' in data:
                            users.append(data['email'])
            return users
        except Exception as e:
            print(f"Error listing users: {e}")
            return []

