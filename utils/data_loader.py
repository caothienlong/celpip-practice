"""
Data loader utility for CELPIP test data.
Loads test data from JSON files and processes them for use in the application.
This module is designed to be platform-agnostic and can be used by web, iOS, or Android apps.
"""

import json
import os
from pathlib import Path


class TestDataLoader:
    """Loads and processes CELPIP test data from JSON files"""
    
    def __init__(self, data_dir='data'):
        """
        Initialize the data loader
        
        Args:
            data_dir: Base directory containing test data (default: 'data')
        """
        self.data_dir = Path(data_dir)
        
    def load_test_part(self, test_number, skill, part_number):
        """
        Load a specific test part
        
        Args:
            test_number: Test number (1-20)
            skill: Skill name ('reading', 'writing', 'speaking', 'listening')
            part_number: Part number (varies by skill)
            
        Returns:
            dict: Test part data
        """
        file_path = self.data_dir / f'test_{test_number}' / skill / f'part{part_number}.json'
        
        if not file_path.exists():
            raise FileNotFoundError(f"Test data not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data
    
    def get_all_questions(self, test_data):
        """
        Extract all questions from test data sections
        
        Args:
            test_data: Test part data dictionary
            
        Returns:
            list: All questions from all sections
        """
        questions = []
        for section in test_data.get('sections', []):
            if 'questions' in section:
                questions.extend(section['questions'])
        return questions
    
    def get_section_by_type(self, test_data, section_type):
        """
        Get a specific section by type
        
        Args:
            test_data: Test part data dictionary
            section_type: Type of section to find
            
        Returns:
            dict: Section data or None if not found
        """
        for section in test_data.get('sections', []):
            if section.get('section_type') == section_type:
                return section
        return None
    
    def get_questions_by_section(self, test_data, section_type):
        """
        Get questions from a specific section type
        
        Args:
            test_data: Test part data dictionary
            section_type: Type of section
            
        Returns:
            list: Questions from the specified section
        """
        section = self.get_section_by_type(test_data, section_type)
        return section.get('questions', []) if section else []
    
    def process_dropdown_content(self, content, questions):
        """
        Replace __DROPDOWN_X__ placeholders with HTML dropdowns
        
        Args:
            content: Text content with dropdown placeholders
            questions: List of question dictionaries
            
        Returns:
            str: HTML content with dropdowns
        """
        for question in questions:
            q_id = question['id']
            placeholder = f"__DROPDOWN_{q_id}__"
            
            # Build dropdown HTML with question number
            options_html = '<option value="" selected disabled>-- Select --</option>'
            for idx, option in enumerate(question['options']):
                options_html += f'<option value="{idx}">{option}</option>'
            
            dropdown_html = (
                f'<strong style="color: #667eea;">{q_id}.</strong> '
                f'<select class="inline-dropdown" name="q{q_id}" data-question="{q_id}" required>'
                f'{options_html}</select>'
            )
            content = content.replace(placeholder, dropdown_html)
        
        return content
    
    def build_question_dropdown_html(self, questions):
        """
        Build HTML for standalone questions with dropdowns
        
        Args:
            questions: List of question dictionaries
            
        Returns:
            str: HTML for questions
        """
        html = ''
        for question in questions:
            q_id = question['id']
            html += f'<div class="question-inline">'
            html += f'<span class="question-number">{q_id}.</span> '
            html += f'<span class="question-label">{question["text"]}</span> '
            html += f'<select class="inline-dropdown" name="q{q_id}" data-question="{q_id}" required>'
            html += '<option value="" selected disabled>-- Select --</option>'
            for idx, option in enumerate(question['options']):
                html += f'<option value="{idx}">{option}</option>'
            html += '</select></div>'
        return html
    
    def list_available_tests(self):
        """
        List all available tests
        
        Returns:
            list: Available test numbers
        """
        tests = []
        for item in self.data_dir.iterdir():
            if item.is_dir() and item.name.startswith('test_'):
                try:
                    test_num = int(item.name.split('_')[1])
                    tests.append(test_num)
                except (ValueError, IndexError):
                    continue
        return sorted(tests)
    
    def list_available_parts(self, test_number, skill):
        """
        List all available parts for a specific test and skill
        
        Args:
            test_number: Test number
            skill: Skill name
            
        Returns:
            list: Available part numbers
        """
        skill_dir = self.data_dir / f'test_{test_number}' / skill
        if not skill_dir.exists():
            return []
        
        parts = []
        for item in skill_dir.iterdir():
            if item.suffix == '.json' and item.stem.startswith('part'):
                try:
                    part_num = int(item.stem.replace('part', ''))
                    parts.append(part_num)
                except ValueError:
                    continue
        return sorted(parts)
    
    def get_correct_answers(self, test_data):
        """
        Get all correct answers from test data
        
        Args:
            test_data: Test part data dictionary
            
        Returns:
            dict: Mapping of question ID to correct answer index
        """
        questions = self.get_all_questions(test_data)
        return {str(q['id']): q['answer'] for q in questions}

