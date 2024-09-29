from flask import Blueprint, request, jsonify
from routes.posts import processPrompt
from utils import executeQuery, errResult


profile_bp = Blueprint('profile', __name__)

###########################################################################
# Route localhost:31000/profile: Used to get a user's information and posts
###########################################################################
@profile_bp.route('/profile', methods=['POST'])
def profile():
    # Get the user_id from the request
    body = request.get_json()
    
    user_id = body.get('user_id')
    
    if not user_id: return jsonify(errResult)
    
    # Get the user's information
    user = executeQuery(f"SELECT user_id, name, username, biography, friends FROM users WHERE user_id = {user_id}")
    
    # Get the user's posts
    posts = executeQuery(f"SELECT P.prompt_id, U.username, P.likes, P.prompt, P.created_at FROM prompts P LEFT JOIN users U on P.user_id = U.user_id WHERE P.user_id = {user_id} ORDER BY P.created_at DESC")
    
    return jsonify({
        'user': user,
        'posts': posts
    })
    
##########################################################################
# Route localhost:31000/updateProfile: Used to update a user's information
##########################################################################
@profile_bp.route('/updateProfile', methods=['POST'])
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