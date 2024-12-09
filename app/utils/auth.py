from functools import wraps
from flask import request, jsonify
from typing import Dict, Optional, Callable
import hashlib
import time

# In-memory token storage: {token: (user_id, expiry_time)}
tokens: Dict[str, tuple[int, float]] = {}

def generate_token(user_id: int) -> str:
    """Generate a token for the given user ID."""
    timestamp = str(time.time())
    token = hashlib.sha256(f"{user_id}{timestamp}".encode()).hexdigest()
    # Token expires in 24 hours
    tokens[token] = (user_id, time.time() + 86400)
    return token

def verify_token(token: str) -> Optional[int]:
    """Verify a token and return the user ID if valid."""
    if token not in tokens:
        return None
    user_id, expiry = tokens[token]
    if time.time() > expiry:
        del tokens[token]
        return None
    return user_id

def token_required(f: Callable) -> Callable:
    """Decorator to protect routes with token authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        token = token.split(' ')[-1]  # Remove 'Bearer ' prefix if present
        user_id = verify_token(token)
        
        if user_id is None:
            return jsonify({'message': 'Invalid or expired token'}), 401
        
        return f(*args, **kwargs)
    return decorated
