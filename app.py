from flask import Flask, render_template, request, jsonify, session
import secrets
from utils.data_loader import TestDataLoader
from config import calculate_timeout, get_timeout

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Initialize data loader
data_loader = TestDataLoader(data_dir='data')


@app.route('/')
def index():
    """Home page showing all available tests"""
    available_tests = data_loader.list_available_tests()
    return render_template('test_list.html', test_numbers=available_tests)


@app.route('/test/<int:test_num>')
def test_detail(test_num):
    """Test detail page showing all 4 skills"""
    # Get available parts for each skill
    reading_parts = data_loader.list_available_parts(test_num, 'reading')
    writing_parts = data_loader.list_available_parts(test_num, 'writing')
    listening_parts = data_loader.list_available_parts(test_num, 'listening')
    speaking_parts = data_loader.list_available_parts(test_num, 'speaking')
    
    # Get scores from session
    if 'scores' not in session:
        session['scores'] = {}
    
    test_key = f'test_{test_num}'
    session_scores = session['scores'].get(test_key, {})
    
    # Calculate totals for reading
    reading_total = None
    reading_max = None
    if reading_parts and 'reading' in session_scores:
        reading_total = sum(session_scores['reading'].values())
        # Calculate max possible score (38 questions for reading)
        reading_max = 38  # 11 + 8 + 9 + 10
    
    return render_template('test_detail.html',
                         test_num=test_num,
                         reading_parts=reading_parts,
                         writing_parts=writing_parts,
                         listening_parts=listening_parts,
                         speaking_parts=speaking_parts,
                         session_scores=session_scores,
                         reading_total=reading_total,
                         reading_max=reading_max)


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
    # Get all questions
    all_questions = data_loader.get_all_questions(test_data)
    num_questions = len(all_questions)
    
    # Calculate timeout (use JSON value if present, otherwise calculate)
    timeout = test_data.get('timeout_minutes')
    if timeout is None:
        # Auto-calculate if not specified in JSON
        timeout = get_timeout(test_data['part'], skill, part_num, num_questions)
    
    processed = {
        'title': f"Part {part_num}: {test_data['title']}",
        'instructions': test_data['instructions'],
        'timeout_minutes': timeout,
        'type': test_data['type'],
        'questions': all_questions,
        'num_questions': num_questions
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
    
    elif test_data['type'] == 'information':
        # Part 3: Reading for Information
        passage_section = data_loader.get_section_by_type(test_data, 'passage')
        questions_section = data_loader.get_section_by_type(test_data, 'questions')
        
        processed['is_information_type'] = True
        
        if passage_section:
            processed['passage'] = passage_section['content']
            processed['passage_note'] = passage_section.get('note', '')
        
        if questions_section:
            processed['questions_html'] = data_loader.build_question_dropdown_html(
                questions_section['questions']
            )
    
    elif test_data['type'] == 'viewpoints':
        # Part 4: Reading for Viewpoints
        passage_section = data_loader.get_section_by_type(test_data, 'passage')
        questions_section = data_loader.get_section_by_type(test_data, 'questions')
        response_section = data_loader.get_section_by_type(test_data, 'response_passage')
        
        processed['is_viewpoints_type'] = True
        
        if passage_section:
            processed['passage'] = passage_section['content']
        
        if questions_section:
            processed['questions_html'] = data_loader.build_question_dropdown_html(
                questions_section['questions']
            )
        
        if response_section:
            processed['response_passage'] = data_loader.process_dropdown_content(
                response_section['content'],
                response_section['questions']
            )
            processed['response_title'] = response_section.get('title', 'Response')
            processed['section_divider_text'] = response_section.get('instruction_text', '')
    
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
        JSON with score, results, and next part info
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
        percentage = round((score / total_questions) * 100, 1) if total_questions > 0 else 0
        
        # Save score to session
        if 'scores' not in session:
            session['scores'] = {}
        
        test_key = f'test_{test_num}'
        if test_key not in session['scores']:
            session['scores'][test_key] = {}
        if skill not in session['scores'][test_key]:
            session['scores'][test_key][skill] = {}
        
        session['scores'][test_key][skill][part_num] = score
        session.modified = True
        
        # Determine next part
        next_part = None
        skill_parts = data_loader.list_available_parts(test_num, skill)
        if part_num in skill_parts:
            current_index = skill_parts.index(part_num)
            if current_index + 1 < len(skill_parts):
                next_part = skill_parts[current_index + 1]
        
        # Calculate skill total
        skill_scores = session['scores'][test_key].get(skill, {})
        skill_total = sum(skill_scores.values())
        skill_max = sum([len(data_loader.get_all_questions(data_loader.load_test_part(test_num, skill, p))) 
                         for p in skill_parts])
        
        return jsonify({
            'score': score,
            'total': total_questions,
            'percentage': percentage,
            'results': results,
            'next_part': next_part,
            'test_num': test_num,
            'skill': skill,
            'skill_total': skill_total,
            'skill_max': skill_max,
            'all_parts_complete': next_part is None
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
