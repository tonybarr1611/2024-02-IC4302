from metrics import total_requests, cache_hits, cache_misses
from config import ELASTIC_INDEX_NAME
from database import elasticsearch_connection
from flask import Blueprint, request, jsonify
from utils import checkCache, executeQuery, getEmbeddings, getVectorSearchQuery, errResult, measure_processing_time, noWhiteSpaces, updateCache

posts_bp = Blueprint('posts', __name__)

##################################################################################################
# Route localhost:31000/feed: Used to get the feed of posts from the user's friends and themselves
##################################################################################################
@posts_bp.route('/feed', methods=['POST'])
@measure_processing_time
def feed():
    total_requests.labels('feed').inc()
    # Get the user_id from the request
    body = request.get_json()
    
    user_id = body.get('user_id')
    
    if not user_id: return jsonify(errResult)
    
    cache_key = f"feed/{noWhiteSpaces(user_id)}"
    cache_value = checkCache(cache_key)
    if cache_value:
        cache_hits.inc()
        return jsonify(cache_value)
    else:
        cache_misses.inc()
    
    # Get the user's friends
    friends = executeQuery(f"SELECT user_id FROM friends WHERE friend_user_id = {user_id}")
    # friends = executeQuery(f"SELECT friends FROM users WHERE user_id = {user_id}")[0]

    if friends:
        friends_copy = friends.copy()
        friends = []
        for friend in friends_copy:
            friends.append(friend[0])
    else:
        friends = []
    
    friends.append(user_id)
    
    # Convert friends list to a string for SQL
    friends_str = ', '.join(str(friend) for friend in friends)  # Ensure all IDs are strings

    # Get the posts from the user's friends
    posts = executeQuery(f"SELECT P.prompt_id, U.username, P.likes, P.prompt, P.updated_at FROM prompts P LEFT JOIN users U on P.user_id = U.user_id WHERE P.user_id IN ({friends_str}) ORDER BY P.created_at DESC")
    
    updateCache(cache_key, {
        'posts': posts
    })
    
    # Return the posts
    return jsonify({
        'posts': posts
    })
    
#########################################################################
# Route localhost:31000/search: Used to search for posts based on a query
#########################################################################
@posts_bp.route('/search', methods=['POST'])
@measure_processing_time
def search():
    total_requests.labels('search').inc()
    # Get the query from the request
    body = request.get_json()
    
    query = body.get('query')
    
    if not query: return jsonify(errResult)
    
    cache_key = f"search/{noWhiteSpaces(query)}"
    cache_value = checkCache(cache_key)
    if cache_value:
        cache_hits.inc()
        return jsonify(cache_value)
    else:
        cache_misses.inc()
    
    # Get the users with names that match the query
    users = executeQuery(f"SELECT user_id FROM users WHERE name LIKE '%{query}%' OR username LIKE '%{query}%'")
    user_ids = [str(user[0]) for user in users]
    user_ids_str = ','.join(user_ids) if user_ids else 'NULL'
    
    # Get the posts that match the query or are from the matching users
    posts = executeQuery(f"SELECT P.prompt_id, U.username, P.likes, P.prompt, P.updated_at FROM prompts P LEFT JOIN users U on P.user_id = U.user_id WHERE P.prompt LIKE '%{query}%' OR P.user_id IN ({user_ids_str})")
    
    updateCache(cache_key, {
        'posts': posts
    })
    
    # Return the posts
    return jsonify({
        'posts': posts
    })
    
#########################################################################
# Route localhost:31000/prompt: Used to get the top n results of a prompt
#########################################################################
@posts_bp.route('/prompt', methods=['POST'])
@measure_processing_time
def encode_prompt():
    total_requests.labels('prompt').inc()
    # Get the prompt from the request arguments
    body = request.get_json()
    
    prompt = body.get('prompt')
    
    if not prompt: return jsonify(errResult)
    
    cache_key = f"prompt/{noWhiteSpaces(prompt)}"
    cache_value = checkCache(cache_key)
    if cache_value:
        cache_hits.inc()
        return jsonify(cache_value)
    else:
        cache_misses.inc()
    
    result = processPrompt(prompt)
    updateCache(cache_key, result)
    
    return jsonify(result)

# Auxiliary function to process the prompt and return the top n results
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
    return result

#########################################################
# Route localhost:31000/postPrompt: Used to post a prompt
#########################################################
@posts_bp.route('/postPrompt', methods=['POST'])
@measure_processing_time
def postPrompt():
    total_requests.labels('postPrompt').inc()
    # Get the user_id and prompt from the request
    body = request.get_json()
    
    user_id = body.get('user_id')
    prompt = body.get('prompt')
    
    if not user_id or not prompt: return jsonify(errResult)
    
    # Insert the prompt into the database
    executeQuery(f"INSERT INTO prompts (user_id, likes, prompt, created_at, updated_at) VALUES ({user_id}, 0, '{prompt}', NOW(), NOW())")
    
    return jsonify({'result': '200'})

#########################################################
# Route localhost:31000/editPrompt: Used to edit a prompt
#########################################################
@posts_bp.route('/editPrompt', methods=['POST'])
@measure_processing_time
def editPrompt():
    total_requests.labels('editPrompt').inc()
    # Get the prompt_id and prompt from the request
    body = request.get_json()
    
    prompt_id = body.get('prompt_id')
    prompt = body.get('prompt')
    
    if not prompt_id or not prompt: return jsonify(errResult)
    
    # Update the prompt
    executeQuery(f"UPDATE prompts SET prompt = '{prompt}', updated_at = NOW() WHERE prompt_id = {prompt_id}")
    
    return jsonify({'result': '200'})

#############################################################
# Route localhost:31000/deletePrompt: Used to delete a prompt
#############################################################
@posts_bp.route('/deletePrompt', methods=['POST'])
@measure_processing_time
def deletePrompt():
    total_requests.labels('deletePrompt').inc()
    # Get the prompt_id from the request
    body = request.get_json()
    
    prompt_id = body.get('prompt_id')
    
    if not prompt_id: return jsonify(errResult)
    
    # Delete likes associated with the prompt to avoid foreign key constraint
    executeQuery(f"DELETE FROM likes WHERE prompt_id = {prompt_id}")
    # Delete the prompt
    executeQuery(f"DELETE FROM prompts WHERE prompt_id = {prompt_id}")
    
    return jsonify({'result': '200'})