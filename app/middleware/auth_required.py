""" middleware/auth_required.py
Authentication required middleware
"""

from functools import wraps
from flask import session, redirect, url_for
from services.session_service import validate_session

def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        
        if not validate_session():
            session.clear()
            return redirect(url_for('auth.login'))
        
        return f(*args, **kwargs)
    return decorated