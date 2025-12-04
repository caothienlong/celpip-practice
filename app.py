from flask import Flask, render_template, request, jsonify
import secrets
from utils.data_loader import TestDataLoader

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Initialize data loader
data_loader = TestDataLoader(data_dir='data')


@app.route('/')
def index():
    """Home page showing all available tests and skills"""
    available_tests = data_loader.list_available_tests()
    
    # For now, we'll show Test 1 with available skills
    test_info = {}
    if available_tests:
        for test_num in available_tests:
            test_info[test_num] = {
                'reading': data_loader.list_available_parts(test_num, 'reading'),
                'writing': data_loader.list_available_parts(test_num, 'writing'),
                'speaking': data_loader.list_available_parts(test_num, 'speaking'),
                'listening': data_loader.list_available_parts(test_num, 'listening')
            }
    
    return render_template('index.html', test_info=test_info)


@app.route('/test/<int:test_num>/<skill>/part<int:part_num>')
def test_part(test_num, skill, part_num):
    """
    Display a specific test part
    
    Args:
        test_num: Test number (1-20)
        skill: Skill name (reading, writing, speaking, listening)
        part_num: Part number
    """
    try:
        # Load test data from JSON
        test_data = data_loader.load_test_part(test_num, skill, part_num)
        
        # Process the test data based on type
        processed_data = prepare_test_data(test_data, skill, part_num)
        
        return render_template(
            'test_section.html',
            section=processed_data,
            test_num=test_num,
            skill=skill,
            part_num=part_num
        )
    except FileNotFoundError as e:
        return f"Test not found: {e}", 404
    except Exception as e:
        return f"Error loading test: {e}", 500


def prepare_test_data(test_data, skill, part_num):
    """
    Prepare test data for rendering
    
    Args:
        test_data: Raw test data from JSON
        skill: Skill name
        part_num: Part number
        
    Returns:
        dict: Processed data ready for template
    """
    processed = {
        'title': f"Part {part_num}: {test_data['title']}",
        'instructions': test_data['instructions'],
        'timeout_minutes': test_data['timeout_minutes'],
        'type': test_data['type'],
        'questions': data_loader.get_all_questions(test_data)
    }
    
    # Process based on test type
    if test_data['type'] == 'correspondence':
        # Part 1: Reading Correspondence
        passage_section = data_loader.get_section_by_type(test_data, 'passage')
        response_section = data_loader.get_section_by_type(test_data, 'response_passage')
        questions_section = data_loader.get_section_by_type(test_data, 'questions')
        
        if passage_section:
            processed['passage'] = passage_section['content']
        
        if questions_section:
            processed['questions_1_6_html'] = data_loader.build_question_dropdown_html(
                questions_section['questions']
            )
        
        if response_section:
            processed['response_passage'] = data_loader.process_dropdown_content(
                response_section['content'],
                response_section['questions']
            )
            processed['section_divider_text'] = response_section.get('instruction_text', '')
    
    elif test_data['type'] == 'diagram':
        # Part 2: Reading to Apply a Diagram
        diagram_section = data_loader.get_section_by_type(test_data, 'diagram_email')
        questions_section = data_loader.get_section_by_type(test_data, 'questions')
        
        processed['has_diagram'] = True
        
        if diagram_section:
            processed['diagram_image'] = diagram_section.get('diagram_image')
            processed['email_content'] = data_loader.process_dropdown_content(
                diagram_section['content'],
                diagram_section['questions']
            )
        
        if questions_section:
            processed['questions_6_8_html'] = data_loader.build_question_dropdown_html(
                questions_section['questions']
            )
    
    return processed


@app.route('/submit_answers', methods=['POST'])
def submit_answers():
    """
    Process submitted answers and return score
    
    Request JSON:
        {
            "answers": {"1": 0, "2": 1, ...},
            "test_num": 1,
            "skill": "reading",
            "part_num": 1
        }
    
    Returns:
        JSON with score and results
    """
    data = request.json
    answers = data.get('answers', {})
    test_num = data.get('test_num')
    skill = data.get('skill')
    part_num = data.get('part_num')
    
    try:
        # Load test data
        test_data = data_loader.load_test_part(test_num, skill, part_num)
        
        # Get correct answers
        correct_answers = data_loader.get_correct_answers(test_data)
        
        # Calculate score
        score = 0
        results = {}
        
        for question_id, user_answer in answers.items():
            if question_id in correct_answers:
                is_correct = user_answer == correct_answers[question_id]
                if is_correct:
                    score += 1
                results[question_id] = {
                    'correct': is_correct,
                    'user_answer': user_answer,
                    'correct_answer': correct_answers[question_id]
                }
        
        total_questions = len(correct_answers)
        
        return jsonify({
            'score': score,
            'total': total_questions,
            'percentage': round((score / total_questions) * 100, 1) if total_questions > 0 else 0,
            'results': results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Legacy routes for backward compatibility
@app.route('/test1/part1')
def test1_part1():
    """Redirect to new route format"""
    return test_part(1, 'reading', 1)


@app.route('/test1/part2')
def test1_part2():
    """Redirect to new route format"""
    return test_part(1, 'reading', 2)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
