"""
Configuration for CELPIP Test Application

This module loads configuration from config.json and provides
utility functions for accessing configuration values.
"""

import json
import os
from pathlib import Path

# Path to config file
CONFIG_FILE = Path(__file__).parent / 'config.json'

# Cache for loaded config
_config_cache = None


def load_config():
    """
    Load configuration from config.json
    
    Returns:
        dict: Configuration dictionary
    """
    global _config_cache
    
    if _config_cache is None:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                _config_cache = json.load(f)
        else:
            # Default configuration if file doesn't exist
            _config_cache = {
                'time_per_question': {
                    'reading': 1.5,
                    'writing': 30.0,
                    'speaking': 1.5,
                    'listening': 1.5
                },
                'default_time_per_question': 1.5,
                'custom_timeouts': {}
            }
    
    return _config_cache


def reload_config():
    """Reload configuration from file (useful after changes)"""
    global _config_cache
    _config_cache = None
    return load_config()


def get_config_value(key_path, default=None):
    """
    Get a configuration value using dot notation
    
    Args:
        key_path: Path to config value (e.g., 'time_per_question.reading')
        default: Default value if key not found
        
    Returns:
        Configuration value or default
        
    Examples:
        >>> get_config_value('time_per_question.reading')
        1.5
        >>> get_config_value('ui_settings.timer_warning_seconds')
        60
    """
    config = load_config()
    keys = key_path.split('.')
    
    value = config
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return default
    
    return value


def get_time_per_question(skill):
    """
    Get the time allocation per question for a specific skill
    
    Args:
        skill: Skill name ('reading', 'writing', 'speaking', 'listening')
        
    Returns:
        float: Minutes per question
    """
    config = load_config()
    time_per_q = config.get('time_per_question', {})
    default = config.get('default_time_per_question', 1.5)
    
    return time_per_q.get(skill.lower(), default)


def calculate_timeout(num_questions, skill='reading'):
    """
    Calculate timeout for a test part
    
    Args:
        num_questions: Number of questions in the part
        skill: Skill name (default: 'reading')
        
    Returns:
        float: Total timeout in minutes
        
    Examples:
        >>> calculate_timeout(11, 'reading')
        16.5
        >>> calculate_timeout(8, 'reading')
        12.0
    """
    time_per_q = get_time_per_question(skill)
    return num_questions * time_per_q


def get_timeout(test_num, skill, part_num, num_questions):
    """
    Get timeout for a specific test part
    
    Checks custom overrides first, then calculates based on questions
    
    Args:
        test_num: Test number
        skill: Skill name
        part_num: Part number
        num_questions: Number of questions
        
    Returns:
        float: Timeout in minutes
    """
    config = load_config()
    custom_timeouts = config.get('custom_timeouts', {})
    
    # Check for custom override using string key format
    key = f"{test_num}_{skill}_{part_num}"
    
    if key in custom_timeouts:
        return custom_timeouts[key]
    
    # Calculate based on number of questions
    return calculate_timeout(num_questions, skill)


# UI Settings helpers
def get_timer_warning_seconds():
    """Get the number of seconds before timeout to show warning"""
    return get_config_value('ui_settings.timer_warning_seconds', 60)


def should_auto_submit():
    """Check if tests should auto-submit on timeout"""
    return get_config_value('ui_settings.auto_submit_on_timeout', True)


def should_show_question_numbers():
    """Check if question numbers should be displayed"""
    return get_config_value('ui_settings.show_question_numbers', True)

