"""
controllers/dashboard_controller.py
Dashboard controller - handles user dashboard
"""

from flask import Blueprint, render_template, session
from config.settings import get_security_mode
from config.database import get_db_connection
from middleware.auth_required import login_required

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