""" controllers/transaction_controller.py
Transaction controller - handles balance checks and transfers
"""

from flask import Blueprint, request, redirect, url_for, session
from markupsafe import escape
from config.settings import get_security_mode
from config.database import get_db_connection
from middleware.auth_required import login_required
from services.api_rate_limiter import rate_limit
from services.transaction_service import process_transfer, check_account_balance

transaction_bp = Blueprint('transaction', __name__)

# Transaction route
@transaction_bp.route('/check_balance', methods=['POST'])
@login_required
@rate_limit(max_requests=10, window=60)
def check_balance():
    account_id = request.form.get('account_id', '')
    result = check_account_balance(account_id)
    return result

@transaction_bp.route('/transfer', methods=['POST'])
@login_required
@rate_limit(max_requests=5, window=60)
def transfer():
    amount = request.form.get('amount', 0)
    recipient = request.form.get('recipient', '')
    
    result = process_transfer(session['user_id'], recipient, amount)
    
    if result['success']:
        return redirect(url_for('dashboard.dashboard'))
    else:
        return result['error'], result.get('status_code', 400)