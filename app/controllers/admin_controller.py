""" controllers/admin_controller.py
Admin controller - handles admin dashboard
"""

from flask import Blueprint, render_template
from config.settings import get_security_mode
from config.database import get_db_connection
from middleware.auth_required import login_required
from middleware.admin_required import admin_required

admin_bp = Blueprint('admin', __name__)

# Admin route (login and admin priviliges required)
@admin_bp.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    
    c.execute("""SELECT t.*, u.username FROM transactions t 
                 JOIN users u ON t.user_id = u.id 
                 ORDER BY t.timestamp DESC""")
    transactions = c.fetchall()
    conn.close()
    
    return render_template('admin.html', users=users, transactions=transactions, mode=get_security_mode())

