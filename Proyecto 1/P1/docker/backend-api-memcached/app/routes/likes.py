from flask import Blueprint, request, jsonify
from metrics import total_requests, cache_hits, cache_misses
from utils import checkCache, executeQuery, errResult, measure_processing_time, noWhiteSpaces, updateCache

likes_bp = Blueprint('likes', __name__)

#####################################################################
# Route localhost:31000/likeOrUnlike: Used to like or unlike a prompt
#####################################################################
@likes_bp.route('/likeOrUnlike', methods=['POST'])
@measure_processing_time
def likeOrUnlike():
    total_requests.labels('likeOrUnlike').inc()
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

############################################################################
# Route localhost:31000/hasLiked: Used to check if a user has liked a prompt
############################################################################
@likes_bp.route('/hasLiked', methods=['POST'])
@measure_processing_time
def hasLiked():
    total_requests.labels('hasLiked').inc()
    # Get the user_id and prompt_id from the request
    body = request.get_json()
    
    user_id = body.get('user_id')
    prompt_id = body.get('prompt_id')
    
    if not user_id or not prompt_id: return jsonify(errResult)
    
    cache_key = f"{noWhiteSpaces(user_id)}-{noWhiteSpaces(prompt_id)}"
    cache_value = checkCache(cache_key)
    if cache_value: 
        cache_hits.inc()
        return jsonify(cache_value)
    else:
        cache_misses.inc()
    
    result = executeQuery(f"SELECT * FROM likes WHERE user_id = {user_id} AND prompt_id = {prompt_id}")
    
    updateCache(cache_key, {'hasLiked': 1 if result else 0})
    
    return jsonify({
        'hasLiked': 1 if result else 0
    })