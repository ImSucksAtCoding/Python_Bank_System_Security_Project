"""
controllers/auth_controller.py
Authentication controller - handles login and registration
"""

from flask import Blueprint, request, render_template, session, redirect, url_for
from config.settings import get_security_mode
from config.database import get_db_connection
from services.auth_service import authenticate_user, register_user
from services.api_rate_limiter import rate_limit

auth_bp = Blueprint('auth', __name__)

# Main auth routes
@auth_bp.route('/')

# Login route (with API rate limiter)
@auth_bp.route('/login', methods=['GET', 'POST'])
@rate_limit(max_requests=10, window=60)
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        result = authenticate_user(username, password)
        
        if result['success']:
            session['user_id'] = result['user_id']
            session['username'] = result['username']
            session['is_admin'] = result['is_admin']
            if 'session_token' in result:
                session['session_token'] = result['session_token']
            
            if result['is_admin'] == 1:
                return redirect(url_for('admin.admin_dashboard'))
            return redirect(url_for('dashboard.dashboard'))
        else:
            return render_template('login.html', error=result['error'], mode=get_security_mode())
    
    return render_template('login.html', mode=get_security_mode())

# Register route (with API rate limiter)
@auth_bp.route('/register', methods=['GET', 'POST'])
@rate_limit(max_requests=3, window=300)
def register():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        result = register_user(username, password)
        
        if result['success']:
            return redirect(url_for('auth.login'))
        else:
            return render_template('register.html', error=result['error'], mode=get_security_mode())
    
    return render_template('register.html', mode=get_security_mode())

# Logout route
@auth_bp.route('/logout')
def logout():
    from services.session_service import clear_session
    clear_session()
    return redirect(url_for('auth.login'))
