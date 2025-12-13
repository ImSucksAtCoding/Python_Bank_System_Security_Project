"""
config/settings.py

Settings module to enable webapp security mode changed between 'vulnerable' and 'secured'
    + Vulnerable version use a weak secret key which is plain text (can be exploitable if the app is not
    configured appropriately)
    + Secured version use a strong secret key using secrets token hexing (might be overkill but still
    the best practice for configuring Flask webapp)
"""
import secrets
from datetime import timedelta

# Constants - Security mode and key 
SECURITY_MODE = "vulnerable" # Default value vulnerable
WEAK_SECRET = "weak_secret_key_123"
STRONG_SECRET = secrets.token_hex(32)

# Config app function - setup different config based on selected mode
def configure_app(app):
    """Configure Flask application based on security mode"""
    global SECURITY_MODE
    
    if SECURITY_MODE == 'secured':
        app.secret_key = STRONG_SECRET
        app.config['SESSION_COOKIE_HTTPONLY'] = True
        app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
        app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
        app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
    else:
        app.secret_key = WEAK_SECRET
        app.config['SESSION_COOKIE_HTTPONLY'] = False
        app.config['SESSION_COOKIE_SECURE'] = False
        app.config['SESSION_COOKIE_SAMESITE'] = None

# Getters - setters
def get_security_mode():
    return SECURITY_MODE

def set_security_mode(mode):
    global SECURITY_MODE
    if mode in ['vulnerable', 'secured']:
        SECURITY_MODE = mode
        return True
    return False
