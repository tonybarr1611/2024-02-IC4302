from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import mariadb
from elasticsearch import Elasticsearch, helpers
import os
import hashlib

'''
    CREATE TABLE IF NOT EXISTS users (
        user_id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255) NOT NULL,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        friends INT NOT NULL,
        email VARCHAR(255) NOT NULL,
        biography VARCHAR(512) NOT NULL,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL
    );

    CREATE TABLE IF NOT EXISTS friends (
        friend_id INT PRIMARY KEY AUTO_INCREMENT,
        user_id INT NOT NULL,
        friend_user_id INT NOT NULL,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (friend_user_id) REFERENCES users(user_id)
    );

    CREATE TABLE IF NOT EXISTS prompts (
        prompt_id INT PRIMARY KEY AUTO_INCREMENT,
        user_id INT NOT NULL,
        likes INT NOT NULL,
        prompt VARCHAR(255) NOT NULL,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );

    CREATE TABLE IF NOT EXISTS likes (
        like_id INT PRIMARY KEY AUTO_INCREMENT,
        user_id INT NOT NULL,
        prompt_id INT NOT NULL,
        created_at DATETIME NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (prompt_id) REFERENCES prompts(prompt_id)
    );
'''

HUGGINGFACE = os.getenv('HUGGINGFACE', 'false')
MARIADB = os.getenv("MARIADB")
MARIADB_USER = os.getenv("MARIADB_USER")
MARIADB_PASSWORD = os.getenv("MARIADB_PASS")
ELASTIC = os.getenv("ELASTIC")
ELASTIC_USER = os.getenv("ELASTIC_USER")
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
ELASTIC_INDEX_NAME = os.getenv("ELASTIC_INDEX_NAME")

print(f"Huggingface: {HUGGINGFACE}")
print(f"MariaDB: {MARIADB}")
print(f"MariaDB User: {MARIADB_USER}")
print(f"MariaDB Password: {MARIADB_PASSWORD}")
print(f"Elasticsearch: {ELASTIC}")
print(f"Elasticsearch User: {ELASTIC_USER}")
print(f"Elasticsearch Password: {ELASTIC_PASSWORD}")
print(f"Elasticsearch Index Name: {ELASTIC_INDEX_NAME}")

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
    
elasticsearch_connection = None
try:
    elasticsearch_connection = Elasticsearch([ELASTIC], basic_auth=[ELASTIC_USER, ELASTIC_PASSWORD])
except Exception as e:
    print(f"Error connecting to Elasticsearch: {e}")
    exit(1)
    
errResult = {'result': '401'}
    
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

def getVectorSearchQuery(vector):
    return {
        "query": {
            "script_score": {
                "query": {
                    "match_all": {}
                },
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embeddings') + 1.0",
                    "params": {
                        "query_vector": vector
                    }
                }
            }
        }
    }
    
def getEmbeddings(prompt):
    response = requests.post(f'http://{HUGGINGFACE}:5000/encode', json={'text': prompt})
    
    # Check if the request was successful
    if response.status_code == 200:
        response_data = response.json()
        return response_data.get('embedding')
    else:
        raise Exception(f"Failed to get embeddings: {response.status_code}, {response.text}")

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.post('/prompt')
def encode_prompt():
    # Get the prompt from the request arguments
    body = request.get_json()
    
    prompt = body.get('prompt')
    
    if not prompt: return jsonify(errResult)
    
    return processPrompt(prompt)

def processPrompt(prompt):
     # Check if the prompt starts with "Top n ..."
    if prompt.lower().startswith("top"):
        try:
            # Extract the number `n` from the prompt
            n = int(prompt.split()[1])
        except (IndexError, ValueError):
            # If there is no valid number after "Top", default to 1 result
            n = 1
    else:
        # If the prompt does not start with "Top n", default to 1 result
        n = 1

    # Generate the embedding for the prompt
    embedding = getEmbeddings(prompt)

    result = []

    # Search query with limited fields (_source) and size based on `n`
    vectors = elasticsearch_connection.search(
        index=ELASTIC_INDEX_NAME,
        body=getVectorSearchQuery(embedding),
        scroll="800ms",
        size=n,  # Fetch `n` results or 1 result based on the prompt
        _source=["id", "title", "artist", "lyrics"] 
    )

    # Extract scroll ID for scrolling through results
    scrollID = vectors['_scroll_id']
    hits = vectors['hits']['hits']

    # Loop through the hits and append only id, title, and artist to the result
    for hit in hits:
        source = hit['_source']
        result.append({
            "id": source.get('id'),
            "title": source.get('title'),
            "artist": source.get('artist'),
            "lyrics": source.get('lyrics')
        })

    # Clear the scroll context
    elasticsearch_connection.clear_scroll(scroll_id=scrollID)

    # Return the result as JSON
    return jsonify(result)

@app.post('/postPrompt')
def postPrompt():
    # Get the user_id and prompt from the request
    body = request.get_json()
    
    user_id = body.get('user_id')
    prompt = body.get('prompt')
    
    if not user_id or not prompt: return jsonify(errResult)
    
    # Insert the prompt into the database
    executeQuery(f"INSERT INTO prompts (user_id, likes, prompt, created_at, updated_at) VALUES ({user_id}, 0, '{prompt}', NOW(), NOW())")
    
    return jsonify({'result': '200'})
  

@app.post('/register')
def register():
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
    
@app.post('/login')
def login():
    # Get the name, username, password, and email from the request body
    body = request.get_json()
    
    email = body.get('email')
    password = body.get('password')
    
    if not email or not password: return jsonify(errResult)
    
    # Hash the password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # Get the user with the matching username and password
    result = executeQuery(f"SELECT user_id FROM users WHERE email = '{email}' AND password = '{hashed_password}'")
    
    # Return 401 if no user was found and 200 if a user was found
    if result: return jsonify({'result': '200', 'user_id': result[0][0]})
    else: return jsonify(errResult)
    
@app.post('/feed')
def feed():
    # Get the user_id from the request
    body = request.get_json()
    
    user_id = body.get('user_id')
    
    if not user_id: return jsonify(errResult)
    
    # Get the user's friends
    friends = executeQuery(f"SELECT user_id FROM friends WHERE friend_user_id = {user_id}")
    # friends = executeQuery(f"SELECT friends FROM users WHERE user_id = {user_id}")[0]
    print(friends)
    if friends:
        friends = list(friends[0])
    else:
        friends = []
    print(friends)
    friends.append(user_id)
    print(friends)
    
    # Convert friends list to a string for SQL
    friends_str = ', '.join(str(friend) for friend in friends)  # Ensure all IDs are strings
    print(friends_str)
    
    # Get the posts from the user's friends
    posts = executeQuery(f"SELECT P.prompt_id, U.username, P.likes, P.prompt, P.created_at FROM prompts P LEFT JOIN users U on P.user_id = U.user_id WHERE P.user_id IN ({friends_str}) ORDER BY P.created_at DESC")
    
    # Return the posts
    return jsonify({
        'posts': posts
    })
    
def hasLiked(user_id: str, prompt_id: str):
    result = executeQuery(f"SELECT * FROM likes WHERE user_id = {user_id} AND prompt_id = {prompt_id}")
    return 1 if result else 0
    
@app.post('/search')
def search():
    # Get the query from the request
    body = request.get_json()
    
    query = body.get('query')
    
    if not query: return jsonify(errResult)
    
    # Get the users with names that match the query
    users = executeQuery(f"SELECT user_id FROM users WHERE name LIKE '%{query}%' OR username LIKE '%{query}%'")
    user_ids = [str(user[0]) for user in users]
    user_ids_str = ','.join(user_ids) if user_ids else 'NULL'
    
    # Get the posts that match the query or are from the matching users
    posts = executeQuery(f"SELECT P.prompt_id, U.username, P.likes, P.prompt, P.created_at FROM prompts P LEFT JOIN users U on P.user_id = U.user_id WHERE P.prompt LIKE '%{query}%' OR P.user_id IN ({user_ids_str})")
    
    # Return the posts
    return jsonify({
        'posts': posts
    })
    
@app.post('/find')
def find():
    # Get the query from the request
    body = request.get_json()
    
    query = body.get('query')
    
    if not query: return jsonify(errResult)
    
    # Get the users with names and usernames that match the query
    users = executeQuery(f"SELECT user_id, name, username, biography, friends FROM users WHERE name LIKE '%{query}%' OR username LIKE '%{query}%'")
    
    return jsonify({
        'users': users
    })
    
@app.post('/isFriend')
def isFriend():
    # Get the user_id and friend_user_id from the request
    body = request.get_json()
    
    user_id = body.get('user_id')
    friend_user_id = body.get('friend_user_id')
    
    if not user_id or not friend_user_id: return jsonify(errResult)
    
    result = executeQuery(f"SELECT * FROM friends WHERE user_id = {friend_user_id} AND friend_user_id = {user_id}")
    
    return jsonify({
        'doesFollow': 1 if result else 0
    })
    
@app.post('/profile')
def profile():
    # Get the user_id from the request
    body = request.get_json()
    
    user_id = body.get('user_id')
    
    if not user_id: return jsonify(errResult)
    
    # Get the user's information
    user = executeQuery(f"SELECT * FROM users WHERE user_id = {user_id}")
    
    # Get the user's posts
    posts = executeQuery(f"SELECT * FROM prompts WHERE user_id = {user_id}")
    
    # Add a field 'answer' to each post by sending it to the function encode_prompt
    for post in posts:
        post['answer'] = encode_prompt(post['prompt'])
    
    return jsonify({
        'user': user,
        'posts': posts
    })
    
@app.post('/likeOrUnlike')
def likeOrUnlike():
    # Get the user_id and prompt_id from the request
    body = request.get_json()
    
    user_id = body.get('user_id')
    prompt_id = body.get('prompt_id')
    
    if not user_id or not prompt_id: return jsonify(errResult)
    
     # Get the prompt's likes
    likes = executeQuery(f"SELECT likes FROM prompts WHERE prompt_id = {prompt_id}")[0][0]
    
    # Check if the user has already liked the prompt
    if (executeQuery(f"SELECT * FROM likes WHERE user_id = {user_id} AND prompt_id = {prompt_id}")):
        return unlike(user_id, prompt_id, likes)
    else:
        return like(user_id, prompt_id, likes)

def like(user_id: str, prompt_id: str, likes: int):
    # Update the prompt's likes and updated_at
    executeQuery(f"UPDATE prompts SET likes = {likes + 1}, updated_at = NOW() WHERE prompt_id = {prompt_id}")
    
    executeQuery(f"INSERT INTO likes (user_id, prompt_id, created_at) VALUES ({user_id}, {prompt_id}, NOW())")
    
    return jsonify({'result': '200'})

def unlike(user_id: str, prompt_id: str, likes: int):
    # Unlike the prompt
    executeQuery(f"DELETE FROM likes WHERE user_id = {user_id} AND prompt_id = {prompt_id}")
    executeQuery(f"UPDATE prompts SET likes = {likes - 1}, updated_at = NOW() WHERE prompt_id = {prompt_id}")
        
    return jsonify({'result': '200'})

@app.post('/hasLiked')
def hasLiked():
    # Get the user_id and prompt_id from the request
    body = request.get_json()
    
    user_id = body.get('user_id')
    prompt_id = body.get('prompt_id')
    
    if not user_id or not prompt_id: return jsonify(errResult)
    
    result = executeQuery(f"SELECT * FROM likes WHERE user_id = {user_id} AND prompt_id = {prompt_id}")
    
    return jsonify({
        'hasLiked': 1 if result else 0
    })

@app.post('/followOrUnfollow')
def followOrUnfollow():
    # Get the user_id and friend_user_id from the request
    body = request.get_json()
    
    user_id = int(body.get('user_id'))
    friend_user_id = int(body.get('friend_user_id'))
    
    if not user_id or not friend_user_id: return jsonify(errResult)
    
    friends = int(executeQuery(f"SELECT friends FROM users WHERE user_id = {friend_user_id}")[0][0])
    # Check if the user is already following the friend
    if (executeQuery(f"SELECT * FROM friends WHERE friend_user_id = {user_id} AND user_id = {friend_user_id}")):
        return unfollow(user_id, friend_user_id, friends)
    else:
        return follow(user_id, friend_user_id, friends)
    
def follow(user_id: int, friend_user_id: int, friends: int):
    # Update the user's friends and updated_at
    friends += 1
    executeQuery(f"UPDATE users SET friends = {friends}, updated_at = NOW() WHERE user_id = {friend_user_id}")
    
    executeQuery(f"INSERT INTO friends (user_id, friend_user_id, created_at, updated_at) VALUES ({friend_user_id}, {user_id}, NOW(), NOW())")
    
    return jsonify({'result': '200', 'friends': friends, 'doesFollow': 1})

def unfollow(user_id: int, friend_user_id: int, friends: int):
    # Unfollow the friend
    friends -= 1
    executeQuery(f"UPDATE users SET friends = {friends}, updated_at = NOW() WHERE user_id = {friend_user_id}")
    
    executeQuery(f"DELETE FROM friends WHERE user_id = {friend_user_id} AND friend_user_id = {user_id}")

    return jsonify({'result': '200', 'friends': friends, 'doesFollow': 0})

@app.post('/updateProfile')
def updateProfile():
    # Get the user_id, name, username, email, and biography from the request
    body = request.get_json()
    
    user_id = body.get('user_id')
    name = body.get('name')
    username = body.get('username')
    biography = body.get('biography')
    
    if not user_id or not name or not username: return jsonify(errResult)
    
    if executeQuery(f"SELECT * FROM users WHERE username = '{username}' AND user_id != {user_id}"): return jsonify(errResult)
    
    # Update the user's information
    executeQuery(f"UPDATE users SET name = '{name}', username = '{username}', biography = '{biography}', updated_at = NOW() WHERE user_id = {user_id}")
    
    return jsonify({'result': '200'})

@app.post('/deletePrompt')
def deletePrompt():
    # Get the prompt_id from the request
    body = request.get_json()
    
    prompt_id = body.get('prompt_id')
    
    if not prompt_id: return jsonify(errResult)
    
    # Delete the prompt
    executeQuery(f"DELETE FROM prompts WHERE prompt_id = {prompt_id}")
    
    return jsonify({'result': '200'})

@app.post('/editPrompt')
def editPrompt():
    # Get the prompt_id and prompt from the request
    body = request.get_json()
    
    prompt_id = body.get('prompt_id')
    prompt = body.get('prompt')
    
    if not prompt_id or not prompt: return jsonify(errResult)
    
    # Update the prompt
    executeQuery(f"UPDATE prompts SET prompt = '{prompt}', updated_at = NOW() WHERE prompt_id = {prompt_id}")
    
    return jsonify({'result': '200'})

@app.post('/friends')
def getFriends():
    # Get the user_id from the request
    body = request.get_json()
    
    user_id = body.get('user_id')
    
    if not user_id: return jsonify(errResult)
    
    # Get the user's friends
    friends = executeQuery(f"SELECT * FROM friends WHERE user_id = {user_id}")
    
    profiles = []
    for friend in friends:
        friend_user_id = friend[2]
        profile = executeQuery(f"SELECT * FROM users WHERE user_id = {friend_user_id}")
        profiles.append(profile)
        
    return jsonify({
        'profiles': profiles
    })
    
if __name__ == '__main__':
    app.run(host='localhost', port=5000)