import hashlib
from flask import Blueprint, request, jsonify
from metrics import total_requests, cache_hits, cache_misses
from utils import executeQuery, errResult, measure_processing_time, checkCache, noWhiteSpaces, updateCache

auth_bp = Blueprint('auth', __name__)

#############################################################
# Route localhost:31000/register: Used to register a new user
#############################################################
@auth_bp.route('/register', methods=['POST'])
@measure_processing_time
def register():
    total_requests.labels('register').inc()
    # Get the name, username, password, and email from the request
    body = request.get_json()
    
    name = body.get('name')
    username = body.get('username')
    password = body.get('password')
    email = body.get('email')
    
    if not name or not username or not password or not email: return jsonify(errResult)
    
    # Get existing users with the same username or email
    existingResult = executeQuery(f"SELECT user_id FROM users WHERE username = '{username}' OR email = '{email}'")
    
    # Stop if there is already a user with the same username or email
    if existingResult: return jsonify(errResult)

    # Hash the password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Insert the user into the database
    executeQuery(f"INSERT INTO users (name, username, password, friends, email, biography, created_at, updated_at) VALUES ('{name}', '{username}', '{hashed_password}', 0, '{email}', '', NOW(), NOW())")
    
    # Get the inserted user_id
    result = executeQuery(f"SELECT user_id FROM users WHERE username = '{username}' AND email = '{email}'")
    
    # Return a success response with the user_id
    return jsonify({
        'result': '200',
        'user_id': result[0][0] if result else None
    })

#############################################################
# Route localhost:31000/login: Used to login an existing user
############################################################# 
@auth_bp.route('/login', methods=['POST'])
@measure_processing_time
def login():
    total_requests.labels('login').inc()
    # Get the name, username, password, and email from the request body
    body = request.get_json()
    
    email = body.get('email')
    password = body.get('password')
    
    if not email or not password: return jsonify(errResult)
    
    cache_key = f"login/{noWhiteSpaces(email)}-{noWhiteSpaces(password)}"
    cache_value = checkCache(cache_key)
    if cache_value: 
        cache_hits.inc()
        return jsonify(cache_value)
    else:
        cache_misses.inc()
    
    # Hash the password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # Get the user with the matching username and password
    result = executeQuery(f"SELECT user_id FROM users WHERE email = '{email}' AND password = '{hashed_password}'")
    
    updateCache(cache_key, {'result': '200', 'user_id': result[0][0]} if result else errResult)
    
    # Return 401 if no user was found and 200 if a user was found
    if result: return jsonify({'result': '200', 'user_id': result[0][0]})
    else: return jsonify(errResult)