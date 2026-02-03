# 🏦 SecureBank - A Simple Python Bank Webapp System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![License](https://img.shields.io/badge/License-Educational-orange.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

**An interactive web application demonstrating common cybersecurity vulnerabilities and Python implementation to address this issues**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Vulnerabilities](#-vulnerabilities) • [Documentation](#-documentation)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Security Modes](#-security-modes)
- [Vulnerabilities Demonstrated](#-vulnerabilities-demonstrated)
- [Attack Testing](#-attack-testing)
- [Educational Resources](#-educational-resources)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [Disclaimer](#%EF%B8%8F-disclaimer)
- [License](#-license)

---

## 🎯 Overview

**SecureBank** is a full-featured banking web application built with Python Flask that serves as an educational platform for learning about web security vulnerabilities and best practices. The application features a unique **dual-mode system** that allows users to toggle between vulnerable and secured implementations in real-time.

### Why SecureBank?

- 🎓 **Learn by Doing**: Hands-on experience with real vulnerabilities
- 🔄 **Compare & Contrast**: Switch between vulnerable and secured modes instantly
- 📚 **Comprehensive Coverage**: 6 major vulnerability categories
- 🛠️ **Practical Tools**: Includes automated attack scripts and manual testing guides
- 💼 **Real-World Scenarios**: Banking context makes concepts relatable
- ✅ **Best Practices**: See how to properly fix each vulnerability

---

## ✨ Features

### Core Functionality

- ✅ **User Authentication System** - Login, registration, and session management
- ✅ **Account Dashboard** - View balance, account details, and transaction history
- ✅ **Money Transfers** - Send money between accounts
- ✅ **Balance Checking** - Query account information
- ✅ **Admin Panel** - Comprehensive view of all users and transactions
- ✅ **30 Pre-generated Users** - Ready-to-test sample accounts

### Security Features

- 🔄 **Switchable Security Modes** - Toggle between vulnerable and secured without restart
- 🎨 **Visual Mode Indicators** - Clear badges showing current security state
- 📊 **Real-time Comparison** - See how attacks behave in each mode
- 🛡️ **Multiple Protection Layers** - Rate limiting, input validation, secure sessions
- 📝 **Detailed Logging** - Track what's happening during attacks

### Educational Tools

- 📜 **Attack Scripts** - Automated Python scripts for testing vulnerabilities
- 📖 **Manual Testing Guide** - Step-by-step instructions for browser-based testing
- 🎯 **Exploit Examples** - Real payloads with explanations
- 📊 **Success Indicators** - Know when attacks work
- 🔍 **Comparison Checklist** - Verify fixes in secured mode

---

## 📁 Project Structure

```
Python_Bank_System_Security_Project             # Root project folder
|
├── 📄LICENSE                                     # MIT LICENSE
├── 📄README.md                                   # This file
├── 📂app                                         # Main app folder
│   ├── 📄app.py                                  # Main entrypoint
│   ├── 📂config                                  
│   │   ├── __pycache__
│   │   ├── database.py                         # Database initialization
│   │   └── settings.py                         # App configuration, security mode
│   ├── 📂controllers
│   │   ├── __pycache__
│   │   ├── admin_controller.py                 # Admin dashboard panel
│   │   ├── auth_controller.py                  # Authorization controller (login/register, logout)
│   │   ├── dashboard_controller.py             # Main dashboard panel
│   │   ├── security_mode.py                    # Security toggle route
│   │   └── transaction_controller.py           # Transaction & balance checks
│   ├── 📂database
│   │   └── banking_system.db                   # Main database
│   ├── middleware
│   │   ├── __pycache__
│   │   ├── admin_required.py                   # Admin authorization middleware
│   │   └── auth_required.py                    # Authorization middleware
│   ├── 📂services
│   │   ├── __pycache__
│   │   ├── api_rate_limiter.py                 # API rate limiter
│   │   ├── auth_service.py                     # Authorization service logic
│   │   ├── session_service.py                  # Session service logic
│   │   ├── transaction_service.py              # Transaction processing
│   │   └── validators.py                       # Input validating functions
│   ├── 📂static
│   │   └── style.css                           # Styling file
│   └── 📂templates
│       ├── admin.html                          # Admin dashboard template
│       ├── dashboard.html                      # Main dashboard template
│       ├── login.html                          # Auth template (login/register)
│       ├── partials
│       │   └── layout.html                     # Shared layout
│       └── register.html
├── 📂attack_scripts
    ├── README.md                               # Cyberattack scripts documentation
    └── attack.py                               # Cyberattack scripts
```

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager) or other Python package manager (uv)
- Web browser (Chrome, Firefox, Safari, etc.)

### Step 1: Clone or Download

```bash
# Option A: Clone with git
git clone https://github.com/ImSucksAtCoding/Python_Bank_System_Security_Project.git
cd Python_Bank_System_Security_Project/app

# Option B: Download and extract ZIP
# Then navigate to the folder
cd Python_Bank_System_Security_Project/app
```

### Step 2: Install Dependencies

```bash
# Install required packages for webapp
pip install flask werkzeug markupsafe

# For attack scripts (optional)
pip install requests beautifulsoup4
```

### Step 3: Verify Installation

```bash
# Check Python version
python --version

# Verify Flask installation
python -c "import flask; print(flask.__version__)"
```

---

## 🎮 Quick Start

### Starting the Application

```bash
# Navigate to project app directory
cd Python_Bank_System_Security_Project/app

# Run the application
python app.py
```

You should see:
```
======================================================================
UNIFIED BANKING SYSTEM - SWITCHABLE SECURITY MODE
======================================================================

🔄 Toggle between Vulnerable and Secured modes in the web interface

Test Accounts:
  Admin: admin/admin123
  User: john_doe/pass123

Access the application at: http://localhost:5000
======================================================================
```

### First Login

1. Open browser: `http://localhost:5000`
2. Login with test account:
   - **Admin**: `admin` / `admin123`
   - **User**: `john_doe` / `pass123`

### Switching Security Modes

1. Go to login page
2. Use dropdown menu: "Security Mode"
3. Select "Vulnerable" or "Secured"
4. Click "Switch Mode"
5. Log in and test!

---

## 🔐 Security Modes

### 🔴 Vulnerable Mode

**Purpose**: Demonstrates common security flaws

**Characteristics**:
- ⚠️ SQL Injection enabled
- ⚠️ No XSS protection
- ⚠️ Command injection possible
- ⚠️ Weak session management
- ⚠️ No rate limiting
- ⚠️ Predictable secret keys

**Use Cases**:
- Learning how attacks work
- Testing attack scripts
- Understanding vulnerability impact
- Demonstrating security concepts

---

### 🟢 Secured Mode

**Purpose**: Shows security best practices

**Characteristics**:
- ✅ Parameterized SQL queries
- ✅ Auto-escaping (XSS protection)
- ✅ Input validation
- ✅ Secure session tokens
- ✅ Rate limiting (5 req/min)
- ✅ Strong cryptographic keys
- ✅ Account lockout (5 attempts)
- ✅ Password hashing (bcrypt)

**Use Cases**:
- Understanding proper security
- Verifying attack prevention
- Learning defensive coding
- Comparing with vulnerable mode

---

## 🎯 Vulnerabilities Demonstrated

### 1. 💉 SQL Injection

**Vulnerable Code**:
```python
query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
```

**Attack Example**:
```
Username: ' OR '1'='1' --
Password: anything
Result: Authentication bypassed ✓
```

**Secure Fix**:
```python
c.execute("SELECT * FROM users WHERE username=?", (username,))
```

**Impact**: Complete database compromise, data theft, authentication bypass

---

### 2. 🔓 Cross-Site Scripting (XSS)

**Vulnerable Code**:
```html
<div>{{ username }}</div>  <!-- No escaping -->
```

**Attack Example**:
```html
Username: <script>alert(document.cookie)</script>
Result: Cookie stolen ✓
```

**Secure Fix**:
```html
<div>{{ username|e }}</div>  <!-- Auto-escaped -->
```

**Impact**: Session hijacking, cookie theft, malicious redirects

---

### 3. 💻 Command Injection

**Vulnerable Code**:
```python
result = subprocess.check_output(f"echo Balance: {account_id}", shell=True)
```

**Attack Example**:
```
Account ID: 1; ls -la
Result: Directory listing shown ✓
```

**Secure Fix**:
```python
# Don't use shell commands with user input!
# Use database queries instead
c.execute("SELECT balance FROM users WHERE id=?", (account_id,))
```

**Impact**: System compromise, data theft, complete server control

---

### 4. 🔑 Session Hijacking

**Vulnerable Code**:
```python
app.secret_key = 'weak_secret_123'  # Predictable!
session['user_id'] = user_id        # No validation
```

**Attack Example**:
```python
# Attacker can forge session cookies
# Access admin panel without authentication
```

**Secure Fix**:
```python
app.secret_key = secrets.token_hex(32)  # Strong random key
session['session_token'] = secrets.token_hex(32)
# Validate token against database on each request
```

**Impact**: Account takeover, unauthorized access, privilege escalation

---

### 5. 🌊 Denial of Service (DoS)

**Vulnerable Code**:
```python
@app.route('/transfer', methods=['POST'])
def transfer():
    # No rate limiting!
    process_transfer()
```

**Attack Example**:
```javascript
// Send 1000 requests rapidly
for(let i=0; i<1000; i++) {
  fetch('/transfer', {method: 'POST', body: data});
}
// Result: Server overwhelmed ✓
```

**Secure Fix**:
```python
@rate_limit(max_requests=5, window=60)  # 5 per minute
def transfer():
    process_transfer()
```

**Impact**: Service disruption, resource exhaustion, downtime

---

### 6. 🚀 Remote Code Execution (RCE)

**Vulnerable Code**:
```python
# Debug mode enabled
app.run(debug=True)

# Or SSTI vulnerability
render_template_string(user_input)
```

**Attack Example**:
```python
# SSTI payload
{{ config['SECRET_KEY'] }}
{{ ''.__class__.__mro__[2].__subclasses__() }}
# Result: Code execution ✓
```

**Secure Fix**:
```python
# Disable debug in production
app.run(debug=False)

# Use static templates
render_template('page.html', data=user_input)
```

**Impact**: Complete system compromise, data breach, malware deployment

---

## 🧪 Attack Testing

### Method 1: Automated Scripts

```bash
# Run attack script
python attack_scripts.py

# Follow interactive menu
1. SQL Injection - Login Bypass
2. XSS - Stored Attack
3. Command Injection
...
13. Run ALL Attacks
```

**Features**:
- ✅ Interactive menu
- ✅ Color-coded output
- ✅ Success indicators
- ✅ Detailed results
- ✅ Run all or select specific attacks

---

### Method 2: Manual Testing (Browser Only)

#### SQL Injection Test
```
1. Go to: http://localhost:5000/login
2. Username: ' OR '1'='1' --
3. Password: anything
4. Click Login
✓ You're in!
```

#### XSS Test
```
1. Go to: http://localhost:5000/register
2. Username: <script>alert('XSS')</script>
3. Password: test123
4. Register → Login as admin → View users
✓ Alert appears!
```

#### Command Injection Test
```
1. Login as: john_doe / pass123
2. Account ID: 1; whoami
3. Click Check Balance
✓ Username displayed!
```

#### DoS Test (Browser Console - F12)
```javascript
for(let i=0; i<100; i++) {
  fetch('/transfer', {
    method: 'POST',
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: 'recipient=admin&amount=0.01'
  });
}
// Vulnerable: All succeed
// Secured: Rate limited after 5
```

### Full explaination and description for the attacks can be found in attack_scripts/README.md

---

## 📚 Educational Resources

### Included Documentation

| Document | Description | Location |
|----------|-------------|----------|
| **Attack Scripts** | Automated testing tool | `attack_scripts.py` |
| **Manual Guide** | Browser-based testing | In artifacts |
| **Security Guide** | Vulnerabilities & fixes | In artifacts |
| **Code Comments** | Inline explanations | Throughout codebase |

### Learning Path

1. **Start Here**: Understand the application (Secured mode)
2. **Switch**: Enable Vulnerable mode
3. **Attack**: Try SQL injection first (easiest)
4. **Compare**: Switch back to Secured mode
5. **Understand**: Read the code to see fixes
6. **Progress**: Move to harder attacks (XSS, RCE)

### Recommended Order

```
Beginner    → SQL Injection → XSS → Command Injection
Intermediate → Session Hijacking → DoS
Advanced    → Flask RCE (SSTI)
```
---

## 🛠️ Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Error: Address already in use
# Solution: Kill process on port 5000
lsof -ti:5000 | xargs kill -9  # Mac/Linux
netstat -ano | findstr :5000   # Windows (find PID, then kill)
```

#### Import Error: escape
```bash
# Error: cannot import name 'escape' from 'flask'
# Solution: Update imports
# Change: from flask import escape
# To: from markupsafe import escape
```

#### Database Locked
```bash
# Error: database is locked
# Solution: Close other connections
rm bank_unified.db  # Delete and restart
python app.py       # Will recreate database
```

#### Rate Limiting Too Strict
```python
# In services/rate_limit.py
# Change: max_requests=5
# To: max_requests=10  # More lenient
```

---

## ⚠️ Disclaimer

### 🔴 THIS IS IMPORTANT - READ CAREFULLY

**This application is designed EXCLUSIVELY for educational purposes.**

#### ✅ Acceptable Use
- Educational learning environments
- Security training courses
- Cybersecurity demonstrations
- Personal learning and practice
- Controlled lab environments
- Academic research

#### ❌ Prohibited Use
- Testing on production systems
- Attacking systems without permission
- Deploying to public internet
- Using on real financial systems
- Penetration testing without authorization
- Any illegal activities

#### ⚖️ Legal Notice

By using this software, you agree that:

1. You will ONLY use it in controlled test environments
2. You will NOT deploy it to production
3. You will NOT test on systems you don't own
4. You understand ethical hacking principles
5. You take full responsibility for your actions

**The author of this project is NOT responsible for any misuse of this educational tool.**

### 🟡 Security Warning

This application contains INTENTIONAL vulnerabilities. Never:
- Use in production
- Expose to the internet
- Store real data
- Use real credentials
- Deploy on shared hosting

---

## 📄 License

This project is released under the **Educational Use License**.

```
MIT License - Educational Use Only

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software for EDUCATIONAL PURPOSES ONLY, subject to the conditions:

- Use only in controlled environments
- Not for production deployment
- Not for unauthorized testing
- Proper attribution required

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
```
---

## 🎓 Learning Resources

### Recommended Reading

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Web Security Academy](https://portswigger.net/web-security)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Flask Security Guide](https://flask.palletsprojects.com/en/2.3.x/security/)

### Practice Platforms

- [HackTheBox](https://www.hackthebox.com/)
- [TryHackMe](https://tryhackme.com/)
- [PentesterLab](https://pentesterlab.com/)
- [OWASP WebGoat](https://owasp.org/www-project-webgoat/)

### Video Tutorials

- Search YouTube: "Web Security Fundamentals"
- Udemy: Web Application Security courses
- Coursera: Cybersecurity specializations

---

## 🙏 Acknowledgments

### Inspiration

- OWASP WebGoat
- DVWA (Damn Vulnerable Web Application)
- Juice Shop
- Web Security Academy

### Technologies

- **Flask** - Web framework
- **SQLite** - Database
- **Werkzeug** - Security utilities
- **Jinja2** - Template engine
- **Python** - Programming language

**Testing webhook - again...**