""" services/session_service.py
Session management service
"""

from flask import session
from config.settings import get_security_mode
from config.database import get_db_connection

"""Validate session token against database"""
def validate_session():
    if get_security_mode() == 'vulnerable':
        return True
    
    if 'user_id' not in session or 'session_token' not in session:
        return False
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT session_token FROM users WHERE id=?", (session['user_id'],))
    result = c.fetchone()
    conn.close()
    
    if not result or result[0] != session['session_token']:
        return False
    
    return True

"""Clear session and update database"""
def clear_session():
    if get_security_mode() == 'secured' and 'user_id' in session:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("UPDATE users SET session_token=NULL WHERE id=?", (session['user_id'],))
        conn.commit()
        conn.close()
    
    session.clear()