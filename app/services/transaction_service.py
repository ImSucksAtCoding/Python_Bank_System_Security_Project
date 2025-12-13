""" services/transaction_services.py
Transaction processing service - support vulnerable and secured version"""

import subprocess
from datetime import datetime
from markupsafe import escape
from config.settings import get_security_mode
from config.database import get_db_connection
from services.validators import validate_username

"""Check account balance - handles both vulnerable and secured modes"""
def check_account_balance(account_id):
    mode = get_security_mode()
    
    if mode == 'vulnerable':
        # [X] VULNERABLE: Command Injection
        try:
            result = subprocess.check_output(f"echo Checking balance for account {account_id}", shell=True)
            return f"<h3>Balance Check Result:</h3><pre>{result.decode()}</pre><a href='/dashboard'>Back</a>"
        except:
            return "Error checking balance"
    
    else:  # SECURED MODE (input escaping)
        if not account_id.isdigit():
            return "Invalid account ID format"
        
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT username, balance, account_type FROM users WHERE id=?", (int(account_id),))
        result = c.fetchone()
        conn.close()
        
        if result:
            output = f"""
            <div style="font-family: Arial; max-width: 600px; margin: 50px auto; padding: 30px; background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h2 style="color: #667eea;">Account Information</h2>
                <p><strong>Username:</strong> {escape(result[0])}</p>
                <p><strong>Balance:</strong> ${result[1]:.2f}</p>
                <p><strong>Account Type:</strong> {escape(result[2])}</p>
                <a href="/dashboard" style="display: inline-block; margin-top: 20px; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px;">Back to Dashboard</a>
            </div>
            """
            return output
        else:
            return "<h3>Account not found</h3><a href='/dashboard'>Back</a>"
        
"""Process money transfer - handles both vulnerable and secured modes"""
def process_transfer(user_id, recipient, amount):
    conn = get_db_connection()
    c = conn.cursor()
    
    mode = get_security_mode()
    
    if mode == 'vulnerable':
        # [X] VULNERABLE: No validation, SQL injection possible
        try:
            c.execute(f"UPDATE users SET balance = balance - {amount} WHERE id = {user_id}")
            c.execute(f"UPDATE users SET balance = balance + {amount} WHERE username = '{recipient}'")
            c.execute(f"INSERT INTO transactions (user_id, type, amount, description, timestamp) VALUES ({user_id}, 'transfer', {amount}, 'Transfer to {recipient}', '{datetime.now()}')")
            conn.commit()
            conn.close()
            return {'success': True}
        except:
            conn.close()
            return {'success': False, 'error': 'Transfer failed'}
    
    else:  # SECURED MODE (validation with parameterized queries)
        try:
            amount = float(amount)
            
            if amount <= 0 or amount > 10000:
                conn.close()
                return {'success': False, 'error': 'Invalid amount (must be between $0 and $10,000)', 'status_code': 400}
            
            if not validate_username(recipient):
                conn.close()
                return {'success': False, 'error': 'Invalid recipient username', 'status_code': 400}
            
            c.execute("SELECT balance FROM users WHERE id=?", (user_id,))
            sender = c.fetchone()
            
            if not sender or sender[0] < amount:
                conn.close()
                return {'success': False, 'error': 'Insufficient funds', 'status_code': 400}
            
            c.execute("SELECT id FROM users WHERE username=?", (recipient,))
            recipient_data = c.fetchone()
            
            if not recipient_data:
                conn.close()
                return {'success': False, 'error': 'Recipient not found', 'status_code': 404}
            
            c.execute("UPDATE users SET balance = balance - ? WHERE id = ?", (amount, user_id))
            c.execute("UPDATE users SET balance = balance + ? WHERE username = ?", (amount, recipient))
            c.execute("""INSERT INTO transactions (user_id, type, amount, description, timestamp) 
                         VALUES (?, ?, ?, ?, ?)""",
                     (user_id, 'transfer', amount, f'Transfer to {recipient}', 
                      datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            
            conn.commit()
            conn.close()
            return {'success': True}
        except ValueError:
            conn.close()
            return {'success': False, 'error': 'Invalid input', 'status_code': 400}
