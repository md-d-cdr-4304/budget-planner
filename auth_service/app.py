"""
Auth Service - Handles user registration and login
Returns dummy tokens for authentication
"""

from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import hashlib
import os
import logging
from pymongo import MongoClient
from bson import ObjectId
import bcrypt
import jwt
from functools import wraps
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# MongoDB connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://admin:password123@mongo-service:27017/budget_planner?authSource=admin')

try:
    client = MongoClient(MONGO_URI)
    db = client.budget_planner
    users_collection = db.users
    logger.info("Auth Service connected to MongoDB successfully")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {str(e)}")
    # Fallback to in-memory storage if MongoDB is not available
    users_db = {}

# Secret key for token generation (in production, use proper secret management)
SECRET_KEY = os.getenv('SECRET_KEY', 'demo-secret-key')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24
JWT_REFRESH_EXPIRATION_DAYS = 7

# Rate limiting storage (in production, use Redis)
rate_limit_storage = {}

def generate_jwt_token(user_id, username):
    """Generate a proper JWT token"""
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow(),
        'type': 'access'
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token

def generate_refresh_token(user_id, username):
    """Generate a refresh token"""
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': datetime.utcnow() + timedelta(days=JWT_REFRESH_EXPIRATION_DAYS),
        'iat': datetime.utcnow(),
        'type': 'refresh'
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token

def verify_jwt_token(token):
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("Token has expired")
        return None
    except jwt.InvalidTokenError:
        logger.warning("Invalid token")
        return None

def rate_limit(max_requests=10, window_seconds=60):
    """Rate limiting decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = request.remote_addr
            current_time = time.time()
            
            # Clean old entries
            if client_ip in rate_limit_storage:
                rate_limit_storage[client_ip] = [
                    req_time for req_time in rate_limit_storage[client_ip]
                    if current_time - req_time < window_seconds
                ]
            else:
                rate_limit_storage[client_ip] = []
            
            # Check rate limit
            if len(rate_limit_storage[client_ip]) >= max_requests:
                return jsonify({'error': 'Rate limit exceeded'}), 429
            
            # Add current request
            rate_limit_storage[client_ip].append(current_time)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_auth(f):
    """Authentication decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Authorization token required'}), 401
        
        # Remove 'Bearer ' prefix if present
        if token.startswith('Bearer '):
            token = token[7:]
        
        payload = verify_jwt_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Add user info to request context
        request.current_user = payload
        return f(*args, **kwargs)
    return decorated_function

def hash_password(password):
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password, hashed):
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def get_user_by_username(username):
    """Get user by username from MongoDB"""
    try:
        user = users_collection.find_one({"username": username})
        if user:
            user['_id'] = str(user['_id'])  # Convert ObjectId to string
        return user
    except Exception as e:
        logger.error(f"Error fetching user: {str(e)}")
        return None

def create_user(user_data):
    """Create a new user in MongoDB"""
    try:
        user_data['created_at'] = datetime.now().isoformat()
        result = users_collection.insert_one(user_data)
        user_data['_id'] = str(result.inserted_id)
        return user_data
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        return None

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'auth-service',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/register', methods=['POST'])
@rate_limit(max_requests=5, window_seconds=300)  # 5 requests per 5 minutes
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Username and password are required'}), 400
        
        username = data['username']
        password = data['password']
        
        # Check if user already exists
        existing_user = get_user_by_username(username)
        if existing_user:
            return jsonify({'error': 'Username already exists'}), 409
        
        # Create new user
        hashed_password = hash_password(password)
        
        # Generate unique user_id based on username hash
        import hashlib
        user_id = int(hashlib.md5(username.encode()).hexdigest()[:8], 16)
        
        user_data = {
            'user_id': user_id,
            'username': username,
            'password': hashed_password
        }
        
        # Save to MongoDB
        created_user = create_user(user_data)
        if not created_user:
            return jsonify({'error': 'Failed to create user'}), 500
        
        # Generate tokens
        access_token = generate_jwt_token(user_id, username)
        refresh_token = generate_refresh_token(user_id, username)
        
        logger.info(f"User registered: {username}")
        
        return jsonify({
            'message': 'User registered successfully',
            'user_id': user_id,
            'username': username,
            'access_token': access_token,
            'refresh_token': refresh_token,
            'expires_in': JWT_EXPIRATION_HOURS * 3600  # seconds
        }), 201
        
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/login', methods=['POST'])
@rate_limit(max_requests=10, window_seconds=300)  # 10 requests per 5 minutes
def login():
    """Login user and return token"""
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Username and password are required'}), 400
        
        username = data['username']
        password = data['password']
        
        # Check if user exists
        user = get_user_by_username(username)
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Verify password
        if not verify_password(password, user['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Generate tokens
        access_token = generate_jwt_token(user['user_id'], username)
        refresh_token = generate_refresh_token(user['user_id'], username)
        
        logger.info(f"User logged in: {username}")
        
        return jsonify({
            'message': 'Login successful',
            'user_id': user['user_id'],
            'username': username,
            'access_token': access_token,
            'refresh_token': refresh_token,
            'expires_in': JWT_EXPIRATION_HOURS * 3600  # seconds
        }), 200
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/verify', methods=['POST'])
@require_auth
def verify_token():
    """Verify JWT token"""
    try:
        # If we reach here, token is valid (handled by @require_auth)
        user_info = request.current_user
        return jsonify({
            'valid': True,
            'user_id': user_info['user_id'],
            'username': user_info['username'],
            'expires_at': user_info['exp']
        }), 200
        
    except Exception as e:
        logger.error(f"Token verification error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/refresh', methods=['POST'])
@rate_limit(max_requests=5, window_seconds=60)  # 5 refresh requests per minute
def refresh_token():
    """Refresh access token using refresh token"""
    try:
        data = request.get_json()
        refresh_token = data.get('refresh_token')
        
        if not refresh_token:
            return jsonify({'error': 'Refresh token is required'}), 400
        
        # Verify refresh token
        payload = verify_jwt_token(refresh_token)
        if not payload or payload.get('type') != 'refresh':
            return jsonify({'error': 'Invalid refresh token'}), 401
        
        # Generate new access token
        new_access_token = generate_jwt_token(payload['user_id'], payload['username'])
        
        return jsonify({
            'access_token': new_access_token,
            'expires_in': JWT_EXPIRATION_HOURS * 3600
        }), 200
        
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/logout', methods=['POST'])
@require_auth
def logout():
    """Logout user (invalidate token)"""
    try:
        # In a production system, you would add the token to a blacklist
        # For now, we'll just return success
        return jsonify({'message': 'Logged out successfully'}), 200
        
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Auth Service on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)

