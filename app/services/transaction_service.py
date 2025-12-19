""" services/transaction_services.py
Transaction processing service - support vulnerable and secured version"""

import subprocess
from datetime import datetime
from markupsafe import escape
from config.settings import get_security_mode
from config.database import get_db_connection
from services.validators import validate_username

def check_account_balance(account_id):
    """Check account balance - handles both vulnerable and secured modes"""
    mode = get_security_mode()
    
    if mode == 'vulnerable':
        # [X] VULNERABLE: Command Injection
        
        conn = get_db_connection()
        c = conn.cursor()
        
        # First, try to get legitimate account info
        try:
            # Extract numeric ID if present
            import re
            numeric_id = re.search(r'\d+', account_id)
            if numeric_id:
                account_id_clean = numeric_id.group()
                c.execute("SELECT username, balance, account_type FROM users WHERE id=?", 
                         (int(account_id_clean),))
                account_info = c.fetchone()
            else:
                account_info = None
        except:
            account_info = None
        
        conn.close()
        
        # Build response with account info
        if account_info:
            response_html = f"""
            <div style="font-family: Arial; max-width: 700px; margin: 50px auto; padding: 30px; background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <div style="background: #fff3cd; border: 1px solid #ffc107; padding: 10px; border-radius: 5px; margin-bottom: 20px; color: #856404;">
                    ⚠️ VULNERABLE MODE - Command Injection Possible
                </div>
                <h2 style="color: #667eea;">Account Information</h2>
                <div style="background: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <p><strong>Username:</strong> {account_info[0]}</p>
                    <p><strong>Balance:</strong> ${account_info[1]:.2f}</p>
                    <p><strong>Account Type:</strong> {account_info[2]}</p>
                    <p><strong>Account ID:</strong> {account_id_clean}</p>
                </div>
            """
        else:
            response_html = f"""
            <div style="font-family: Arial; max-width: 700px; margin: 50px auto; padding: 30px; background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <div style="background: #fff3cd; border: 1px solid #ffc107; padding: 10px; border-radius: 5px; margin-bottom: 20px; color: #856404;">
                    ⚠️ VULNERABLE MODE - Command Injection Possible
                </div>
                <h2 style="color: #667eea;">Balance Check</h2>
                <p style="color: #dc3545;">Account not found or invalid ID</p>
            """
            
        try:
            # VULNERABLE: Executes arbitrary commands
            result = subprocess.check_output(
                f"echo Checking balance for account {account_id}", 
                shell=True,
                stderr=subprocess.STDOUT,
                timeout=5
            )
            command_output = result.decode('utf-8', errors='ignore')
            
            # Append command output to show the vulnerability
            response_html += f"""
                <div style="margin-top: 30px; padding-top: 20px; border-top: 2px solid #dc3545;">
                    <h3 style="color: #dc3545;">⚠️ Command Execution Output (Vulnerability Demonstration)</h3>
                    <div style="background: #f8d7da; border: 1px solid #f5c6cb; padding: 15px; border-radius: 5px; margin-top: 10px;">
                        <pre style="margin: 0; font-family: monospace; white-space: pre-wrap; word-wrap: break-word;">{command_output}</pre>
                    </div>
                    <p style="color: #721c24; font-size: 12px; margin-top: 10px;">
                        ⚠️ This output demonstrates command injection vulnerability. 
                        The system executed: <code>echo Checking balance for account {account_id}</code>
                    </p>
                </div>
            """
        except subprocess.TimeoutExpired:
            response_html += """
                <div style="margin-top: 30px; padding: 15px; background: #f8d7da; border: 1px solid #f5c6cb; border-radius: 5px;">
                    <p style="color: #721c24; margin: 0;">⚠️ Command execution timed out (5 seconds limit)</p>
                </div>
            """
        except Exception as e:
            response_html += f"""
                <div style="margin-top: 30px; padding: 15px; background: #f8d7da; border: 1px solid #f5c6cb; border-radius: 5px;">
                    <p style="color: #721c24; margin: 0;">⚠️ Command execution error: {escape(str(e))}</p>
                </div>
            """
        
        # Close the main div and add back button
        response_html += """
                <a href="/dashboard" style="display: inline-block; margin-top: 20px; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px;">Back to Dashboard</a>
            </div>
        """
        
        return response_html
    
    else:  # SECURED MODE
        if not account_id.isdigit():
            return """
            <div style="font-family: Arial; max-width: 600px; margin: 50px auto; padding: 30px; background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <div style="background: #d4edda; border: 1px solid #28a745; padding: 10px; border-radius: 5px; margin-bottom: 20px; color: #155724;">
                    ✓ SECURED MODE - Command Injection Blocked
                </div>
                <h2 style="color: #dc3545;">Invalid Account ID Format</h2>
                <p>Account ID must contain only numbers.</p>
                <a href="/dashboard" style="display: inline-block; margin-top: 20px; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px;">Back to Dashboard</a>
            </div>
            """
        
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT username, balance, account_type FROM users WHERE id=?", (int(account_id),))
        result = c.fetchone()
        conn.close()
        
        if result:
            output = f"""
            <div style="font-family: Arial; max-width: 600px; margin: 50px auto; padding: 30px; background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <div style="background: #d4edda; border: 1px solid #28a745; padding: 10px; border-radius: 5px; margin-bottom: 20px; color: #155724;">
                    ✓ SECURED MODE - Input Validated, No Command Execution
                </div>
                <h2 style="color: #667eea;">Account Information</h2>
                <div style="background: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <p><strong>Username:</strong> {escape(result[0])}</p>
                    <p><strong>Balance:</strong> ${result[1]:.2f}</p>
                    <p><strong>Account Type:</strong> {escape(result[2])}</p>
                    <p><strong>Account ID:</strong> {account_id}</p>
                </div>
                <a href="/dashboard" style="display: inline-block; margin-top: 20px; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px;">Back to Dashboard</a>
            </div>
            """
            return output
        else:
            return """
            <div style="font-family: Arial; max-width: 600px; margin: 50px auto; padding: 30px; background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h2 style="color: #dc3545;">Account Not Found</h2>
                <p>No account exists with this ID.</p>
                <a href="/dashboard" style="display: inline-block; margin-top: 20px; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px;">Back to Dashboard</a>
            </div>
            """

def process_transfer(user_id, recipient, amount):
    """Process money transfer - handles both vulnerable and secured modes"""
    conn = get_db_connection()
    c = conn.cursor()
    
    mode = get_security_mode()
    
    if mode == 'vulnerable':
        # VULNERABLE: No validation, SQL injection possible
        try:
            c.execute(f"UPDATE users SET balance = balance - {amount} WHERE id = {user_id}")
            c.execute(f"UPDATE users SET balance = balance + {amount} WHERE username = '{recipient}'")
            c.execute(f"INSERT INTO transactions (user_id, type, amount, description, timestamp) VALUES ({user_id}, 'transfer', {amount}, 'Transfer to {recipient}', '{datetime.now()}')")
            conn.commit()
            conn.close()
            return {'success': True}
        except Exception as e:
            conn.close()
            return {'success': False, 'error': f'Transfer failed: {str(e)}'}
    
    else:  # SECURED MODE
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