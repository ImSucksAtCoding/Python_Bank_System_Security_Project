"""
controllers/dashboard_controller.py
Dashboard controller - handles user dashboard
"""

from flask import Blueprint, render_template, session, render_template_string, request
from config.settings import get_security_mode
from config.database import get_db_connection
from middleware.auth_required import login_required
from markupsafe import escape

dashboard_bp = Blueprint('dashboard', __name__)

# Dashboard route
@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Get security mode
    mode = get_security_mode()
    
    if mode == 'vulnerable':
        # [X] Vulnerable to SQL injection attacks
        c.execute(f"SELECT * FROM users WHERE id={session['user_id']}")
    else:
        # [+] Safe practice: Use parameterized queries
        c.execute("SELECT * FROM users WHERE id=?", (session['user_id'],))
    
    user = c.fetchone()
    
    if mode == 'vulnerable':
        # [X] Vulnerable to SQL injection attacks
        c.execute(f"SELECT * FROM transactions WHERE user_id={session['user_id']} ORDER BY timestamp DESC LIMIT 10")
    else:
        # [+] Safe practice: Use parameterized queries
        c.execute("SELECT * FROM transactions WHERE user_id=? ORDER BY timestamp DESC LIMIT 10", 
                 (session['user_id'],))
    
    transactions = c.fetchall()
    conn.close()
    
    return render_template('dashboard.html', user=user, transactions=transactions, mode=mode)

# NEW ROUTE: Custom Message Feature (SSTI RCE Vulnerability)
@dashboard_bp.route('/custom_message', methods=['GET', 'POST'])
@login_required
def custom_message():
    """
    Custom message feature - demonstrates SSTI vulnerability
    Allows users to create custom dashboard messages
    """
    mode = get_security_mode()
    
    if request.method == 'POST':
        message_template = request.form.get('message', '')
        
        if mode == 'vulnerable':
            # [X] VULNERABLE: Renders user input as template - SSTI!
            try:
                return render_template_string(f'''
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Custom Message - SecureBank</title>
                    <link rel="stylesheet" href="/static/style.css">
                    <style>
                        .preview {{ background: #fff3cd; border: 2px solid #ffc107; padding: 20px; 
                                   margin: 20px 0; border-radius: 5px; }}
                        .message-output {{ background: white; padding: 15px; border-radius: 5px; 
                                         margin-top: 10px; min-height: 50px; }}
                    </style>
                </head>
                <body>
                    <div class="header">
                        <h1>🏦 SecureBank - Custom Message</h1>
                        <a href="/dashboard" class="btn-danger">Back to Dashboard</a>
                    </div>
                    <div class="container">
                        <div class="card">
                            <div class="security-info vulnerable-info">
                                ⚠️ VULNERABLE MODE - Server-Side Template Injection (SSTI) Possible
                            </div>
                            <h2>Message Preview</h2>
                            <div class="preview">
                                <p><strong>Your Input:</strong></p>
                                <code>{message_template}</code>
                                
                                <p style="margin-top: 15px;"><strong>Rendered Output:</strong></p>
                                <div class="message-output">
                                    {message_template}
                                </div>
                            </div>
                            
                            <p style="color: #721c24; margin-top: 15px;">
                                ⚠️ <strong>Vulnerability Demonstrated:</strong> Your input was processed as a 
                                Jinja2 template. Template expressions like {{{{ 7*7 }}}} are evaluated!
                            </p>
                            
                            <a href="/custom_message" class="btn-primary" style="margin-top: 20px;">Try Another Message</a>
                        </div>
                    </div>
                </body>
                </html>
                ''')
            
            except Exception as e:
                error_message = str(e)
                return render_template_string(f'''
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Error - SecureBank</title>
                    <link rel="stylesheet" href="/static/style.css">
                </head>
                <body>
                    <div class="header">
                        <h1>🏦 SecureBank</h1>
                        <a href="/dashboard" class="btn-danger">Back</a>
                    </div>
                    <div class="container">
                        <div class="card">
                            <h2 style="color: #dc3545;">Template Error</h2>
                            <div style="background: #f8d7da; padding: 15px; border-radius: 5px;">
                                <pre>{escape(error_message)}</pre>
                            </div>
                            <a href="/custom_message" class="btn-primary" style="margin-top: 20px;">Try Again</a>
                        </div>
                    </div>
                </body>
                </html>
                ''')
        
        else:  # SECURED MODE
            # SECURE: Treats input as plain text, not as template
            safe_message = escape(message_template)
            
            return render_template_string(f'''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Custom Message - SecureBank</title>
                <link rel="stylesheet" href="/static/style.css">
                <style>
                    .preview {{ background: #d4edda; border: 2px solid #28a745; padding: 20px; 
                               margin: 20px 0; border-radius: 5px; }}
                    .message-output {{ background: white; padding: 15px; border-radius: 5px; 
                                     margin-top: 10px; min-height: 50px; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>🏦 SecureBank - Custom Message</h1>
                    <a href="/dashboard" class="btn-danger">Back to Dashboard</a>
                </div>
                <div class="container">
                    <div class="card">
                        <div class="security-info secured-info">
                            ✓ SECURED MODE - Input Escaped, SSTI Prevention Active
                        </div>
                        <h2>Message Preview</h2>
                        <div class="preview">
                            <p><strong>Your Input:</strong></p>
                            <code>{safe_message}</code>
                            
                            <p style="margin-top: 15px;"><strong>Rendered Output:</strong></p>
                            <div class="message-output">
                                {safe_message}
                            </div>
                        </div>
                        
                        <p style="color: #155724; margin-top: 15px;">
                            ✓ <strong>Protected:</strong> Your input was escaped and treated as plain text.
                            Template expressions are not evaluated.
                        </p>
                        
                        <a href="/custom_message" class="btn-primary" style="margin-top: 20px;">Try Another Message</a>
                    </div>
                </div>
            </body>
            </html>
            ''')
    
    # GET request - show form
    mode_indicator = "⚠️ VULNERABLE" if mode == 'vulnerable' else "✓ SECURED"
    mode_class = "vulnerable-info" if mode == 'vulnerable' else "secured-info"
    
    return render_template_string(f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Custom Message - SecureBank</title>
        <link rel="stylesheet" href="/static/style.css">
        <style>
            .example-box {{ background: #f8f9fa; padding: 15px; border-radius: 5px; 
                           margin: 15px 0; border-left: 4px solid #667eea; }}
            .example-box code {{ background: white; padding: 2px 6px; border-radius: 3px; 
                                font-family: monospace; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🏦 SecureBank - Custom Message</h1>
            <a href="/dashboard" class="btn-danger">Back to Dashboard</a>
        </div>
        <div class="container">
            <div class="card">
                <div class="security-info {mode_class}">
                    {mode_indicator} MODE - Custom Dashboard Message
                </div>
                
                <h2>Create Custom Message</h2>
                <p>Create a custom message for your dashboard. You can use your name and other details.</p>
                
                <form method="POST" style="margin-top: 20px;">
                    <div class="form-group">
                        <label>Message Template:</label>
                        <textarea name="message" rows="5" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-family: monospace;" placeholder="Enter your custom message..."></textarea>
                    </div>
                    <button type="submit" class="btn-primary">Preview Message</button>
                </form>
                
                {'<div class="example-box"><strong>⚠️ Try SSTI Payloads:</strong><br>' +
                 '7*7  - Simple math<br>' +
                 'config.items() - Config disclosure<br>' +
                 'self.__init__.__globals__  - Globals access<br>' +
                 'session.username - Session data<br>' +
                 '</div>' if mode == 'vulnerable' else
                 '<div class="example-box"><strong>✓ Try These Safe Examples:</strong><br>' +
                 'Hello, welcome to SecureBank!<br>' +
                 'Your account is secure.<br>' +
                 '</div>'}
            </div>
        </div>
    </body>
    </html>
    ''')