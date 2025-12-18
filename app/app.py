"""
app.py - Main entry point 

***SIMPLE PYTHON BANKING SYSTEM - WITH SWITCHABLE SECURITY VERSION***

- Support 2 versions - vulnerable and secured
    + Vulnerable version webapp can be exploited by common cyberattacks (SQL injection, XSS, session hijacking, etc.)
    + Secured version provides safe Python implementation to address these issues

- NOTE: [!] DO NOT DEPLOY THIS WEBAPP TO A PRODUCTION ENVIRONMENT OR PUBLIC NETWORK. THIS IS A PERSONAL PROJECT 
FOR EDUCATIONAL PURPOSE ONLY. IF YOU WANT TO TEST THE WEBAPP, DEPLOY IT LOCALLY AND INSIDE A SANDBOX ENVIRONMENT
"""

from flask import Flask
from config.settings import configure_app, get_security_mode
from config.database import init_db
from controllers.auth_controller import auth_bp
from controllers.dashboard_controller import dashboard_bp
from controllers.transaction_controller import transaction_bp
from controllers.admin_controller import admin_bp
from controllers.security_mode import security_bp

# App configuration
app = Flask(__name__)
configure_app(app)

"""Configure autoescape based on security mode
   Here, we will force the app to not auto-escape input in vulnerable mode
   In modern Flask version, Jinja2 template is supported to escape the input
   So we need to disable it to simulate the vulnerable version

   Vulnerable version: Jinja2 disable
   Secured version: Jinja2 enable
   """
@app.before_request
def configure_autoescape():
    if get_security_mode() == 'vulnerable':
        app.jinja_env.autoescape = False  # Disable for vulnerable
    else:
        app.jinja_env.autoescape = True   # Enable for secured

# Register blueprints routes
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(transaction_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(security_bp)

# Main entry point
def main():
    init_db()
    print("\n" + "="*70)
    print("SIMPLE BANKING SYSTEM IN PYTHON WITH SWITCHABLE SECURITY MODE")
    print("="*70)
    print("\nToggle between Vulnerable and Secured modes in the web interface")
    print("\nFeatures:")
    print("  • Switch modes without restarting the server")
    print("  • Compare vulnerable vs secured implementations")
    print("  • Educational tool for learning web security")
    print("\nVulnerabilities in Vulnerable Mode:")
    print("  1. SQL Injection in login/register")
    print("  2. XSS in dashboard")
    print("  3. Command Injection in balance check")
    print("  4. Weak session management")
    print("  5. No rate limiting (DoS)")
    print("  6. Weak secret key")
    print("\nSecurity Features in Secured Mode:")
    print("  ✓ Parameterized queries")
    print("  ✓ XSS prevention with auto-escaping")
    print("  ✓ Input validation")
    print("  ✓ Secure session tokens")
    print("  ✓ Rate limiting")
    print("  ✓ Password hashing")
    print("  ✓ Account lockout")
    print("\nTest Accounts:")
    print("  Admin: admin/admin123")
    print("  User: john_doe/pass123")
    print("\nAccess the application at: http://localhost:5000")
    print("="*70 + "\n")
    
    app.run(debug=True, port=5000)

if __name__ == "__main__":
    main()