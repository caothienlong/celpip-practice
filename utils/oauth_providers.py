"""
OAuth Integration Module
Handles OAuth flows for Google, Facebook, and other providers
"""
import os
from authlib.integrations.flask_client import OAuth
from flask import url_for


def init_oauth(app):
    """
    Initialize OAuth for multiple providers
    
    Returns:
        OAuth instance configured with providers
    """
    oauth = OAuth(app)
    
    # Google OAuth
    oauth.register(
        name='google',
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
    
    # Facebook OAuth
    oauth.register(
        name='facebook',
        client_id=os.getenv('FACEBOOK_CLIENT_ID'),
        client_secret=os.getenv('FACEBOOK_CLIENT_SECRET'),
        access_token_url='https://graph.facebook.com/oauth/access_token',
        access_token_params=None,
        authorize_url='https://www.facebook.com/dialog/oauth',
        authorize_params=None,
        api_base_url='https://graph.facebook.com/',
        client_kwargs={'scope': 'email public_profile'},
    )
    
    return oauth


def get_oauth_providers():
    """
    Get list of available OAuth providers
    
    Returns:
        List of dictionaries with provider info
    """
    providers = []
    
    if os.getenv('GOOGLE_CLIENT_ID'):
        providers.append({
            'name': 'google',
            'display_name': 'Google',
            'icon': '🔵',
            'color': '#4285f4'
        })
    
    if os.getenv('FACEBOOK_CLIENT_ID'):
        providers.append({
            'name': 'facebook',
            'display_name': 'Facebook',
            'icon': '📘',
            'color': '#1877f2'
        })
    
    return providers


def extract_user_info(provider, token_data):
    """
    Extract user information from OAuth token data
    
    Args:
        provider: Provider name ('google', 'facebook', etc.)
        token_data: Token data from OAuth provider
    
    Returns:
        Dictionary with user info (email, name, etc.)
    """
    if provider == 'google':
        return {
            'email': token_data.get('email'),
            'name': token_data.get('name'),
            'picture': token_data.get('picture'),
            'provider': 'google',
            'provider_user_id': token_data.get('sub')
        }
    
    elif provider == 'facebook':
        return {
            'email': token_data.get('email'),
            'name': token_data.get('name'),
            'picture': token_data.get('picture', {}).get('data', {}).get('url'),
            'provider': 'facebook',
            'provider_user_id': token_data.get('id')
        }
    
    return {}

