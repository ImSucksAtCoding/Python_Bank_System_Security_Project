""" services/auth_service.py
Authentication service to support auth routes (login, register, logout)
"""

import secrets
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash, generate_password_hash
from config.settings import get_security_mode
from config.database import get_db_connection
from services.validators import validate_username, validate_password

"""Authenticate user - handles both vulnerable and secured modes"""
def authenticate_user(username, password):
    conn = get_db_connection()
    c = conn.cursor()
    
    mode = get_security_mode()
    
    if mode == 'vulnerable':
        # [X] VULNERABLE: SQL Injection
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        try:
            c.execute(query)
            user = c.fetchone()
        except:
            conn.close()
            return {'success': False, 'error': 'Database error'}
        
        if user:
            conn.close()
            return {
                'success': True,
                'user_id': user[0],
                'username': user[1],
                'is_admin': user[6]
            }
        else:
            conn.close()
            return {'success': False, 'error': 'Invalid credentials'}
    
    else:  # SECURED MODE (include fail attempts, account lock time and secured SQL query)
        if not validate_username(username):
            conn.close()
            return {'success': False, 'error': 'Invalid username format'}
        
        c.execute("SELECT locked_until, failed_attempts FROM users WHERE username=?", (username,))
        lock_info = c.fetchone()
        
        # If current time < locked_until, display error message
        if lock_info and lock_info[0]:
            locked_until = datetime.strptime(lock_info[0], '%Y-%m-%d %H:%M:%S')
            if datetime.now() < locked_until:
                conn.close()
                return {'success': False, 'error': 'Account locked. Try again later.'}
        
        # Else, execute query (safe practice with parameterized query)
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
        
        if user and check_password_hash(user[3], password):
            session_token = secrets.token_hex(32)
            c.execute("""UPDATE users SET failed_attempts=0, locked_until=NULL, 
                         session_token=? WHERE id=?""", (session_token, user[0]))
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'user_id': user[0],
                'username': user[1],
                'is_admin': user[6],
                'session_token': session_token
            }
        else:
            if user:
                failed = (lock_info[1] if lock_info else 0) + 1
                if failed >= 5:
                    locked_until = (datetime.now() + timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M:%S')
                    c.execute("UPDATE users SET failed_attempts=?, locked_until=? WHERE username=?", 
                             (failed, locked_until, username))
                else:
                    c.execute("UPDATE users SET failed_attempts=? WHERE username=?", (failed, username))
                conn.commit()
            
            conn.close()
            return {'success': False, 'error': 'Invalid credentials'}

"""Register new user - handles both vulnerable and secured modes"""      
def register_user(username, password):
    conn = get_db_connection()
    c = conn.cursor()
    
    # Get mode
    mode = get_security_mode()
    
    if mode == 'vulnerable':
        # [X] VULNERABLE: XSS allowed but SQL quotes escaped to prevent breakage
        # This allows XSS payloads while keeping SQL functional
        username_sql_safe = username.replace("'", "''")  # Escape single quotes for SQL only

        query = f"INSERT INTO users (username, password, password_hash, balance, account_type, is_admin) VALUES ('{username_sql_safe}', '{password}', '', 1000.00, 'Checking', 0)"
        try:
            c.execute(query)
            conn.commit()
            conn.close()
            return {'success': True}
        except Exception as e:
            conn.close()
            return {'success': False, 'error': f'Registration failed ! Error: {str(e)}'}
    
    else:  # SECURED MODE (Validate username and password, password hashing before storing into database)
        if not validate_username(username):
            conn.close()
            return {'success': False, 'error': 'Username must be 3-50 characters, alphanumeric only'}
        
        if not validate_password(password):
            conn.close()
            return {'success': False, 'error': 'Password must be at least 6 characters'}
        
        # Password hashing
        hashed_pw = generate_password_hash(password)
        
        try:
            # Best practice: Use parameterized SQL query
            c.execute("""INSERT INTO users 
                         (username, password, password_hash, balance, account_type, is_admin) 
                         VALUES (?, ?, ?, ?, ?, ?)""",
                     (username, password, hashed_pw, 1000.00, 'Checking', 0))
            conn.commit()
            conn.close()
            return {'success': True}
        except:
            conn.close()
            return {'success': False, 'error': 'Username already exists'}
