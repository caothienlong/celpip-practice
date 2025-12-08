"""
Authentication Module
Handles OAuth login with Google, Facebook, and other providers
"""
from functools import wraps
from flask import redirect, url_for, session
from flask_login import LoginManager, UserMixin, current_user


class User(UserMixin):
    """User model for Flask-Login"""
    
    def __init__(self, user_id, email, name=None, provider=None, profile_data=None):
        self.id = user_id
        self.email = email
        self.name = name
        self.provider = provider  # 'google', 'facebook', 'email', etc.
        self.profile_data = profile_data or {}
    
    def get_id(self):
        """Return user ID as string"""
        return str(self.id)
    
    def __repr__(self):
        return f'<User {self.email}>'


def init_auth(app, results_tracker):
    """
    Initialize authentication system
    
    Args:
        app: Flask application
        results_tracker: ResultsTracker instance for user management
    """
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.session_protection = 'strong'  # Stronger session protection
    
    @login_manager.user_loader
    def load_user(user_id):
        """Load user from user_id (email)"""
        try:
            profile = results_tracker.get_user_profile(user_id)
            if profile and profile.get('email'):
                return User(
                    user_id=profile['email'],
                    email=profile['email'],
                    name=profile.get('name'),
                    provider=profile.get('provider'),
                    profile_data=profile
                )
        except Exception as e:
            print(f"Error loading user {user_id}: {e}")
        return None
    
    return login_manager


def login_required_optional(f):
    """
    Decorator that allows access but saves user info if logged in
    Used for optional authentication (session-only mode still works)
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Store whether user is logged in
        if current_user.is_authenticated:
            session['user_email'] = current_user.email
        return f(*args, **kwargs)
    return decorated_function


def get_current_user_email():
    """
    Get current user's email
    Returns email from authenticated user or session
    """
    if current_user.is_authenticated:
        return current_user.email
    return session.get('user_email')

