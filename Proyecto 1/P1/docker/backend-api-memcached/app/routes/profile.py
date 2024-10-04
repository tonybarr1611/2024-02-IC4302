from flask import Blueprint, request, jsonify
from metrics import total_requests, cache_hits, cache_misses
from utils import checkCache, executeQuery, errResult, measure_processing_time, noWhiteSpaces, updateCache

profile_bp = Blueprint('profile', __name__)

###########################################################################
# Route localhost:31000/profile: Used to get a user's information and posts
###########################################################################
@profile_bp.route('/profile', methods=['POST'])
@measure_processing_time
def profile():
    total_requests.labels('profile').inc()
    # Get the user_id from the request
    body = request.get_json()
    
    user_id = body.get('user_id')
    
    if not user_id: return jsonify(errResult)
    
    cache_key = f"profile/{noWhiteSpaces(user_id)}"
    cache_value = checkCache(cache_key)
    if cache_value:
        cache_hits.inc()
        return jsonify(cache_value)
    else:
        cache_misses.inc()
    
    # Get the user's information
    user = executeQuery(f"SELECT user_id, name, username, biography, friends FROM users WHERE user_id = {user_id}")
    
    # Get the user's posts
    posts = executeQuery(f"SELECT P.prompt_id, U.username, P.likes, P.prompt, P.created_at FROM prompts P LEFT JOIN users U on P.user_id = U.user_id WHERE P.user_id = {user_id} ORDER BY P.created_at DESC")
    
    updateCache(cache_key, {
        'user': user,
        'posts': posts
    })
    
    return jsonify({
        'user': user,
        'posts': posts
    })
    
##########################################################################
# Route localhost:31000/updateProfile: Used to update a user's information
##########################################################################
@profile_bp.route('/updateProfile', methods=['POST'])
@measure_processing_time
def updateProfile():
    total_requests.labels('updateProfile').inc()
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