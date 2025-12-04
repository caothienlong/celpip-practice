"""
Configuration for CELPIP Test Application
"""

# Time allocation per question (in minutes)
TIME_PER_QUESTION = {
    'reading': 1.5,      # 1.5 minutes per question for reading
    'writing': 30.0,     # 30 minutes per task for writing
    'speaking': 1.5,     # Varies by part for speaking
    'listening': 1.5,    # 1.5 minutes per question for listening
}

# Default if skill not found
DEFAULT_TIME_PER_QUESTION = 1.5

def get_time_per_question(skill):
    """
    Get the time allocation per question for a specific skill
    
    Args:
        skill: Skill name ('reading', 'writing', 'speaking', 'listening')
        
    Returns:
        float: Minutes per question
    """
    return TIME_PER_QUESTION.get(skill.lower(), DEFAULT_TIME_PER_QUESTION)


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


# Test-specific overrides (optional)
CUSTOM_TIMEOUTS = {
    # Format: (test_num, skill, part_num): timeout_minutes
    # Example: (1, 'writing', 1): 27.0,  # Override for specific part
}

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
    key = (test_num, skill, part_num)
    
    # Check for custom override
    if key in CUSTOM_TIMEOUTS:
        return CUSTOM_TIMEOUTS[key]
    
    # Calculate based on number of questions
    return calculate_timeout(num_questions, skill)

