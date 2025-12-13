"""
services/api_rate_limiter.py

Service module to limit API request for an endpoint, mitigating brute-force SQL injection attacks or
DoS attacks (only applied on secured version)
"""
from functools import wraps
from flask import request
from datetime import datetime
from config.settings import get_security_mode

# Rate limiting store
rate_limit_store = {}

# API rate limiter function (default max requests 10, customizable)
def rate_limit(max_requests=10, window=60):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if get_security_mode() == 'vulnerable':
                return f(*args, **kwargs)
            
            ip = request.remote_addr
            now = datetime.now()
            
            if ip not in rate_limit_store:
                rate_limit_store[ip] = []
            
            rate_limit_store[ip] = [req_time for req_time in rate_limit_store[ip] 
                                   if (now - req_time).seconds < window]
            
            if len(rate_limit_store[ip]) >= max_requests:
                return "Too many requests. Please try again later.", 429
            
            rate_limit_store[ip].append(now)
            return f(*args, **kwargs)
        return wrapped
    return decorator