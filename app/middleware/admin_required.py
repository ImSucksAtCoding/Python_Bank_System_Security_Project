""" middleware/admin_required.py
Admin authorization middleware
"""

from functools import wraps
from flask import session
from config.settings import get_security_mode

def admin_required(f):
    """Decorator to require admin privileges"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if get_security_mode() == 'secured':
            if 'user_id' not in session or session.get('is_admin') != 1:
                return "Access Denied - Admin privileges required", 403
        else:
            if session.get('is_admin') != 1:
                return "Access Denied", 403
        return f(*args, **kwargs)
    return decorated