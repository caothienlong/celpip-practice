from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import secrets
import uuid
import os
from dotenv import load_dotenv
from utils.data_loader import TestDataLoader
from utils.results_tracker import ResultsTracker
from utils.auth import init_auth, User, login_required_optional, get_current_user_email
from utils.oauth_providers import init_oauth, get_oauth_providers, extract_user_info
from flask_login import login_user, logout_user, current_user
from config import calculate_timeout, get_timeout

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', secrets.token_hex(32))

# Session configuration for proper logout
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24 hours
app.config['SESSION_REFRESH_EACH_REQUEST'] = True

# Initialize data loader and results tracker
data_loader = TestDataLoader(data_dir='data')
results_tracker = ResultsTracker(users_dir='users')

# Initialize authentication
login_manager = init_auth(app, results_tracker)

# Initialize OAuth
oauth = init_oauth(app)


# ============================================================================
# AUTHENTICATION ROUTES
# ============================================================================

@app.route('/login')
def login():
    """Display login page with OAuth options"""
    providers = get_oauth_providers()
    error = request.args.get('error')
    return render_template('login.html', providers=providers, error=error)


@app.route('/login/<provider>')
def oauth_login(provider):
    """Initiate OAuth login with provider"""
    try:
        oauth_provider = oauth.create_client(provider)
        redirect_uri = url_for('oauth_callback', provider=provider, _external=True)
        return oauth_provider.authorize_redirect(redirect_uri)
    except Exception as e:
        return redirect(url_for('login', error=f'Failed to connect to {provider}'))


@app.route('/callback/<provider>')
def oauth_callback(provider):
    """Handle OAuth callback from provider"""
    try:
        oauth_provider = oauth.create_client(provider)
        token = oauth_provider.authorize_access_token()
        
        # Get user info
        if provider == 'google':
            user_info_raw = token.get('userinfo')
        elif provider == 'facebook':
            resp = oauth_provider.get('me?fields=id,name,email')
            user_info_raw = resp.json()
        else:
            user_info_raw = {}
        
        # Extract user information
        user_info = extract_user_info(provider, user_info_raw)
        
        if not user_info.get('email'):
            return redirect(url_for('login', error='Could not get email from provider'))
        
        # Create or update user
        email = user_info['email']
        profile = results_tracker.get_user_profile(email)
        
        # Update profile with OAuth info
        profile['name'] = user_info.get('name', profile.get('name'))
        profile['provider'] = provider
        profile['picture'] = user_info.get('picture')
        
        # Save profile
        results_tracker._save_user_profile(email, profile)
        
        # Create User object and login
        user = User(
            user_id=email,
            email=email,
            name=user_info.get('name'),
            provider=provider,
            profile_data=profile
        )
        login_user(user, remember=True)
        
        # Set session email for backwards compatibility
        session['user_email'] = email
        session.modified = True
        
        return redirect(url_for('index'))
        
    except Exception as e:
        print(f"OAuth callback error: {e}")
        return redirect(url_for('login', error='Authentication failed. Please try again.'))


@app.route('/logout')
def logout():
    """Logout user and clear all session data"""
    # Get all session keys to clear
    session_keys = list(session.keys())
    
    # Logout Flask-Login user
    logout_user()
    
    # Clear each session key explicitly
    for key in session_keys:
        session.pop(key, None)
    
    # Also clear the entire session
    session.clear()
    
    # Create response with cache busting
    response = redirect(url_for('index'))
    
    # Prevent caching
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    # Delete session cookie explicitly
    response.set_cookie('session', '', expires=0, max_age=0)
    
    return response


# ============================================================================
# MAIN ROUTES
# ============================================================================

@app.route('/')
@login_required_optional
def index():
    """Home page showing all available tests"""
    available_tests = data_loader.list_available_tests()
    
    # Get exam completion status and scores from session
    # Only show if session has valid data
    exam_status = {}
    for test_num in available_tests:
        test_key = f'exam_{test_num}'
        
        # Check if the exam data exists and is valid
        if test_key in session and session[test_key]:
            if session[test_key].get('completed'):
                exam_status[test_num] = {
                    'completed': True,
                    'in_progress': False,
                    'total_score': session[test_key].get('total_score', 0),
                    'max_score': session[test_key].get('max_score', 0)
                }
            elif session[test_key].get('current_skill'):
                # Only show in_progress if there's actually progress data
                exam_status[test_num] = {
                    'completed': False,
                    'in_progress': True,
                    'current_skill': session[test_key].get('current_skill', 'reading'),
                    'current_part': session[test_key].get('current_part', 1)
                }
            else:
                # No valid data
                exam_status[test_num] = {
                    'completed': False,
                    'in_progress': False
                }
        else:
            exam_status[test_num] = {
                'completed': False,
                'in_progress': False
            }
    
    # Get historical data from JSON ONLY if user is authenticated
    # Guest mode should not show any historical data
    test_history = {}
    user_email = None
    
    if current_user.is_authenticated:
        user_email = current_user.email
        test_history = results_tracker.get_all_tests_summary(user_email)
    
    return render_template('test_list.html', 
                         test_numbers=available_tests,
                         exam_status=exam_status,
                         test_history=test_history,
                         user_email=user_email,
                         current_user=current_user)


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
    """Start or Resume Test Mode"""
    # Test Mode works for both logged in and guest users
    # Logged in: History saved permanently
    # Guest: History saved in session only
    
    test_key = f'exam_{test_num}'
    
    # Check if there's an existing in-progress exam
    if test_key in session and not session[test_key].get('completed', False):
        # Resume existing exam - get current position
        current_skill = session[test_key].get('current_skill', 'reading')
        current_part = session[test_key].get('current_part', 1)
        
        # Redirect to current position
        return test_mode_part(test_num, current_skill, current_part)
    
    # Start new exam - generate unique attempt ID
    attempt_id = str(uuid.uuid4())
    
    # Initialize new exam session
    session[test_key] = {
        'mode': 'exam',
        'current_skill': 'reading',
        'current_part': 1,
        'scores': {},
        'completed': False,
        'attempt_id': attempt_id
    }
    session.modified = True
    
    # Create user in tracking system (only if logged in)
    user_email = get_current_user_email()
    if user_email:
        results_tracker.get_or_create_user(user_email)
    
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
        
        # Save current position in session
        test_key = f'exam_{test_num}'
        if test_key in session:
            session[test_key]['current_skill'] = skill
            session[test_key]['current_part'] = part_num
            session.modified = True
        
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
        
        # Get saved answers for this part from session
        test_key = f'test_{test_num}'
        saved_answers = session.get('answers', {}).get(test_key, {}).get(skill, {}).get(str(part_num), {})
        
        return render_template(
            'test_section.html',
            section=processed_data,
            test_num=test_num,
            skill=skill,
            part_num=part_num,
            saved_answers=saved_answers
        )
    except FileNotFoundError as e:
        return f"Test not found: {e}", 404
    except Exception as e:
        return f"Error loading test: {e}", 500


@app.route('/test/<int:test_num>/<skill>/part<int:part_num>/answers')
def answer_key(test_num, skill, part_num):
    """
    Display answer key for a specific test part (Practice Mode only)
    
    Args:
        test_num: Test number (1-20)
        skill: Skill name (reading, writing, speaking, listening)
        part_num: Part number
    """
    try:
        # Load test data from JSON
        test_data = data_loader.load_test_part(test_num, skill, part_num)
        
        # Process the test data for answer key display
        processed_data = prepare_answer_key_data(test_data, skill, part_num)
        
        # Determine next part
        next_part = None
        skill_parts = data_loader.list_available_parts(test_num, skill)
        if part_num in skill_parts:
            current_index = skill_parts.index(part_num)
            if current_index + 1 < len(skill_parts):
                next_part = skill_parts[current_index + 1]
        
        return render_template(
            'answer_key.html',
            section=processed_data,
            test_num=test_num,
            skill=skill,
            part_num=part_num,
            next_part=next_part
        )
    except FileNotFoundError as e:
        return f"Test not found: {e}", 404
    except Exception as e:
        return f"Error loading answer key: {e}", 500


@app.route('/test/<int:test_num>/<skill>/answer-key')
def comprehensive_answer_key(test_num, skill):
    """
    Display comprehensive answer key for all parts of a skill
    Shows correct answers, user answers, and comparison
    """
    try:
        # Get all parts for this skill
        skill_parts = data_loader.list_available_parts(test_num, skill)
        
        # Get user's saved answers from session (try both Practice and Test Mode)
        test_key = f'test_{test_num}'
        exam_key = f'exam_{test_num}'
        
        # Check if this is from Test Mode or Practice Mode
        is_test_mode = exam_key in session.get('exam_answers', {})
        
        if is_test_mode:
            saved_answers = session.get('exam_answers', {}).get(exam_key, {}).get(skill, {})
        else:
            saved_answers = session.get('answers', {}).get(test_key, {}).get(skill, {})
        
        parts_data = []
        total_questions = 0
        correct_answers = 0
        incorrect_answers = 0
        unanswered = 0
        
        for part_num in skill_parts:
            # Load test data
            test_data = data_loader.load_test_part(test_num, skill, part_num)
            all_questions = data_loader.get_all_questions(test_data)
            correct_answer_map = data_loader.get_correct_answers(test_data)
            
            # Get user's answers for this part
            part_answers = saved_answers.get(str(part_num), {})
            
            # Build questions list with answers
            questions_list = []
            for q in all_questions:
                q_id = q['id']  # Use int
                q_id_str = str(q_id)  # String version for part_answers lookup
                correct_idx = correct_answer_map.get(q_id)
                # Convert user answer to int if it's a string
                user_answer_idx = part_answers.get(q_id_str)
                if user_answer_idx is not None:
                    user_answer_idx = int(user_answer_idx) if isinstance(user_answer_idx, str) else user_answer_idx
                
                # Get answer texts
                correct_answer_text = q['options'][correct_idx] if correct_idx is not None else '—'
                user_answer_text = q['options'][user_answer_idx] if user_answer_idx is not None and user_answer_idx < len(q['options']) else None
                
                is_correct = user_answer_idx == correct_idx if user_answer_idx is not None else False
                
                questions_list.append({
                    'question_text': f"Q{q['id']}. {q.get('text', q.get('question', ''))}",
                    'correct_answer_text': correct_answer_text,
                    'user_answer_text': user_answer_text,
                    'is_correct': is_correct
                })
                
                total_questions += 1
                if user_answer_text is None:
                    unanswered += 1
                elif is_correct:
                    correct_answers += 1
                else:
                    incorrect_answers += 1
            
            parts_data.append({
                'part_num': part_num,
                'title': test_data.get('title', f'Part {part_num}'),
                'questions': questions_list
            })
        
        # Calculate summary
        percentage = round((correct_answers / total_questions) * 100, 1) if total_questions > 0 else 0
        
        summary = {
            'total_questions': total_questions,
            'correct_answers': correct_answers,
            'incorrect_answers': incorrect_answers,
            'unanswered': unanswered,
            'percentage': percentage
        }
        
        return render_template(
            'comprehensive_answer_key.html',
            test_num=test_num,
            skill=skill,
            parts_data=parts_data,
            summary=summary,
            is_test_mode=is_test_mode
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


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
                questions_section['questions'],
                test_type='information'
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


def prepare_answer_key_data(test_data, skill, part_num):
    """
    Prepare test data for answer key display
    
    Args:
        test_data: Raw test data from JSON
        skill: Skill name
        part_num: Part number
        
    Returns:
        dict: Processed data ready for answer key template
    """
    # Get all questions
    all_questions = data_loader.get_all_questions(test_data)
    correct_answers = data_loader.get_correct_answers(test_data)
    
    processed = {
        'title': f"Part {part_num}: {test_data['title']}",
        'instructions': test_data['instructions'],
        'type': test_data['type'],
        'all_questions': []
    }
    
    # Process based on test type
    if test_data['type'] == 'correspondence':
        # Part 1: Reading Correspondence
        passage_section = data_loader.get_section_by_type(test_data, 'passage')
        response_section = data_loader.get_section_by_type(test_data, 'response_passage')
        questions_section = data_loader.get_section_by_type(test_data, 'questions')
        
        if passage_section:
            processed['passage'] = passage_section['content']
        
        processed['questions_1_6'] = []
        processed['questions_7_11'] = []
        
        if questions_section:
            for q in questions_section['questions']:
                q_data = {
                    'id': q['id'],
                    'text': q.get('text', q.get('question', f"Question {q['id']}")),
                    'options': [(idx, opt) for idx, opt in enumerate(q['options'])],
                    'correct_answer': correct_answers.get(q['id'])
                }
                processed['questions_1_6'].append(q_data)
        
        if response_section and 'questions' in response_section:
            for q in response_section['questions']:
                q_data = {
                    'id': q['id'],
                    'text': q.get('question', f"Question {q['id']}"),
                    'options': [(idx, opt) for idx, opt in enumerate(q['options'])],
                    'correct_answer': correct_answers.get(q['id'])
                }
                processed['questions_7_11'].append(q_data)
    
    elif test_data['type'] == 'diagram':
        # Part 2: Reading to Apply a Diagram
        diagram_section = data_loader.get_section_by_type(test_data, 'diagram_email')
        questions_section = data_loader.get_section_by_type(test_data, 'questions')
        
        processed['has_diagram'] = True
        
        if diagram_section:
            processed['diagram_image'] = diagram_section.get('diagram_image')
            processed['email_text'] = diagram_section['content']
        
        # Collect all questions
        if diagram_section and 'questions' in diagram_section:
            for q in diagram_section['questions']:
                q_data = {
                    'id': q['id'],
                    'text': q.get('question', f"Question {q['id']}"),
                    'options': [(idx, opt) for idx, opt in enumerate(q['options'])],
                    'correct_answer': correct_answers.get(q['id'])
                }
                processed['all_questions'].append(q_data)
        
        if questions_section:
            for q in questions_section['questions']:
                q_data = {
                    'id': q['id'],
                    'text': q.get('text', q.get('question', f"Question {q['id']}")),
                    'options': [(idx, opt) for idx, opt in enumerate(q['options'])],
                    'correct_answer': correct_answers.get(q['id'])
                }
                processed['all_questions'].append(q_data)
    
    elif test_data['type'] == 'information':
        # Part 3: Reading for Information
        passage_section = data_loader.get_section_by_type(test_data, 'passage')
        questions_section = data_loader.get_section_by_type(test_data, 'questions')
        
        processed['is_information_type'] = True
        
        if passage_section:
            processed['passage'] = passage_section['content']
            processed['passage_note'] = passage_section.get('note', '')
        
        if questions_section:
            for q in questions_section['questions']:
                q_data = {
                    'id': q['id'],
                    'text': q.get('text', q.get('question', f"Question {q['id']}")),
                    'options': [(idx, opt) for idx, opt in enumerate(q['options'])],
                    'correct_answer': correct_answers.get(q['id'])
                }
                processed['all_questions'].append(q_data)
    
    elif test_data['type'] == 'viewpoints':
        # Part 4: Reading for Viewpoints
        passage_section = data_loader.get_section_by_type(test_data, 'passage')
        questions_section = data_loader.get_section_by_type(test_data, 'questions')
        response_section = data_loader.get_section_by_type(test_data, 'response_passage')
        
        processed['is_viewpoints_type'] = True
        
        if passage_section:
            processed['passage'] = passage_section['content']
        
        if questions_section:
            for q in questions_section['questions']:
                q_data = {
                    'id': q['id'],
                    'text': q.get('text', q.get('question', f"Question {q['id']}")),
                    'options': [(idx, opt) for idx, opt in enumerate(q['options'])],
                    'correct_answer': correct_answers.get(q['id'])
                }
                processed['all_questions'].append(q_data)
        
        processed['response_passage_questions'] = []
        if response_section and 'questions' in response_section:
            processed['response_title'] = response_section.get('title', 'Response')
            processed['section_divider_text'] = response_section.get('instruction_text', '')
            
            for q in response_section['questions']:
                q_data = {
                    'id': q['id'],
                    'text': q.get('question', f"Question {q['id']}"),
                    'options': [(idx, opt) for idx, opt in enumerate(q['options'])],
                    'correct_answer': correct_answers.get(q['id'])
                }
                processed['response_passage_questions'].append(q_data)
    
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
            
            # Update session with next position
            session[test_key]['current_part'] = next_part
            session.modified = True
            
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
        
        # Get correct answers (returns {int: int})
        correct_answers = data_loader.get_correct_answers(test_data)
        
        # Convert answers keys to int for comparison
        int_answers = {int(k): int(v) for k, v in answers.items()}
        
        # Calculate score
        score = 0
        results = {}
        
        for question_id, user_answer in int_answers.items():
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


@app.route('/save_answer', methods=['POST'])
def save_answer():
    """
    Save a single answer to session (auto-save when dropdown changes)
    
    Request JSON:
        {
            "test_num": 1,
            "skill": "reading",
            "part_num": 1,
            "question_id": "1",
            "answer": 0
        }
    
    Returns:
        JSON with success status
    """
    data = request.json
    test_num = data.get('test_num')
    skill = data.get('skill')
    part_num = data.get('part_num')
    question_id = str(data.get('question_id'))
    answer = data.get('answer')
    
    try:
        # Initialize session structure if needed
        if 'answers' not in session:
            session['answers'] = {}
        
        test_key = f'test_{test_num}'
        if test_key not in session['answers']:
            session['answers'][test_key] = {}
        if skill not in session['answers'][test_key]:
            session['answers'][test_key][skill] = {}
        if str(part_num) not in session['answers'][test_key][skill]:
            session['answers'][test_key][skill][str(part_num)] = {}
        
        # Save the answer
        session['answers'][test_key][skill][str(part_num)][question_id] = answer
        session.modified = True
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/reset_test/<int:test_num>/<skill>', methods=['POST'])
def reset_test(test_num, skill):
    """
    Reset a test by clearing all saved answers for that test and skill
    
    Args:
        test_num: Test number (1-20)
        skill: Skill name (reading, writing, speaking, listening)
    
    Returns:
        JSON with success status
    """
    try:
        test_key = f'test_{test_num}'
        
        # Clear answers from session
        if 'answers' in session and test_key in session['answers']:
            if skill in session['answers'][test_key]:
                del session['answers'][test_key][skill]
                # Clean up if no skills left
                if not session['answers'][test_key]:
                    del session['answers'][test_key]
        
        # Clear scores from session (if any)
        if 'scores' in session and test_key in session['scores']:
            if skill in session['scores'][test_key]:
                del session['scores'][test_key][skill]
                # Clean up if no skills left
                if not session['scores'][test_key]:
                    del session['scores'][test_key]
        
        session.modified = True
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/save_test_mode_answer', methods=['POST'])
def save_test_mode_answer():
    """
    Save a single answer to session in Test Mode (auto-save when dropdown changes)
    Uses exam_<test_num> key to separate from Practice Mode
    
    Request JSON:
        {
            "test_num": 1,
            "skill": "reading",
            "part_num": 1,
            "question_id": "1",
            "answer": 0
        }
    
    Returns:
        JSON with success status
    """
    data = request.json
    test_num = data.get('test_num')
    skill = data.get('skill')
    part_num = data.get('part_num')
    question_id = str(data.get('question_id'))
    answer = data.get('answer')
    
    try:
        # Initialize session structure for Test Mode
        if 'exam_answers' not in session:
            session['exam_answers'] = {}
        
        test_key = f'exam_{test_num}'
        if test_key not in session['exam_answers']:
            session['exam_answers'][test_key] = {}
        if skill not in session['exam_answers'][test_key]:
            session['exam_answers'][test_key][skill] = {}
        if str(part_num) not in session['exam_answers'][test_key][skill]:
            session['exam_answers'][test_key][skill][str(part_num)] = {}
        
        # Save the answer
        session['exam_answers'][test_key][skill][str(part_num)][question_id] = answer
        session.modified = True
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# Legacy routes for backward compatibility
@app.route('/test1/part1')
def test1_part1():
    """Redirect to new route format"""
    return test_part(1, 'reading', 1)


@app.route('/test1/part2')
def test1_part2():
    """Redirect to new route format"""
    return test_part(1, 'reading', 2)


# ============================================================================
# VOCABULARY NOTES ROUTES
# ============================================================================

@app.route('/save_vocabulary_note', methods=['POST'])
@login_required_optional
def save_vocabulary_note():
    """Save a vocabulary note"""
    # Check if user is authenticated
    if not current_user.is_authenticated:
        return jsonify({'success': False, 'error': 'Please login to save vocabulary notes'}), 401
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['test_num', 'skill', 'part_num', 'word', 'definition']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing field: {field}'}), 400
        
        # Save note
        note_id = results_tracker.save_vocabulary_note(
            user_email=current_user.email,
            test_num=int(data['test_num']),
            skill=data['skill'],
            part_num=int(data['part_num']),
            word=data['word'],
            definition=data['definition'],
            context=data.get('context', '')
        )
        
        return jsonify({
            'success': True,
            'note_id': note_id,
            'message': 'Vocabulary note saved!'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/get_vocabulary_notes', methods=['GET'])
@login_required_optional
def get_vocabulary_notes_route():
    """Get vocabulary notes with optional filtering"""
    # Check if user is authenticated
    if not current_user.is_authenticated:
        return jsonify({'success': False, 'notes': [], 'error': 'Please login to view notes'}), 401
    
    try:
        # Get filter parameters
        test_num = request.args.get('test_num', type=int)
        skill = request.args.get('skill', type=str)
        part_num = request.args.get('part_num', type=int)
        
        # Get notes
        notes = results_tracker.get_vocabulary_notes(
            user_email=current_user.email,
            test_num=test_num,
            skill=skill,
            part_num=part_num
        )
        
        return jsonify({
            'success': True,
            'notes': notes,
            'count': len(notes)
        })
    
    except Exception as e:
        return jsonify({'success': False, 'notes': [], 'error': str(e)}), 500


@app.route('/delete_vocabulary_note', methods=['POST'])
@login_required_optional
def delete_vocabulary_note_route():
    """Delete a vocabulary note"""
    # Check if user is authenticated
    if not current_user.is_authenticated:
        return jsonify({'success': False, 'error': 'Authentication required'}), 401
    
    try:
        data = request.get_json()
        note_id = data.get('note_id')
        
        if not note_id:
            return jsonify({'success': False, 'error': 'Missing note_id'}), 400
        
        # Delete note
        deleted = results_tracker.delete_vocabulary_note(
            user_email=current_user.email,
            note_id=note_id
        )
        
        if deleted:
            return jsonify({
                'success': True,
                'message': 'Note deleted successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Note not found'
            }), 404
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/update_vocabulary_note', methods=['POST'])
@login_required_optional
def update_vocabulary_note_route():
    """Update a vocabulary note"""
    # Check if user is authenticated
    if not current_user.is_authenticated:
        return jsonify({'success': False, 'error': 'Authentication required'}), 401
    
    try:
        data = request.get_json()
        note_id = data.get('note_id')
        
        if not note_id:
            return jsonify({'success': False, 'error': 'Missing note_id'}), 400
        
        # Update note
        updated = results_tracker.update_vocabulary_note(
            user_email=current_user.email,
            note_id=note_id,
            word=data.get('word'),
            definition=data.get('definition'),
            context=data.get('context')
        )
        
        if updated:
            return jsonify({
                'success': True,
                'message': 'Note updated successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Note not found'
            }), 404
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/test/<int:test_num>/vocabulary')
@login_required_optional
def vocabulary_notes_page(test_num):
    """Display all vocabulary notes for a test"""
    # Check if user is authenticated
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    try:
        # Get all notes for this test
        notes = results_tracker.get_vocabulary_notes(
            user_email=current_user.email,
            test_num=test_num
        )
        
        # Group notes by part
        notes_by_part = {}
        for note in notes:
            part_key = f"{note['skill']}_part_{note['part_num']}"
            if part_key not in notes_by_part:
                notes_by_part[part_key] = {
                    'skill': note['skill'],
                    'part_num': note['part_num'],
                    'notes': []
                }
            notes_by_part[part_key]['notes'].append(note)
        
        return render_template(
            'vocabulary_notes.html',
            test_num=test_num,
            notes_by_part=notes_by_part,
            total_notes=len(notes),
            current_user=current_user
        )
    
    except Exception as e:
        return f"Error loading vocabulary notes: {str(e)}", 500


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
