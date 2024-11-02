from metrics import total_requests, cache_hits, cache_misses
from flask import Blueprint, request, jsonify
from utils import checkCache, executeQuery, errResult, measure_processing_time, noWhiteSpaces, updateCache

friends_bp = Blueprint('friends', __name__)

###########################################################################
# Route localhost:31000/followOrUnfollow: Used to follow or unfollow a user
###########################################################################
@friends_bp.route('/followOrUnfollow', methods=['POST'])
@measure_processing_time
def followOrUnfollow():
    total_requests.labels('followOrUnfollow').inc()
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
    
# Auxiliary function to follow a user
def follow(user_id: int, friend_user_id: int, friends: int):
    # Update the user's friends and updated_at
    friends += 1
    executeQuery(f"UPDATE users SET friends = {friends}, updated_at = NOW() WHERE user_id = {friend_user_id}")
    
    executeQuery(f"INSERT INTO friends (user_id, friend_user_id, created_at, updated_at) VALUES ({friend_user_id}, {user_id}, NOW(), NOW())")
    
    return jsonify({'result': '200', 'friends': friends, 'doesFollow': 1})

# Auxiliary function to unfollow a user
def unfollow(user_id: int, friend_user_id: int, friends: int):
    # Unfollow the friend
    friends -= 1
    executeQuery(f"UPDATE users SET friends = {friends}, updated_at = NOW() WHERE user_id = {friend_user_id}")
    
    executeQuery(f"DELETE FROM friends WHERE user_id = {friend_user_id} AND friend_user_id = {user_id}")

    return jsonify({'result': '200', 'friends': friends, 'doesFollow': 0})

####################################################################
# Route localhost:31000/find: Used to find users by name or username
####################################################################
@friends_bp.route('/find', methods=['POST'])
@measure_processing_time
def find():
    total_requests.labels('find').inc()
    # Get the query from the request
    body = request.get_json()
    
    query = body.get('query')
    
    if not query: return jsonify(errResult)
    
    cache_key = f"find/{noWhiteSpaces(query)}"
    cache_value = checkCache(cache_key)
    if cache_value: 
        cache_hits.inc()
        return jsonify(cache_value)
    else:
        cache_misses.inc()
    
    # Get the users with names and usernames that match the query
    users = executeQuery(f"SELECT user_id, name, username, biography, friends FROM users WHERE name LIKE '%{query}%' OR username LIKE '%{query}%'")
    
    return jsonify({
        'users': users
    })

#####################################################################
# Route localhost:31000/isFriend: Used to check if a user is a friend
#####################################################################
@friends_bp.route('/isFriend', methods=['POST'])
@measure_processing_time
def isFriend():
    total_requests.labels('isFriend').inc()
    # Get the user_id and friend_user_id from the request
    body = request.get_json()
    
    user_id = body.get('user_id')
    friend_user_id = body.get('friend_user_id')
    
    if not user_id or not friend_user_id: return jsonify(errResult)
    
    cache_key = f"isFriend/{noWhiteSpaces(user_id)}-{noWhiteSpaces(friend_user_id)}"
    cache_value = checkCache(cache_key)
    if cache_value: 
        cache_hits.inc()
        return jsonify(cache_value)
    else:
        cache_misses.inc()
    
    result = executeQuery(f"SELECT * FROM friends WHERE user_id = {friend_user_id} AND friend_user_id = {user_id}")
    
    updateCache(cache_key, {'doesFollow': 1 if result else 0})
    
    return jsonify({
        'doesFollow': 1 if result else 0
    })
  
#############################################################
# Route localhost:31000/friends: Used to get a user's friends
#############################################################  
@friends_bp.route('/friends', methods=['POST'])
@measure_processing_time
def getFriends():
    total_requests.labels('friends').inc()
    # Get the user_id from the request
    body = request.get_json()
    
    user_id = body.get('user_id')
    
    if not user_id: return jsonify(errResult)
    
    cache_key = f"friends/{noWhiteSpaces(user_id)}"
    cache_value = checkCache(cache_key)
    if cache_value: 
        cache_hits.inc()
        return jsonify(cache_value)
    else:
        cache_misses.inc()
    
    # Get the user's friends
    friends = executeQuery(f"SELECT * FROM friends WHERE friend_user_id = {user_id}")
    
    profiles = []
    for friend in friends:
        friend_user_id = friend[1]
        profile = executeQuery(f"SELECT user_id, name, username, biography, friends FROM users WHERE user_id = {friend_user_id}")
        profiles.append(profile[0])
        
    updateCache(cache_key, {'profiles': profiles})
        
    return jsonify({
        'profiles': profiles
    })