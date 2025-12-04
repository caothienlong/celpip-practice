"""
Results Tracker Module
Handles storing and retrieving user test results to/from JSON file
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional


class ResultsTracker:
    def __init__(self, results_file='data/test_results.json'):
        self.results_file = results_file
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create results file if it doesn't exist"""
        if not os.path.exists(self.results_file):
            os.makedirs(os.path.dirname(self.results_file), exist_ok=True)
            with open(self.results_file, 'w') as f:
                json.dump({'users': {}}, f, indent=2)
    
    def _load_results(self) -> Dict:
        """Load all results from JSON file"""
        try:
            with open(self.results_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading results: {e}")
            return {'users': {}}
    
    def _save_results(self, data: Dict):
        """Save results to JSON file"""
        try:
            with open(self.results_file, 'w') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving results: {e}")
    
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
        data = self._load_results()
        
        # Initialize user if not exists
        if user_email not in data['users']:
            data['users'][user_email] = {
                'email': user_email,
                'tests': {}
            }
        
        user_data = data['users'][user_email]
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
        
        self._save_results(data)
    
    def complete_test_attempt(self, user_email: str, test_num: int, attempt_id: str):
        """Mark a test attempt as completed"""
        data = self._load_results()
        
        if user_email in data['users']:
            test_key = f'test_{test_num}'
            if test_key in data['users'][user_email]['tests']:
                for attempt in data['users'][user_email]['tests'][test_key]['attempts']:
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
                
                self._save_results(data)
    
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
        data = self._load_results()
        
        if user_email not in data['users']:
            return {
                'attempt_count': 0,
                'latest_attempt': None,
                'all_attempts': []
            }
        
        test_key = f'test_{test_num}'
        if test_key not in data['users'][user_email]['tests']:
            return {
                'attempt_count': 0,
                'latest_attempt': None,
                'all_attempts': []
            }
        
        attempts = data['users'][user_email]['tests'][test_key]['attempts']
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
        data = self._load_results()
        
        if user_email not in data['users']:
            return {}
        
        summary = {}
        user_tests = data['users'][user_email]['tests']
        
        for test_key, test_data in user_tests.items():
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
        data = self._load_results()
        
        if user_email not in data['users']:
            data['users'][user_email] = {
                'email': user_email,
                'created_at': datetime.now().isoformat(),
                'tests': {}
            }
            self._save_results(data)
        
        return data['users'][user_email]

