from flask import Flask, render_template, request, jsonify, session
import secrets
import uuid
from utils.data_loader import TestDataLoader
from utils.results_tracker import ResultsTracker
from config import calculate_timeout, get_timeout

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Initialize data loader and results tracker
data_loader = TestDataLoader(data_dir='data')
results_tracker = ResultsTracker(results_file='data/test_results.json')


@app.route('/')
def index():
    """Home page showing all available tests"""
    available_tests = data_loader.list_available_tests()
    
    # Get exam completion status and scores from session
    exam_status = {}
    for test_num in available_tests:
        test_key = f'exam_{test_num}'
        if test_key in session and session[test_key].get('completed'):
            exam_status[test_num] = {
                'completed': True,
                'total_score': session[test_key].get('total_score', 0),
                'max_score': session[test_key].get('max_score', 0)
            }
        else:
            exam_status[test_num] = {'completed': False}
    
    # Get historical data from JSON if user email is set
    test_history = {}
    if 'user_email' in session:
        user_email = session['user_email']
        test_history = results_tracker.get_all_tests_summary(user_email)
    
    return render_template('test_list.html', 
                         test_numbers=available_tests,
                         exam_status=exam_status,
                         test_history=test_history,
                         user_email=session.get('user_email'))


@app.route('/test/<int:test_num>')
def test_detail(test_num):
    """Test detail page showing all 4 skills (Practice Mode)"""
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


@app.route('/test/<int:test_num>/exam')
def start_exam(test_num):
    """Start Test Mode - begins with Reading Part 1"""
    # Check if user email is set, if not redirect to email collection
    if 'user_email' not in session or not session['user_email']:
        return render_template('collect_email.html', test_num=test_num)
    
    # Generate unique attempt ID for this test attempt
    attempt_id = str(uuid.uuid4())
    
    # Clear any existing exam session (for retakes)
    test_key = f'exam_{test_num}'
    session[test_key] = {
        'mode': 'exam',
        'current_skill': 'reading',
        'current_part': 1,
        'scores': {},
        'completed': False,
        'attempt_id': attempt_id
    }
    session.modified = True
    
    # Create user in tracking system
    results_tracker.get_or_create_user(session['user_email'])
    
    # Redirect to reading part 1
    return test_mode_part(test_num, 'reading', 1)


@app.route('/set_user_email', methods=['POST'])
def set_user_email():
    """Set user email in session"""
    data = request.json
    email = data.get('email', '').strip()
    
    if email:
        session['user_email'] = email
        session.modified = True
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Email is required'}), 400


@app.route('/clear_session')
def clear_session():
    """Clear user session and return to home"""
    session.clear()
    return render_template('session_cleared.html')


@app.route('/test/<int:test_num>/exam/<skill>/part<int:part_num>')
def test_mode_part(test_num, skill, part_num):
    """Display a test part in Test Mode (no going back, sequential only)"""
    try:
        # Load test data
        test_data = data_loader.load_test_part(test_num, skill, part_num)
        processed_data = prepare_test_data(test_data, skill, part_num)
        
        # Determine skill order and progress
        skill_order = ['reading', 'listening', 'writing', 'speaking']
        available_parts = data_loader.list_available_parts(test_num, skill)
        
        # Check if this is the last part of current skill
        is_last_part_of_skill = (part_num == available_parts[-1]) if available_parts else False
        
        # Determine next skill
        next_skill = None
        if is_last_part_of_skill:
            current_skill_index = skill_order.index(skill)
            for i in range(current_skill_index + 1, len(skill_order)):
                next_skill_candidate = skill_order[i]
                if data_loader.list_available_parts(test_num, next_skill_candidate):
                    next_skill = next_skill_candidate
                    break
        
        # Calculate progress
        total_parts = len(available_parts)
        progress = (part_num / total_parts) * 100 if total_parts > 0 else 0
        
        return render_template(
            'test_mode_section.html',
            section=processed_data,
            test_num=test_num,
            skill=skill,
            part_num=part_num,
            total_parts=total_parts,
            progress=progress,
            is_last_part_of_skill=is_last_part_of_skill,
            next_skill=next_skill
        )
    except FileNotFoundError as e:
        return f"Test not found: {e}", 404
    except Exception as e:
        return f"Error loading test: {e}", 500


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


@app.route('/submit_test_mode', methods=['POST'])
def submit_test_mode():
    """
    Process Test Mode submission - stores scores but doesn't show answers
    Only shows final score at end of each skill
    """
    data = request.json
    answers = data.get('answers', {})
    test_num = data.get('test_num')
    skill = data.get('skill')
    part_num = data.get('part_num')
    is_last_part = data.get('is_last_part', False)
    
    try:
        # Load test data and calculate score
        test_data = data_loader.load_test_part(test_num, skill, part_num)
        correct_answers = data_loader.get_correct_answers(test_data)
        
        # Convert answers keys to int for comparison
        int_answers = {int(k): int(v) for k, v in answers.items()}
        
        score = 0
        for question_id, user_answer in int_answers.items():
            if question_id in correct_answers:
                if user_answer == correct_answers[question_id]:
                    score += 1
        
        max_score = len(correct_answers)
        
        # Save score to exam session
        test_key = f'exam_{test_num}'
        if test_key not in session:
            session[test_key] = {'scores': {}, 'attempt_id': str(uuid.uuid4())}
        if 'scores' not in session[test_key]:
            session[test_key]['scores'] = {}
        if skill not in session[test_key]['scores']:
            session[test_key]['scores'][skill] = {}
        
        session[test_key]['scores'][skill][str(part_num)] = score
        session.modified = True
        
        # Save to JSON tracking if user email is set
        if 'user_email' in session:
            attempt_id = session[test_key].get('attempt_id', str(uuid.uuid4()))
            results_tracker.save_test_result(
                user_email=session['user_email'],
                test_num=test_num,
                skill=skill,
                part_num=part_num,
                answers=int_answers,
                correct_answers=correct_answers,
                score=score,
                max_score=max_score,
                attempt_id=attempt_id
            )
        
        # Determine next action
        skill_parts = data_loader.list_available_parts(test_num, skill)
        skill_order = ['reading', 'listening', 'writing', 'speaking']
        
        if is_last_part:
            # Calculate skill total
            skill_scores = session[test_key]['scores'][skill]
            skill_total = sum(skill_scores.values())
            skill_max = sum([len(data_loader.get_all_questions(data_loader.load_test_part(test_num, skill, p))) 
                           for p in skill_parts])
            skill_percentage = round((skill_total / skill_max) * 100, 1) if skill_max > 0 else 0
            
            # Check if this is the last skill
            current_skill_index = skill_order.index(skill)
            has_next_skill = False
            for i in range(current_skill_index + 1, len(skill_order)):
                next_skill_candidate = skill_order[i]
                if data_loader.list_available_parts(test_num, next_skill_candidate):
                    has_next_skill = True
                    break
            
            # If last skill, mark exam as completed and calculate total score
            if not has_next_skill:
                total_score = 0
                max_score_total = 0
                for completed_skill in session[test_key]['scores']:
                    skill_score_dict = session[test_key]['scores'][completed_skill]
                    total_score += sum(skill_score_dict.values())
                    # Calculate max for this skill
                    skill_parts_list = data_loader.list_available_parts(test_num, completed_skill)
                    for p in skill_parts_list:
                        max_score_total += len(data_loader.get_all_questions(data_loader.load_test_part(test_num, completed_skill, p)))
                
                session[test_key]['completed'] = True
                session[test_key]['total_score'] = total_score
                session[test_key]['max_score'] = max_score_total
                session.modified = True
                
                # Mark attempt as completed in JSON tracking
                if 'user_email' in session:
                    attempt_id = session[test_key].get('attempt_id', str(uuid.uuid4()))
                    results_tracker.complete_test_attempt(
                        user_email=session['user_email'],
                        test_num=test_num,
                        attempt_id=attempt_id
                    )
            
            return jsonify({
                'show_skill_score': True,
                'skill_total': skill_total,
                'skill_max': skill_max,
                'skill_percentage': skill_percentage,
                'skill': skill,
                'is_final': not has_next_skill
            })
        else:
            # Move to next part
            current_index = skill_parts.index(part_num)
            next_part = skill_parts[current_index + 1]
            
            return jsonify({
                'show_skill_score': False,
                'next_part': next_part,
                'test_num': test_num,
                'skill': skill
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 400


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
        
        # Save score to session (use string keys for consistency)
        if 'scores' not in session:
            session['scores'] = {}
        
        test_key = f'test_{test_num}'
        if test_key not in session['scores']:
            session['scores'][test_key] = {}
        if skill not in session['scores'][test_key]:
            session['scores'][test_key][skill] = {}
        
        # Convert part_num to string to avoid mixing int/str keys in session
        session['scores'][test_key][skill][str(part_num)] = score
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
        # Calculate max possible score for all available parts
        try:
            skill_max = sum([len(data_loader.get_all_questions(data_loader.load_test_part(test_num, skill, p))) 
                             for p in skill_parts])
        except:
            skill_max = len(skill_parts) * 10  # Fallback estimation
        
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
    import os
    import sys
    
    # Get host and port from environment variables or command line
    # Default to localhost only for security
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', 5000))
    
    # Check for command line arguments
    if '--host' in sys.argv:
        idx = sys.argv.index('--host')
        if idx + 1 < len(sys.argv):
            host = sys.argv[idx + 1]
    if '--port' in sys.argv:
        idx = sys.argv.index('--port')
        if idx + 1 < len(sys.argv):
            port = int(sys.argv[idx + 1])
    
    print(f"\n{'='*60}")
    print(f"🚀 CELPIP Practice Test Platform")
    print(f"{'='*60}")
    print(f"📍 Running on: http://{host}:{port}")
    
    if host == '0.0.0.0':
        # Show local network IP for convenience
        import socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            print(f"🌐 Network access: http://{local_ip}:{port}")
            print(f"📱 Share this URL with devices on your network!")
        except:
            print(f"🌐 Network access enabled on all interfaces")
    else:
        print(f"🔒 Localhost only (use --host 0.0.0.0 for network access)")
    
    print(f"{'='*60}\n")
    
    app.run(
        host=host,
        port=port,
        debug=True
    )
