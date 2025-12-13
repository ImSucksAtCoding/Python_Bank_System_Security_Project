"""
services/validators.py
A simple validator module to validate username and password inputs
"""
import re

def validate_username(username):
    """Validate username format"""
    if not username or len(username) < 3 or len(username) > 50:
        return False
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False
    return True

def validate_password(password):
    """Validate password strength"""
    if not password or len(password) < 6:
        return False
    return True