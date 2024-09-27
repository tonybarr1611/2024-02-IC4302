from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import mariadb
import os
import hashlib

HUGGINGFACE = os.getenv('HUGGINGFACE', 'false')
MARIADB = os.getenv("MARIADB")
MARIADB_USER = os.getenv("MARIADB_USER")
MARIADB_PASSWORD = os.getenv("MARIADB_PASS")

print(f"Huggingface: {HUGGINGFACE}")
print(f"MariaDB: {MARIADB}")
print(f"MariaDB User: {MARIADB_USER}")
print(f"MariaDB Password: {MARIADB_PASSWORD}")

app = Flask(__name__)
# Allow CORS for your frontend URL
CORS(app, resources={r"/*": {"origins": "http://localhost:30080"}})

mariadb_connection = None
try:
  mariadb_connection = mariadb.ConnectionPool(
        pool_name="mariadb_pool",
        pool_size=5,
        host=MARIADB,
        user=MARIADB_USER,
        password=MARIADB_PASSWORD,
        database="control"
    )
except Exception as e:
    print(f"Error connecting to MariaDB: {e}")
    exit(1)
    
def executeQuery(query):
    global mariadb_connection
    conn = mariadb_connection.get_connection()
    cur = conn.cursor()
    cur.execute(query)
    result = []
    try:
        result = cur.fetchall()
    except Exception as e:
        print("No result dataset")
    conn.commit()
    conn.close()
    return result

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.post('/prompt')
def encode_prompt():
    prompt = request.args.get('prompt')

    # Send request to localhost:5000/encode with the prompt in the body as 'text'
    response = requests.post(f'http://{HUGGINGFACE}:5000/encode', json={'text': prompt})
    response_data = response.json()
    
    return jsonify(response_data)

@app.post('/register')
def register():
    # Get the name, username, password, and email from the request
    body = request.get_json()
    
    name = body.get('name')
    username = body.get('username')
    password = body.get('password')
    email = body.get('email')
    
    # Get existing users with the same username or email
    existingResult = executeQuery(f"SELECT user_id FROM users WHERE username = '{username}' OR email = '{email}'")
    
    # Stop if there is already a user with the same username or email
    if existingResult: return jsonify({'result': '401'})

    # Hash the password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Insert the user into the database
    executeQuery(f"INSERT INTO users (name, username, password, friends, email, biography, created_at, updated_at) VALUES ('{name}', '{username}', '{hashed_password}', 0, '{email}', '', NOW(), NOW())")
    
    # Return a success response
    return jsonify({
        'result': '200'
    })
    
@app.post('/login')
def login():
    # Get the name, username, password, and email from the request body
    body = request.get_json()
    
    email = body.get('email')
    password = body.get('password')
    
    if not email or not password: return jsonify({'result': '401'})
    
    # Hash the password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # Get the user with the matching username and password
    result = executeQuery(f"SELECT user_id FROM users WHERE email = '{email}' AND password = '{hashed_password}'")
    
    # Return 401 if no user was found and 200 if a user was found
    if result: return jsonify({'result': '200', 'user_id': result[0][0]})
    else: return jsonify({'result': '401'})
    
@app.post('/feed')
def feed():
    # Get the user_id from the request
    user_id = request.args.get('user_id')
    
    # Get the user's friends
    friends = executeQuery(f"SELECT friends FROM users WHERE user_id = {user_id}")[0][0]
    
    # Get the posts from the user's friends
    posts = executeQuery(f"SELECT * FROM prompts WHERE user_id IN ({friends}) OR user_id = {user_id} ORDER BY created_at DESC")
    
    # Return the posts
    return jsonify({
        'posts': posts
    })
    
@app.post('/search')
def search():
    # Get the query from the request
    query = request.args.get('query')
    
    # Get the users with names that match the query
    users = executeQuery(f"SELECT user_id FROM users WHERE name LIKE '%{query}%' OR username LIKE '%{query}%'")
    user_ids = [str(user[0]) for user in users]
    user_ids_str = ','.join(user_ids) if user_ids else 'NULL'
    
    # Get the posts that match the query or are from the matching users
    posts = executeQuery(f"SELECT * FROM prompts WHERE prompt LIKE '%{query}%' OR user_id IN ({user_ids_str})")
    
    # Return the posts
    return jsonify({
        'posts': posts
    })
    
@app.post('/find')
def find():
    # Get the query from the request
    query = request.args.get('query')
    
    # Get the users with names and usernames that match the query
    users = executeQuery(f"SELECT * FROM users WHERE name LIKE '%{query}%' OR username LIKE '%{query}%'")
    
    return jsonify({
        'users': users
    })
    
@app.post('/profile')
def profile():
    # Get the user_id from the request
    user_id = request.args.get('user_id')
    
    # Get the user's information
    user = executeQuery(f"SELECT * FROM users WHERE user_id = {user_id}")
    
    # Get the user's posts
    posts = executeQuery(f"SELECT * FROM prompts WHERE user_id = {user_id}")
    
    return jsonify({
        'user': user,
        'posts': posts
    })
    
if __name__ == '__main__':
    app.run(host='localhost', port=5000)