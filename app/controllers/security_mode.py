""" controllers/security_mode.py
Security mode controller - handles mode switching
"""

from flask import Blueprint, request, redirect, url_for, session
from config.settings import set_security_mode, configure_app, WEAK_SECRET, STRONG_SECRET
from flask import current_app

security_bp = Blueprint('security', __name__)

# Security toggle route
@security_bp.route('/toggle_security', methods=['POST'])
def toggle_security():
    mode = request.form.get('mode', 'vulnerable')
    
    if set_security_mode(mode):
        # Update app configuration
        if mode == 'secured':
            current_app.secret_key = STRONG_SECRET
            current_app.config['SESSION_COOKIE_HTTPONLY'] = True
            current_app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
        else:
            current_app.secret_key = WEAK_SECRET
            current_app.config['SESSION_COOKIE_HTTPONLY'] = False
            current_app.config['SESSION_COOKIE_SAMESITE'] = None
        
        # Clear sessions when switching
        session.clear()
    
    return redirect(url_for('auth.login'))