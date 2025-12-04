#!/usr/bin/env python3
"""
Script to create test templates for CELPIP Reading tests

Usage:
    python scripts/create_test_template.py <test_number>
"""

import json
import sys
from pathlib import Path

def create_part1_template(test_num):
    """Create Part 1: Reading Correspondence template"""
    return {
        "part": 1,
        "title": "Reading Correspondence",
        "type": "correspondence",
        "instructions": "Read the following message and answer the questions.",
        "sections": [
            {
                "section_type": "passage",
                "title": f"Message (Test {test_num})",
                "content": "TODO: Add the reading passage here.\n\nThis should be a letter or email from the PDF."
            },
            {
                "section_type": "questions",
                "instruction_text": "Questions 1-6: Choose the best option according to the information given in the message.",
                "question_format": "dropdown",
                "questions": [
                    {
                        "id": i,
                        "text": f"Question {i} text here",
                        "options": [
                            "Option A",
                            "Option B",
                            "Option C",
                            "Option D"
                        ],
                        "answer": 0
                    } for i in range(1, 7)
                ]
            },
            {
                "section_type": "response_passage",
                "title": "Response Message",
                "instruction_text": "Questions 7-11: Complete the response by filling in the blanks.",
                "content": "TODO: Add response message with __DROPDOWN_7__, __DROPDOWN_8__, __DROPDOWN_9__, __DROPDOWN_10__, __DROPDOWN_11__ placeholders.",
                "questions": [
                    {
                        "id": i,
                        "text": f"{i}.",
                        "options": [
                            "Option A",
                            "Option B",
                            "Option C",
                            "Option D"
                        ],
                        "answer": 0
                    } for i in range(7, 12)
                ]
            }
        ]
    }

def create_part2_template(test_num):
    """Create Part 2: Reading to Apply a Diagram template"""
    return {
        "part": 2,
        "title": "Reading to Apply a Diagram",
        "type": "diagram",
        "instructions": "Read the following email message about the diagram. Complete the email by filling in the blanks.",
        "sections": [
            {
                "section_type": "diagram_email",
                "diagram_image": f"part2_diagram.png",
                "email_title": "Email Message",
                "content": f"Subject: TODO - Add subject\nTo: TODO\nFrom: TODO\n\nTODO: Add email content with __DROPDOWN_1__, __DROPDOWN_2__, __DROPDOWN_3__, __DROPDOWN_4__, __DROPDOWN_5__ placeholders.",
                "questions": [
                    {
                        "id": i,
                        "text": f"{i}.",
                        "options": [
                            "Option A",
                            "Option B",
                            "Option C",
                            "Option D"
                        ],
                        "answer": 0
                    } for i in range(1, 6)
                ]
            },
            {
                "section_type": "questions",
                "instruction_text": "Using the drop-down menu, choose the best option.",
                "question_format": "dropdown",
                "questions": [
                    {
                        "id": i,
                        "text": f"Question {i} text here",
                        "options": [
                            "Option A",
                            "Option B",
                            "Option C",
                            "Option D"
                        ],
                        "answer": 0
                    } for i in range(6, 9)
                ]
            }
        ]
    }

def create_part3_template(test_num):
    """Create Part 3: Reading for Information template"""
    return {
        "part": 3,
        "title": "Reading for Information",
        "type": "information",
        "instructions": "Read the following passage and answer the questions. Decide which paragraph (A to D) has the information given in each statement. Select E if the information is not given in any of the paragraphs.",
        "sections": [
            {
                "section_type": "passage",
                "title": f"Reading Passage (Test {test_num})",
                "content": "A. TODO: Add paragraph A content here.\n\nB. TODO: Add paragraph B content here.\n\nC. TODO: Add paragraph C content here.\n\nD. TODO: Add paragraph D content here.",
                "note": "E. Not given in any of the above paragraphs."
            },
            {
                "section_type": "questions",
                "instruction_text": "Decide which paragraph, A to D, has the information given in each statement below. Select E if the information is not given in any of the paragraphs.",
                "question_format": "dropdown",
                "questions": [
                    {
                        "id": i,
                        "text": f"Statement {i} - TODO: Add statement text",
                        "options": [
                            "Paragraph A",
                            "Paragraph B",
                            "Paragraph C",
                            "Paragraph D",
                            "Not given (E)"
                        ],
                        "answer": 0
                    } for i in range(1, 10)
                ]
            }
        ]
    }

def create_part4_template(test_num):
    """Create Part 4: Reading for Viewpoints template"""
    return {
        "part": 4,
        "title": "Reading for Viewpoints",
        "type": "viewpoints",
        "instructions": "Read the following article from a website and answer the questions.",
        "sections": [
            {
                "section_type": "passage",
                "title": f"Article (Test {test_num})",
                "content": "TODO: Add article content here. This should be an opinion piece or article with different viewpoints."
            },
            {
                "section_type": "questions",
                "instruction_text": "Using the drop-down menu, choose the best option according to the information given on the website.",
                "question_format": "dropdown",
                "questions": [
                    {
                        "id": i,
                        "text": f"Question {i} text here",
                        "options": [
                            "Option A",
                            "Option B",
                            "Option C",
                            "Option D"
                        ],
                        "answer": 0
                    } for i in range(1, 6)
                ]
            },
            {
                "section_type": "response_passage",
                "title": "Website Comment",
                "instruction_text": "The following is a comment by a visitor to the website page. Complete the comment by choosing the best option to fill in each blank.",
                "content": "TODO: Add comment content with __DROPDOWN_6__, __DROPDOWN_7__, __DROPDOWN_8__, __DROPDOWN_9__, __DROPDOWN_10__ placeholders.",
                "questions": [
                    {
                        "id": i,
                        "text": f"{i}.",
                        "options": [
                            "Option A",
                            "Option B",
                            "Option C",
                            "Option D"
                        ],
                        "answer": 0
                    } for i in range(6, 11)
                ]
            }
        ]
    }

def create_test_templates(test_num):
    """Create all 4 parts for a test"""
    base_path = Path(__file__).parent.parent / 'data' / f'test_{test_num}' / 'reading'
    base_path.mkdir(parents=True, exist_ok=True)
    
    templates = {
        'part1.json': create_part1_template(test_num),
        'part2.json': create_part2_template(test_num),
        'part3.json': create_part3_template(test_num),
        'part4.json': create_part4_template(test_num)
    }
    
    for filename, template in templates.items():
        filepath = base_path / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(template, f, indent=2, ensure_ascii=False)
        print(f"✓ Created: {filepath}")
    
    # Create README for images
    images_path = Path(__file__).parent.parent / 'static' / 'images' / f'test_{test_num}' / 'reading'
    images_path.mkdir(parents=True, exist_ok=True)
    
    readme_content = f"""# Test {test_num} - Reading Images

Place diagram images for Test {test_num} Reading tests here.

## Required Images

- `part2_diagram.png` - Activities diagram for Part 2

## How to Extract from PDF

1. Open the PDF for Test {test_num}
2. Navigate to Part 2 page with the diagram
3. Take a screenshot or use the selection tool
4. Save as `part2_diagram.png` in this folder
"""
    
    readme_path = images_path / 'README.md'
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"✓ Created: {readme_path}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        test_num = int(sys.argv[1])
        create_test_templates(test_num)
    else:
        # Create templates for tests 2-5
        for test_num in range(2, 6):
            print(f"\n📝 Creating Test {test_num}...")
            create_test_templates(test_num)
        print("\n✅ All test templates created!")
        print("\n📌 Next steps:")
        print("1. Fill in TODO sections in each JSON file with actual test content")
        print("2. Add diagram images to static/images/test_X/reading/")
        print("3. Update correct answer indices")

