"""
Budget Service - Handles monthly budgets and daily expenses
Serves web UI and provides REST API endpoints
"""

from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from datetime import datetime, timedelta
import os
import logging
import requests
from pymongo import MongoClient
from bson import ObjectId
import jwt

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'demo-secret-key')

# Configure session settings for better persistence
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# Configuration
AUTH_SERVICE_URL = os.getenv('AUTH_SERVICE_URL', 'http://localhost:5001')
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://admin:password123@mongo-service:27017/budget_planner?authSource=admin')

# MongoDB connection
try:
    client = MongoClient(MONGO_URI)
    db = client.budget_planner
    monthly_budgets_collection = db.monthly_budgets
    daily_expenses_collection = db.daily_expenses
    users_collection = db.users
    logger.info("Connected to MongoDB successfully")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {str(e)}")
    # Fallback to in-memory storage if MongoDB is not available
    monthly_budgets = {}
    daily_expenses = {}

def verify_token(token):
    """Verify token - improved for better session management"""
    try:
        # If no token provided, return False
        if not token or not token.strip():
            logger.warning("No token provided for verification")
            return False
        
        # For local development or debug mode, accept any non-empty token
        if os.getenv('DEBUG', 'False').lower() == 'true':
            logger.info(f"Debug mode: accepting token of length {len(token)}")
            return True
        
        # Accept demo-token for fallback scenarios (when Auth Service is unavailable)
        if token == 'demo-token':
            logger.info("Accepting demo-token for fallback scenario")
            return True
        
        # Get the same secret key used by Auth Service
        SECRET_KEY = os.getenv('SECRET_KEY', 'demo-secret-key')
        
        # Try to verify JWT token first
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            logger.info("JWT token verified successfully")
            return True
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as jwt_error:
            logger.info(f"JWT verification failed: {jwt_error}")
            # If JWT verification fails, check if it's a hash token (backward compatibility)
            # Accept any token that looks like a hash (alphanumeric, reasonable length)
            if token.isalnum() and len(token) >= 32:
                logger.info("Hash token accepted for backward compatibility")
                return True
            logger.warning(f"Token format not recognized: length={len(token)}, alnum={token.isalnum()}")
            return False
        
    except Exception as e:
        logger.error(f"Token verification failed: {str(e)}")
        # For local development, return True if token exists
        return bool(token and token.strip())

def get_current_user():
    """Get current user from session"""
    user_id = session.get('user_id')
    username = session.get('username')
    token = session.get('token')
    logger.info(f"Session data - user_id: {user_id}, username: {username}, token length: {len(token) if token else 0}")
    return user_id, username, token

def get_user_budgets(user_id):
    """Get user's monthly budgets from MongoDB"""
    try:
        budgets = list(monthly_budgets_collection.find({"user_id": user_id}))
        # Convert ObjectId to string for JSON serialization
        for budget in budgets:
            budget['_id'] = str(budget['_id'])
        return budgets
    except Exception as e:
        logger.error(f"Error fetching budgets: {str(e)}")
        return []

def get_user_expenses(user_id):
    """Get user's daily expenses from MongoDB"""
    try:
        expenses = list(daily_expenses_collection.find({"user_id": user_id}))
        # Convert ObjectId to string for JSON serialization
        for expense in expenses:
            expense['_id'] = str(expense['_id'])
        return expenses
    except Exception as e:
        logger.error(f"Error fetching expenses: {str(e)}")
        return []

def create_budget(user_id, budget_data):
    """Create a new monthly budget in MongoDB"""
    try:
        budget_data['user_id'] = user_id
        budget_data['created_at'] = datetime.now().isoformat()
        result = monthly_budgets_collection.insert_one(budget_data)
        budget_data['_id'] = str(result.inserted_id)
        return budget_data
    except Exception as e:
        logger.error(f"Error creating budget: {str(e)}")
        return None

def create_expense(user_id, expense_data):
    """Create a new daily expense in MongoDB"""
    try:
        expense_data['user_id'] = user_id
        expense_data['created_at'] = datetime.now().isoformat()
        result = daily_expenses_collection.insert_one(expense_data)
        expense_data['_id'] = str(result.inserted_id)
        return expense_data
    except Exception as e:
        logger.error(f"Error creating expense: {str(e)}")
        return None

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'budget-service',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/', methods=['GET'])
def index():
    """Login/Register page"""
    user_id, username, token = get_current_user()
    if user_id and token and verify_token(token):
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    """Handle login form submission"""
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return render_template('login.html', error='Username and password are required')
        
        # For local development, accept any credentials
        if os.getenv('DEBUG', 'False').lower() == 'true':
            # Generate unique user_id based on username hash
            import hashlib
            user_id = int(hashlib.md5(username.encode()).hexdigest()[:8], 16)
            session['user_id'] = user_id
            session['username'] = username
            session['token'] = 'demo-token'
            logger.info(f"Debug login successful for user: {username}")
            return redirect(url_for('dashboard'))
        
        # Call Auth Service
        response = requests.post(f"{AUTH_SERVICE_URL}/login", 
                               json={'username': username, 'password': password},
                               timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            session['user_id'] = data['user_id']
            session['username'] = data['username']
            # Handle both old and new token formats
            session['token'] = data.get('access_token') or data.get('token', '')
            session['refresh_token'] = data.get('refresh_token', '')  # Store refresh token
            session.permanent = True  # Make session permanent
            logger.info(f"Login successful for user: {username}, token length: {len(session['token'])}")
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
            
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        # For local development, accept any credentials if Auth Service is unavailable
        import hashlib
        user_id = int(hashlib.md5(username.encode()).hexdigest()[:8], 16)
        session['user_id'] = user_id
        session['username'] = username
        session['token'] = 'demo-token'
        return redirect(url_for('dashboard'))

@app.route('/register', methods=['POST'])
def register():
    """Handle registration form submission"""
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return render_template('login.html', error='Username and password are required')
        
        # For local development, accept any credentials
        if os.getenv('DEBUG', 'False').lower() == 'true':
            # Generate unique user_id based on username hash
            import hashlib
            user_id = int(hashlib.md5(username.encode()).hexdigest()[:8], 16)
            session['user_id'] = user_id
            session['username'] = username
            session['token'] = 'demo-token'
            return redirect(url_for('dashboard'))
        
        # Call Auth Service
        response = requests.post(f"{AUTH_SERVICE_URL}/register", 
                               json={'username': username, 'password': password},
                               timeout=5)
        
        if response.status_code == 201:
            data = response.json()
            session['user_id'] = data['user_id']
            session['username'] = data['username']
            # Handle both old and new token formats
            session['token'] = data.get('access_token') or data.get('token', '')
            session['refresh_token'] = data.get('refresh_token', '')  # Store refresh token
            session.permanent = True  # Make session permanent
            logger.info(f"Registration successful for user: {username}, token length: {len(session['token'])}")
            return redirect(url_for('dashboard'))
        else:
            error_data = response.json()
            return render_template('login.html', error=error_data.get('error', 'Registration failed'))
            
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        # For local development, accept any credentials if Auth Service is unavailable
        import hashlib
        user_id = int(hashlib.md5(username.encode()).hexdigest()[:8], 16)
        session['user_id'] = user_id
        session['username'] = username
        session['token'] = 'demo-token'
        logger.info(f"Debug registration successful for user: {username}")
        return redirect(url_for('dashboard'))

@app.route('/logout', methods=['POST'])
def logout():
    """Handle logout - improved session clearing"""
    try:
        # Clear all session data
        session.clear()
        # Also clear any cookies that might be set
        response = redirect(url_for('index'))
        response.set_cookie('session', '', expires=0)
        logger.info("User logged out successfully")
        return response
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        session.clear()
        return redirect(url_for('index'))

@app.route('/dashboard', methods=['GET'])
def dashboard():
    """Budget dashboard"""
    user_id, username, token = get_current_user()
    
    logger.info(f"Dashboard access attempt - user_id: {user_id}, username: {username}, token length: {len(token) if token else 0}")
    
    if not user_id or not token or not verify_token(token):
        logger.warning(f"Dashboard access denied - user_id: {user_id}, token: {bool(token)}, verify_token: {verify_token(token) if token else False}")
        return redirect(url_for('index'))
    
    # Get user's budgets and expenses from MongoDB
    user_budgets = get_user_budgets(user_id)
    user_expenses = get_user_expenses(user_id)
    
    # Get current date and month for form defaults
    current_date = datetime.now().strftime('%Y-%m-%d')
    current_month = datetime.now().strftime('%Y-%m')
    
    return render_template('dashboard.html', 
                         username=username,
                         budgets=user_budgets,
                         expenses=user_expenses,
                         current_date=current_date,
                         current_month=current_month)

# API Endpoints

@app.route('/api/monthly-budgets', methods=['POST'])
def create_monthly_budget():
    """Create a new monthly budget"""
    user_id, username, token = get_current_user()
    
    # For local development, use session user_id or generate from username
    if not user_id:
        username = session.get('username', 'default')
        import hashlib
        user_id = int(hashlib.md5(username.encode()).hexdigest()[:8], 16)
    
    try:
        data = request.get_json()
        
        if not data or 'amount' not in data or 'category' not in data:
            return jsonify({'error': 'Amount and category are required'}), 400
        
        budget_data = {
            'amount': float(data['amount']),
            'category': data['category'],
            'month': data.get('month', datetime.now().strftime('%Y-%m'))
        }
        
        logger.info(f"Creating budget for user {user_id}: {budget_data}")
        budget = create_budget(user_id, budget_data)
        if budget:
            logger.info(f"Created monthly budget for user {user_id}: {budget['category']} - ${budget['amount']}")
            return jsonify(budget), 201
        else:
            logger.error(f"Failed to create budget for user {user_id}")
            return jsonify({'error': 'Failed to create budget'}), 500
        
    except Exception as e:
        logger.error(f"Budget creation error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/monthly-budgets', methods=['GET'])
def get_monthly_budgets():
    """Get user's monthly budgets"""
    user_id, username, token = get_current_user()
    
    # For local development, use session user_id or generate from username
    if not user_id:
        username = session.get('username', 'default')
        import hashlib
        user_id = int(hashlib.md5(username.encode()).hexdigest()[:8], 16)
    
    logger.info(f"Getting budgets for user_id: {user_id}, username: {username}")
    budgets = get_user_budgets(user_id)
    logger.info(f"Found {len(budgets)} budgets: {budgets}")
    return jsonify(budgets)

@app.route('/api/daily-expenses', methods=['POST'])
def create_daily_expense():
    """Create a new daily expense"""
    user_id, username, token = get_current_user()
    
    # For local development, use session user_id or generate from username
    if not user_id:
        username = session.get('username', 'default')
        import hashlib
        user_id = int(hashlib.md5(username.encode()).hexdigest()[:8], 16)
    
    try:
        data = request.get_json()
        
        if not data or 'amount' not in data or 'description' not in data:
            return jsonify({'error': 'Amount and description are required'}), 400
        
        expense_data = {
            'amount': float(data['amount']),
            'description': data['description'],
            'category': data.get('category', 'Other'),
            'date': data.get('date', datetime.now().strftime('%Y-%m-%d'))
        }
        
        expense = create_expense(user_id, expense_data)
        if expense:
            logger.info(f"Created daily expense for user {user_id}: {expense['description']} - ${expense['amount']}")
            return jsonify(expense), 201
        else:
            return jsonify({'error': 'Failed to create expense'}), 500
        
    except Exception as e:
        logger.error(f"Expense creation error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/daily-expenses', methods=['GET'])
def get_daily_expenses():
    """Get user's daily expenses"""
    user_id, username, token = get_current_user()
    
    # For local development, use session user_id or generate from username
    if not user_id:
        username = session.get('username', 'default')
        import hashlib
        user_id = int(hashlib.md5(username.encode()).hexdigest()[:8], 16)
    
    logger.info(f"Getting expenses for user_id: {user_id}, username: {username}")
    expenses = get_user_expenses(user_id)
    logger.info(f"Found {len(expenses)} expenses: {expenses}")
    return jsonify(expenses)

# CRUD Operations for Budgets
@app.route('/api/monthly-budgets/<budget_id>', methods=['PUT'])
def update_monthly_budget(budget_id):
    """Update an existing monthly budget"""
    try:
        user_id, username, token = get_current_user()
        
        if not user_id:
            username = session.get('username', 'default')
            import hashlib
            user_id = int(hashlib.md5(username.encode()).hexdigest()[:8], 16)
        
        data = request.get_json()
        
        if not data or 'amount' not in data or 'category' not in data:
            return jsonify({'error': 'Amount and category are required'}), 400
        
        # Update in MongoDB
        if 'monthly_budgets_collection' in globals():
            try:
                result = monthly_budgets_collection.update_one(
                    {'_id': ObjectId(budget_id), 'user_id': user_id},
                    {'$set': {
                        'amount': float(data['amount']),
                        'category': data['category'],
                        'month': data.get('month', datetime.now().strftime('%Y-%m')),
                        'updated_at': datetime.now().isoformat()
                    }}
                )
                
                if result.matched_count == 0:
                    return jsonify({'error': 'Budget not found'}), 404
                
                # Get updated budget
                updated_budget = monthly_budgets_collection.find_one({'_id': ObjectId(budget_id)})
                updated_budget['_id'] = str(updated_budget['_id'])
                
                logger.info(f"Updated budget {budget_id} for user {user_id}")
                return jsonify(updated_budget), 200
                
            except Exception as e:
                logger.error(f"Error updating budget: {str(e)}")
                return jsonify({'error': 'Failed to update budget'}), 500
        else:
            return jsonify({'error': 'Database not available'}), 500
        
    except Exception as e:
        logger.error(f"Error updating monthly budget: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/monthly-budgets/<budget_id>', methods=['DELETE'])
def delete_monthly_budget(budget_id):
    """Delete a monthly budget"""
    try:
        user_id, username, token = get_current_user()
        
        if not user_id:
            username = session.get('username', 'default')
            import hashlib
            user_id = int(hashlib.md5(username.encode()).hexdigest()[:8], 16)
        
        # Delete from MongoDB
        if 'monthly_budgets_collection' in globals():
            try:
                result = monthly_budgets_collection.delete_one({
                    '_id': ObjectId(budget_id),
                    'user_id': user_id
                })
                
                if result.deleted_count == 0:
                    return jsonify({'error': 'Budget not found'}), 404
                
                logger.info(f"Deleted budget {budget_id} for user {user_id}")
                return jsonify({'message': 'Budget deleted successfully'}), 200
                
            except Exception as e:
                logger.error(f"Error deleting budget: {str(e)}")
                return jsonify({'error': 'Failed to delete budget'}), 500
        else:
            return jsonify({'error': 'Database not available'}), 500
        
    except Exception as e:
        logger.error(f"Error deleting monthly budget: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# CRUD Operations for Expenses
@app.route('/api/daily-expenses/<expense_id>', methods=['PUT'])
def update_daily_expense(expense_id):
    """Update an existing daily expense"""
    try:
        user_id, username, token = get_current_user()
        
        if not user_id:
            username = session.get('username', 'default')
            import hashlib
            user_id = int(hashlib.md5(username.encode()).hexdigest()[:8], 16)
        
        data = request.get_json()
        
        if not data or 'amount' not in data or 'description' not in data:
            return jsonify({'error': 'Amount and description are required'}), 400
        
        # Update in MongoDB
        if 'daily_expenses_collection' in globals():
            try:
                result = daily_expenses_collection.update_one(
                    {'_id': ObjectId(expense_id), 'user_id': user_id},
                    {'$set': {
                        'amount': float(data['amount']),
                        'description': data['description'],
                        'category': data.get('category', 'Other'),
                        'date': data.get('date', datetime.now().strftime('%Y-%m-%d')),
                        'updated_at': datetime.now().isoformat()
                    }}
                )
                
                if result.matched_count == 0:
                    return jsonify({'error': 'Expense not found'}), 404
                
                # Get updated expense
                updated_expense = daily_expenses_collection.find_one({'_id': ObjectId(expense_id)})
                updated_expense['_id'] = str(updated_expense['_id'])
                
                logger.info(f"Updated expense {expense_id} for user {user_id}")
                return jsonify(updated_expense), 200
                
            except Exception as e:
                logger.error(f"Error updating expense: {str(e)}")
                return jsonify({'error': 'Failed to update expense'}), 500
        else:
            return jsonify({'error': 'Database not available'}), 500
        
    except Exception as e:
        logger.error(f"Error updating daily expense: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/daily-expenses/<expense_id>', methods=['DELETE'])
def delete_daily_expense(expense_id):
    """Delete a daily expense"""
    try:
        user_id, username, token = get_current_user()
        
        if not user_id:
            username = session.get('username', 'default')
            import hashlib
            user_id = int(hashlib.md5(username.encode()).hexdigest()[:8], 16)
        
        # Delete from MongoDB
        if 'daily_expenses_collection' in globals():
            try:
                result = daily_expenses_collection.delete_one({
                    '_id': ObjectId(expense_id),
                    'user_id': user_id
                })
                
                if result.deleted_count == 0:
                    return jsonify({'error': 'Expense not found'}), 404
                
                logger.info(f"Deleted expense {expense_id} for user {user_id}")
                return jsonify({'message': 'Expense deleted successfully'}), 200
                
            except Exception as e:
                logger.error(f"Error deleting expense: {str(e)}")
                return jsonify({'error': 'Failed to delete expense'}), 500
        else:
            return jsonify({'error': 'Database not available'}), 500
        
    except Exception as e:
        logger.error(f"Error deleting daily expense: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Analytics Endpoints
@app.route('/api/analytics/summary', methods=['GET'])
def get_analytics_summary():
    """Get analytics summary for the current user"""
    try:
        user_id, username, token = get_current_user()
        
        if not user_id:
            username = session.get('username', 'default')
            import hashlib
            user_id = int(hashlib.md5(username.encode()).hexdigest()[:8], 16)
        
        # Get current month
        current_month = datetime.now().strftime('%Y-%m')
        
        # Get budgets and expenses for current month
        if 'monthly_budgets_collection' in globals() and 'daily_expenses_collection' in globals():
            budgets = list(monthly_budgets_collection.find({
                'user_id': user_id,
                'month': current_month
            }))
            
            expenses = list(daily_expenses_collection.find({
                'user_id': user_id,
                'date': {'$regex': f'^{current_month}'}
            }))
            
            # Calculate totals
            total_budget = sum(budget['amount'] for budget in budgets)
            total_expenses = sum(expense['amount'] for expense in expenses)
            remaining = total_budget - total_expenses
            savings_rate = (remaining / total_budget * 100) if total_budget > 0 else 0
            
            # Category breakdown
            category_expenses = {}
            for expense in expenses:
                category = expense.get('category', 'Other')
                category_expenses[category] = category_expenses.get(category, 0) + expense['amount']
            
            return jsonify({
                'total_budget': total_budget,
                'total_expenses': total_expenses,
                'remaining': remaining,
                'savings_rate': round(savings_rate, 1),
                'category_breakdown': category_expenses,
                'budget_progress': [
                    {
                        'category': budget['category'],
                        'budgeted': budget['amount'],
                        'spent': sum(exp['amount'] for exp in expenses if exp.get('category') == budget['category']),
                        'percentage': 0  # Will be calculated on frontend
                    }
                    for budget in budgets
                ]
            }), 200
        else:
            return jsonify({'error': 'Database not available'}), 500
        
    except Exception as e:
        logger.error(f"Error getting analytics summary: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Budget Service on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)

