"""
config/database.py

Database module to setup a simple SQL lite database and load data samples for operation
"""

import sqlite3
from werkzeug.security import generate_password_hash
from pathlib import Path
import os

"""Constants - absolute path to database to avoid 'Database path not found' error
   Ensure that the database will be loaded regardless of the place where the app is runned"""

# Path of the project root (where app.py is)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Absolute path to database folder
DATABASE_DIR = os.path.join(PROJECT_ROOT, "database")

# Ensure the database directory exists
os.makedirs(DATABASE_DIR, exist_ok=True)

# Full absolute path to the DB file
DATABASE_PATH = os.path.join(DATABASE_DIR, "banking_system.db")

# Get database
def get_db_connection():
    return sqlite3.connect(DATABASE_PATH)

# Initialize database
def init_db():
    conn = get_db_connection()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, 
                  password_hash TEXT, balance REAL, account_type TEXT, 
                  is_admin INTEGER, session_token TEXT, failed_attempts INTEGER DEFAULT 0,
                  locked_until TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY, user_id INTEGER, type TEXT, 
                  amount REAL, description TEXT, timestamp TEXT,
                  FOREIGN KEY(user_id) REFERENCES users(id))''')
    
    # Load sample data into database
    users_data = [
        ('admin', 'admin123', 1000000.00, 'Admin', 1),
        ('john_doe', 'pass123', 5420.50, 'Savings', 0),
        ('jane_smith', 'jane2024', 12350.75, 'Checking', 0),
        ('bob_wilson', 'bob456', 8750.25, 'Savings', 0),
        ('alice_brown', 'alice789', 15600.00, 'Premium', 0),
        ('charlie_davis', 'charlie111', 3200.40, 'Checking', 0),
        ('diana_miller', 'diana222', 9875.60, 'Savings', 0),
        ('edward_moore', 'edward333', 6543.20, 'Checking', 0),
        ('fiona_taylor', 'fiona444', 11234.80, 'Premium', 0),
        ('george_anderson', 'george555', 4567.90, 'Savings', 0),
        ('hannah_thomas', 'hannah666', 7890.30, 'Checking', 0),
        ('ivan_jackson', 'ivan777', 13456.70, 'Premium', 0),
        ('julia_white', 'julia888', 5678.40, 'Savings', 0),
        ('kevin_harris', 'kevin999', 9012.60, 'Checking', 0),
        ('laura_martin', 'laura000', 14567.20, 'Premium', 0),
        ('michael_lee', 'michael111', 3456.80, 'Savings', 0),
        ('nancy_walker', 'nancy222', 8901.50, 'Checking', 0),
        ('oscar_hall', 'oscar333', 12345.90, 'Premium', 0),
        ('paula_allen', 'paula444', 6789.30, 'Savings', 0),
        ('quincy_young', 'quincy555', 10234.70, 'Checking', 0),
        ('rachel_king', 'rachel666', 15678.40, 'Premium', 0),
        ('samuel_wright', 'samuel777', 4321.60, 'Savings', 0),
        ('tina_lopez', 'tina888', 9876.20, 'Checking', 0),
        ('uma_hill', 'uma999', 13579.80, 'Premium', 0),
        ('victor_green', 'victor000', 5432.40, 'Savings', 0),
        ('wendy_adams', 'wendy111', 8765.90, 'Checking', 0),
        ('xavier_baker', 'xavier222', 11098.50, 'Premium', 0),
        ('yolanda_nelson', 'yolanda333', 6543.70, 'Savings', 0),
        ('zachary_carter', 'zachary444', 9321.30, 'Checking', 0),
        ('amy_mitchell', 'amy555', 14890.60, 'Premium', 0)
    ]
    
    for user in users_data:
        username, password, balance, account_type, is_admin = user
        hashed_pw = generate_password_hash(password)
        c.execute("""INSERT OR IGNORE INTO users 
                     (username, password, password_hash, balance, account_type, is_admin) 
                     VALUES (?, ?, ?, ?, ?, ?)""", 
                  (username, password, hashed_pw, balance, account_type, is_admin))
    
    # Transactions data
    transactions = [
        (2, 'deposit', 500.00, 'Salary deposit', '2024-12-01 10:30:00'),
        (2, 'withdrawal', 200.00, 'ATM withdrawal', '2024-12-02 14:15:00'),
        (3, 'deposit', 1000.00, 'Transfer from savings', '2024-12-01 09:00:00'),
        (4, 'withdrawal', 300.00, 'Bill payment', '2024-12-03 11:20:00'),
        (5, 'deposit', 2000.00, 'Business income', '2024-12-01 16:45:00'),
    ]
    
    for trans in transactions:
        c.execute("""INSERT OR IGNORE INTO transactions 
                     (user_id, type, amount, description, timestamp) 
                     VALUES (?, ?, ?, ?, ?)""", trans)
    
    conn.commit()
    conn.close()